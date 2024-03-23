import os.path
from collections import defaultdict

import antlr4
from antlr4 import CommonTokenStream, ParseTreeWalker

from Listener import Listener
from data import Code, EPS, Term, Nonterm, EOF
from generated.GramLexer import GramLexer
from generated.GramParser import GramParser


class ParserGenerator:
    def __init__(self, listener: Listener, output_dir='.'):
        self.listener = listener
        self.output_dir = output_dir
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

        #print(self.listener.rules.items())
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
                        #print(cur_nt)
                        if EPS in self.first[cur_nt]:
                            prev_len = len(self.first[name])
                            self.first[name].update(self.first[cur_nt])
                            if i == len(prods) - 1:
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
                            to_add = self.first[prod[i + 1].name].copy()
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
        self.code_strings.append(" " * (4 * self.indent) + s + "\n")

    def map_rule(self, name, rule):
        rules_map = {
            prod: (self.follow[name] if prod.prods[0].name == EPS else self.first[prod.prods[0].name]) for prod in
            rule.productions
        }
        st = set()
        full = sum(len(value) for _, value in rules_map.items())
        for map, val in rules_map.items():
            st.update(val)
        if len(st) != full:
            raise Exception("Not ll1")


        return rules_map


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
                tokens = map(lambda y: f'"{self.listener.token_to_id[y]}"', filter(lambda x: x != EPS, tokens))
                self.line(f'case {" | ".join(tokens)}:')
                self.indent += 1
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
            self.line("case _:")
            self.indent += 1
            self.line("raise Exception('Unexpected token type')")
            self.indent -= 1
            self.indent -= 1
            self.indent -= 1
            self.newline()

        self.line("def parse(self):")
        self.indent += 1
        self.line("self.token = next(self.tokens)")
        self.line(f"return self.{self.listener.start}()")

        with open(os.path.join(self.output_dir, "generated_parser.py"), "w") as file:
            file.write("".join(self.code_strings))

    def gen_file_lexer(self):
        strs = ["import re", "from tokenizer import Tokenizer", "literals={"]

        for token_id, s in self.listener.literals.items():
            s_esc = s.replace("\\", "\\\\")
            strs.append(f' "_{token_id}": re.escape("{s_esc}"),')
        strs.append("}")
        strs.append("regex={")

        for token_id, s in self.listener.regex.items():
            s_esc = s.replace("\\", "\\\\")
            strs.append(f' "_{token_id}": "{s_esc}",')
        strs.append("}")

        strs.append('skip_values = [')
        for token in self.listener.tokens_to_skip:
            strs.append(f'"_{token}",')
            strs.append(']')

        strs.append('unknown = {"_unknown": ".+"}')
        strs.append('tokenizer = Tokenizer(literals, regex, unknown, skip_values)')
        with open(os.path.join(self.output_dir, 'generated_lexer.py'), "w") as f:
            f.write("\n".join(strs))

    def gen_all(self):
        self.generate()
        self.gen_file_lexer()
        open(os.path.join(self.output_dir,"__init__.py"), "w")

