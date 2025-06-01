from ply import yacc
from lexer import tokens, lexer

"""
P1: init → PROGRAM program_name

P2: program_name → ID ';' program_body

P3: program_body → new_funct
                 | var_decl begin_progr
                 | begin_progr

P4: func_decls → func_decl 
               | func_decls func_decl

P5: func_decl → FUNCTION ID LPAREN var_decl_lines RPAREN COLON type SEMICOLON program_body

P6: var_decl → VAR var_decl_lines

P7: var_decl_lines → var_decl_line
                   | var_decl_lines var_decl_line

P8: var_decl_line → id_list ':' type ';'

P9: id_list → ID
            | id_list ',' ID

P10: type → INTEGERTYPE
         | FLOATTYPE
         | BOOLEANTYPE
         | STRINGTYPE

P11: begin_progr → compound_statement DOT
                 | compound_statement SEMICOLON program_body

P12: statement_list → statement
                    | statement_list statement

P13: statement → simple_statement SEMICOLON
               | compound_statement SEMICOLON
               | selection_statement SEMICOLON
               | for_statement

P14: simple_statement → ID EQUALS expression
                      | WRITEFUNC LPAREN expression RPAREN SEMICOLON

P15: selection_statement → IF expression THEN statement
                         | IF expression THEN statement ELSE statement

P16: for_statement → FOR ID ASSIGN expression TO expression DO statement
                    | FOR ID ASSIGN expression DOWNTO expression DO statement

P17: compound_statement → BEGIN statement_list END

P18: expression → expression PLUS expression
                | expression MINUS expression
                | expression TIMES expression
                | expression DIVIDE expression
                | STRING
                | NUMBER
                | CHAR
                | ID

P19: expression_list → expression
                     | expression_list ',' expression 
"""

def p_init(p):
    'init : PROGRAM program_name'
    p[0] = ("program", p[2])

def p_program_name(p):
    'program_name : ID SEMICOLON program_body'
    p[0] = ({
            'program_name': p[1],
            'program_body': p[3],
        })

def p_program_body(p):  # Assumir que vem sempre na ordem correta ou fazer uma lista de declarations para apanahr qualquer ordem
    '''program_body : const_decls func_decls var_decl begin_progr
                    | func_decls var_decl begin_progr
                    | const_decls var_decl begin_progr
                    | const_decls func_decls begin_progr
                    | const_decls begin_progr
                    | func_decls begin_progr
                    | var_decl begin_progr
                    | begin_progr'''
    if len(p) == 5:
        p[0] = ({
            'consts': p[1],
            'functions': p[2],
            'var_declaration': p[3],
            'program_code': p[4],
        })
    elif len(p) == 4 and p.slice[1].type == 'func_decls':
        p[0] = ({
            'functions': p[1],
            'var_declaration': p[2],
            'program_code': p[3],
        })
    elif len(p) == 4 and p.slice[1].type == 'const_decls' and p.slice[2].type == 'var_decl':
        p[0] = ({
            'consts': p[1],
            'var_declaration': p[2],
            'program_code': p[3],
        })
    elif len(p) == 4 and p.slice[1].type == 'const_decls' and p.slice[2].type == 'func_decls':
        p[0] = ({
            'consts': p[1],
            'functions': p[2],
            'program_code': p[3],
        })
    elif  len(p) == 3 and p.slice[1].type == 'const_decls':
        p[0] = ({
            'consts': p[1],
            'program_code': p[2],
        })
    elif  len(p) == 3 and p.slice[1].type == 'func_decls':
        p[0] = ({
            'functions': p[1],
            'program_code': p[2],
        })
    elif len(p) == 3 and p.slice[1].type == 'var_decl':
        p[0] = ({
            'var_declaration': p[1],
            'program_code': p[2],
        })
    else:
        p[0] = ({
            'program_code': p[1],
        })

def p_const_decls(p):
    '''const_decls : CONST const_decl_list'''
    p[0] = p[2]

def p_const_decl_list(p):
    '''const_decl_list : const_decl 
                       | const_decl_list const_decl'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_const_decl(p):
    'const_decl : ID EQ expression SEMICOLON'
    p[0] = ('const', {
        'name': p[1],
        'value': p[3]
    })

def p_func_decls(p):
    '''func_decls : func_decl 
                  | func_decls func_decl'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_func_decl(p):
    'func_decl : FUNCTION ID LPAREN var_decl_lines RPAREN COLON type SEMICOLON begin_func'
    p[0] = ('function', {
        'name': p[2],
        'parameters': p[4],
        'return_type': p[7],
        'body': p[9]
    })

def p_begin_funct(p):
    '''begin_func : var_decl compound_statement SEMICOLON
                  | compound_statement SEMICOLON'''
    if len(p) == 4:
        p[0] = (("var_declaration", p[1]), p[2])
    else:
        p[0] = (p[1])

def p_var_decl(p):
    'var_decl : VAR var_decl_lines'
    p[0] = ("var_decl_lines", p[2])

def p_var_decl_lines(p):
    '''var_decl_lines : var_decl_line
                      | var_decl_lines var_decl_line'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_var_decl_line(p):
    '''var_decl_line : id_list COLON type SEMICOLON
                     | id_list COLON type'''
    p[0] = (("vars", p[1]), ("type", p[3]))

def p_id_list(p):
    '''id_list : ID
               | id_list COMMA ID'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_type(p):
    '''type : INTEGERTYPE
            | FLOATTYPE
            | BOOLEANTYPE
            | STRINGTYPE
            | ARRAY LBRACKET NUMBER DOTDOT NUMBER RBRACKET OF type'''
    if p.slice[1].type == 'ARRAY':
        p[0] = ('array', {'low': p[3], 'high': p[5], 'elem_type': p[8]})
    else:
        p[0] = p[1]

def p_begin_progr(p):
    'begin_progr : compound_statement DOT'
    p[0] =  p[1]

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : COMMENT
                 | simple_statement SEMICOLON
                 | compound_statement SEMICOLON
                 | selection_statement
                 | while_statement
                 | for_statement'''
    if p.slice[1].type == 'COMMENT':
        p[0] = ("comment", p[1])
    else:
        p[0] = p[1]

def p_simple_statement(p):
    '''simple_statement : ID ASSIGN expression
                        | WRITEFUNC LPAREN expression_list RPAREN
                        | WRITEFUNCLN LPAREN expression_list RPAREN
                        | READFUNC expression
                        | READFUNCLN expression
                        | BREAK'''
    function = p.slice[1].type
    if function in 'WRITEFUNC':
        p[0] = ('write', p[3])
    elif function in 'WRITEFUNCLN':
        p[0] = ('writeln', p[3])
    elif function in 'READFUNC':
        p[0] = ('read', p[2])
    elif function in 'READFUNCLN':
        p[0] = ('readln', p[2])
    elif function == 'BREAK':
        p[0] = ('break')
    else:
        p[0] = ("assign", p[1], p[3])

def p_compound_statement(p):
    '''compound_statement : BEGIN statement_list END'''
    p[0] = ("compound", p[2])

def p_selection_statement(p):
    '''selection_statement : IF expression THEN statement
                           | IF expression THEN inside_statement ELSE statement'''
    if len(p) == 5:
        p[0] = ('if', {
            'case': p[2],
            'do': p[4]
        })
    else:
        p[0] = ('if', {
            'case': p[2],
            'do': p[4],
            'else': p[6]
        })

def p_inside_statement(p):
    '''inside_statement : simple_statement
                        | compound_statement
                        | inside_selection_statement'''
    p[0] = p[1]

def p_inside_selection_statement(p):
    '''inside_selection_statement : IF expression THEN inside_statement
                                  | IF expression THEN inside_statement ELSE inside_statement'''
    if len(p) == 5:
        p[0] = ('if', {
            'case': p[2],
            'do': p[4]
        })
    else:
        p[0] = ('if', {
            'case': p[2],
            'do': p[4],
            'else': p[6]
        })

def p_for_statement(p):
    '''for_statement : FOR ID ASSIGN expression TO expression DO statement
                     | FOR ID ASSIGN expression DOWNTO expression DO statement'''
    direction = 'to' if p.slice[5].type == 'TO' else 'downto'
    p[0] = ('for', {
        'var': p[2],
        'start': p[4],
        'end': p[6],
        'direction': direction,
        'body': p[8]
    })

def p_while_statement(p):
    'while_statement : WHILE expression DO statement'
    p[0] = ('while', {
        'condition': p[2],
        'body': p[4]
    })

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIV expression
                  | expression MOD expression
                  | expression AND expression
                  | expression GT expression
                  | expression LT expression
                  | expression GE expression
                  | expression LE expression
                  | expression EQ expression
                  | expression NE expression
                  | expression OR expression'''
    p[0] = ('binop', p[2], p[1], p[3])
    p[0] = ('binop', {
        'type': p[2],
        'left': p[1],
        'right': p[3],
    })

def p_expression_value(p):
    '''expression : STRING
                  | NUMBER
                  | FLOAT
                  | FALSE
                  | TRUE
                  | CHAR
                  | ID
                  | ID LBRACKET expression RBRACKET'''
    if len(p) > 2:
        p[0] = ('array', {
        'name': p[1],
        'index': p[3]
    })
    else:
        p[0] = p[1]
    
def p_expression_function_call(p):
    '''expression : ID LPAREN expression_list RPAREN
                  | ID LPAREN RPAREN'''
    if len(p) == 5:
        p[0] = ("Function_call", {
            "name": p[1],
            "args": p[3]
        })
    else:
        p[0] = ("Function_call", {
            "name": p[1],
            "args": []
        })
    
def p_expression_list(p):
    '''expression_list : expression
                       | expression_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_expression_not(p):
    'expression : NOT expression'
    p[0] = ('NOT', p[2])

def p_expression_empty(p):
    'expression :'
    p[0] = "empty"

def p_expression_builtinfunction(p): ###
    '''expression : ORDFUNC    expression
                  | PREDFUNC   expression
                  | SUCCFUNC   expression
                  | LENGTHFUNC expression'''
    function = p.slice[1].type
    if function == 'LENGTHFUNC':
        p[0] = ('length', p[2])
    elif function == 'ORDFUNC':
        p[0] = ('ord', p[2])
    elif function == 'PREDFUNC':
        p[0] = ('pred', p[2])
    else:
        p[0] = ('succ', p[2])
    
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

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


r'''
data4="""
program SumExample;

function Add(a: integer; b: integer): integer;
begin
    writeln('num1 is positive');
end;

var
    num1, num2, result: integer;
begin
    num1 := 5;
    num2 := 3;
    result := Add(num1, num2);
    writeln('The sum is: ');
end.
"""

data8 = """
program SumExample;

function Add(a: integer; b: integer): integer;
begin
    Add := a + b;
end;

var
    num1, num2, result: integer;
begin
    num1 := 5;
    num2 := 3;
    result := Add(num1, num2);
    writeln(result);
end.
"""

data11 = """
program SomaArray;
var
    numeros: array[1..5] of integer;
    i, soma: integer;
begin
    soma := 0;
    writeln('Introduza 5 números inteiros:');
    for i := 1 to 5 do
    begin
        readln(numeros[i]);
        soma := soma + numeros[i];
    end;

    writeln('A soma dos números é: ', soma);
end.
"""

if __name__ == "__main__":
    #test_parser(data4)
    test_parser(data8)
    #test_parser(data11)'''