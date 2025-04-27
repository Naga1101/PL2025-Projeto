from ply import yacc
from lexer import tokens, lexer

"""
P1: init → PROGRAM func_name

P2: func_name → ID ';' var_decl_or_func

P3: var_decl_or_func → var_decl begin_func
                     | begin_func

P4: var_decl → VAR var_decl_lines

P5: var_decl_lines → var_decl_line
                   | var_decl_lines var_decl_line

P6: var_decl_line → id_list ':' type ';'

P7: id_list → ID
            | id_list ',' ID

P8: type → INTEGERTYPE
         | BOOLEANTYPE
         | STRINGTYPE

P9: begin_func → compound_statement DOT

P10: statement_list → statement
                    | statement_list statement

P11: statement → simple_statement SEMICOLON
               | compound_statement SEMICOLON
               | selection_statement SEMICOLON

P12: simple_statement → ID EQUALS expression

P13: selection_statement → IF expression THEN statement
                         | IF expression THEN statement ELSE statement

P14: compound_statement → BEGIN statement_list END

P15: expression → expression PLUS expression
                | expression MINUS expression
                | expression TIMES expression
                | expression DIVIDE expression
                | NUMBER
                | ID
"""

def p_init(p):
    'init : PROGRAM func_name'
    p[0] = ("program", p[2])
### mudar a partir daqui
def p_func_name_decl(p):
    'func_name : ID SEMICOLON var_decl'
    p[0] = ("functionName", p[1], p[3])

def p_func_name_begin(p):
    'func_name : ID SEMICOLON begin_func'
    p[0] = ("begin", p[1])

def p_var_decl(p):
    'var_decl : VAR var_decl_list'
    p[0] = ("var_decl", p[2])

def p_var_decl_list(p):
    'var_decl_list : ID id_list_cont'
    p[0] = ("var", [p[1]] + p[2])

def p_id_list_cont_more(p):
    'id_list_cont : COMMA ID id_list_cont'
    p[0] = [p[2]] + p[3]

def p_id_list_cont_type(p):
    'id_list_cont : COLON type_recognition'
    p[0] = [("type_recognition", p[2])]

def p_type_recognition_var(p):
    'type_recognition : typedefinition SEMICOLON var_decl_list'
    p[0] = ("typed_vars", p[1], p[3])

def p_type_recognition_begin(p):
    'type_recognition : typedefinition SEMICOLON begin_func'
    p[0] = ("type_and_begin", p[1], p[3])  

def p_typedefinition(p):
    '''typedefinition : INTEGERTYPE
                      | BOOLEANTYPE
                      | STRINGTYPE'''
    p[0] = ("typedefinition", p[1])

def p_begin_func(p):
    'begin_func : BEGIN'
    p[0] = "BEGIN_BLOCK"  # Falta a parte dos statements

def p_error(p):
    print(f"Syntax error at {p.value if p else 'EOF'}")

parser = yacc.yacc(debug=True)

def test_parser(data):
    lexer.input(data)
    lexer_clone = lexer.clone() 
    for tok in lexer_clone:
        print(tok)
    result = parser.parse(lexer=lexer, debug=True)
    print(result)

data0 = """
program Maior3;
begin
"""

data1 = """
program Maior3;
var
    num1, num2, num3, maior: Integer;
begin
"""

data2 = """
program Maior3;
var
    num1, num2, num3, maior: Integer;
    bol1, bol2: Boolean;
begin
"""

if __name__ == "__main__":
    print("Primeiro teste:")
    test_parser(data0)
    print("Segundo teste:")
    test_parser(data1)
    print("Terceiro teste:")
    test_parser(data2)
