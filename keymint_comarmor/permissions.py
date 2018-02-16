# Copyright 2014 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import xml.etree.ElementTree as ElementTree

from copy import deepcopy

import xmlschema

import comarmor
from comarmor.xml.utils import pretty_xml, tidy_xml, beautify_xml

# from .exceptions import InvalidPermissionsXML
# from .namespace import DDSNamespaceHelper
# from .schemas import get_dds_schema_path
# from .smime.sign import sign_data


class CriteriasHelpter:
    """Help build criteria into artifacts."""

    def __init__(self):
        pass


# class KeymintCriteriasHelper(CriteriasHelpter):
#     """Help build permission into artifacts."""
#
#     _dds_expression_list_types = ['partitions', 'data_tags']
#
#     def __init__(self):
#         self.dds_namespaces_helper = DDSNamespaceHelper()
#
#     def _dds_expressions(self, dds_criteria, dds_criterias):
#         for dds_criteria in dds_criterias:
#             dds_criteria.append(expression_list)
#
#     def topics(self, expression_list):
#         topics = ElementTree.Element('topics')
#         for expression in expression_list.getchildren():
#             topic = ElementTree.Element('topic')
#             formater = getattr(self.dds_namespaces_helper, expression.tag)
#             topic.text = formater(expression.text)
#             topics.append(topic)
#         return topics
#
#     def ros_publish(self, context, criteria):
#         dds_publish = ElementTree.Element('publish')
#         dds_criterias = []
#         dds_criterias.append(dds_publish)
#         for expression_list in criteria.getchildren():
#             if expression_list.tag in self._dds_expression_list_types:
#                 self._dds_expressions(dds_criteria, dds_criterias)
#                 continue
#             else:
#                 formater = getattr(self, expression_list.tag)
#                 expression_list = formater(expression_list)
#                 dds_publish.append(expression_list)
#         return dds_criterias
#
#     def ros_subscribe(self, context, criteria):
#         dds_subscribe = ElementTree.Element('subscribe')
#         dds_criterias = []
#         dds_criterias.append(dds_subscribe)
#         for expression_list in criteria.getchildren():
#             if expression_list.tag in self._dds_expression_list_types:
#                 self._dds_expressions(dds_criteria, dds_criterias)
#                 continue
#             else:
#                 formater = getattr(self, expression_list.tag)
#                 expression_list = formater(expression_list)
#                 dds_subscribe.append(expression_list)
#         return dds_criterias
#
#     def ros_call(self, context, criteria):
#         # TODO
#         return []
#
#     def ros_execute(self, context, criteria):
#         # TODO
#         return []
#
#     def ros_request(self, context, criteria):
#         # TODO
#         return []
#
#     def ros_operate(self, context, criteria):
#         # TODO
#         return []
#
#     def ros_read(self, context, criteria):
#         # TODO
#         return []
#
#     def ros_write(self, context, criteria):
#         # TODO
#         return []


class PermissionsHelper:
    """Help build permission into artifacts."""

    def __init__(self):
        pass

    def create(self, context):
        raise NotImplementedError


class ComArmorPermissionsHelper(PermissionsHelper):
    """Help build permission into artifacts."""

    def __init__(self):
        pass
        # self.keymint_criterias_helper = KeymintCriteriasHelper()

    def _build_criterias(self, context, comarmor_rule):
        keymint_criterias = ElementTree.Element(comarmor_rule.tag + 's')
        keymint_criteria = ElementTree.Element(comarmor_rule.tag)
        keymint_criteria.text = comarmor_rule.find('attachment').text
        keymint_criterias.append(keymint_criteria)
        return keymint_criterias

    def _build_rules(self, context, comarmor_rules):
        keymint_rules = ElementTree.Element('keymint_rules')

        for comarmor_rule in comarmor_rules.getchildren():
            comarmor_permissions = comarmor_rule.find('permissions')
            for comarmor_permission in comarmor_permissions.getchildren():
                keymint_rule = ElementTree.Element(comarmor_permission.tag)
                keymint_criterias = self._build_criterias(context, comarmor_rule)
                keymint_rule.append(keymint_criterias)
                keymint_rules.append(keymint_rule)

        return keymint_rules

    def _build_grant(self, context, profile_storage):

        grant = ElementTree.Element('grant')
        grant.set('name', context.pkg_name)

        profile_storage_filtered = profile_storage.filter_profiles(key='/' + context.pkg_name)

        deny_rule = ElementTree.Element('deny_rule')
        comarmor_deny_rules = profile_storage_filtered.findall('.//*[@qualifier="DENY"]')
        keymint_deny_rules = self._build_rules(context, comarmor_deny_rules)
        deny_rule.extend(keymint_deny_rules)
        if len(deny_rule):
            grant.append(deny_rule)

        allow_rule = ElementTree.Element('allow_rule')
        comarmor_allow_rules = profile_storage_filtered.findall('.//*[@qualifier="ALLOW"]')
        keymint_allow_rules = self._build_rules(context, comarmor_allow_rules)
        allow_rule.extend(keymint_allow_rules)
        if len(allow_rule):
            grant.append(allow_rule)

        default =  ElementTree.Element('default')
        default.text = "DENY"
        grant.append(default)

        return grant

    def create(self, context):
        policies = deepcopy(context.profile_manifest.policies)
        permissions = ElementTree.Element('permissions')

        profile_paths = []
        for profile_path in policies.findall("./policy/comarmor/profile_path"):
            profile_paths.append(os.path.join(context.profile_space, profile_path.text))

        profile_storage = comarmor.parse_profiles(profile_paths)
        grant = self._build_grant(context, profile_storage)

        print(comarmor.xml.utils.beautify_xml(grant))

        return grant
