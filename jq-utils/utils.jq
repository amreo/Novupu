#!/usr/bin/jq -f
def normalize_tshark_json: 
    walk(
        if type == "object" then 
            with_entries(.key |= (. | split(".")[-1])) 
        else 
            . 
        end
    );

def only_layers:
    map(._source.layers);
def only_layer($layer_name):
    map(._source.layers | .[$layer_name]);
def filter_by_layer($layer_name):
    map(select(._source.layers | has($layer_name)));
def filter_llc_info_by_ids($ids):
    if ($ids | type) == "number" then
        map(select(.id == $ids))
    elif ($ids | type) == "array" then
       map(select(.id as $id | $ids | contains([$id])))
    else
        .
    end;
def filter_llc_info_by_unknown_answer_type:
    map(select(.parsed_data | has("payload")) | select(.parsed_data.payload | has("answer")) | select(.parsed_data.payload.answer.kstype=="UnknownType"));
def filter_no_erroneous_llc_info:
    map(select(.parsed_data | type == "object"));
def filter_erroneous_llc_info:
    map(select(.parsed_data | type != "object"));


# Copied from https://rosettacode.org/wiki/Non-decimal_radices/Convert#jq
# Convert the input integer to a string in the specified base (2 to 36 inclusive)
def convert(base):
  def stream:
    recurse(if . > 0 then ./base|floor else empty end) | . % base ;
  if . == 0 then "0"
  else  [stream] | reverse | .[1:]
  | if   base <  10 then map(tostring) | join("")
    elif base <= 36 then map(if . < 10 then 48 + . else . + 87 end) | implode
    else error("base too large")
    end
  end;
 
# input string is converted from "base" to an integer, within limits
# of the underlying arithmetic operations, and without error-checking:
def to_i(base):
  explode
  | reverse
  | map(if . > 96  then . - 87 else . - 48 end)  # "a" ~ 97 => 10 ~ 87
  | reduce .[] as $c
      # state: [power, ans]
      ([1,0]; (.[0] * base) as $b | [$b, .[1] + (.[0] * $c)])
  | .[1];

def remove_colons:
    split(":")
    | join("");

