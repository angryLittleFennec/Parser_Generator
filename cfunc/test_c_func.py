from cfunc.generated_lexer import tokenizer
from cfunc.generated_parser import Parser


print(Parser(tokenizer.tokenize('int a()')).parse())
print(Parser(tokenizer.tokenize("int a(int b, int c)")).parse())
print(Parser(tokenizer.tokenize("int a(int*** **b, int, int c)")).parse())