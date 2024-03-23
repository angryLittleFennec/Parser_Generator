import re
from tokenizer import Tokenizer
literals={
 "_0": re.escape("-"),
 "_1": re.escape("+"),
 "_2": re.escape("**"),
 "_3": re.escape("*"),
 "_4": re.escape("("),
 "_5": re.escape("?"),
 "_6": re.escape("!"),
 "_7": re.escape(":"),
 "_8": re.escape("/"),
 "_9": re.escape(")"),
}
regex={
 "_10": "[0-9]+",
 "_11": "\\s+",
}
skip_values = [
"_11",
]
unknown = {"_unknown": ".+"}
tokenizer = Tokenizer(literals, regex, unknown, skip_values)