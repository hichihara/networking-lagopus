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

SOCKET_ISSUE = "Socket connection refused.  Lagopus is not running?\n"


class LagopusCommand(object):

    def _lagosh(self, cmd=None):
        if not cmd:
            return
        lagosh_client = lagosh.ds_client()
        try:
            return lagosh_client.call(cmd)
        except socket.error:
            pass
        except lagosh.DSLError as e:
            pass

    def show_interfaces(self):
        cmd = "interface\n"
        return self._lagosh(cmd)

    def plug_tap(self, tap_name, port_num, bridge_name='bridge01'):
        cmd = ("interface %(tap)s create -type ethernet-rawsock "
               "-device %(tap)s\n") % {'tap': tap_name}
        self._lagosh(cmd)
        cmd = ("port p-%(tap)s create -interface "
               "%(tap)s\n") % {'tap': tap_name}
        self._lagosh(cmd)
        cmd = ("bridge %(bridge_name)s config -port p-%(tap)s "
               "%(num)s\n") % {'bridge_name': bridge_name,
                               'tap': tap_name,
                               'num': port_num}
        self._lagosh(cmd)

    def unplug_tap(self, tap_name, bridge_name='bridge01'):
        cmd = ("bridge %(bridge_name)s config -port "
               "-p-%(tap)s\n") % {'bridge_name': bridge_name,
                                  'tap': tap_name}
        self._lagosh(cmd)
        cmd = ("port p-%(tap)s destroy\n") % {'tap': tap_name}
        self._lagosh(cmd)
        cmd = ("interface %(tap)s destroy\n") % {'tap': tap_name}
        self._lagosh(cmd)

    def add_flow(self, port_num, bridge_name='bridge01'):
        cmd = ("flow %(bridge_name)s add in_port=%(num)s apply_actions=output:"
               "4294967292\n") % {'bridge_name': bridge_name, 'num': port_num}
        self._lagosh(cmd)

    def del_flow(self, bridge_name='bridge01', port_num = None, tap_name=None):
        if port_num:
            cmd = ("flow %(bridge_name)s del in_port=%(num)s apply_actions="
                   "output:4294967292\n") % {'bridge_name': bridge_name,
                                             'num': port_num}
        elif tap_name:
            ports = self._lagosh("port\n")
            for port in ports:
                if port['interface'] == tap_name:
                    port_num = port['port-number']
            if port_num is None:
                # TODO(hichihara): Raise proper error
                return
            cmd = ("flow %(bridge_name)s del in_port=%(num)s apply_actions="
                   "output:4294967292\n") % {'bridge_name': bridge_name,
                                             'num': port_num}
        else:
            # TODO(hichihara): Raise proper error
            return
        self._lagosh(cmd)
