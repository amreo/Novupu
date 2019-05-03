#!/usr/bin/jq -f
include "jq-utils/utils";
filter_by_layer("eth") 
| filter_by_layer("llc")
| only_layers
| map({
    src: .eth.src,
    dst: .eth.dst,
    ssap: .llc.ssap | .[2:],
    dsap: .llc.dsap | .[2:],
    data_len: .data.len,
    data: .data.data | remove_colons
})