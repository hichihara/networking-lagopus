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

from oslo_log import helpers as log_helpers
from oslo_log import log as logging

from neutron.plugins.ml2.drivers import mech_agent

LOG = logging.getLogger(__name__)


class LagopusMechanismDriver(mech_agent.SimpleAgentMechanismDriverBase):

    @log_helpers.log_method_call
    def __init__(self):
        pass

    def initialize(self):
        pass

    def get_allowed_network_types(self, agent=None):
        pass

    def get_mappings(self, agent):
        pass

    @log_helpers.log_method_call
    def create_network_precommit(self, context):
        pass

    def create_network_postcommit(self, context):
        pass

    def update_network_precommit(self, context):
        pass

    def update_network_postcommit(self, context):
        pass

    @log_helpers.log_method_call
    def delete_network_precommit(self, context):
        pass

    def delete_network_postcommit(self, context):
        pass

    def create_subnet_precommit(self, context):
        pass

    def create_subnet_postcommit(self, context):
        pass

    def update_subnet_precommit(self, context):
        pass

    def update_subnet_postcommit(self, context):
        pass

    def delete_subnet_precommit(self, context):
        pass

    def delete_subnet_postcommit(self, context):
        pass

    def create_port_precommit(self, context):
        pass

    def create_port_postcommit(self, context):
        pass

    def update_port_precommit(self, context):
        pass

    def update_port_postcommit(self, context):
        pass

    def delete_port_precommit(self, context):
        pass

    def delete_port_postcommit(self, context):
        pass

    def bind_port(self, context):
        pass

    
