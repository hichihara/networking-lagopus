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

from neutron_lib import constants as n_const
from oslo_log import log as logging

from neutron.agent.linux import interface as n_interface
from neutron.agent.linux import ip_lib
from neutron.agent.linux import utils

from networking_lagopus._i18n import _LE, _LW
from networking_lagopus.agent import lagopus_lib

LOG = logging.getLogger(__name__)


class LagopusInterfaceDriver(n_interface.LinuxInterfaceDriver):

    def _disable_tcp_offload(self, namespace, device_name):
        ip_wrapper = ip_lib.IPWrapper(namespace)
        cmd = ['ethtool', '-K', device_name, 'tx', 'off', 'tso', 'off']
        ip_wrapper.netns.execute(cmd)

    def plug_new(self, network_id, port_id, device_name, mac_address,
                 bridge=None, namespace=None, prefix=None, mtu=None):
        """Plugin the interface."""
        ip = ip_lib.IPWrapper()
        tap_name = device_name.replace(prefix or self.DEV_NAME_PREFIX,
                                       n_const.TAP_DEVICE_PREFIX)
        root_veth, ns_veth = ip.add_veth(tap_name, device_name,
                                         namespace2=namespace)
        root_veth.disable_ipv6()
        ns_veth.link.set_address(mac_address)

        if mtu:
            root_veth.link.set_mtu(mtu)
            ns_veth.link.set_mtu(mtu)
        else:
            LOG.warning(_LW("No MTU configured for port %s"), port_id)

        root_veth.link.set_up()
        ns_veth.link.set_up()
        self._disable_tcp_offload(namespace, device_name)

    def unplug(self, device_name, bridge=None, namespace=None, prefix=None):
        """Unplug the interface."""
        device = ip_lib.IPDevice(device_name, namespace=namespace)
        tap_name = device_name.replace(prefix or self.DEV_NAME_PREFIX,
                                       n_const.TAP_DEVICE_PREFIX)
        lagopus_client = lagopus_lib.LagopusCommand()
        bridge_name = 'bridge01'
        try:
            lagopus_client.del_flow(bridge_name=bridge_name, tap_name=tap_name)
            lagopus_client.unplug_tap(tap_name, bridge_name)
            device.link.delete()
            LOG.debug("Unplugged interface '%s'", device_name)
        except RuntimeError:
            LOG.error(_LE("Failed unplugging interface '%s'"),
                      device_name)

