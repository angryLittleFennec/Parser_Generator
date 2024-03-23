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

    def expr(self, ):
        match self.token.type:
            case "_4" | "_10":
                term = self.term()
                exprs = self.exprs(term)
                return exprs
                pass
            case _:
                raise Exception('Unexpected token type')

    def exprs(self, acc):
        match self.token.type:
            case "_1":
                PLUS = self.skip("_1")
                term = self.term()
                next = acc + term
                exprs = self.exprs(next)
                return exprs
                pass
            case "_0":
                MINUS = self.skip("_0")
                term = self.term()
                next = acc - term
                exprs = self.exprs(next)
                return exprs
                pass
            case "EOF" | "_9":
                return acc
                pass
            case _:
                raise Exception('Unexpected token type')

    def term(self, ):
        match self.token.type:
            case "_4" | "_10":
                single = self.single()
                terms = self.terms(single)
                return terms
                pass
            case _:
                raise Exception('Unexpected token type')

    def terms(self, acc):
        match self.token.type:
            case "_3":
                MUL = self.skip("_3")
                single = self.single()
                terms = self.terms(acc * single)
                return terms
                pass
            case "_8":
                DIV = self.skip("_8")
                single = self.single()
                terms = self.terms(acc / single)
                return terms
                pass
            case "_1" | "EOF" | "_9" | "_0":
                return acc
                pass
            case _:
                raise Exception('Unexpected token type')

    def tern(self, ):
        match self.token.type:
            case "_4" | "_10":
                single = self.single()
                terns = self.terns(single)
                return single
                pass
            case _:
                raise Exception('Unexpected token type')

    def terns(self, acc):
        match self.token.type:
            case "_5":
                QUESTION = self.skip("_5")
                single = self.single()
                x = single
                COLON = self.skip("_7")
                single = self.single()
                terns = self.terns(x if acc else single)
                return terns
                pass
            case "_1" | "_7" | "_9" | "_8" | "_0" | "_5" | "_3" | "EOF":
                return acc
                pass
            case _:
                raise Exception('Unexpected token type')

    def single(self, ):
        match self.token.type:
            case "_4":
                O = self.skip("_4")
                expr = self.expr()
                C = self.skip("_9")
                return expr
                pass
            case "_10":
                num = self.num()
                return num
                pass
            case "_4" | "_10":
                tern = self.tern()
                return tern
                pass
            case _:
                raise Exception('Unexpected token type')

    def num(self, ):
        match self.token.type:
            case "_10":
                NUM = self.skip("_10")
                terns = self.terns(int(NUM))
                return terns
                pass
            case _:
                raise Exception('Unexpected token type')

    def parse(self):
        self.token = next(self.tokens)
        return self.expr()
