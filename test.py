import json

f = open('test.txt')
a = json.loads(f.read())
print(a["server_port"])