"""
    pygments.lexers.hc
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Haskell and related languages.

    :copyright: Copyright 2006-2023 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import Lexer, RegexLexer, bygroups, do_insertions, \
    default, include, inherit, line_re
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Generic, Whitespace
from pygments import unistring as uni

__all__ = ['HC']


uniLlWithoutD = uni.Ll.replace("d", "")

baseType = r"(?:(?:%?[sturႨωmk][0-9]{0,2}|lCtor|lCtorOrSym|fiTys|kthFiTy|othFiTys)\b'?\.?|@[0-9]{1,2}|¤'?[_" + uni.Ll + r"][\w']*|('')?[" + uni.Lu + r"][\w\'#]*|(')[" + uni.Lu + r"][\w\']*|(')\[[^\]]*\]|(')\([^)]*\)|(')[:!#$%&*+.\\/<=>?@^|~-]+)"
typeApp = lambda b: r"(?:" + b + r"|(?:\s*" + b + r")+)"
typeList = r"\[" + typeApp(baseType) + r"\]"
nestedTypeList = r"\[\[" + typeApp(baseType) + r"\]\]"
taOrListTa = r"(?:" + typeApp(baseType) + r"|" + typeList + r"|" + nestedTypeList + r")"
taList = typeApp(taOrListTa)
talTuple = r"(?:\(*\s*,?\s*" + taList + r"\)*)+"
nestedTypeTuple = r"(?:\(*\s*,?\s*" + talTuple + r"\)*)+"
finalType = r"(?:" + talTuple + r"|" + nestedTypeTuple + r")"

class HC(RegexLexer):
    
    """
    A Haskell lexer extended with support for some unicode symbols.

    .. versionadded⩴ 0.8
    """
    name = 'Haskell'
    url = 'https://www.haskell.org/'
    aliases = ['hc', 'haskellc']
    filenames = ['*.hs']
    mimetypes = ['text/x-haskell']

    reserved = ('case', 'class', 'data', 'default', 'deriving', 'do', 'else',
                'family', 'if', 'in', 'infix[lr]?', 'instance',
                'let', 'newtype', 'of', 'then', 'type', 'where', '_', 'forall', '∀') # tbagrel1: added forall
    ascii = ('NUL', 'SOH', '[SE]TX', 'EOT', 'ENQ', 'ACK',
             'BEL', 'BS', 'HT', 'LF', 'VT', 'FF', 'CR', 'S[OI]', 'DLE',
             'DC[1-4]', 'NAK', 'SYN', 'ETB', 'CAN',
             'EM', 'SUB', 'ESC', '[FGRU]S', 'SP', 'DEL')

    tokens = {
        'root': [
            # Whitespace:
            (r'\s+', Whitespace),
            # (r'--\s*|.*$', Comment.Doc),
            (r'--(?![!#$%&*+./<=>?@^|_~:\\]).*?$', Comment.Single),
            (r'\{-', Comment.Multiline, 'comment'),
            # Lexemes:
            #  Identifiers
            (r'\bimport\b', Keyword.Reserved, 'import'),
            (r'\bmodule\b', Keyword.Reserved, 'module'),
            (r'\berror\b', Name.Exception),
            (r'\b(%s)(?!\')\b' % '|'.join(reserved), Keyword.Reserved),
            # (r"'[^\\]'", String.Char),  # this has to come before the TH quote
            (r"'[^\\]'", Keyword.Type),  # this has to come before the TH quote
#            (r'^([_' + uniLlWithoutD + r'][\w\']|[_' + uni.Ll + r'][\w\']{2,})', Name.Function), # tbagrel1: functions must be 2 char long not starting with d, or 3+ char long
            # (r"\(?\b(?:[abcsr]|lCtor)(\.|\)|\]|\,|\b)+", Keyword.Type), # tbagrel1: a, b, c, s, r are type variables
            # #(r"(?<=(?:[abcsr]|lCtor))\)*,*", Keyword.Type),
            # (r"¤'?[_" + uni.Ll + r"][\w']*", Keyword.Type),
            (r'¤\(\)', Name.Class),
            (r'\(\)', Keyword.Type), # tbagrel1: changed unit to Keyword.Type
            (finalType, Keyword.Type),
            (r"[_□" + uni.Ll + r"][\w'#]*", Name),
            (r"¤('')?[" + uni.Lu + r"][\w\'#]*", Name.Class),
            
#            (r"(?<=')[" + uni.Lu + r"][\w\']*", Operator),
            # (r"\(?('')?[" + uni.Lu + r"][\w\']*", Keyword.Type),
            # (r"(')[" + uni.Lu + r"][\w\']*", Keyword.Type),
            # (r"\[(?:(?:[abcsr]|lCtor)\b|¤'?[_" + uni.Ll + r"][\w']*|('')?[" + uni.Lu + r"][\w\']*|(')[" + uni.Lu + r"][\w\']*|\[(?:[abcsr]|lCtor)\]|(')\[[^\]]*\]|(')\([^)]*\)|(')[:!#$%&*+.\\/<=>?@^|~-]+)\]\)*", Keyword.Type), # deactivated so that tuple and lists are treated the same at type level
            # (r"(')\[[^\]]*\]", Keyword.Type),  # tuples and lists get special treatment in GHC
            # (r"(')\([^)]*\)", Keyword.Type),  # ..
            # (r"(')[:!#$%&*+.\\/<=>?@^|~-]+", Keyword.Type),  # promoted type operators

            # # need recursive regex support to work
            # # (r"\((?:\s*(?:(?:[abcsr]|lCtor)\b|¤'?[_" + uni.Ll + r"][\w']*|('')?[" + uni.Lu + r"][\w\']*|(')[" + uni.Lu + r"][\w\']*|\[(?:[abcsr]|lCtor)\]|(')\[[^\]]*\]|(')\([^)]*\)|(')[:!#$%&*+.\\/<=>?@^|~-]+|(?R)))+(?:\s*,(?:\s*(?:(?:[abcsr]|lCtor)\b|¤'?[_" + uni.Ll + r"][\w']*|('')?[" + uni.Lu + r"][\w\']*|(')[" + uni.Lu + r"][\w\']*|\[(?:[abcsr]|lCtor)\]|(')\[[^\]]*\]|(')\([^)]*\)|(')[:!#$%&*+.\\/<=>?@^|~-]+|(?R)))+)*\)", Keyword.Type),
            # (r"\(?,?(?:\s*)+\)+\,?", Keyword.Type),
            # (r"(\s*,?\s*(?:\s*(?:(?:[abcsr]|lCtor)\b|¤'?[_" + uni.Ll + r"][\w']*|('')?[" + uni.Lu + r"][\w\']*|(')[" + uni.Lu + r"][\w\']*|\[(?:[abcsr]|lCtor)\]|(')\[[^\]]*\]|(')\([^)]*\)|(')[:!#$%&*+.\\/<=>?@^|~-]+))+\))+\)*", Keyword.Type),


            #  Operators
            (r'\\(?![:!#$%&*+.\\/<=>?@^|~-]+)', Operator.Word),  # lambda operator
            (r'(<-|⩴|->|=>|=|⊸|→|⇒|←|∀|forall\b)(?![:!#$%&*+.\\/<=>?@^|~-]+)', Operator.Word),  # specials # tbagrel1: added support for some unicode arrows
            (r'[=@](?![:!#$%&*+.\\/<=>?@^|~-]+)', Operator.Word),
            (r'[|](?![:!#$%&*+.\\/<=>?@^|~-]+)', Operator.Word),
#             (r':[!#$%&*+.\\/<=>?@^|~-]*', Keyword.Type),  # Constructor operators
            (r'[!#$%&*+.\\/<=>?@^|~-;]+', Operator),  # Other operators # tbagrel1: added support for grec interrogation mark
            #  Numbers
            (r"`?[_" + uni.Ll + r"][\w']*`", Operator),
            (r'0[xX]_*[\da-fA-F](_*[\da-fA-F])*_*[pP][+-]?\d(_*\d)*', Number.Float),
            (r'0[xX]_*[\da-fA-F](_*[\da-fA-F])*\.[\da-fA-F](_*[\da-fA-F])*'
             r'(_*[pP][+-]?\d(_*\d)*)?', Number.Float),
            (r'\d(_*\d)*_*[eE][+-]?\d(_*\d)*', Number.Float),
            (r'\d(_*\d)*\.\d(_*\d)*(_*[eE][+-]?\d(_*\d)*)?', Number.Float),
            (r'0[bB]_*[01](_*[01])*', Number.Bin),
            (r'0[oO]_*[0-7](_*[0-7])*', Number.Oct),
            (r'0[xX]_*[\da-fA-F](_*[\da-fA-F])*', Number.Hex),
            (r'\d(_*\d)*', Number.Integer),
            #  Character/String Literals
            (r"'", String.Char, 'character'),
            (r'"', String, 'string'),
            #  Special
            (r'\[\]', Name.Class),
            (r'¤\(', Keyword.Type),
            (r'¤\)', Keyword.Type),
            (r'¤\[', Keyword.Type),
            (r'¤\]', Keyword.Type),
            (r'[:,]', Name.Class),
            # (r'\(:\)', Name.Class),
            # (r'\(,\)', Name.Class),
            (r'[][)(]', Name.Class),
            # \((?:[^)(]+|(?R))(?:\s*,\s*(?:[^)(]+|(?R)))+\)

            #(r'\((?=(?:[^)(]+|(?R))(?:\s*,\s*(?:[^)(]+|(?R)))+\))', Operator), # match opening tuple paren

            (r'[;`{}]', Punctuation),
        ],
        'import': [
            # Import statements
            (r'\s+', Whitespace),
            (r'"', String, 'string'),
            # after "funclist" state
            (r'\)', Punctuation, '#pop'),
            (r'qualified\b', Keyword),
            # import X as Y
            (r'([' + uni.Lu + r'][\w.]*)(\s+)(as)(\s+)([' + uni.Lu + r'][\w.]*)',
             bygroups(Name.Namespace, Whitespace, Keyword, Whitespace, Name), '#pop'),
            # import X hiding (functions)
            (r'([' + uni.Lu + r'][\w.]*)(\s+)(hiding)(\s+)(\()',
             bygroups(Name.Namespace, Whitespace, Keyword, Whitespace, Punctuation), 'funclist'),
            # import X (functions)
            (r'([' + uni.Lu + r'][\w.]*)(\s+)(\()',
             bygroups(Name.Namespace, Whitespace, Punctuation), 'funclist'),
            # import X
            (r'[\w.]+', Name.Namespace, '#pop'),
        ],
        'module': [
            (r'\s+', Whitespace),
            (r'([' + uni.Lu + r'][\w.]*)(\s+)(\()',
             bygroups(Name.Namespace, Whitespace, Punctuation), 'funclist'),
            (r'[' + uni.Lu + r'][\w.]*', Name.Namespace, '#pop'),
        ],
        'funclist': [
            (r'\s+', Whitespace),
            (r'[' + uni.Lu + r']\w*', Keyword.Type),
            (r'(_[\w\']+|[' + uni.Ll + r'][\w\']*)', Name.Function),
            (r'--(?![!#$%&*+./<=>?@^|_~:\\]).*?$', Comment.Single),
            (r'\{-', Comment.Multiline, 'comment'),
            (r',', Punctuation),
            (r'[:!#$%&*+.\\/<=>?@^|~-]+', Operator),
            # (HACK, but it makes sense to push two instances, believe me)
            (r'\(', Punctuation, ('funclist', 'funclist')),
            (r'\)', Punctuation, '#pop:2'),
        ],
        # NOTE: the next four states are shared in the AgdaLexer; make sure
        # any change is compatible with Agda as well or copy over and change
        'comment': [
            # Multiline Comments
            (r'[^-{}]+', Comment.Multiline),
            (r'\{-', Comment.Multiline, '#push'),
            (r'-\}', Comment.Multiline, '#pop'),
            (r'[-{}]', Comment.Multiline),
        ],
        'character': [
            # Allows multi-chars, incorrectly.
            (r"[^\\']'", String.Char, '#pop'),
            (r"\\", String.Escape, 'escape'),
            ("'", String.Char, '#pop'),
        ],
        'string': [
            (r'[^\\"]+', String),
            (r"\\", String.Escape, 'escape'),
            ('"', String, '#pop'),
        ],
        'escape': [
            (r'[abfnrtv"\'&\\]', String.Escape, '#pop'),
            (r'\^[][' + uni.Lu + r'@^_]', String.Escape, '#pop'),
            ('|'.join(ascii), String.Escape, '#pop'),
            (r'o[0-7]+', String.Escape, '#pop'),
            (r'x[\da-fA-F]+', String.Escape, '#pop'),
            (r'\d+', String.Escape, '#pop'),
            (r'(\s+)(\\)', bygroups(Whitespace, String.Escape), '#pop'),
        ],
    }
