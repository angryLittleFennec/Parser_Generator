from generated_parser import Parser
from generated_lexer import tokenizer
print(Parser(tokenizer.tokenize("int a(int b, int**** *****c, int c)")).parse())