import re
from tokenizer import Tokenizer
literals={
 "_0": re.escape("0"),
 "_1": re.escape("1"),
 "_2": re.escape("2"),
}
regex={
}
skip_values = [
unknown = {"_unknown": ".+"}
tokenizer = Tokenizer(literals, regex, unknown, skip_values)