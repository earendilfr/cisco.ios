# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the
# ansible.content_builder.
#
# Manually editing this file is not advised.
#
# To update the argspec make the desired changes
# in the documentation in the module file and re-run
# ansible.content_builder commenting out
# the path to external 'docstring' in build.yaml.
#
##############################################

"""
The arg spec for the ios_user_global module
"""


class User_globalArgs(object):  # pylint: disable=R0903
    """The arg spec for the ios_user_global module
    """

    argument_spec = {
        "config": {
            "type": "dict",
            "options": {
                "enable": {
                    "elements": "dict",
                    "options": {
                        "password": {
                            "type": "dict",
                            "options": {
                                "type": {
                                    "choices": ["password", "secret"],
                                    "default": "secret",
                                    "type": "str",
                                },
                                "hash": {
                                    "choices": [0, 5, 6, 7, 8, 9],
                                    "default": 0,
                                    "type": "int",
                                },
                                "value": {"type": "str", "no_log": True},
                            },
                            "no_log": False,
                        },
                        "level": {"type": "int"},
                    },
                    "type": "list",
                },
                "users": {
                    "elements": "dict",
                    "options": {
                        "name": {"type": "str", "required": True},
                        "command": {
                            "choices": ["new", "old"],
                            "default": "old",
                            "type": "str",
                        },
                        "parameters": {
                            "type": "dict",
                            "options": {
                                "nopassword": {"type": "bool"},
                                "password": {
                                    "type": "dict",
                                    "options": {
                                        "type": {
                                            "choices": ["password", "secret"],
                                            "default": "secret",
                                            "type": "str",
                                        },
                                        "hash": {
                                            "choices": [0, 5, 6, 7, 8, 9],
                                            "default": 0,
                                            "type": "int",
                                        },
                                        "value": {"type": "str", "no_log": True},
                                    },
                                    "no_log": False,
                                },
                                "privilege": {"type": "int"},
                                "view": {"type": "str"},
                            },
                        },
                    },
                    "type": "list",
                },
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "choices": [
                "merged",
                "overridden",
                "deleted",
                "rendered",
                "gathered",
                "parsed",
            ],
            "default": "merged",
            "type": "str",
        },
    }  # pylint: disable=C0301
