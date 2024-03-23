from typing import NamedTuple
import re


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int


class Tokenizer:
    def __init__(self, literals, regex, unknown, skip_values):
        self.literals = literals
        self.regex = regex
        self.skip_values = skip_values
        self.unknown = unknown

    def tokenize(self, code):
        token_specification = list(self.literals.items()) + list(self.regex.items()) + list(self.unknown.items())
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        #print(tok_regex)
        line_num = 1
        line_start = 0
        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start
            if kind == "_unknown":
                raise Exception(f"unexpected token, value:{value}, line:{line_num}")
            if kind in self.skip_values:
                continue
            yield Token(kind, value, line_num, column)
        yield Token("EOF", "EOF", 0, 0)
