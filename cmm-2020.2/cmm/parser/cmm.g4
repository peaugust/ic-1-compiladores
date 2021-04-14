grammar cmm;

start: func* EOF;

func: 'def' name = ID '(' args? ')' statms;

args: ID (',' ID)*;

statms: '{' statm* '}' | statm;

statm:
	ID '=' expr ';'													# assign
	| 'print' expr ';'												# print
	| 'if' cond = expr then = statms ('else' otherwise = statms)?	# if
	| 'while' cond = expr statms									# while
	| 'do' statms 'while' cond = expr ';'                           # do
	| 'return' expr ';'												# return;

call: name = ID '(' exprs? ')';

exprs: expr (',' expr)*;

expr:
	left = summ (
		op = ('>' | '<' | '>=' | '<=' | '==' | '!=') right = expr
	)*;

summ: left = mult (op = ('+' | '-') right = summ)*;

mult: left = atom (op = ('*' | '/') right = mult)*;

atom: '(' expr ')' | INT | ID | FLOAT | STRING | BOOL| 'input' | call ;

BOOL: '\'true\'' | '\'false\'';
INPUT: 'input';
ELSE: 'else';
ID: [a-zA-Z]+ [0-9a-zA-Z]*;
INT: [0-9]+;
FLOAT : [0-9]+'.'[0-9]+;
STRING : '"' ~('"')* '"';
WS: [ \r\n\t]+ -> skip;
