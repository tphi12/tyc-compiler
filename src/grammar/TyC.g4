grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

program: (structDecl | funcDecl)* EOF;

structDecl: STRUCT IDENTIFIER LEFT_BRACE structMember* RIGHT_BRACE SEMICOLON;

structMember: typeSpec IDENTIFIER SEMICOLON;

funcDecl: returnType? IDENTIFIER LEFT_PAREN paramList? RIGHT_PAREN blockStmt;

returnType: primitiveType | IDENTIFIER;

primitiveType: INT_TYPE | FLOAT_TYPE | STRING_TYPE | VOID;

paramList: param (COMMA param)*;

param: typeSpec IDENTIFIER;

typeSpec: primitiveType | IDENTIFIER;

stmt
    : varDecl
    | blockStmt
    | ifStmt
    | whileStmt
    | forStmt
    | switchStmt
    | breakStmt
    | continueStmt
    | returnStmt
    | exprStmt
    ;

varDecl
    : AUTO IDENTIFIER (ASSIGN expr)? SEMICOLON
    | typeSpec IDENTIFIER (ASSIGN expr)? SEMICOLON
    | typeSpec IDENTIFIER ASSIGN LEFT_BRACE exprList? RIGHT_BRACE SEMICOLON
    ;

exprList: expr (COMMA expr)*;

blockStmt: LEFT_BRACE (varDecl | stmt)* RIGHT_BRACE;

ifStmt: IF LEFT_PAREN expr RIGHT_PAREN stmt (ELSE stmt)?;

whileStmt: WHILE LEFT_PAREN expr RIGHT_PAREN stmt;

forStmt: FOR LEFT_PAREN forInit? SEMICOLON forCondition? SEMICOLON forUpdate? RIGHT_PAREN stmt;

forInit
    : AUTO IDENTIFIER (ASSIGN expr)?
    | typeSpec IDENTIFIER (ASSIGN expr)?
    | assignExpr
    ;

forCondition: expr;

forUpdate
    : assignExpr
    | postfixExpr
    ;

switchStmt: SWITCH LEFT_PAREN expr RIGHT_PAREN LEFT_BRACE caseClause* RIGHT_BRACE;

caseClause
    : CASE expr COLON stmt*
    | DEFAULT COLON stmt*
    ;

breakStmt: BREAK SEMICOLON;

continueStmt: CONTINUE SEMICOLON;

returnStmt: RETURN expr? SEMICOLON;

exprStmt: expr SEMICOLON;

expr: assignExpr;

assignExpr
    : logicalOrExpr (ASSIGN assignExpr)?
    ;

logicalOrExpr
    : logicalAndExpr (LOGICAL_OR logicalAndExpr)*
    ;

logicalAndExpr
    : equalityExpr (LOGICAL_AND equalityExpr)*
    ;

equalityExpr
    : relationalExpr ((EQUAL | NOT_EQUAL) relationalExpr)*
    ;

relationalExpr
    : additiveExpr ((LESS_THAN | LESS_EQUAL | GREATER_THAN | GREATER_EQUAL) additiveExpr)*
    ;

additiveExpr
    : multiplicativeExpr ((PLUS | MINUS) multiplicativeExpr)*
    ;

multiplicativeExpr
    : unaryExpr ((MULTIPLY | DIVIDE | MODULUS) unaryExpr)*
    ;

unaryExpr
    : (PLUS | MINUS | LOGICAL_NOT) unaryExpr
    | (INCREMENT | DECREMENT) unaryExpr
    | postfixExpr
    ;

postfixExpr
    : primaryExpr (
        DOT IDENTIFIER
        | LEFT_PAREN exprList? RIGHT_PAREN
        | INCREMENT
        | DECREMENT
      )*
    ;

primaryExpr
    : INTEGER_LITERAL
    | FLOAT_LITERAL
    | STRING_LITERAL
    | IDENTIFIER
    | LEFT_PAREN expr RIGHT_PAREN
    | LEFT_BRACE exprList? RIGHT_BRACE
    ;
AUTO: 'auto';
BREAK: 'break';
CASE: 'case';
CONTINUE: 'continue';
DEFAULT: 'default';
ELSE: 'else';
FLOAT_TYPE: 'float';
FOR: 'for';
IF: 'if';
INT_TYPE: 'int';
RETURN: 'return';
STRING_TYPE: 'string';
STRUCT: 'struct';
SWITCH: 'switch';
VOID: 'void';
WHILE: 'while';

LOGICAL_OR: '||';
LOGICAL_AND: '&&';
EQUAL: '==';
NOT_EQUAL: '!=';
LESS_EQUAL: '<=';
GREATER_EQUAL: '>=';
INCREMENT: '++';
DECREMENT: '--';

PLUS: '+';
MINUS: '-';
MULTIPLY: '*';
DIVIDE: '/';
MODULUS: '%';
LESS_THAN: '<';
GREATER_THAN: '>';
LOGICAL_NOT: '!';
ASSIGN: '=';
DOT: '.';

LEFT_BRACE: '{';
RIGHT_BRACE: '}';
LEFT_BRACKET: '[';
RIGHT_BRACKET: ']';
LEFT_PAREN: '(';
RIGHT_PAREN: ')';
SEMICOLON: ';';
COMMA: ',';
COLON: ':';

BLOCK_COMMENT: '/*' .*? '*/' -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;

IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*;

FLOAT_LITERAL
    : DIGIT+ '.' DIGIT* EXPONENT?
    | '.' DIGIT+ EXPONENT?
    | DIGIT+ EXPONENT
    ;

INTEGER_LITERAL: DIGIT+;

STRING_LITERAL
    : '"' (STR_CHAR | ESC_SEQ)* '"'
    {
        # Strip the surrounding quotes from the token text
        self.text = self.text[1:-1]
    }
    ;

ILLEGAL_ESCAPE
    : '"' (STR_CHAR | ESC_SEQ)* '\\' ~[bfrnt"\\]
    {
        # Strip the opening quote
        self.text = self.text[1:]
    }
    ;

UNCLOSE_STRING
    : '"' (STR_CHAR | ESC_SEQ)* ([\r\n] | EOF)
    {
        # Strip the opening quote
        self.text = self.text[1:]
    }
    ;

WS: [ \t\f\r\n]+ -> skip;

ERROR_CHAR: .;

fragment DIGIT: [0-9];

fragment EXPONENT: [eE] [+-]? DIGIT+;

fragment STR_CHAR: ~["\\\r\n];

fragment ESC_SEQ: '\\' [bfrnt"\\];
