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
            case "_0":
                t = self.t()
                N = self.skip("_0")
                O = self.skip("_1")
                a = self.a()
                C = self.skip("_2")
                pass
    def t(self, ):
        match self.token.type:
            case "_0":
                N = self.skip("_0")
                tt = self.tt()
                pass
    def tt(self, ):
        match self.token.type:
            case "_4":
                MUL = self.skip("_4")
                tt = self.tt()
                pass
            case "_0":
                pass
    def a(self, ):
        match self.token.type:
            case "_0":
                b = self.b()
                aa = self.aa()
                pass
            case "_2":
                pass
    def aa(self, ):
        match self.token.type:
            case "_3":
                COMMA = self.skip("_3")
                a = self.a()
                pass
            case "_2":
                pass
    def b(self, ):
        match self.token.type:
            case "_0":
                t = self.t()
                N = self.skip("_0")
                pass

    def parse(self):
        self.token = next(self.tokens)
        return self.s()

