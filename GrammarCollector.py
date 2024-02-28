from collections import defaultdict
from dataclasses import dataclass, field

import antlr4
from antlr4 import CommonTokenStream, ParseTreeWalker

from generated.GramLexer import GramLexer
from generated.GramListener import GramListener
from generated.GramParser import GramParser


@dataclass
class Rule:
    name: str
    productions: tuple= field(default_factory=tuple)
    args: tuple = field(default_factory=tuple)


@dataclass(eq=True, frozen=True)
class Prod:
    prods: tuple = field(default_factory=tuple)
    native: tuple = field(default_factory=tuple)


@dataclass(eq=True, frozen=True)
class Code:
    code: str

@dataclass(eq=True, frozen=True)
class Term:
    name: str

@dataclass(eq=True, frozen=True)
class Nonterm:
    name: str
    args: tuple

EPS = "EPS"
EOF = "EOF"

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
            self.token_to_id[token] = f"_{self.token_cnt}"
            token_id = self.token_cnt
            self.token_cnt += 1

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

    def exitFile(self, ctx:GramParser.FileContext):
        self.token_to_id[EOF] = EOF

    def exitParserRulee(self, ctx:GramParser.ParserRuleeContext):
        rule_id = ctx.NT_ID().__str__()
        rule_args = []
        if (in_ := ctx.inAttrs()) is not None:

            i = 0
            while (arg := in_.NT_ID(i)) is not None:
                rule_args.append(arg.__str__())
                i += 1

        productions=[]
        for prods in ctx.prods():
            prod_ = []
            prod = prods.prod()
            for pr in prod:
                if not_term := pr.NT_ID():
                    args_ = []
                    if args := pr.args():
                        arg = args.arg()
                        for a in arg:
                            args_.append(str(LexerListener.get_arg(a)).strip("{} "))
                    prod_.append(Nonterm(str(not_term), tuple(args_)))

                if term := pr.T_ID():
                    prod_.append(Term(str(term)))
                if code := pr.CODE():
                    prod_.append(Code(str(code).strip("{} ")))

            prod__ = list(filter(lambda x: isinstance(x, Term) or isinstance(x, Nonterm),  prod_))
            if not prod__:
                self.has_eps_prods = True
                prod__.append(Term(EPS))
                prod_.insert(0, prod__[0])
            productions.append(Prod(tuple(prod__), tuple(prod_)))

        self.rules[rule_id] = Rule(name=rule_id, args=tuple(rule_args), productions=tuple(productions))


class ParserGenerator:
    def __init__(self, listener: LexerListener):
        self.listener = listener
        self.first = defaultdict(set)
        self.follow = defaultdict(set)
        self.gen_first()
        self.gen_follow()
        self.indent = 0
        self.code_strings = []

    @property
    def terms(self):
        if self.listener.has_eps_prods:
            return list(self.listener.token_to_id.keys()) + [EPS]
        else:
            return list(self.listener.token_to_id.keys())

    def gen_first(self):

        for token in self.terms:
            self.first[token].add(token)

        print(self.listener.rules.items())
        for name, rule in self.listener.rules.items():
            for prod in rule.productions:
                if prod.prods[0].name == EPS:
                    self.first[name].add(EPS)

        changed = True
        while changed:
            changed = False
            for name, rule in self.listener.rules.items():
                for production in rule.productions:
                    prods = production.prods
                    for i, elem in enumerate(prods):
                        cur_nt = elem.name
                        print(cur_nt)
                        if EPS in self.first[cur_nt]:
                            prev_len = len(self.first[name])
                            self.first[name].update(self.first[cur_nt])
                            if i == len(prods) -1:
                                self.first[name].add(EPS)
                            if len(self.first[name]) != prev_len:
                                changed = True
                        else:
                            prev_len = len(self.first[name])
                            self.first[name].update(self.first[cur_nt])
                            if len(self.first[name]) != prev_len:
                                changed = True
                            break

    def gen_follow(self):
        self.follow[self.listener.start].add(EOF)
        changed = True
        while changed:
            changed = False
            for name, rule in self.listener.rules.items():
                for production in rule.productions:
                    prod = production.prods
                    for i, elem in enumerate(prod):
                        if i <= len(prod) - 2 and isinstance(elem, Nonterm):
                            prev_len = len(self.follow[elem.name])
                            to_add = self.first[prod[i+1].name].copy()
                            to_add.discard(EPS)
                            self.follow[elem.name].update(to_add)
                            if prev_len != len(self.follow[elem.name]):
                                changed = True
                        else:
                            if isinstance(elem, Nonterm):
                                prev_len = len(self.follow[elem.name])
                                self.follow[elem.name].update(self.follow[name])
                                if len(self.follow[elem.name]) != prev_len:
                                    changed = True
                    if len(prod) > 1 and EPS in self.first[prod[-1].name]:
                        prev = prod[-2]
                        if isinstance(prev, Nonterm):
                            prev_len = len(self.follow[prev.name])
                            self.follow[prev.name].update(self.follow[name])
                            if prev_len != len(self.follow[prev.name]):
                                changed = True

    def newline(self):
        self.code_strings.append("\n")

    def line(self, s):
        self.code_strings.append(" "*(4*self.indent) + s + "\n")

    def map_rule(self, name, rule):
        return {
            prod: (self.follow[name] if prod.prods[0].name == EPS else self.first[prod.prods[0].name]) for prod in rule.productions
        }

    def generate(self):
        self.line("class Parser:")
        self.indent += 1
        self.line("def __init__(self, tokens):")
        self.indent += 1
        self.line("self.tokens = tokens")
        self.line("self.token=None")
        self.indent -= 1
        self.newline()
        self.line("def skip(self, token_type):")
        self.indent += 1
        self.line("if self.token.type == token_type:")
        self.indent += 1
        self.line("res = self.token.value")
        self.line("self.token = next(self.tokens)")
        self.line("return res")
        self.indent -= 1
        self.line("raise Exception('Unexpected token')")
        self.indent -= 1
        self.newline()

        for name, rule in self.listener.rules.items():
            m = self.map_rule(name, rule)
            self.line(f"def {rule.name}(self, {', '.join(rule.args)}):")
            self.indent += 1
            self.line("match self.token.type:")
            self.indent += 1
            for prods, tokens in m.items():
                tokens = map(lambda y:  f'"{self.listener.token_to_id[y]}"', filter(lambda x: x != EPS, tokens))
                self.line(f'case {" | ".join(tokens)}:')
                self.indent +=1
                for elem in prods.native:
                    if isinstance(elem, Nonterm):
                        self.line(f"{elem.name} = self.{elem.name}({' ,'.join(elem.args)})")
                    if isinstance(elem, Term):
                        if elem.name == EPS:
                            continue
                        self.line(f'{elem.name} = self.skip("{self.listener.token_to_id[elem.name]}")')
                    if isinstance(elem, Code):
                        self.line(f"{elem.code}")
                self.line("pass")
                self.indent -= 1
            self.indent -= 1
            self.indent -=1
        self.newline()

        self.line("def parse(self):")
        self.indent += 1
        self.line("self.token = next(self.tokens)")
        self.line(f"return self.{self.listener.start}()")
        self.newline()



        with open("generated_parser.py", "w") as file:
            file.write("".join(self.code_strings))


def gen_file_lexer(listener: LexerListener):
    strs = []
    strs.append("import re")
    strs.append("from tokenizer import Tokenizer")
    strs.append("literals={")

    for token_id, s in l.literals.items():
        s_esc = s.replace("\\", "\\\\")
        strs.append(f' "_{token_id}": re.escape("{s_esc}"),')
    strs.append("}")
    strs.append("regex={")

    for token_id, s in l.regex.items():
        s_esc = s.replace("\\", "\\\\")
        strs.append(f' "_{token_id}": "{s_esc}",')
    strs.append("}")

    strs.append('skip_values = [')
    for token in listener.tokens_to_skip:
        strs.append(f'"_{token}",')
        strs.append(']')

    strs.append('unknown = {"_unknown": ".+"}')
    strs.append('tokenizer = Tokenizer(literals, regex, unknown, skip_values)')
    with open('generated_lexer.py', "w") as f:
        f.write("\n".join(strs))


if __name__ == "__main__":
    lexer=GramLexer(antlr4.InputStream(
    """
    |> s
    
    s := t N O a C;
    t := N tt;
    tt := MUL tt |;
    a := b aa |;
    aa := COMMA a |;
    b := t N;
    
    N = '[a-zA-z][a-zA-Z0-9_]*';
    O = "(";
    C = ")";
    COMMA = ",";
    MUL = "*";
    WS => '\s+';
    
    
    """))


#     lexer = GramLexer(antlr4.InputStream("""
# |> expr
#
# expr := term exprs(term) { return exprs } ;
# exprs <acc> := PLUS term { next = acc + term } exprs(next) { return exprs} | MINUS term { next = acc - term } exprs(next) {return exprs} | { return acc} ;
#
# term := single terms(single) {return terms} ;
# terms <acc> := MUL single terms({acc * single}) {return terms} | DIV single terms({acc // single}) {return terms} | {return acc} ;
#
# single := O expr C {return expr} | num {return num} ;
# num := NUM {return int(NUM)} ;
#
# MINUS = "-"
# PLUS = "+";
# DMUL = "**";
# MUL = "*";
# O = "(";
# DIV = "//"
# C = ")";
# NUM = '[0-9]+';
#
# WS => '\s+';"""))
    stream = CommonTokenStream(lexer)
    parser = GramParser(stream)
    walker = ParseTreeWalker()
    l = LexerListener()
    walker.walk(l, parser.file_())
    print(gen_file_lexer(l))
    print(ParserGenerator(l).generate())
