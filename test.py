import re

literals = {
    3: ";",
}
regex = {
    1: re.compile("\\s+"),
    2: re.compile("[a-z]+"),
}
skip_values = [
    1,
]