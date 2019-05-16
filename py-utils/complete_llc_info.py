#!/usr/bin/env python3
import sys, json
import tempfile
import subprocess
import time
from l40p import L40p
from enum import Enum


def serialize(obj):
    if isinstance(obj, bytes):
        return obj.hex()
    asDict = obj.__dict__
    if isinstance(obj, Enum):
        return obj.name
    asDict.pop("_root", 0)
    asDict.pop("_parent",0)
    asDict.pop("_io", 0)
    asDict["kstype"]=obj.__class__.__name__
    return asDict

data = json.load(sys.stdin)
for item in data:
    print ("ID:", item["id"], file=sys.stderr)
    try:
        parsedData = L40p.from_bytes(bytes.fromhex(item["data"]))
        item["parsed_data"] = parsedData
    except Exception as e:
        item["parsed_data"] = "ERROR!"
        print("    STDERR:", e, file=sys.stderr)

json.dump(data, sys.stdout, default=serialize)