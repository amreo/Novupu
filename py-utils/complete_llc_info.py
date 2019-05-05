#!/usr/bin/env python3
import sys, json
import l40p
import tempfile
import subprocess
import time

data = json.load(sys.stdin)
for item in data:
    print (">>>", item["id"], file=sys.stderr)
    with tempfile.NamedTemporaryFile() as temp: 
        print(temp.name, file=sys.stderr)
        temp.write(bytes.fromhex(item["data"]))
        temp.flush()
        ksdump = subprocess.run(["ksdump", "--format", "json", temp.name, "ksy/L40P.ksy"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        item["parsed_data"] = json.loads(ksdump.stdout.decode())
json.dump(data, sys.stdout)