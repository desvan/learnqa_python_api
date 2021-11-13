import json


json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And ' \
            'this is a second message","timestamp":"2021-06-04 16:41:01"}]} '
obj = json.loads(json_text)

key = "message2"

try:
    print(obj["messages"][1][key])
except KeyError:
    print(f'There is no key parameter <{key}> in JSON or an incorrect path is specified for the key parameter <{key}>')


