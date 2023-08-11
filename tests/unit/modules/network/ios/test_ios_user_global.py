# (c) 2016 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent

from ansible_collections.cisco.ios.plugins.modules import ios_user_global
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosUserGlobalModule(TestIosModule):
    module = ios_user_global

    def setUp(self):
        super(TestIosUserGlobalModule, self).setUp()
        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.user_global.user_global."
            "User_globalFacts.get_users_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosUserGlobalModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_user_global_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            enable secret 9 $9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo
            username admin secret 9 $9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg
            """,
        )

        playbook = {
            "config": {
                "enable": [
                    {
                        "password": {
                            "type": "secret",
                            "hash": 9,
                            "value": "$9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo",
                        },
                    },
                ],
                "users": [
                    {
                        "name": "admin",
                        "password": {
                            "type": "secret",
                            "hash": 9,
                            "value": "$9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg",
                        },
                    },
                ],
            },
        }
        merged = []
        playbook["state"] = "merged"
        set_module_args(playbook)
        result = self.execute_module()

        self.assertEqual(sorted(result["commands"]), sorted(merged))

    def test_ios_user_global_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            username johndoe secret 5 $5$cAYu$0he5yPyPAbXoXo6U0fjzb4NbLLyqDRehwQU3ysKEC33
            """,
        )

        playbook = {
            "config": {
                "enable": [
                    {
                        "password": {
                            "type": "secret",
                            "hash": 9,
                            "value": "$9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo",
                        },
                    },
                ],
                "users": [
                    {
                        "name": "admin",
                        "password": {
                            "type": "secret",
                            "hash": 9,
                            "value": "$9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg",
                        },
                    },
                ],
            },
        }
        merged = [
            "enable secret 9 $9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo",
            "username admin secret 9 $9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg",
        ]
        playbook["state"] = "merged"
        set_module_args(playbook)
        result = self.execute_module(changed=True)

        self.assertEqual(sorted(result["commands"]), sorted(merged))

    def test_ios_user_global_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            username johndoe secret 5 $5$cAYu$0he5yPyPAbXoXo6U0fjzb4NbLLyqDRehwQU3ysKEC33
            """,
        )
        playbook = {"config": {}}
        deleted = [
            "no username johndoe secret 5 $5$cAYu$0he5yPyPAbXoXo6U0fjzb4NbLLyqDRehwQU3ysKEC33",
        ]
        playbook["state"] = "deleted"
        set_module_args(playbook)
        self.maxDiff = None
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(deleted))

    def test_ios_user_global_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            username johndoe secret 5 $5$cAYu$0he5yPyPAbXoXo6U0fjzb4NbLLyqDRehwQU3ysKEC33
            """,
        )

        playbook = {
            "config": {
                "enable": [
                    {
                        "password": {
                            "type": "secret",
                            "hash": 9,
                            "value": "$9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo",
                        },
                    },
                ],
                "users": [
                    {
                        "name": "admin",
                        "password": {
                            "type": "secret",
                            "hash": 9,
                            "value": "$9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg",
                        },
                    },
                ],
            },
        }
        overridden = [
            "enable secret 9 $9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo",
            "no username johndoe secret 5 $5$cAYu$0he5yPyPAbXoXo6U0fjzb4NbLLyqDRehwQU3ysKEC33",
            "username admin secret 9 $9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg",
        ]
        playbook["state"] = "overridden"
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(overridden))

    def test_ios_user_global_overridden_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            enable secret 9 $9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo
            username admin secret 9 $9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg
            """,
        )

        playbook = {
            "config": {
                "enable": [
                    {
                        "password": {
                            "type": "secret",
                            "hash": 9,
                            "value": "$9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo",
                        },
                    },
                ],
                "users": [
                    {
                        "name": "admin",
                        "password": {
                            "type": "secret",
                            "hash": 9,
                            "value": "$9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg",
                        },
                    },
                ],
            },
        }
        overridden = []
        playbook["state"] = "overridden"
        set_module_args(playbook)
        result = self.execute_module(changed=False)
        self.maxDiff = None
        self.assertEqual(sorted(result["commands"]), sorted(overridden))

    def test_ios_user_global_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    enable secret 9 $9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo
                    username admin secret 9 $9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg
                    """,
                ),
                state="parsed",
            ),
        )
        parsed = {
            "enable": [
                {
                    "password": {
                        "type": "secret",
                        "hash": 9,
                        "value": "$9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo",
                    },
                },
            ],
            "users": [
                {
                    "name": "admin",
                    "password": {
                        "type": "secret",
                        "hash": 9,
                        "value": "$9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg",
                    },
                },
            ],
        }
        result = self.execute_module(changed=False)
        self.maxDiff = None
        self.assertEqual(result["parsed"], parsed)

    def test_ios_user_global_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            enable secret 9 $9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo
            username admin secret 9 $9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg
            """,
        )
        set_module_args(dict(state="gathered"))
        gathered = {
            "enable": [
                {
                    "password": {
                        "type": "secret",
                        "hash": 9,
                        "value": "$9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo",
                    },
                },
            ],
            "users": [
                {
                    "name": "admin",
                    "password": {
                        "type": "secret",
                        "hash": 9,
                        "value": "$9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg",
                    },
                },
            ],
        }
        result = self.execute_module(changed=False)
        self.maxDiff = None
        self.assertEqual(sorted(result["gathered"]), sorted(gathered))

    def test_ios_user_global_rendered(self):
        set_module_args(
            {
                "config": {
                    "enable": [
                        {
                            "password": {
                                "type": "secret",
                                "hash": 9,
                                "value": "$9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo",
                            },
                        },
                    ],
                    "users": [
                        {
                            "name": "admin",
                            "password": {
                                "type": "secret",
                                "hash": 9,
                                "value": "$9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg",
                            },
                        },
                    ],
                },
                "state": "rendered",
            },
        )
        rendered = [
            "enable secret 9 $9$q3zuC3f3vjWnWk$4BwPgPt25AUkm8Gts6aqW.NLK/90zBDnmWtOeMQqoDo",
            "username admin secret 9 $9$oV7t.SyAkhiemE$D7GYIpVS/IOc0c15ev/n3p4Wo509XwQpPfyL1fuC5Dg",
        ]
        result = self.execute_module(changed=False)
        self.maxDiff = None
        self.assertEqual(sorted(result["rendered"]), sorted(rendered))
