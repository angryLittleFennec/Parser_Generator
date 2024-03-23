from calc.generated_lexer import tokenizer
from calc.generated_parser import Parser



print(Parser(tokenizer.tokenize("1+33+3")).parse())
print(Parser(tokenizer.tokenize("123+333/233/2212")).parse())
print(Parser(tokenizer.tokenize("5-3")).parse())

print(Parser(tokenizer.tokenize("1 ? 2 : 3 ")).parse())


print(Parser(tokenizer.tokenize("1 ? (2-3) : (3-3) ")).parse())

print(Parser(tokenizer.tokenize("0 ? ((2-3)*233) : (3-3) + 0 ? 2 : 1 ")).parse())
