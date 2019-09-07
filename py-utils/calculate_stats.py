#!/usr/bin/env python3
import json, sys, io
if len(sys.argv) > 1:
    dest_dir = sys.argv[1]
else:
    dest_dir = "." 
if dest_dir.endswith("/"):
    dest_dir = dest_dir[:-1]

def str_parsed_data(parsed_data):
    if not "payload" in item["parsed_data"]:
        return "NULL"
    payload = item["parsed_data"]["payload"]
    if "question" in payload:
        return "Q" + str(payload["mysterious_magic"]) + "_" + str(payload["type"]) 
    elif "answer" in payload: 
        return "A" + str(payload["mysterious_magic"]) + "_" + str(payload["type"]) 

data = json.load(sys.stdin)
stats = {}
prev = "START"
stats["count"] = 0
stats["count_frame_from_src_00"] = 0
stats["count_frame_from_src_01"] = 0
stats["count_frame_ssap_0x41"] = 0
stats["count_frame_ssap_0x11"] = 0
stats["count_frame_mysterious_magic_0x8008"] = 0
stats["count_frame_mysterious_magic_0x0000"] = 0
stats["count_frame_null"] = 0
stats["count_frame_question"] = 0
stats["count_frame_answer"] = 0
stats["stats_grouped_by_question_type"] = {}
stats["stats_grouped_by_answer_type"] = {}
stats["prev_types"] = {}

for item in data:
    print ("ID:", item["id"], file=sys.stderr)
    # print(item, file=sys.stderr)
    stats["count"] += 1 
    if item["src"] == "00:16:08:ff:00:00":
        stats["count_frame_from_src_00"] += 1
    if item["src"] == "00:16:08:ff:00:01":
        stats["count_frame_from_src_01"] += 1
    if item["ssap"] == "00000041":
        stats["count_frame_ssap_0x41"] += 1
    if not "payload" in item["parsed_data"]:
        stats["count_frame_null"] += 1
        continue
    payload = item["parsed_data"]["payload"]

    if payload["mysterious_magic"] == 32776:
        stats["count_frame_mysterious_magic_0x8008"] += 1
    if payload["mysterious_magic"] == 0:
        stats["count_frame_mysterious_magic_0x0000"] += 1
     
    if not str_parsed_data(item["parsed_data"]) in stats["prev_types"]:
        stats["prev_types"][str_parsed_data(item["parsed_data"])] = {}
    if not prev in stats["prev_types"][str_parsed_data(item["parsed_data"])]:
        stats["prev_types"][str_parsed_data(item["parsed_data"])][prev] = 0     
    stats["prev_types"][str_parsed_data(item["parsed_data"])][prev] += 1

    prev = str_parsed_data(item["parsed_data"])

    if "question" in payload:
        stats["count_frame_question"] += 1
        if not str(payload["type"]) in stats["stats_grouped_by_question_type"]:
            stats["stats_grouped_by_question_type"][str(payload["type"])] = {
                "count":0,
                "last_time_epoch": item["time_epoch"],
                "time_epoch_delta_sum": 0.0,
                "medium_time_epoch_delta": 0.0
            }
        stats_quest_type = stats["stats_grouped_by_question_type"][str(payload["type"])]
        stats_quest_type["count"]+=1
        if stats_quest_type["last_time_epoch"] != 0.0:
            stats_quest_type["time_epoch_delta_sum"] += (item["time_epoch"] - stats_quest_type["last_time_epoch"])
        stats_quest_type["last_time_epoch"] = item["time_epoch"]

    elif "answer" in payload: 
        stats["count_frame_answer"] += 1
        if not str(payload["type"]) in stats["stats_grouped_by_answer_type"]:
            stats["stats_grouped_by_answer_type"][str(payload["type"])] = {
                "count":0,
                "last_time_epoch": item["time_epoch"],
                "time_epoch_delta_sum": 0.0,
                "medium_time_epoch_delta": 0.0
            }
        stats_answer_type = stats["stats_grouped_by_answer_type"][str(payload["type"])]
        stats_answer_type["count"]+=1
        if stats_answer_type["last_time_epoch"] != 0.0:
            stats_answer_type["time_epoch_delta_sum"] += (item["time_epoch"] - stats_answer_type["last_time_epoch"])
        stats_answer_type["last_time_epoch"] = item["time_epoch"]

for qtype in stats["stats_grouped_by_question_type"]:
    qtype_stats = stats["stats_grouped_by_question_type"][qtype]
    if qtype_stats["count"] > 1:
        qtype_stats["medium_time_epoch_delta"] = qtype_stats["time_epoch_delta_sum"]/(qtype_stats["count"]-1)
    qtype_stats["qtype_total_ratio"] = qtype_stats["count"]/stats["count"]*100
    qtype_stats["qtype_questions_ratio"] = qtype_stats["count"]/stats["count_frame_question"]*100
for atype in stats["stats_grouped_by_answer_type"]:
    atype_stats = stats["stats_grouped_by_answer_type"][atype]
    if atype_stats["count"] > 1:
        atype_stats["medium_time_epoch_delta"] = atype_stats["time_epoch_delta_sum"]/(atype_stats["count"]-1)
    atype_stats["atype_total_ratio"] = atype_stats["count"]/stats["count"]*100
    atype_stats["atype_questions_ratio"] = atype_stats["count"]/stats["count_frame_answer"]*100

stats["frame_from_src_00_total_ratio"] = stats["count_frame_from_src_00"]/stats["count"]*100
stats["frame_from_src_01_total_ratio"] = stats["count_frame_from_src_01"]/stats["count"]*100
stats["frame_ssap_0x41_total_ratio"] = stats["count_frame_ssap_0x41"]/stats["count"]*100
stats["frame_ssap_0x11_total_ratio"] = stats["count_frame_ssap_0x11"]/stats["count"]*100
stats["frame_mysterious_magic_0x8008_total_ratio"] = stats["count_frame_mysterious_magic_0x8008"]/stats["count"]*100
stats["frame_mysterious_magic_0x0000_total_ratio"] = stats["count_frame_mysterious_magic_0x0000"]/stats["count"]*100
stats["frame_null_total_ratio"] = stats["count_frame_null"]/stats["count"]*100
stats["frame_question_total_ratio"] = stats["count_frame_question"]/stats["count"]*100
stats["frame_answer_total_ratio"] = stats["count_frame_answer"]/stats["count"]*100

json.dump(stats, sys.stdout)