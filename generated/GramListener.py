# Generated from Gram.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .GramParser import GramParser
else:
    from GramParser import GramParser

# This class defines a complete listener for a parse tree produced by GramParser.
class GramListener(ParseTreeListener):

    # Enter a parse tree produced by GramParser#file.
    def enterFile(self, ctx:GramParser.FileContext):
        pass

    # Exit a parse tree produced by GramParser#file.
    def exitFile(self, ctx:GramParser.FileContext):
        pass


    # Enter a parse tree produced by GramParser#begin.
    def enterBegin(self, ctx:GramParser.BeginContext):
        pass

    # Exit a parse tree produced by GramParser#begin.
    def exitBegin(self, ctx:GramParser.BeginContext):
        pass


    # Enter a parse tree produced by GramParser#rulee.
    def enterRulee(self, ctx:GramParser.RuleeContext):
        pass

    # Exit a parse tree produced by GramParser#rulee.
    def exitRulee(self, ctx:GramParser.RuleeContext):
        pass


    # Enter a parse tree produced by GramParser#parserRulee.
    def enterParserRulee(self, ctx:GramParser.ParserRuleeContext):
        pass

    # Exit a parse tree produced by GramParser#parserRulee.
    def exitParserRulee(self, ctx:GramParser.ParserRuleeContext):
        pass


    # Enter a parse tree produced by GramParser#inAttrs.
    def enterInAttrs(self, ctx:GramParser.InAttrsContext):
        pass

    # Exit a parse tree produced by GramParser#inAttrs.
    def exitInAttrs(self, ctx:GramParser.InAttrsContext):
        pass


    # Enter a parse tree produced by GramParser#param.
    def enterParam(self, ctx:GramParser.ParamContext):
        pass

    # Exit a parse tree produced by GramParser#param.
    def exitParam(self, ctx:GramParser.ParamContext):
        pass


    # Enter a parse tree produced by GramParser#paramName.
    def enterParamName(self, ctx:GramParser.ParamNameContext):
        pass

    # Exit a parse tree produced by GramParser#paramName.
    def exitParamName(self, ctx:GramParser.ParamNameContext):
        pass


    # Enter a parse tree produced by GramParser#prods.
    def enterProds(self, ctx:GramParser.ProdsContext):
        pass

    # Exit a parse tree produced by GramParser#prods.
    def exitProds(self, ctx:GramParser.ProdsContext):
        pass


    # Enter a parse tree produced by GramParser#prod.
    def enterProd(self, ctx:GramParser.ProdContext):
        pass

    # Exit a parse tree produced by GramParser#prod.
    def exitProd(self, ctx:GramParser.ProdContext):
        pass


    # Enter a parse tree produced by GramParser#args.
    def enterArgs(self, ctx:GramParser.ArgsContext):
        pass

    # Exit a parse tree produced by GramParser#args.
    def exitArgs(self, ctx:GramParser.ArgsContext):
        pass


    # Enter a parse tree produced by GramParser#arg.
    def enterArg(self, ctx:GramParser.ArgContext):
        pass

    # Exit a parse tree produced by GramParser#arg.
    def exitArg(self, ctx:GramParser.ArgContext):
        pass


    # Enter a parse tree produced by GramParser#tokenRule.
    def enterTokenRule(self, ctx:GramParser.TokenRuleContext):
        pass

    # Exit a parse tree produced by GramParser#tokenRule.
    def exitTokenRule(self, ctx:GramParser.TokenRuleContext):
        pass


    # Enter a parse tree produced by GramParser#skipRule.
    def enterSkipRule(self, ctx:GramParser.SkipRuleContext):
        pass

    # Exit a parse tree produced by GramParser#skipRule.
    def exitSkipRule(self, ctx:GramParser.SkipRuleContext):
        pass


    # Enter a parse tree produced by GramParser#term_value.
    def enterTerm_value(self, ctx:GramParser.Term_valueContext):
        pass

    # Exit a parse tree produced by GramParser#term_value.
    def exitTerm_value(self, ctx:GramParser.Term_valueContext):
        pass



del GramParser