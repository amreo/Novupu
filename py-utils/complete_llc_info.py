#!/usr/bin/env python3
import sys, json
import tempfile
import subprocess
import time

data = json.load(sys.stdin)
for item in data:
    print ("ID:", item["id"], file=sys.stderr)
    with tempfile.NamedTemporaryFile() as temp: 
        print("    TMP:", temp.name, file=sys.stderr)
        temp.write(bytes.fromhex(item["data"]))
        temp.flush()
        
        ksdump = subprocess.run(["ksdump", "--format", "json", temp.name, "ksy/L40P.ksy"], capture_output=True)
        if ksdump.returncode == 0:
            item["parsed_data"] = json.loads(ksdump.stdout.decode())
        else:
            json.dump(item, sys.stderr)
            print("    STDERR:", ksdump.stderr.decode(), file=sys.stderr)
            item["parsed_data"] = "ERROR!"
        
json.dump(data, sys.stdout)