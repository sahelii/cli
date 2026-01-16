import re

from pygments.lexer import bygroups, using, RegexLexer
from pygments.lexers.data import JsonLexer
from pygments.token import Token

PREFIX_TOKEN = Token.Error
# Original prefix regex - matches anything except {, [, "
PREFIX_REGEX = r'[^{\["]+'


class EnhancedJsonLexer(RegexLexer):
    """
    Enhanced JSON lexer for Pygments.

    It adds support for eventual data prefixing the actual JSON body.

    """
    name = 'JSON'
    flags = re.IGNORECASE | re.DOTALL
    tokens = {
        'root': [
            # Eventual non-JSON data prefix followed by actual JSON body.
            # Handle numbers specially: match prefix that doesn't end with digits
            # when a number follows (to avoid matching numbers in prefixes like while(1);)
            (
                r'([^{\["]+?)(?=[{\["tfn]|(?<![a-zA-Z0-9)])-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?(?![;)\]}]))'
                + r'((?:[{\["]|true|false|null|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?).*)',
                bygroups(PREFIX_TOKEN, using(JsonLexer))
            ),
            # JSON body.
            (r'.+', using(JsonLexer)),
        ],
    }
