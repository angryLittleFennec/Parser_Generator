from dataclasses import dataclass, field


@dataclass
class Rule:
    name: str
    productions: tuple= field(default_factory=tuple)
    args: tuple = field(default_factory=tuple)


@dataclass(eq=True, frozen=True)
class Prod:
    prods: tuple = field(default_factory=tuple)
    native: tuple = field(default_factory=tuple)


@dataclass(eq=True, frozen=True)
class Code:
    code: str

@dataclass(eq=True, frozen=True)
class Term:
    name: str

@dataclass(eq=True, frozen=True)
class Nonterm:
    name: str
    args: tuple

EPS = "EPS"
EOF = "EOF"
