import re

from pygments.lexer import bygroups, using, RegexLexer
from pygments.lexers.data import JsonLexer
from pygments.token import Token

PREFIX_TOKEN = Token.Error
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
            (
                fr'({PREFIX_REGEX})' + r'((?:[{\["]|true|false|null|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?).*)',
                bygroups(PREFIX_TOKEN, using(JsonLexer))
            ),
            # JSON body.
            (r'.+', using(JsonLexer)),
        ],
    }
