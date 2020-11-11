import fastjsonschema
import json


# """Valid Data Types
# In JSON, values must be one of the following data types:
#
# a string
# a number
# an object (JSON object)
# an array
# a boolean
# null
#
# JSON values cannot be one of the following data types:
#
# a function
# a date
# undefined"""

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


def test():
    schema_file_name = 'my_first_schema.json'
    json_data_to_validate = {"nombre": "Marcelo",
        "apellido1": "Arizaga",
        "apellido2": "Foronda",
        "fecha_nacimiento": "hola"}
    r = validate_json(json_data_to_validate, schema_file_name)
    print(r)


test()