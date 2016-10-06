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

from neutron.extensions import portbindings
from neutron.plugins.common import constants as p_constants
from neutron.plugins.ml2.drivers import mech_agent

LOG = logging.getLogger(__name__)
AGENT_TYPE_LAGOPUS = 'Lagopus agent'


class LagopusMechanismDriver(mech_agent.SimpleAgentMechanismDriverBase):

    @log_helpers.log_method_call
    def __init__(self):
        super(LagopusMechanismDriver, self).__init__(
            AGENT_TYPE_LAGOPUS,
            portbindings.VIF_TYPE_VHOST_USER,
            {portbindings.CAP_PORT_FILTER: False})

    def get_allowed_network_types(self, agent=None):
        return [p_constants.TYPE_FLAT,p_constants.TYPE_LOCAL]

    def get_mappings(self, agent):
        return agent['configurations'].get('interface_mappings', {})

    def try_to_bind_segment_for_agent(self, context, segment, agent):
        if self.check_segment_for_agent(segment, agent):
            # Default vif type
            vif_type = self.vif_type

            vif_details = dict(self.vif_details)

            # TODO(hichihara): Implement whether vhost or tap

            vif_details[portbindings.VHOST_USER_SOCKET] = '/tmp/sock0'
            vif_details[portbindings.VHOST_USER_MODE] = \
                portbindings.VHOST_USER_MODE_CLIENT
            context.set_binding(segment[api.ID],
                                vif_type,
                                vif_details)
            return True
        else:
            return False

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
    
