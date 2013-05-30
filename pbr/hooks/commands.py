# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from pbr.hooks import base
from pbr import packaging


class CommandsConfig(base.BaseConfig):

    section = 'global'

    def __init__(self, config):
        super(CommandsConfig, self).__init__(config)
        self.commands = self.config.get('commands', "")

    def save(self):
        self.config['commands'] = self.commands
        super(CommandsConfig, self).save()

    def add_command(self, command):
        self.commands = "%s\n%s" % (self.commands, command)

    def hook(self):
        self.add_command('pbr.packaging.LocalSDist')

        if packaging.have_sphinx():
            self.add_command('pbr.packaging.LocalBuildDoc')
            self.add_command('pbr.packaging.LocalBuildLatex')

        use_egg = packaging.get_boolean_option(
            self.pbr_config, 'use-egg', 'PBR_USE_EGG')
        # We always want non-egg install unless explicitly requested
        if 'manpages' in self.pbr_config or not use_egg:
            self.add_command('pbr.packaging.DistutilsInstall')