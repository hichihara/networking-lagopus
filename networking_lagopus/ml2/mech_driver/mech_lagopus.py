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

from neutron.plugins.ml2.drivers import mech_agent

class LagopusMechanismDriver(mech_agent.SimpleAgentMechanismDriverBase):

    def __init__(self):
        pass

    def initialize(self):
        pass

    def get_allowed_network_types(self, agent=None):
        pass

    def get_mappings(self, agent):
        pass
