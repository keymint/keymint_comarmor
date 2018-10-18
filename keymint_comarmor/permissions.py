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

from copy import deepcopy
import os
from xml.etree import cElementTree as ElementTree

import comarmor
from comarmor.xml.utils import beautify_xml


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

    def _build_criterias(self, context, comarmor_rule):
        keymint_criterias = ElementTree.Element(comarmor_rule.tag + 's')
        comarmor_attachments = comarmor_rule.find('attachments')
        for comarmor_attachment in list(comarmor_attachments):
            keymint_criteria = ElementTree.Element(comarmor_rule.tag)
            keymint_criteria.text = comarmor_attachment.text
            keymint_criterias.append(keymint_criteria)
        return keymint_criterias

    def _compress_rule(self, context, rule):
        keymint_rule = ElementTree.Element(rule.tag)

        for criteria in list(rule):
            keymint_criteria = keymint_rule.find(criteria.tag)
            if keymint_criteria is None:
                keymint_rule.append(criteria)
            else:
                for criterians in criteria.getchildren():
                    keymint_criterians = keymint_criteria.find(criterians.tag)
                    keymint_criterian_texts = list(keymint_criterians.itertext())
                    for criterian in criterians:
                        if criterian.text not in keymint_criterian_texts:
                            keymint_criterians.append(criterian)
        return keymint_rule

    def _build_rules(self, context, comarmor_rules):
        keymint_rules = ElementTree.Element('keymint_rules')

        for comarmor_rule in comarmor_rules.getchildren():
            comarmor_permissions = comarmor_rule.find('permissions')
            for comarmor_permission in comarmor_permissions.getchildren():
                keymint_rule = ElementTree.Element(comarmor_permission.tag)
                keymint_criterias = self._build_criterias(context, comarmor_rule)
                keymint_rule.append(keymint_criterias)
                keymint_rules.append(keymint_rule)

        keymint_rules = self._compress_rule(context, keymint_rules)
        return keymint_rules

    def _build_grant(self, context, profile_storage):

        grant = ElementTree.Element('grant')
        grant.set('name', context.pkg_name)

        profile_storage_filtered = profile_storage.filter_profile(key='/' + context.pkg_name)

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

        default = ElementTree.Element('default')
        default.text = 'DENY'
        grant.append(default)

        return grant

    def _build_permissions(self, context, policies):
        permissions = ElementTree.Element('permissions')

        profile_paths = []
        for profile_path in policies.findall('./policy/comarmor/profile_path'):
            profile_paths.append(os.path.join(context.profile_space, profile_path.text))

        profile_storage = comarmor.parse_profiles(profile_paths)
        grant = self._build_grant(context, profile_storage)

        permissions.append(grant)
        return permissions

    def create(self, context):
        root = ElementTree.Element('package')

        policies = deepcopy(context.profile_manifest.policies)
        permissions = self._build_permissions(context, policies)

        root.append(permissions)
        return beautify_xml(root)
