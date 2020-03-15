#!/usr/bin/env python3

import os
import json
import subprocess
from string import Template
from pprint import pprint

if 'OP_SESSION_my' not in os.environ:
  print("please set OP_SESSION_my with this command: eval $(op signin my)")
  exit()

print("loading 1password data...")
op_list = json.loads(subprocess.check_output(['op', 'list', 'items']))
print("done.")

for item in op_list:
  print("{}: {}".format(item['uuid'], item['overview']['title'].encode('utf-8').decode('utf-8')))
