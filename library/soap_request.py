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
    method:
        required: false
        description:
            - GET|POST
    body:
        required: true
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
import urllib2
import ssl
import base64

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get_auth_token(user, password):
    token = 'Basic '
    if all(v is not None for v in [user, password]):
        token += base64.b64encode(user + ":" + password)
    return token


def get(url, headers, force_basic_auth, user, password):
    req = urllib2.urlopen(url)
    if force_basic_auth:
        req.add_header('Authorization', get_auth_token(user, password))
    response = urllib2.Request(req)
    return response.read()


def post(url, headers, body, force_basic_auth, user, password):
    req = urllib2.Request(url)
    if force_basic_auth:
        req.add_header('Authorization', get_auth_token(user, password))
    for header_key, header_value in headers.iteritems():
        req.add_header(header_key, header_value)
    response = urllib2.urlopen(req, data=body, context=ctx)
    return response.read()


def run_module():
    module_args = dict(
        url=dict(type='str', required=True),
        force_basic_auth=dict(type='bool', required=False, default=False),
        user=dict(type='str', required=False, default=None),
        password=dict(type='str', required=False, default=None),
        method=dict(required=False, default='GET', choices=['GET', 'POST', 'PUT']),
        body=dict(type='str', required=True),
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
    body = module.params['body']
    user = module.params['user']
    password = module.params['password']
    force_basic_auth = module.params['force_basic_auth']

    if module.check_mode:
        return result

    if module.params['method'] == 'GET':
        result['message'] = get(url, headers, force_basic_auth, user, password)
    elif module.params['method'] == 'POST':
        result['message'] = post(url, headers, body, force_basic_auth, user, password)
        result['changed'] = True
    else:
        module.fail_json(msg='pls specify a method GET|POST', **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
