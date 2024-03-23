import re
from tokenizer import Tokenizer
literals={
 "_1": re.escape("("),
 "_2": re.escape(")"),
 "_3": re.escape(","),
 "_4": re.escape("*"),
}
regex={
 "_0": "[a-zA-z][a-zA-Z0-9_]*",
 "_5": "\\s+",
}
skip_values = [
"_5",
]
unknown = {"_unknown": ".+"}
tokenizer = Tokenizer(literals, regex, unknown, skip_values)