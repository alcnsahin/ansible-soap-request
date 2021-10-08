SOAP Request
=========

This plugin calls SOAP and REST APIs by POST and GET methods. 

There are two modules under the ./library folder with different Python versions.

**./library**:
- soap_request_py2.py
- soap_request_py3.py

Simply change the name of the module as soap_request.py that you want to use.

Example Playbook
----------------

`ansible-playbook -i localhost soap-request.yml`


    - name: Soap Request
      hosts: localhost
      tasks:
      - name: call soap service
        soap_request:
          url: "https://host:port/api/endpoint.svc"
          method: 'POST'
          headers:
            Content-Type: text/xml; charset=utf-8
            Another-Header: foo
          body: '<xmlString></xmlString>'
        register: result
      - name: dump result
        debug:
          msg: '{{ result }}'

Author Information
------------------

If you have any question please contact me on [Linkedin](https://www.linkedin.com/in/alcnsahin/)
