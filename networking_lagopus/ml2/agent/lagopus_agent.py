#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import sys

from neutron_lib import constants as n_const
from oslo_config import cfg
from oslo_log import helpers as log_helpers
from oslo_log import log as logging
import oslo_messaging
from oslo_service import service

from neutron.agent.linux import ip_lib
from neutron.agent.linux import utils
from neutron.common import config as common_config
from neutron.common import profiler as setup_profiler
from neutron.common import topics
from neutron.plugins.ml2.drivers.agent import _agent_manager_base as amb
from neutron.plugins.ml2.drivers.agent import _common_agent as ca

from networking_lagopus._i18n import _LE, _LI
from networking_lagopus.agent import lagopus_lib

LOG = logging.getLogger(__name__)

LAGOPUS_AGENT_BINARY = 'neutron-lagopus-agent'
AGENT_TYPE_LAGOPUS = 'Lagopus agent'
EXTENSION_DRIVER_TYPE = 'lagopus'
LAGOPUS_FS = "/sys/class/net/"
RESOURCE_ID_LENGTH = 11


class LagopusManager(amb.CommonAgentManagerBase):

    def __init__(self):
        self.interface_mappings = {}

    def ensure_port_admin_state(self, device, admin_state_up):
        pass

    def get_agent_configurations(self):
        configurations = {}
        return configurations

    def get_agent_id(self):
        devices = ip_lib.IPWrapper().get_devices(True)
        if devices:
            mac = utils.get_interface_mac(devices[0].name)
            return 'lagopus%s' % mac.replace(":", "")
        else:
            LOG.error(_LE("Unable to obtain MAC address for unique ID. "
                          "Agent terminated!"))
            sys.exit(1)

    def get_all_devices(self):
        devices = set()
        all_device_names = os.listdir(LAGOPUS_FS)
        for device_name in all_device_names:
            if device_name.startswith(n_const.TAP_DEVICE_PREFIX):
                devices.add(device_name)
        return devices

    def get_devices_modified_timestamps(self, devices):
        return {}

    def get_extension_driver_type(self):
        return EXTENSION_DRIVER_TYPE

    def get_rpc_callbacks(self, context, agent, sg_agent):
        return LagopusRpcCallbacks(context, agent, sg_agent)

    def get_rpc_consumers(self):
        consumers = [[topics.PORT, topics.UPDATE],
                     [topics.NETWORK, topics.DELETE],
                     [topics.NETWORK, topics.UPDATE],
                     [topics.SECURITY_GROUP, topics.UPDATE]]
        return consumers
        
    @staticmethod
    def get_tap_device_name(interface_id):
        tap_device_name = (n_const.TAP_DEVICE_PREFIX +
                           interface_id[:RESOURCE_ID_LENGTH])
        return tap_device_name

    @log_helpers.log_method_call
    def plug_interface(self, network_id, network_segment, tap_name,
                       device_owner):
        port_num = len(self.interface_mappings) + 1
        bridge_name = 'bridge01'
        lagopus_client = lagopus_lib.LagopusCommand()
        lagopus_client.plug_tap(tap_name, port_num, bridge_name)
        lagopus_client.add_flow(port_num, bridge_name)
        self.interface_mappings[tap_name] = port_num
        return True

    def setup_arp_spoofing_protection(self, device, device_details):
        pass

    def delete_arp_spoofing_protection(self, devices):
        pass

    def delete_unreferenced_arp_protection(self, current_devices):
        pass


class LagopusRpcCallbacks(amb.CommonAgentManagerRpcCallBackBase):
        # Set RPC API version to 1.0 by default.
        # history
        #   1.1 Support Security Group RPC
        #   1.3 Added param devices_to_update to security_groups_provider_updated
        #   1.4 Added support for network_update
        target = oslo_messaging.Target(version='1.4')
        def network_delete(self, context, **kwargs):
            pass

        @log_helpers.log_method_call
        def port_update(self, context, **kwargs):
            port_id = kwargs['port']['id']
            device_name = self.agent.mgr.get_tap_device_name(port_id)
            self.updated_devices.add(device_name)
            LOG.debug("port_update RPC received for port: %s", port_id)

        def security_groups_rule_updated(self, context, **kwargs):
            pass

        def security_groups_member_updated(self, context, **kwargs):
            pass

        def security_groups_provider_updated(self, context, **kwargs):
            pass


def main():
    common_config.init(sys.argv[1:])
    common_config.setup_logging()

    manager = LagopusManager()

    polling_interval = cfg.CONF.AGENT.polling_interval
    quitting_rpc_timeout = cfg.CONF.AGENT.quitting_rpc_timeout
    agent = ca.CommonAgentLoop(manager, polling_interval,
                               quitting_rpc_timeout,
                               AGENT_TYPE_LAGOPUS,
                               LAGOPUS_AGENT_BINARY)
    setup_profiler.setup(LAGOPUS_AGENT_BINARY, cfg.CONF.host)
    LOG.info(_LI("Agent initialized successfully, now running... "))
    launcher = service.launch(cfg.CONF, agent)
    launcher.wait()
