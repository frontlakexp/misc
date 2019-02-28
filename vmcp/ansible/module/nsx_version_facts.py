#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: nsx_version_facts

short_description: Collect NSX version information
description:
    - "Collect docker containers version information."
version_added: "2.7"
notes:
- Tested on NSX 2.2.0.0.0.8680778
'''

EXAMPLES = r'''
- name: Collect NSX version information
  nsx_version_facts:
    hostname: '{{ vcenter_hostname }}'
    username: '{{ vcenter_username }}'
    password: '{{ vcenter_password }}'
'''

RETURN = '''
components
    description:
    - dict about NSX version information
    type: object
        {
          "invocation": {
            "module_args": {
              "username": "admin",
              "password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
              "validate_certs": "no",
              "hostname": "192.168.100.3"
            }
          },
          "changed": false,
          "components": {
            "nsx": {
              "version": "2.2.0.0.0.8680778"
            }
          }
        }
'''

from ansible.module_utils.basic import AnsibleModule
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def nsx_argument_spec():
    return dict(
        hostname=dict(type='str',
                      required=True,
                      ),
        username=dict(type='str',
                      required=True),
        password=dict(type='str',
                      required=True,
                      no_log=True),
        validate_certs=dict(type='str',
                            required=False,
                            default='yes'))

def run_module():
    module = AnsibleModule(
        argument_spec=nsx_argument_spec(),
        supports_check_mode=True
    )

    hostname = module.params['hostname']
    username = module.params['username']
    password = module.params['password']
    validate_certs = module.params['validate_certs'] in ['yes', 'Yes', 'YES']

    url = "https://{}/api/v1/node".format(hostname)
    res = requests.get(url, auth=(username, password), verify=validate_certs)
    if res.status_code == 200:
        payload = res.json()
        result = dict(
            changed=False,
            components=dict(
                nsx=dict(
                    version=payload['node_version']
                )
            )
        )
        module.exit_json(**result)
    else:
        module.fail_json(error_code=res.status_code)

def main():
    run_module()

if __name__ == '__main__':
    main()
