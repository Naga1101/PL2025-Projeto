import ply.lex as lex
import json
import sys

tokens = (
    # --- Keywords ---
    'PROGRAM',
    'VAR',
    'BEGIN',
    'END',
    'FUNCTION',
    'PROCEDURE',
    'CONST',
    'TYPE',
    'IF',
    'THEN',
    'ELSE',
    'WHILE',
    'DO',
    'FOR',
    'TO',
    'DOWNTO',
    'REPEAT',
    'UNTIL',
    'BREAK',
    'CASE',
    'OF',
    # --- Funções Predefinidas --- 
    'WRITEFUNC',
    'READFUNC',
    'WRITEFUNCLN',
    'READFUNCLN',
    'LENGTHFUNC',
    'ARRAY',
    'ORDFUNC',
    'PREDFUNC',
    'SUCCFUNC',
    # --- Simbolos ---
    'LBRACKET',   # [
    'RBRACKET',   # ]
    'DOTDOT',     # ..
    'LPAREN',     # (
    'RPAREN',     # )
    'COMMA',      # ,
    'COLON',      # :
    'SEMICOLON',  # ;
    'DOT',        # .
    'ASSIGN',     # :=
    # --- Operators --- 
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQ',
    'NE',
    'LT',
    'LE',
    'GT',
    'GE',
    'AND',
    'OR',
    'NOT', 
    # --- Tipos ---
    'INTEGERTYPE',
    'BOOLEANTYPE',
    'STRINGTYPE',
    # --- Literais ---
    'STRING',     # 'string'
    'CHAR',
    'NUMBER',     # 123
    # --- Comentario ---
    'COMMENT',
    # --- Identificadores ---
    'ID' 
)

# Regular expressions

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
    r'\bfunction\b'
    return t

def t_PROCEDURE(t):
    r'\bprocedure\b'
    return t

def t_CONST(t):
    r'\bconst\b'
    return t

def t_TYPE(t):
    r'\btype\b'
    return t

def t_IF(t):
    r'\bif\b'
    return t


def t_THEN(t):
    r'\bthen\b'
    return t


def t_ELSE(t):
    r'\belse\b'
    return t


def t_WHILE(t):
    r'\bwhile\b'
    return t


def t_DO(t):
    r'\bdo\b'
    return t


def t_FOR(t):
    r'\bfor\b'
    return t


def t_TO(t):
    r'\bto\b'
    return t


def t_DOWNTO(t):
    r'\bdownto\b'
    return t


def t_REPEAT(t):
    r'\brepeat\b'
    return t


def t_UNTIL(t):
    r'\buntil\b'
    return t

def t_BREAK(t):
    r'\bbreak\b'
    return t

def t_CASE(t):
    r'\bcase\b'
    return t


def t_OF(t):
    r'\bof\b'
    return t

def t_AND(t):
    r'\band\b'
    return t


def t_OR(t):
    r'\bor\b'
    return t


def t_NOT(t):
    r'\bnot\b'
    return t

## Funções Predefinidas

def t_WRITEFUNC(t):
    r'Write|write\b'
    return t

def t_READFUNC(t):
    r'\bRead|read\b'
    return t

def t_WRITEFUNCLN(t):
    r'\bWriteln|writeln\b'
    return t

def t_READFUNCLN(t):
    r'\bReadLn|readLn\b'
    return t

def t_LENGTHFUNC(t):
    r'\bLength\b|\blength\b'
    return t

def t_ORDFUNC(t):
    r'\b[oO]rd\b'
    return t

def t_PREDFUNC(t):
    r'\b[pP]red\b'
    return t

def t_SUCCFUNC(t):
    r'\b[sS]ucc\b'
    return t

def t_ARRAY(t):
    r'\barray\b'
    return t

## Simbolos

def t_DOTDOT(t):
    r'\.\.'
    return t

def t_LBRACKET(t): 
    r'\['
    return t

def t_RBRACKET(t): 
    r'\]'
    return t

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

## Operadores

def t_PLUS(t):
    r'\+'
    return t

def t_MINUS(t):
    r'-'
    return t

def t_TIMES(t):
    r'\*'
    return t

def t_DIVIDE(t):
    r'/'
    return t

def t_EQ(t):
    r'='
    return t

def t_NE(t): 
    r'<>'
    return t

def t_LE(t): 
    r'<='
    return t

def t_LT(t): 
    r'<'
    return t

def t_GE(t): 
    r'>='
    return t

def t_GT(t): 
    r'>'
    return t

## Tipos de variáveis

def t_INTEGERTYPE(t):
    r'\bInteger\b|\binteger\b'
    return t

def t_BOOLEANTYPE(t):
    r'\bBoolean\b|\bboolean\b'
    return t

def t_STRINGTYPE(t):
    r'\bString\b|\bstring\b'
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

## Comentarios

def t_COMMENT(t):
    r'\{[^}]*\}'
    return t

## Identifiers

def t_ID(t):
    r'\b[a-zA-Z_]{1}[a-zA-Z0-9_]*\b'
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
    var2 := "Ola, Mundo!";
    Writeln writeln
    { Ler 3 números }
    { Ler 4 
    números }
    end.
    """

    lexer.input(data)

    print("Tokens:")
    for tok in lexer:
        print(f"{tok.type}({tok.value}) at line {tok.lineno}, position {tok.lexpos}")

if __name__ == "__main__":
    main()
