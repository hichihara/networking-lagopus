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

import commands
import json
import socket

from neutron.agent.linux import utils

from networking_lagopus.agent import lagosh


class LagopusCommand(object):

    def show_interfaces(cls, **kwargs):
        cmd = ['lagosh', '-c', 'show', 'interface']
        result = utils.execute(cmd, **kwargs)
        decode_result = json.loads(result)
        return decode_result

    def _lagosh(self, cmd=None):
        if not cmd:
            return
        lagosh_client = lagosh.ds_client()
        try:
            lagosh_client.call(cmd)
        except socket.error:
            pass
        except lagosh.DSLError as e:
            pass

    def plug_tap(self, tap_name, port_num, bridge_name='bridge01'):
        cmd = ("interface interface%(num)s create -type ethernet-rawsock "
               "-device %(tap)s\n") % {'num': port_num, 'tap': tap_name}
        self._lagosh(cmd)
        cmd = ("port port%(num)s create -interface "
               "interface%(num)s\n") % {'num': port_num}
        self._lagosh(cmd)
        cmd = ("bridge %(bridge_name)s config -port port%(num)s "
               "%(num)s\n") % {'bridge_name': bridge_name, 'num': port_num}
        self._lagosh(cmd)

    def add_flow(self, port_num, bridge_name='bridge01'):
        cmd = ("flow %(bridge_name)s add in_port=%(num)s apply_actions=output:"
               "4294967292\n") % {'bridge_name': bridge_name, 'num': port_num}
        self._lagosh(cmd)
