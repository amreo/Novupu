#!/usr/bin/env python3
import json, sys, io
if len(sys.argv) > 1:
    dest_dir = sys.argv[1]
else:
    dest_dir = "." 
if dest_dir.endswith("/"):
    dest_dir = dest_dir[:-1]

data = json.load(sys.stdin)

for item in data:
    file = open(dest_dir + "/" + item["id"] + ".bin", "wb")
    file.write(bytes.fromhex(item["data"]))
    file.close()