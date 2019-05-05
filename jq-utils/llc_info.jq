#!/usr/bin/jq -f
include "jq-utils/utils";
filter_by_layer("eth") 
| filter_by_layer("llc")
| only_layers
| map({
    id: .frame.number | tonumber,
    time: .frame.time,
    time_epoch: .frame.time_epoch | tonumber,  
    src: .eth.src,
    dst: .eth.dst,
    ssap: .llc.ssap | .[2:],
    dsap: .llc.dsap | .[2:],
    data_len: .data.len | tonumber,
    data: .data.data | remove_colons
})