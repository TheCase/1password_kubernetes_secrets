#!/usr/bin/env python3

import json
import yaml
import subprocess
import base64
from string import Template
from attrdict import AttrDict
from pprint import pprint

mapfile = 'field_map.yaml'

outfile = 'secrets.yaml'

output = str()

try:
    f = open(mapfile)
    imap = yaml.load(f.read(), Loader=yaml.SafeLoader)
    f.close()
except FileNotFoundError:
    print('{} does not exist'.format(mapfile))

print("reading map for a list of necessary OP items...")
uuids = list()
for name, properties in imap.items():
  for secret, detail in properties['secrets'].items():
      if detail['uuid'] not in uuids:
        uuids.append(detail['uuid'])

op_secrets = dict()
for uuid in uuids:
  print("fetching details for {}".format(uuid))
  op_secrets[uuid] = json.loads(subprocess.check_output(['op', 'get', 'item', uuid]))

template = Template("""---
apiVersion: v1
kind: Secret
type: Opaque
metadata:
  name: $name
  namespace: $namespace
data:
$items""")

def section_search(uuid,d,field):
  for i in d:
    if 'fields' in i.keys():
      for e in i.fields:
        for k,v in e.items():
          if k == 't':
            key = v
          if k == 'v':
            value = v
        if key == field:
          return(value)
  print("ERROR: field '{}' not found in uuid:{}".format(field,uuid))
  print("debug (available section fields): ")
  pprint(s.details.sections)
  exit()


for name, properties in imap.items():
  items = str()
  for secret, detail in properties['secrets'].items():
    uuid = detail['uuid']
    field = detail['field']
    s = AttrDict(op_secrets[uuid])
    if field == 'username':
      raw = s.details.fields[0].value
    elif field == 'password':
      raw = s.details.fields[1].value
    elif field == 'url':
      raw = s.overview.url
    else:
      raw = section_search(uuid, s.details.sections, field).rstrip()
    encrypted = base64.b64encode(raw.encode('utf-8'))
    items += "  {}: {}\n".format(secret, encrypted.decode('utf-8'))
  block = template.substitute(name=name,
                              namespace=properties['namespace'],
                              items=items)
  output += block

print("writing out to {}".format(outfile))
f = open(outfile, "w")
f.write(output)
f.close()


print("finished.")

