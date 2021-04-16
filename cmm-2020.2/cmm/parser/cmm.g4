grammar cmm;

start: file_body* EOF;

file_body: def_class | func | assign_statm;

func: 'def' name = ID '(' args? ')' statms;

def_class:
	'class' name = CLASS_ID '{' init = init_func scope = class_scope* '}';

init_func: 'def' name = 'init' '(' args? ')' statms;

class_scope: func | assign_statm;

args: ID (',' ID)*;

statms: '{' statm* '}' | statm;

assign_statm: ID '=' expr ';';

statm:
	assign_statm													# assign
	| 'print' expr ';'												# print
	| 'if' cond = expr then = statms ('else' otherwise = statms)?	# if
	| 'while' cond = expr statms									# while
	| 'return' expr ';'												# return;

call: name = ID '(' exprs? ')';
class_call: className = CLASS_ID '(' args? ')';

exprs: expr (',' expr)*;

expr:
	left = summ (
		op = ('>' | '<' | '>=' | '<=' | '==' | '!=') right = expr
	)*;

summ: left = mult (op = ('+' | '-') right = summ)*;

mult: left = atom (op = ('*' | '/') right = mult)*;

atom:
	'(' expr ')'
	| INT
	| ID
	| FLOAT
	| STRING
	| BOOL
	| 'input'
	| class_call
	| call;

BOOL: '\'true\'' | '\'false\'';
INPUT: 'input';
ELSE: 'else';
CLASS_ID: [A-Z]+ [a-zA-Z]*;
ID: [a-zA-Z]+ [0-9a-zA-Z]*;
INT: [0-9]+;
FLOAT: [0-9]+ '.' [0-9]+;
STRING: '"' ~('"')* '"';
WS: [ \r\n\t]+ -> skip;
