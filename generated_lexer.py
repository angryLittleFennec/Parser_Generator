import re
literals={
 1: "e",
 2: "+",
 3: "**",
 4: "*",
 5: "(",
 6: ")",
}
regex={
 7: re.compile("[0-9]+"),
 8: re.compile("\\s+"),
}
skip_values = [
8,
]