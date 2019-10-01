#!/usr/bin/env python3
import sys, json

data = json.load(sys.stdin)

qa_map = {}
out = []

for item in data:
    if not "payload" in item["parsed_data"]:
        continue
    payload = item["parsed_data"]["payload"]
    print ("ID:", item["id"], " QID:", payload["type"], file=sys.stderr)
    if "question" in payload:
        if not str(payload["question"]["question_id"]) in qa_map:
            qa_map[str(payload["question"]["question_id"])] = { 
                "question": None, 
                "answer": None
            }
        qa_map[str(payload["question"]["question_id"])]["question"] = item
    elif "answer" in payload:
        if not str(payload["answer"]["question_id"]) in qa_map:
            qa_map[str(payload["answer"]["question_id"])] = { 
                "question": None, 
                "answer": None
            }
        qa_map[str(payload["answer"]["question_id"])]["answer"] = item


for key in qa_map:
    out.append({ 
        "question": qa_map[key]["question"], 
        "answer": qa_map[key]["answer"]
    })


json.dump(out, sys.stdout)