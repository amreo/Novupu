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
      - id: informations
        type: 
          switch-on: type
          cases:
            _: unknown_type
        size: _parent.length-4
  unknown_type:
    seq:
      - id: data
        size-eos: true
