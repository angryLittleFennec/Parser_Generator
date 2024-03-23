import antlr4
from antlr4 import CommonTokenStream, ParseTreeWalker

from ParserGenerator import ParserGenerator
from Listener import Listener
from generated.GramLexer import GramLexer
from generated.GramParser import GramParser


def gen_calc():
    with open("calc.txt", "r") as f:
        lexer = GramLexer(antlr4.InputStream(f.read()))

        stream = CommonTokenStream(lexer)
        parser = GramParser(stream)
        walker = ParseTreeWalker()
        l = Listener()
        walker.walk(l, parser.file_())
        ParserGenerator(l, output_dir='./calc').gen_all()


def gen_c_func():
    with open("cfunc.txt", "r") as f:
        lexer = GramLexer(antlr4.InputStream(f.read()))

        stream = CommonTokenStream(lexer)
        parser = GramParser(stream)
        walker = ParseTreeWalker()
        l = Listener()
        walker.walk(l, parser.file_())
        ParserGenerator(l, output_dir='./cfunc').gen_all()


def gen_notll1():
    with open("notll1.txt", "r") as f:
        lexer = GramLexer(antlr4.InputStream(f.read()))

        stream = CommonTokenStream(lexer)
        parser = GramParser(stream)
        walker = ParseTreeWalker()
        l = Listener()
        walker.walk(l, parser.file_())
        ParserGenerator(l, output_dir='./notll1').gen_all()


gen_c_func()
#gen_notll1()