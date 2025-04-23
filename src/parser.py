from ply import yacc
from lexer import tokens

"""
P1: Init        →   program FuncName
P2: FuncName    →   ID ';' VarDeclPart | BeginPart
P3: VarDeclPart    →   var VarDeclList
P4: VarDeclList →   ID IDListCont
P5: IDListCont  →   ',' ID IDListCont | ':' Type ';'
P6: Type        →   TIPOVAR VarDeclList | BeginPart
P7: BeginPart   →   begin ...
"""

def p_init(p):
    'init : PROGRAM funcname'
    p[0] = ("program", p[2])

def p_funcname_decl(p):
    'funcname : ID PONTOEVIRGULA VarDeclPart'
    p[0] = ("functionName", p[1], p[3])

def p_funcname_begin(p):
    'funcname : beginpart'
    p[0] = ("begin", p[1])

def p_varDeclPart(p):
    'VarDeclPart : VAR vardecllist'
    p[0] = ("var_decl", p[2])

def p_vardecllist(p):
    'vardecllist : ID idlistcont'
    p[0] = ("var", [p[1]] + p[2])

def p_idlistcont_more(p):
    'idlistcont : VIRGULA ID idlistcont'
    p[0] = [p[2]] + p[3]

def p_idlistcont_type(p):
    'idlistcont : DOISPONTOS type PONTOEVIRGULA'
    p[0] = [("type", p[2])]

def p_type_var(p):
    'type : TIPOVAR vardecllist'
    p[0] = ("typed_vars", p[1], p[2])

def p_type_begin(p):
    'type : beginpart'
    p[0] = p[1]

def p_beginpart(p):
    'beginpart : BEGIN'
    p[0] = "BEGIN_BLOCK"  # Placeholder for now

def p_error(p):
    print(f"Syntax error at {p.value if p else 'EOF'}")

parser = yacc.yacc()