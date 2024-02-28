from typing import Generator

import real_parser
from generated_lexer import tokenizer


class Parser:
    def __init__(self, tokens: Generator):
        self.tokens = tokens
        self.token = None

    def expr(self, ):
        match self.token.type:
            case "_4" | "_6":
                term = self.term()
                exprs = self.exprs(term)
                return exprs
        raise

    def exprs(self, acc):
        match self.token.type:
            case "_1":
                plus = self.skip("_1")
                term = self.term()
                next = acc + term
                exprs = self.exprs(next)
                return exprs
            case "eof" | "_5":
                return acc
        raise

    def term(self, ):
        match self.token.type:
            case "_4" | "_6":
                factor = self.factor()
                terms = self.terms(factor)
                return terms
        raise

    def terms(self, acc):
        match self.token.type:
            case "_3":
                mul = self.skip("_3")
                factor = self.factor()
                terms = self.terms(acc*factor)
                return terms
            case "eof" | "_1" | "5":
                return acc


    def skip(self, token_type):
        if self.token.type == token_type:
            res = self.token.value
            self.token = next(self.tokens)
            return res
        else:
            raise Exception

    def factor(self, ):
        single = self.single()
        print(f"single in factor {single}")
        factors = self.factors(single)
        return factors

    def factors(self, acc):
        match self.token.type:
            case "_2":
                single = self.single()
                factor = self.factors(single**acc)
                return factor
            case _:
                return acc
    def single(self, ):
        match self.token.type:
            case "_4":
                self.skip("_4")
                expr = self.expr()
                print(expr)
                self.skip("_5")
                return expr
            case _:
                print("here")
                num = self.num()
                print(f"num={num}")
                return num

    def num(self, ):
        NUM = self.skip("_6")
        print(NUM)
        return self.numExp(int(NUM))

    def numExp(self, base):
        return base

    def parse(self):
        self.token = next(self.tokens)
        return self.expr()


print(real_parser.Parser(tokenizer.tokenize("(11229)*(1121212)")).parse())