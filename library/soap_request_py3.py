#!/usr/bin/python

# Copyright: (c) 2020, Alican Sahin <alcnsahin@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: soap_request
short_description: Soap request handler
version_added: "1.0"
description:
    - "This module calls soap web services"
options:
    url:
        required: true
        description:
            - url of the services
    force_basic_auth:
        required: false
        description:
            - ...
    user:
        required: false
        description:
            - ...
    password:
        required: false
        description:
            - ...
    api_type:
        required: true
        description:
            - REST|SOAP
    method:
        required: false
        description:
            - GET|POST
    json_body:
        required: false
        description:
            - ...
    xml_body:
        required: false
        description:
            - ...
    headers:
        required: false
        description:
            - ...
author:
    - Alican Sahin (@alcnsahin)
'''

EXAMPLES = '''
# Simple example
- name: Test with a message and changed output
  soap_request:
    url: https://host:port/endpoint
    method: 'POST'
    body: '<xmlString></xmlString>'
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''

from ansible.module_utils.basic import AnsibleModule
import requests
import urllib3
import json
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_auth_token(user, password):
    token = 'Basic '
    if all(v is not None for v in [user, password]):
        token += base64.b64encode(user + ":" + password)
    return token


def get(url, headers, force_basic_auth, user, password):
    if force_basic_auth:
        headers["Authorization"] = get_auth_token(user, password)
    r = requests.get(url, headers=headers)
    return r.text, r.headers


def post(url, headers, body, force_basic_auth, user, password):
    if force_basic_auth:
        headers["Authorization"] = get_auth_token(user, password)
    for header_key, header_value in headers.items():
        headers[header_key] = header_value
    r = requests.post(url, data=body, headers=headers)
    return r.text, r.headers


def run_module():
    module_args = dict(
        url=dict(type='str', required=True),
        force_basic_auth=dict(type='bool', required=False, default=False),
        user=dict(type='str', required=False, default=None),
        password=dict(type='str', required=False, default=None),
        api_type=dict(type='str', required=True, choices=['REST', 'SOAP']),
        method=dict(required=False, default='GET', choices=['GET', 'POST']),
        json_body=dict(type='json', required=False),
        xml_body=dict(type='str', required=False),
        headers=dict(required=False, type='dict', default={})
    )
    result = dict(
        changed=False,
        original_message='',
        message=''
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    url = module.params['url']
    headers = module.params['headers']
    api_type = module.params['api_type']
    json_body = module.params['json_body']
    xml_body = module.params['xml_body']
    user = module.params['user']
    password = module.params['password']
    force_basic_auth = module.params['force_basic_auth']

    if module.check_mode:
        return result

    if module.params['method'] == 'GET':
        response_body, response_headers = get(url, headers, force_basic_auth, user, password)
        result['message'] = response_body
        result['response_headers'] = dict(response_headers)

    elif module.params['method'] == 'POST':
        if api_type == "REST":
            body = json.loads(json_body)
        else:
            body = xml_body

        response_body, response_headers = post(url, headers, body, force_basic_auth, user, password)
        result['message'] = response_body
        result['response_headers'] = dict(response_headers)
        result['changed'] = True

    else:
        module.fail_json(msg='specify the http method (get or post available)', **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
