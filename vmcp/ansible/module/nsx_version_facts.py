#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: containers_facts

short_description: Collect docker containers version information

version_added: "2.4"

description:
    - "Collect docker containers version information."
'''


RETURN = '''
containers
    description: a list of containers version information
    type: list
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
