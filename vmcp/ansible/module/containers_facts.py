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
import docker

def get_containers_facts():
    facts = []
    client = docker.from_env()
    for c in client.containers.list():
        facts.append({
            "name"  : c.name,
            "id"    : c.short_id,
            "image" : c.attrs['Config']['Image'],
            "status"   : c.attrs['State']['Status'],
            "created"   : c.attrs['Created']
        })
    return facts

def run_module():
    result = dict(
        changed=False,
        containers=get_containers_facts()
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
