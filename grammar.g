start: (syntax | import | option | package) _SEMICOLON start
     | _SERVICE IDENTIFIER _OPEN_BRACE service_body _CLOSE_BRACE start  -> service
     | _MESSAGE IDENTIFIER _OPEN_BRACE message_body _CLOSE_BRACE start  -> message
     | _ENUM IDENTIFIER _OPEN_BRACE _CLOSE_BRACE    start  -> enum
     |


//
// Headers
//
syntax: _SYNTAX _EQUAL ESCAPED_STRING

import: _IMPORT ESCAPED_STRING

option: _OPTION IDENTIFIER _EQUAL (ESCAPED_STRING | CTRUE | CFALSE | SIGNED_NUMBER)

package: _PACKAGE IDENTIFIER


service_body: function _SEMICOLON service_body
            |

function: RPC IDENTIFIER _OPEN_PAREN STREAM? IDENTIFIER _CLOSE_PAREN RETURNS _OPEN_PAREN STREAM? IDENTIFIER _CLOSE_PAREN _OPEN_BRACE _CLOSE_BRACE


message_body: field _SEMICOLON message_body
            |

field: REPEATED? IDENTIFIER IDENTIFIER _EQUAL constant


?constant: CTRUE
        | CFALSE
        | SIGNED_NUMBER
        | ESCAPED_STRING


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

CTRUE: "true"
CFALSE: "false"

_SYNTAX: "syntax"
_IMPORT: "import"
_OPTION: "option"
_PACKAGE: "package"
_SERVICE: "service"
_MESSAGE: "message"
_ENUM: "enum"

REPEATED: "repeated"
RETURNS: "returns"
STREAM: "stream"
RPC: "rpc"
