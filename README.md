SOAP Request
=========

This plugin calls soap and rest apis by POST and GET methods.


Example Playbook
----------------

`ansible-playbook soap-request.yml`


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
