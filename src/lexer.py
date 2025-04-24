import ply.lex as lex
import json
import sys

tokens = (
    'BEGIN',
    'LPAREN',     # (
    'RPAREN',     # )
    'COMMA',      # ,
    'COLON',      # :
    'SEMICOLON',  # ;
    'DOT',        # .
    'ASSIGN',     # :=
    'STRING',     # 'string'
    'NUMBER',     # 123
    'ID' # o parser é que decide se é uma var ou o nome de uma func
)

keywords = {
    'begin': 'BEGIN',
}

#Regular expressions
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_COLON = r':'
t_SEMICOLON = r';'
t_DOT = r'\.'
t_ASSIGN = r':='

# Literais numéricos
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Literais de strings/char
def t_STRING(t):
    r'\'([^\'\n]|(\\\'))*\''
    value = t.value[1:-1]
    if len(value) == 1:
        t.type = 'CHAR'
    t.value = value
    return t

def t_ID(t):
    r'^[a-zA-Z_]{1}[a-zA-Z0-9_]*'
    t.type = keywords.get(t.value.lower(), 'ID')
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
