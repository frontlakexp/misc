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
module: my_sample_module

short_description: This is my sample module

version_added: "2.4"

description:
    - "This is my longer description explaining my sample module"

options:
    name:
        description:
            - This is the message to send to the sample module
        required: true
    new:
        description:
            - Control to demo if the result of this module is changed or not
        required: false

extends_documentation_fragment:
    - azure

author:
    - Your Name (@yourhandle)
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  my_new_test_module:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_new_test_module:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_new_test_module:
    name: fail me
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''

from ansible.module_utils.basic import AnsibleModule
import docker

def get_docker_facts():
    facts = []
    client = docker.from_env()
    for c in client.containers.list():
        facts.append({
            "name"  : c.name,
            "id"    : c.short_id,
            "image" : c.attrs['Config']['Image'],
            "status"   : c.attrs['State']['Status']
        })
    return facts

def run_module():
    result = dict(
        changed=False,
        containers=get_docker_facts()
    )

    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True
    )

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()

