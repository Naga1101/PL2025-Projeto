import ply.lex as lex
import json
import sys

tokens = (
    'BEGIN',
    'ID' # o parser é que decide se é uma var ou o nome de uma func 
)

keywords = {
    'begin': 'BEGIN',
}

def t_ID(t):
    r'^[a-zA-Z_]{1}[a-zA-Z0-9_]*'
    t.type = keywords.get(t.value.lower(), 'ID')
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
