grammar Gram;

file : (begin rulee+)? EOF;

begin: '|>' NT_ID;

rulee
	: parserRulee ';'
	| lexerRule ';'
	;

parserRulee : NT_ID inAttrs? ':=' prods ('|' prods)*;

inAttrs : '<' NT_ID (',' NT_ID)* '>';
param : paramName;
paramName : NT_ID;

prods: prod*;
prod: NT_ID args? | T_ID | CODE;
args: '(' arg (',' arg)* ')';
arg : NT_ID | T_ID | CODE;

lexerRule
	: T_ID '=' term_value  # tokenRule
	| T_ID '=>' term_value # skipRule
	;

term_value
	: REGEX
	| STRING
	;

NT_ID : [a-z][a-zA-Z0-9]*;
T_ID : [A-Z][a-zA-Z0-9]*;

REGEX : '\'' (~('\''|'\r' | '\n') | '\\\'')* '\'';
STRING : '"' (~('"') | '\\"')* '"';

CODE : '{' (~[{}]+ CODE?)* '}' ;

WS  : [ \t\r\n]+ -> skip ;