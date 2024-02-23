from dataclasses import dataclass, field
from typing import Any

import antlr4
from antlr4 import CommonTokenStream, ParseTreeWalker

from generated.GramLexer import GramLexer
from generated.GramListener import GramListener
from generated.GramParser import GramParser


@dataclass
class Rule:
    name: str
    productions: list = field(default_factory=list)
    args: list = field(default_factory=list)


@dataclass
class Code:
    code: str

@dataclass
class Term:
    term: str

@dataclass
class Nonterm:
    nonterm: str
    args: list

EPS = "eps"

class LexerListener(GramListener):
    def __init__(self):
        self.token_cnt = 0
        self.start = None
        self.tokens_to_skip = set()
        self.token_to_id: dict = {}
        self.literals = {}
        self.regex = {}
        self.rules = {}
        self.has_eps_prods = False

    def exitSkipRule(self, ctx:GramParser.SkipRuleContext):
        self.fill_map(ctx.T_ID().__str__(), ctx.term_value(), True)

    def exitTokenRule(self, ctx:GramParser.TokenRuleContext):
        self.fill_map(ctx.T_ID().__str__(), ctx.term_value(), False)

    def fill_map(self, token: str, right: GramParser.Term_valueContext, skip: bool):
        if token in self.token_to_id:
            token_id = self.token_to_id[token]
        else:
            self.token_cnt += 1
            self.token_to_id[token] = self.token_cnt
            token_id = self.token_cnt

        if right.STRING() is not None:
            self.literals[token_id] = right.STRING().__str__().strip('"')
        else:
            self.regex[token_id] = right.REGEX().__str__().strip("'")

        if skip:
            self.tokens_to_skip.add(token_id)

     ##### PARSER #####

    def exitBegin(self, ctx:GramParser.BeginContext):
        self.start = str(ctx.NT_ID())

    @staticmethod
    def get_arg(arg):
        if arg.NT_ID():
            return str(arg.NT_ID())
        if arg.T_ID():
            return str(arg.T_ID())
        if arg.CODE():
            return str(arg.CODE())

    def exitParserRulee(self, ctx:GramParser.ParserRuleeContext):
        rule_id = ctx.NT_ID().__str__()
        rule_args = []
        if (in_:= ctx.inAttrs()) is not None:

            i = 0
            while (arg := in_.NT_ID(i)) is not None:
                rule_args.append(arg.__str__())
                i += 1

        productions =[]
        for prods in ctx.prods():
            prod_ = []
            productions.append(prod_)
            prod = prods.prod()
            for pr in prod:
                if not_term := pr.NT_ID():
                    args_ = []
                    if args := pr.args():
                        arg = args.arg()
                        for a in arg:
                            args_.append(str(LexerListener.get_arg(a)).strip("{} "))
                    prod_.append(Nonterm(str(not_term), args_))

                if term := pr.T_ID():
                    prod_.append(Term(str(term)))
                if code := pr.CODE():
                    prod_.append(Code(str(code).strip("{} ")))
        if not any(map(lambda x: isinstance(x, Term) or isinstance(x, Nonterm), productions)):
            self.has_eps_prods = True
            productions.append(Term(EPS))

        self.rules[rule_id] = Rule(name=rule_id, args=rule_args, productions=productions)


def gen_file_lexer(listener: LexerListener):
    strs = []
    strs.append("import re")
    strs.append("literals={")
    for token_id, s in l.literals.items():
        s_esc = s.replace("\\", "\\\\")
        strs.append(f' {token_id}: "{s_esc}",')
    strs.append("}")
    strs.append("regex={")

    for token_id, s in l.regex.items():
        s_esc = s.replace("\\", "\\\\")
        strs.append(f' {token_id}: re.compile("{s_esc}"),')
    strs.append("}")

    strs.append('skip_values = [')
    for token in listener.tokens_to_skip:
        strs.append(f"{token},")
        strs.append(']')
    with open('generated_lexer.py', "w") as f:
        f.write("\n".join(strs))


if __name__ == "__main__":
    lexer = GramLexer(antlr4.InputStream("""
|> expr

expr := term exprs(term) { exprs } ;
exprs <acc> := PLUS term { val next = acc + term } exprs(next) {exprs} | {acc} ;

term := factor terms(factor) {terms} ;
terms <acc> := MUL factor terms({acc * factor}) {terms} | {acc} ;

factor := single factors(single) {factors};
factors <acc> := DMUL single factors({Math.pow(single.toDouble(), acc.toDouble()).toInt()}) {factors} | {acc};
3
single := O expr C {expr} | num {num} ;
num := NUM numExp({NUM.toInt()}) {numExp} ;
numExp <base> := EXP NUM { Math.pow(base.toDouble(), NUM.toDouble()).toInt() } | {base};

EXP = "e";
PLUS = "+";
DMUL = "**";
MUL = "*";
O = "(";
C = ")";
NUM = '[0-9]+';

WS => '\s+';"""))
    stream = CommonTokenStream(lexer)
    parser = GramParser(stream)
    walker = ParseTreeWalker()
    l = LexerListener()
    walker.walk(l, parser.file_())
    print(gen_file_lexer(l))
    print(l.rules)




