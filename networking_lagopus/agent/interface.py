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

from oslo_log import log as logging

from neutron.agent.linux import interface as n_interface
from neutron.agent.linux import ip_lib
from neutron.common import constants as n_const

from networking._i18n import _LE, _LW

LOG = logging.getLogger(__name__)


class LagopusInterfaceDriver(n_interface.LinuxInterfaceDriver):

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


    def unplug(self, device_name, bridge=None, namespace=None, prefix=None):
        """Unplug the interface."""
        device = ip_lib.IPDevice(device_name, namespace=namespace)
        try:
            device.link.delete()
            # TODO(hichihara): Delete flow and eth in Lagopus swith
            LOG.debug("Unplugged interface '%s'", device_name)
        except RuntimeError:
            LOG.error(_LE("Failed unplugging interface '%s'"),
                      device_name)

