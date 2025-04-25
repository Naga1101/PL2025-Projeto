import ply.lex as lex
import json
import sys

tokens = (
    'PROGRAM',
    'VAR',
    'BEGIN',
    'END',
    'PROGRAM','BEGIN','END','VAR','FUNCTION','PROCEDURE',
    'IF','THEN','ELSE','WHILE','DO','FOR','TO','DOWNTO',
    'REPEAT','UNTIL','CASE','OF','CONST','TYPE',
    'PLUS','MINUS','TIMES','DIVIDE',
    'EQ','NE','LT','LE','GT','GE','ASSIGN',
    'AND','OR','NOT', 
    'LPAREN',     # (
    'RPAREN',     # )
    'COMMA',      # ,
    'COLON',      # :
    'SEMICOLON',  # ;
    'DOT',        # .
    'ASSIGN',     # :=
    'INTEGERTYPE',
    'BOOLEANTYPE',
    'STRINGTYPE',
    'STRING',     # 'string'
    'CHAR',
    'NUMBER',     # 123
    'ID' # o parser é que decide se é uma var ou o nome de uma func
)

# Regular expressions

#Operators
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_EQ = r"="
t_NE = r"<>"
t_LE = r"<="
t_LT = r"<"
t_GE = r">="
t_GT = r">"
t_ASSIGN = r":="

## Keywords

def t_PROGRAM(t):
    r'\bprogram\b'
    return t

def t_VAR(t):
    r'\bvar\b'
    return t

def t_BEGIN(t):
    r'\bbegin\b'
    return t

def t_END(t):
    r'\bend\b'
    return t

def t_FUNCTION(t):
    r"\function\b"
    return t


def t_PROCEDURE(t):
    r"\bprocedure\b"
    return t


def t_IF(t):
    r"\if\b"
    return t


def t_THEN(t):
    r"\then\b"
    return t


def t_ELSE(t):
    r"\else\b"
    return t


def t_WHILE(t):
    r"\while\b"
    return t


def t_DO(t):
    r"\do\b"
    return t


def t_FOR(t):
    r"\for\b"
    return t


def t_TO(t):
    r"\to\b"
    return t


def t_DOWNTO(t):
    r"\downto\b"
    return t


def t_REPEAT(t):
    r"\repeat\b"
    return t


def t_UNTIL(t):
    r"\until\b"
    return t


def t_CASE(t):
    r"\case\b"
    return t


def t_OF(t):
    r"\of\b"
    return t


def t_CONST(t):
    r"\const\b"
    return t


def t_TYPE(t):
    r"\type\b"
    return t


def t_AND(t):
    r"\band\b"
    return t


def t_OR(t):
    r"\bor\b"
    return t


def t_NOT(t):
    r"\bnot\b"
    return t

## Simbolos

def t_LPAREN(t): 
    r'\('
    return t

def t_RPAREN(t): 
    r'\)'
    return t

def t_COMMA(t): 
    r','
    return t

def t_ASSIGN(t):
    r':='
    return t

def t_COLON(t): 
    r':'
    return t

def t_SEMICOLON(t): 
    r';'
    return t

def t_DOT(t): 
    r'\.'
    return t

## Tipos de variáveis

def t_INTEGERTYPE(t):
    r'\binteger\b'
    return t

def t_BOOLEANTYPE(t):
    r'\bboolean\b'
    return t

def t_STRINGTYPE(t):
    r'\bstring\b'
    return t

## Literais

### Literais numéricos
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

### Literais de strings/char
def t_STRING(t):
    r'\'([^\'\n]|(\\\'))*\''
    value = t.value[1:-1]
    if len(value) == 1:
        t.type = 'CHAR'
    t.value = value
    return t


## Identifiers

def t_ID(t):
    r'\b[a-zA-Z_]{1}[a-zA-Z0-9_]*'
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def main():
    data = """
    program funcaoTeste
    var
    var1, var2: integer;
    begin
    var1 := 10;
    var2 := 'a';
    end.
    """

    lexer.input(data)

    print("Tokens:")
    for tok in lexer:
        print(f"{tok.type}({tok.value}) at line {tok.lineno}, position {tok.lexpos}")

if __name__ == '__main__':
    main()
