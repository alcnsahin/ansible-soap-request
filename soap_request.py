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

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get(url):
    req = urllib2.urlopen(url)
    response = urllib2.Request(req)
    return response.read()


def post(url, headers, body):
    req = urllib2.Request(url)
    for header_key, header_value in headers.iteritems():
        req.add_header(header_key, header_value)
    response = urllib2.urlopen(req, data=body, context=ctx)
    return response.read()


def run_module():
    module_args = dict(
        url=dict(type='str', required=True),
        force_basic_auth=dict(type='bool', required=False, default=False),
        user=dict(type='str', required=False),
        password=dict(type='str', required=False),
        method=dict(required=False, default='GET',
                    choices=['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'OPTIONS', 'PATCH', 'TRACE', 'CONNECT',
                             'REFRESH']),
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

    if module.check_mode:
        return result

    if module.params['method'] == 'GET':
        result['message'] = get(module.params['url'])
    elif module.params['method'] == 'POST':
        result['message'] = post(module.params['url'], module.params['headers'], module.params['body'])
        result['changed'] = True
    else:
        module.fail_json(msg='pls specify a method GET|POST', **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
