start: (syntax | import | option | package) _SEMICOLON start -> header
     | definition_unit start
     | definition_unit
     | _NEWLINE

definition_unit: service
               | message
               | enum

//
// Headers
//
syntax: _SYNTAX _EQUAL ESCAPED_STRING

import: _IMPORT PUBLIC? ESCAPED_STRING

option: _OPTION IDENTIFIER _EQUAL (ESCAPED_STRING | CTRUE | CFALSE | SIGNED_NUMBER)

package: _PACKAGE IDENTIFIER

service: _SERVICE IDENTIFIER _OPEN_BRACE service_body _CLOSE_BRACE

service_body: function _SEMICOLON service_body
            |

function: RPC IDENTIFIER _OPEN_PAREN STREAM? type_name _CLOSE_PAREN RETURNS _OPEN_PAREN STREAM? type_name _CLOSE_PAREN _OPEN_BRACE _CLOSE_BRACE

message: _MESSAGE IDENTIFIER _OPEN_BRACE message_body _CLOSE_BRACE

message_body: oneof_block message_body
            | field _SEMICOLON message_body
            | reserved message_body
            | enum message_body
            | message message_body
            |

reserved: _RESERVED reserved_list

?reserved_list: (reserved_unit _COMMA)* reserved_unit _SEMICOLON

?reserved_unit: ESCAPED_STRING
             | reserved_list_int_unit

?reserved_list_int_unit: SIGNED_NUMBER "to" (SIGNED_NUMBER | MAX) -> interval
                      | SIGNED_NUMBER

field: REPEATED? type_name IDENTIFIER _EQUAL SIGNED_NUMBER
     | map_type

map_type: REPEATED? _MAP _LT_CAROT type_name _COMMA type_name _GT_CAROT IDENTIFIER _EQUAL SIGNED_NUMBER

oneof_block: _ONEOF IDENTIFIER _OPEN_BRACE oneof_body _CLOSE_BRACE

oneof_body: field _SEMICOLON oneof_body
          |

enum: _ENUM IDENTIFIER _OPEN_BRACE enum_body _CLOSE_BRACE

enum_option: option

enum_body: enum_option _SEMICOLON enum_body
         | enum_field _SEMICOLON enum_body
         |

enum_field: IDENTIFIER _EQUAL SIGNED_NUMBER

?type_name: TBOOL
         | TDOUBLE
         | TFLOAT
         | TINT32
         | TINT64
         | TUNIT32
         | TUNIT64
         | TSINT32
         | TSINT64
         | TFINT32
         | TFINT64
         | TSFINT32
         | TSFINT64
         | TSTR
         | TBYTE
         | IDENTIFIER

?constant: CTRUE
        | CFALSE
        | SIGNED_NUMBER
        | ESCAPED_STRING


%import common.INT
%import common.ESCAPED_STRING
%import common.SIGNED_NUMBER
IDENTIFIER: /[a-zA-Z_][0-9a-zA-Z_.]*/


COMMENT: "/*" /(.|\n)+/ "*/"
       |  "//" /(.)+/ _NEWLINE
_NEWLINE: /\r?\n[\t ]*/+
_SPACE: " "

// Skip past comments
%ignore COMMENT
%ignore _NEWLINE
%ignore _SPACE

// Constants
_SEMICOLON: ";"
_EQUAL: "="
_OPEN_BRACE: "{"
_CLOSE_BRACE: "}"
_OPEN_PAREN: "("
_CLOSE_PAREN: ")"
_COMMA: ","
_LT_CAROT: "<"
_GT_CAROT: ">"

// Type Names
TBOOL: "bool"
TDOUBLE: "double"
TFLOAT: "float"
TINT32: "int32"
TINT64: "int64"
TUNIT32: "uint32"
TUNIT64: "uint64"
TSINT32: "sint32"
TSINT64: "sint64"
TFINT32: "fixed32"
TFINT64: "fixed64"
TSFINT32: "sfixed32"
TSFINT64: "sfixed64"
TSTR: "string"
TBYTE: "bytes"

CTRUE: "true"
CFALSE: "false"

_SYNTAX: "syntax"
_IMPORT: "import"
_OPTION: "option"
_PACKAGE: "package"
_SERVICE: "service"
_MESSAGE: "message"
_ENUM: "enum"
_RESERVED: "reserved"
_ONEOF: "oneof"
_MAP: "map"

REPEATED: "repeated"
RETURNS: "returns"
STREAM: "stream"
RPC: "rpc"
MAX: "max"
PUBLIC: "public"
