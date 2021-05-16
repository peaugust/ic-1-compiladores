grammar cmm;

start: file_body* EOF;

file_body: def_class | func | assign_statm | class_prop_call;

func: 'def' name = ID '(' args? ')' statms;

func_call: name = ID '(' args? ')' ';';

class_props: func_call | name = ID ';';

def_class:
	'class' name = CLASS_ID '{' atbs = assign_statm* init = func scope = class_scope* '}';

class_scope: func | assign_statm;

args: ID (',' ID)* | INT (',' INT)*;

statms: '{' statm* '}' | statm;

assign_statm: ID '=' expr ';';
class_prop_call: ID '.' class_props;

statm:
	assign_statm													                             # assign
	| 'print' expr ';'												                             # print
	| 'if' cond = expr then = statms ('else' otherwise = statms)?	                             # if
	| 'while' cond = expr statms									                             # while
	| 'do' statms 'while' cond = expr ';'														 # do
	|  for_stm                                                                                   # for
	| switch_case_stm												                             # switch
	| 'break' ';'													                             # break
	| 'return' expr ';'												                             # return
    ;


for_stm: 'for' '('assign_statm   cond = expr ';' expr|'++'ID|'--'ID|ID'++'|ID'--' ')' statms;

switch_case_stm:
	'switch' '(' expr ')' (( 'case' expr ':')+ statm+)+ (
		'default' ':' statm
	)?;

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
	| FLOAT
	| STRING
	| BOOL
	| 'input'
	| class_call
	| ID
	| call;

BOOL: '\'true\'' | '\'false\'';
INPUT: 'input';
ELSE: 'else';
INT: [0-9]+;
FLOAT: [0-9]+ '.' [0-9]+;
STRING: '"' ~('"')* '"';
WS: [ \r\n\t]+ -> skip;
CLASS_ID: [A-Z]+ [a-zA-Z]*;
ID: [a-zA-Z]+ [0-9a-zA-Z]*;
