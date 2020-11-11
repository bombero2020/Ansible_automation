#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import fastjsonschema
import json


# Copyright: (c) 2020, Marcelo Arizaga <marceloarizagaforonda@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: jsonator

short_description: json + validator = jsonator

version_added: "1.0"

description:
    - "This module is designed for validate a json data and structure based on a given schema"
    - Valid Data Types
In JSON, values must be one of the following data types:

a string
a number
an object (JSON object)
an array
a boolean
null

JSON values cannot be one of the following data types:

a function
a date
undefined

options:
    src:
        description:
            - The json schema source file 
        required: true
    data:
        description:
            - The input data to validate against the schema
        required: true

extends_documentation_fragment:
    - file

author:
    - Marcelo Arizaga (marceloarizagaforonda@gmail.com)
'''

EXAMPLES = '''
Pass in a correct data
  schema.json:
  {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"},
    }
  }
- name: test with a correct data
  jsonator:
    src: schema.json
    data: {"name": "Marcelo", "age": 33}

# pass in a message and have changed true
# ---------RESERVED FOR FIX JSON --------------------
# - name: Test with a message and changed output
#   jsonator:
#     src: schema.json
#     data: {"a": "Hola\\n"}
#----------------------------------------------------

# fail the module
- name: Test failure of the module
  jsonator:
    src: schema.json
    data: {"name": 26, "age": 33}
'''

RETURN = '''
src_schema:
    description: The original schema passed in as input
    type: obj
    returned: always
data_input:
    description: The original json data passed in as input
    type: ibj
    returned: always
'''


def load_schema(schema_file_name):
    """ This function handle the loading of the schema """
    try:
        with open(schema_file_name, 'r') as f:
            schema = json.load(f)
            # print(json.dumps(schema, indent=4))
        return schema
    except Exception as e:
        # print(e)
        return None


def validate_json(input_data, schema_file):
    """This function uses validate method on fastjsonschema
    INPUTS: json data for validate"""
    sche = load_schema(schema_file)
    if sche is None:
        return 'Fail', 'Could not load the schema'
    validate = fastjsonschema.compile(sche)
    try:
        data = validate(input_data)
        # print(data)
        return 'Ok', data
    except Exception as e:
        # print(e)
        return 'Fail', e


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        src=dict(type='str', required=True),
        data=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        src_schema='',
        data_input='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['data_input'] = module.params['data']
    result['src_schema'] = module.params['src']
    res = validate_json(input_data=module.params['data'], schema_file=module.params['src'])
    if res[0] is 'Ok':
        result['message'] = res[0]

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    # if module.params['new']:
    #     result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if res[0] == 'Fail':
        module.fail_json(msg=res[0]+' '+res[1], **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()


if __name__ == '__main__':
    main()