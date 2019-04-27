meta:
  id: l10p
  title: A protocol used to acknowledge L40P requests
  license: CC-4.0-NC-SA
  encoding: ascii
  endian: be
doc: |
  I think L10P is a protocol used to acknowledge L40P requests.
  A L10P pdu is L40P pdu wih zero length payload
seq:
  - id: seq
    type: u2
    doc: Sequence number
  - id: ack_seq
    type: u2
    doc: Acknowledged sequence number
  - id: magic0
    contents: [0x00, 0x00, 0x00, 0x00]
