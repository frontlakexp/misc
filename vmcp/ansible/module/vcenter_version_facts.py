#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: vcenter_version_facts
short_description: Collect vCenter and ESX hosts version information
description:
- This module can be used to collect vCenter and ESX hosts version information.
notes:
- Tested on vCenter 6.7
requirements:
- python >= 2.6
- PyVmomi
extends_documentation_fragment: vmware.documentation
'''

EXAMPLES = r'''
- name: Collect vCenter and ESX hosts version information
  vcenter_version_facts:
    hostname: '{{ vcenter_hostname }}'
    username: '{{ vcenter_username }}'
    password: '{{ vcenter_password }}'
'''

RETURN = r'''
components:
    description:
    - dict about vCenter version information
    returned: success
    type: object
    sample:
        {
          "invocation": {
            "module_args": {
              "username": "administrator@vmcp.local",
              "password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
              "validate_certs": false,
              "hostname": "192.168.100.2",
              "port": 443
            }
          },
          "changed": false,
          "components": {
            "vCenter": {
              "name": "VMware vCenter Server",
              "apiVersion": "6.7",
              "apiType": "VirtualCenter",
              "version": "6.7.0",
              "build": "9433931",
              "fullName": "VMware vCenter Server 6.7.0 build-9433931"
            },
          "hosts": [
              {
                "esx09-r02.p01.lsvg02.vmcp.vs.management": {
                  "name": "VMware ESXi",
                  "apiVersion": "6.7",
                  "apiType": "HostAgent",
                  "version": "6.7.0",
                  "build": "9484548",
                  "fullName": "VMware ESXi 6.7.0 build-9484548"
                }
              },
              {
                "esx10-r02.p01.lsvg02.vmcp.vs.management": {
                  "name": "VMware ESXi",
                  "apiVersion": "6.7",
                  "apiType": "HostAgent",
                  "version": "6.7.0",
                  "build": "9484548",
                  "fullName": "VMware ESXi 6.7.0 build-9484548"
                }
              }
             }
            ]
          }
        }
 '''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware import vmware_argument_spec, PyVmomi
from pyVmomi import vim

VCENTER_FACTS = [
   # "dynamicType",
   # "dynamicProperty",
   "name",
   "fullName",
   # "vendor",
   "version",
   "build",
   # "localeVersion",
   # "localeBuild",
   # "osType",
   # "productLineId",
   "apiType",
   "apiVersion",
   # "instanceUuid",
   # "licenseProductName",
   # "licenseProductVersion"
]

HOSTS_FACTS = [
   # "dynamicType",
   # "dynamicProperty",
   "name",
   "fullName",
   # "vendor",
   "version",
   "build",
   # "localeVersion",
   # "localeBuild",
   # "osType",
   # "productLineId",
   "apiType",
   "apiVersion",
   # "instanceUuid",
   # "licenseProductName",
   # "licenseProductVersion",
]

def extract_facts(obj, attributes):
    facts = {}
    for attr in attributes:
        facts[attr] = getattr(obj, attr, '')

    return facts


class VCenterVersionManager(PyVmomi):
    def __init__(self, module):
        super(VCenterVersionManager, self).__init__(module)

    def gather_version_facts(self):

        if not self.content:
            self.module.exit_json(changed=False, components=dict())

        vc_facts = extract_facts(self.content.about, VCENTER_FACTS)

        container = self.content.viewManager.CreateContainerView(
                self.content.rootFolder, [vim.HostSystem], True)
        hosts_facts = []
        for host in container.view:
            hosts_facts.append({host.summary.config.name :
                extract_facts(host.summary.config.product, HOSTS_FACTS)})

        self.module.exit_json(
            changed=False,
            components=dict(
                vCenter=vc_facts,
                hosts=hosts_facts
            )
        )


def main():
    argument_spec = vmware_argument_spec()

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    vcenter_version_facts_mgr = VCenterVersionManager(module)
    vcenter_version_facts_mgr.gather_version_facts()


if __name__ == "__main__":
    main()
