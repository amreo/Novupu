meta:
  id: l40p
  title: A protocol used to establish a LTE connection using a WLTSS-114
  license: CC-4.0-NC-SA
  encoding: ascii
  endian: be
doc: |
  I think L40P is a protocol used to establish a LTE connection using a WLTSS-114.
  It seems to use a request/response mechanism.
  Any L10P pdu is L40P wih zero length payload.
seq:
  - id: seq
    type: u2
    doc: Sequence number
  - id: request_seq
    type: u2
    doc: The sequence number of the request
  - id: magic0
    contents: [0x00, 0x00]
  - id: length
    type: u2
    doc: The length of the payload
  - id: payload
    type: payload
    doc: The payload
    size: length
    if: length > 0 
types:
  payload:
    seq:
      - id: mysterious_magic
        type: u2
        doc: A mysterious magic value. It may be 0x8008 or 0x0000. Maybe a primary type?
      - id: type
        type: u2
        doc: The type of information (or command?)
      - id: question
        if: _parent.length-4 == 8
        type: question
      - id: answer
        type: 
          switch-on: type
          cases:
            0x0002: dev_info
            0x00DD: unknown_answer_type2
            0x00F0: unknown_answer_type3
            0x00F4: network_status_info
            0x010D: apn_info
            0x010F: data_link_connection_info 
            0x0133: ping_info
            0x0136: ping2_info  
            0x014B: iccid_info
            0x0151: unknown_answer_type1
            0x0175: unknown_answer_type0
            0x0186:  data_link_status_info2
            0x0187: data_link_status_info
            _: unknown_type
        size: _parent.length-4
        if: _parent.length-4 > 8
  unknown_type:
    seq:
      - id: data
        size-eos: true
  question:
    seq:
      - id: time0
        type: u4
        doc: I suspect this field contains the number of milliseconds passed since something something, but it doesn't seem regular...
      - id: magic0
        contents: [0x00, 0x00]
      - id: question_id
        type: u2
        doc: The id of the questions
  iccid_info:
    seq:
      - id: time_delta_milliseconds
        type: u4
        doc: I suspect this field contains the number of milliseconds passed since something something  
      - id: magic0
        contents: [0x00, 0x00]
        doc: I suspect this magic0 and unknown1 is a u4 number
      - id: question_id
        type: u2
        doc: The question being answered
      - id: iccid
        type: str
        size: 21
        doc: ICCID number
      - id: magic1
        contents: [0x00, 0x00, 0x00, 0x00]
  dev_info:
    seq:
      - id: time_delta_milliseconds
        type: u4
        doc: I suspect this field contains the number of milliseconds passed since something something  
      - id: magic0
        contents: [0x00, 0x00]
      - id: question_id
        type: u2
        doc: The question being answered
      - id: magic1
        contents: [0x00]
      - id: version
        type: u1
        repeat: expr
        repeat-expr: 4
        doc: It should contain the version of the firmware
      - id: magic2
        contents: [0x00, 0x00, 0x00, 0x7a, 0xbe, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
      - id: entries_length
        type: u2
        doc: The length of all entries
      - id: entries
        type: dev_info_entries
        size: entries_length
      - id: magic3
        contents: [0x00, 0x00, 0x00, 0x00]
  dev_info_entries:
    seq:
      - id: entries
        type: dev_info_entry
        repeat: eos
  dev_info_entry: 
    seq: 
      - id: magic0
        contents: [0x80, 0x01]
      - id: entry_type
        type: u2
        enum: dev_info_entry_type
        doc: The type of the entry
      - id: info_length
        type: u2
        doc: The length of the informations
      - id: info
        type: u1
        repeat: expr
        repeat-expr: info_length
    enums:
      dev_info_entry_type:
        0x10: unknown0
        0x5: unknown1
        0x12: vendor
        0x16: serial_number
        0x4: family
        0x11: model
  apn_info:
    seq:
      - id: time_delta_milliseconds
        type: u4
        doc: I suspect this field contains the number of milliseconds passed since something something  
      - id: magic0
        contents: [0x00, 0x00]
      - id: question_id
        type: u2
        doc: The question being answered
      - id: magic1
        contents: [0x00, 0x00, 0x00, 0x01]
      - id: apn
        type: strz
        doc: The apn url of the apn
      - id: ipv4
        size: 4
        doc: (Current?) Ip address
      - id: magic2
        contents: [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x4f, 0xab, 0xa0, 0x14, 0x4f, 0xab, 0xa4, 0x14, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00] 
      - id: magic3
        contents: [0x00, 0x00, 0x00, 0x00]
  data_link_connection_info:
    seq: 
      - id: time_delta_milliseconds
        type: u4
        doc: I suspect this field contains the number of milliseconds passed since something something  
      - id: magic0
        contents: [0x00, 0x00]
      - id: question_id
        type: u2
        doc: The question being answered
      - id: magic1
        contents: [0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x04, 0x11, 0x00]
      - id: id_e_node_b
        type: u2
        doc: ID eNodeB
      - id: cell_id
        type: u1
      - id: magic2
        contents: [0x00, 0x00, 0x00, 0x00]
      - id: network_code
        type: strz
        doc: MCC+MNC
      - id: magic3
        contents: [0x00, 0x00, 0x00, 0x00, 0x00, 0x7b, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x2a, 0x00, 0xb8, 0xff, 0xff]
      - id: unknown1
        type: u2
        doc: This field seems to have a oscillating value, like link intensity o quality
      - id: magic4
        contents: [0xff, 0xff]
        doc: I suspect this field is part of the next field
      - id: unknown2
        type: u2
        doc: This field seems to have a oscillating value, like link intensity o quality
      - id: magic5
        contents: [0x00, 0x00, 0x00, 0x00]
  ping_info: 
    seq: 
      - id: time_delta_milliseconds
        type: u4
        doc: I suspect this field contains the number of milliseconds passed since something something  
      - id: magic0
        contents: [0x00, 0x00]
      - id: question_id
        type: u2
        doc: The question being answered
      - id: magic1
        contents: [0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00]
  ping2_info: 
    seq: 
      - id: time_delta_milliseconds
        type: u4
        doc: I suspect this field contains the number of milliseconds passed since something something  
      - id: magic0
        contents: [0x00, 0x00]
      - id: question_id
        type: u2
        doc: The question being answered
      - id: magic1
        contents: [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
  data_link_status_info:
    seq: 
      - id: time_delta_milliseconds
        type: u4
        doc: I suspect this field contains the number of milliseconds passed since something something  
      - id: magic0
        contents: [0x00, 0x00]
      - id: question_id
        type: u2
        doc: The question being answered
      - id: magic1
        contents: [0x00, 0x00]
      - id: unknown1
        type: u2
        doc: It seem to be a oscillating value!
      - id: unknown2
        type: s4
        doc: It seem to be a oscillating value!
      - id: magic2
        contents: [0x00, 0x00]
      - id: unknown3
        type: u2
        doc: It seem to be a oscillating value!
      - id: magic3
        contents: [0x00, 0x00]
      - id: unknown4
        type: u2
        doc: It seem to be a oscillating value!
      - id: unknown5
        type: u2
        doc: It seem to be a oscillating value!
      - id: magic4
        contents: [0x00, 0x00, 0x00, 0x00]
  network_status_info: 
    seq: 
      - id: time_delta_milliseconds
        type: u4
        doc: I suspect this field contains the number of milliseconds passed since something something  
      - id: magic0
        contents: [0x00, 0x00]
      - id: question_id
        type: u2
        doc: The question being answered
      - id: magic1
        contents: [0x00, 0x00]
      - id: magic2
        contents: [0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01]
      - id: ipv4_address
        size: 4
        doc: ipv4_address of the device
      - id: magic3
        contents: [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x02,
          0x00, 0x00, 0x00, 0x02] 
      - id: magic4
        contents: [0x00, 0x00, 0x00, 0x00]
  unknown_answer_type0:
    seq:
      - id: time_delta_milliseconds
        type: u4
        doc: I suspect this field contains the number of milliseconds passed since something something  
      - id: magic0
        contents: [0x00, 0x00]
      - id: question_id
        type: u2
        doc: The question being answered
      - id: magic1
        contents: [0x00, 0x00]
      - id: magic2
        contents: [0x00, 0x02, 0x00, 0x00, 0x00, 0x00]
      - id: unknown0
        type: u1
      - id: magic3
        contents: [0x00, 0x00, 0x00]
      - id: unknown1
        type: u1
      - id: unknown2
        type: u1 
      - id: magic4
        contents: [0x00, 0x00, 0x00]
      - id: unknown3
        type: u1
      - id: magic5
        contents: [0x00, 0x00, 0x00, 0x00, 0x00,  0x00, 0x00, 0x02]
      - id: unknown4
        type: u1
      - id: magic6
        contents: [0x00, 0x00, 0x00]
      - id: unknown5
        type: u1
      - id: unknown6
        type: u1
      - id: magic7
        contents: [0x00, 0x00]
      - id: unknown7
        type: u1
      - id: magic8
        contents: [0x00, 0x00, 0x00]
      - id: unknown8
        type: u1
      - id: unknown9
        type: u1
      - id: magic9
        contents: [0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
      - id: unknown10
        type: u1
      - id: magic10
        contents: [0x00, 0x00]
      - id: unknown11
        type: u2 
      - id: magic11
        contents: [0x00, 0x00]
      - id: unknown12
        type: u2
      - id: magic12
        contents: [0x00, 0x00] 
      - id: unknown13
        type: u2
      - id: magic13
        contents: [0x00, 0x00] 
      - id: unknown14
        type: u2
      - id: magic14
        contents: [0x00, 0x00, 0x00, 0x00]
      - id: magic15
        contents: [0x00, 0x00, 0x00, 0x00]
  unknown_answer_type1:
    seq:
      - id: time_delta_milliseconds
        type: u4
        doc: I suspect this field contains the number of milliseconds passed since something something  
      - id: magic0
        contents: [0x00, 0x00]
      - id: question_id
        type: u2
        doc: The question being answered
      - id: magic1
        contents: [0x00, 0x00]
      - id: magic2
        contents: [0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
      - id: unknown0
        type: u2
      - id: unknown1
        type: u2
      - id: magic3
        contents: [0x00, 0x00, 0x00, 0x05, 0x07, 0x02]
      - id: unknown2
        type: u4
      - id: unknown3
        type: u2
      - id: magic4
        contents: [0x00, 0x00]
      - id: unknown4
        type: u4
      - id: magic5
        contents: [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
      - id: unknown5
        type: u2
      - id: unknown6
        type: u2
      - id: unknown7
        type: u2
      - id: unknown8
        type: u2
      - id: magic6
        contents: [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x04, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] 
      - id: unknown9
        type: u2
      - id: magic7
        contents: [0x00, 0x00]
      - id: unknown10
        type: u4
      - id: unknown11
        type: u2
      - id: magic8
        contents: [0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
      - id: unknown12
        type: u2
      - id: magic9
        contents: [0x00, 0x80, 0x2a, 0x00, 0x00]
      - id: unknown13
        type: u2
      - id: magic10
        contents: [0x00, 0x00]
      - id: unknown14
        type: u2
      - id: magic12
        contents: [0x00, 0x00, 0x00, 0x00]
  data_link_status_info2:
    seq:
      - id: time_delta_milliseconds
        type: u4
        doc: I suspect this field contains the number of milliseconds passed since something something  
      - id: magic0
        contents: [0x00, 0x00]
      - id: question_id
        type: u2
        doc: The question being answered
      - id: unknown0
        type: s4
        doc: It seem to be a oscillating value!
      - id: unknown1
        type: s4
        doc: It seem to be a oscillating value!
      - id: unknown2
        type: s4
        doc: It seem to be a oscillating value!
      - id: magic1
        contents: [0x00, 0x00]
      - id: unknown3
        type: u2
        doc: It seem to be a oscillating value!
      - id: magic2
        contents: [0x00, 0x00]
      - id: unknown4
        type: u2
        doc: It seem to be a oscillating value!
      - id: unknown5
        type: s4
        doc: It seem to be a oscillating value!
      - id: unknown6
        type: s4
        doc: It seem to be a oscillating value!
      - id: unknown7
        type: s4
        doc: It seem to be a oscillating value!
      - id: unknown8
        type: s4
        doc: It seem to be a oscillating value!
      - id: unknown9
        type: s4
        doc: It seem to be a oscillating value!
      - id: unknown10
        type: s4
        doc: It seem to be a oscillating value!
      - id: magic3
        contents: [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
      - id: unknown11
        type: u2
        doc: It seem to 0x00 or 0x81
      - id: magic4
        contents: [0x00, 0x00]
      - id: unknown12
        type: u2
        doc: It seem to be a oscillating value!
      - id: magic5
        contents: [0x00, 0x00]
      - id: unknown13
        type: u2
        doc: It seem to be a oscillating value!
      - id: unknown14
        type: u1
        doc: It seem to be a oscillating value!
      - id: magic6
        contents: [0x09]
      - id: unknown15
        type: u1
        doc: It seem to be a oscillating value!
      - id: magic7
        contents: [0x00]
      - id: magic8
        contents: [0x00, 0x00]
      - id: unknown16
        type: u2
        doc: It seem to be a oscillating value!
      - id: magic9
        contents: [0x00, 0x00]
      - id: unknown17
        type: u2
        doc: It seem to be a oscillating value!
      - id: magic10
        contents: [0x00, 0x00]
      - id: unknown18
        type: u2
        doc: It seem to be a oscillating value!
      - id: magic11
        contents: [0x00, 0x00]
      - id: unknown19
        type: u2
        doc: It seem to be a oscillating value!
      - id: magic12
        contents: [0x00, 0x00]
      - id: unknown20
        type: u2
        doc: It seem to be a oscillating value!
      - id: magic13
        contents: [0x00, 0x00, 0x00, 0x00]
  unknown_answer_type2:
    seq:
      - id: time_delta_milliseconds
        type: u4
        doc: I suspect this field contains the number of milliseconds passed since something something  
      - id: magic0
        contents: [0x00, 0x00]
      - id: question_id
        type: u2
        doc: The question being answered
      - id: magic1
        contents: [0x00, 0x00]
      - id: magic2
        contents: [0x00, 0x01]
      - id: magic3
        contents: [0x00, 0x00, 0x00, 0x00]
  unknown_answer_type3:
    seq:
      - id: time_delta_milliseconds
        type: u4
        doc: I suspect this field contains the number of milliseconds passed since something something  
      - id: magic0
        contents: [0x00, 0x00]
      - id: question_id
        type: u2
        doc: The question being answered
      - id: magic1
        contents: [0x00, 0x00]
      - id: magic2
        contents: [0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
          0x0F, 0x02, 0x02, 0x02, 0x03, 0x08, 0x00, 0x00, 0x00, 0x00, 0x08, 
          0x02, 0x05, 0x00, 0x03, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
          0x02, 0x02, 0x02, 0x00, 0x03, 0x08, 0x0F, 0x00, 0xD3, 0x50, 0x02, 
          0x00, 0xC6, 0x88, 0x3D, 0x5D]
      - id: magic3
        contents: [0x00, 0x00, 0x00, 0x00]