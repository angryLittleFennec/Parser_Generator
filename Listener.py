from data import EOF, Nonterm, Term, Code, EPS, Prod, Rule
from generated.GramListener import GramListener
from generated.GramParser import GramParser


class Listener(GramListener):
    def __init__(self):
        self.token_cnt = 0
        self.start = None
        self.tokens_to_skip = set()
        self.token_to_id: dict = {}
        self.literals = {}
        self.regex = {}
        self.rules = {}
        self.has_eps_prods = False

    def exitSkipRule(self, ctx: GramParser.SkipRuleContext):
        self.fill_map(ctx.T_ID().__str__(), ctx.term_value(), True)

    def exitTokenRule(self, ctx: GramParser.TokenRuleContext):
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

    def exitBegin(self, ctx: GramParser.BeginContext):
        self.start = str(ctx.NT_ID())

    @staticmethod
    def get_arg(arg):
        if arg.NT_ID():
            return str(arg.NT_ID())
        if arg.T_ID():
            return str(arg.T_ID())
        if arg.CODE():
            return str(arg.CODE())

    def exitFile(self, ctx: GramParser.FileContext):
        self.token_to_id[EOF] = EOF

    def exitParserRulee(self, ctx: GramParser.ParserRuleeContext):
        rule_id = ctx.NT_ID().__str__()
        rule_args = []
        if (in_ := ctx.inAttrs()) is not None:

            i = 0
            while (arg := in_.NT_ID(i)) is not None:
                rule_args.append(arg.__str__())
                i += 1

        productions = []
        for prods in ctx.prods():
            prod_ = []
            prod = prods.prod()
            for pr in prod:
                if not_term := pr.NT_ID():
                    args_ = []
                    if args := pr.args():
                        arg = args.arg()
                        for a in arg:
                            args_.append(str(Listener.get_arg(a)).strip("{} "))
                    prod_.append(Nonterm(str(not_term), tuple(args_)))

                if term := pr.T_ID():
                    prod_.append(Term(str(term)))
                if code := pr.CODE():
                    prod_.append(Code(str(code).strip("{} ")))

            prod__ = list(filter(lambda x: isinstance(x, Term) or isinstance(x, Nonterm), prod_))
            if not prod__:
                self.has_eps_prods = True
                prod__.append(Term(EPS))
                prod_.insert(0, prod__[0])
            productions.append(Prod(tuple(prod__), tuple(prod_)))

        self.rules[rule_id] = Rule(name=rule_id, args=tuple(rule_args), productions=tuple(productions))
