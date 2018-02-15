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


# class DDSCriteriasHelper(CriteriasHelpter):
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

    # _dds_criteria_types = ['publish', 'subscribe', 'relay']

    def __init__(self):
        pass
        # self.dds_criterias_helper = DDSCriteriasHelper()

    # def _build_criterias(self, context, criteria):
    #     formater = getattr(self.dds_criterias_helper, criteria.tag)
    #     return formater(context, criteria)

    # def _build_rule(self, context, rule):
    #     dds_rule = ElementTree.Element(rule.tag)
    #
    #     domains = rule.find('domains')
    #     dds_rule.append(domains)
    #     rule.remove(domains)
    #
    #     for criteria in rule.getchildren():
    #         if criteria.tag in self._dds_criteria_types:
    #             dds_rule.append(criteria)
    #         else:
    #             dds_criterias = self._build_criterias(context, criteria)
    #             dds_rule.extend(dds_criterias)
    #     return dds_rule

    # def _build_grant(self, context, grant):
    #
    #     dds_grant = ElementTree.Element('grant')
    #
    #     name = grant.get('name')
    #     dds_grant.set('name', name)
    #
    #     subject_name = grant.find('subject_name')
    #     subject_name.text = subject_name.text.format(**grant.attrib)
    #     dds_grant.append(subject_name)
    #     grant.remove(subject_name)
    #
    #     validity = grant.find('validity')
    #     dds_grant.append(validity)
    #     grant.remove(validity)
    #
    #     default = grant.find('default')
    #     grant.remove(default)
    #
    #     for rule in grant.getchildren():
    #         dds_rule = self._build_rule(context, rule)
    #         dds_grant.append(dds_rule)
    #
    #     dds_grant.append(default)
    #
    #     return dds_grant

    def create(self, context):
        policies = deepcopy(context.profile_manifest.policies)
        permissions = ElementTree.Element('permissions')

        profile_paths = []
        for profile_path in policies.findall("./policy/comarmor/profile_path"):
            profile_paths.append(os.path.join(context.profile_space, profile_path.text))

        profile_storage = comarmor.parse_profiles(profile_paths)
        profile_storage_filtered = profile_storage.filter_profiles(key='/' + context.pkg_name)
        results = profile_storage_filtered.findall('.//*[@qualifier="ALLOW"]')
        print(comarmor.xml.utils.beautify_xml(results))

        return None
