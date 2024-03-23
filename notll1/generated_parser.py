class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token=None

    def skip(self, token_type):
        if self.token.type == token_type:
            res = self.token.value
            self.token = next(self.tokens)
            return res
        raise Exception('Unexpected token')

    def s(self, ):
        match self.token.type:
            case "_1":
                ONE = self.skip("_1")
                s = self.s()
                TWO = self.skip("_2")
                pass
            case "_0" | "_1":
                s = self.s()
                ZERO = self.skip("_0")
                pass
            case "_0" | "_2" | "EOF":
                pass
            case _:
                raise Exception('Unexpected token type')

    def parse(self):
        self.token = next(self.tokens)
        return self.s()
