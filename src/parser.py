from ply import yacc
from lexer import tokens, lexer

"""
P1: Init        →   program FuncName
P2: FuncName    →   ID ';' VarDeclPart | BeginPart
P3: VarDeclPart    →   var VarDeclList
P4: VarDeclList →   ID IDListCont
P5: IDListCont  →   ',' ID IDListCont | ':' Type ';'
P6: TypeRecognition  →   TYPE VarDeclList | BeginPart
P7: TYPE → INTEGERTYPE | BOOLEANTYPE | STRINGTYPE
P8: BeginPart   →   begin ...
"""

def p_init(p):
    'init : PROGRAM funcname'
    p[0] = ("program", p[2])

def p_funcname_decl(p):
    'funcname : ID SEMICOLON VarDeclPart'
    p[0] = ("functionName", p[1], p[3])

def p_funcname_begin(p):
    'funcname : ID SEMICOLON beginpart'
    p[0] = ("begin", p[1])

def p_varDeclPart(p):
    'VarDeclPart : VAR vardecllist'
    p[0] = ("var_decl", p[2])

def p_vardecllist(p):
    'vardecllist : ID idlistcont'
    p[0] = ("var", [p[1]] + p[2])

def p_idlistcont_more(p):
    'idlistcont : COMMA ID idlistcont'
    p[0] = [p[2]] + p[3]

def p_idlistcont_type(p):
    'idlistcont : COLON typerecognition'
    p[0] = [("typerecognition", p[2])]

def p_typerecognition_var(p): # integer type for testing
    'typerecognition : typedefinition SEMICOLON vardecllist'
    p[0] = ("typed_vars", p[1], p[2])

def p_typerecognition_begin(p):
    'typerecognition : typedefinition SEMICOLON beginpart'
    p[0] = p[1]

def p_typedefinition(p):
    '''typedefinition : INTEGERTYPE
                      | BOOLEANTYPE
                      | STRINGTYPE'''
    p[0] = ("typedefinition", p[1])

def p_beginpart(p):
    'beginpart : BEGIN'
    p[0] = "BEGIN_BLOCK"  # Placeholder for now

def p_error(p):
    print(f"Syntax error at {p.value if p else 'EOF'}")

parser = yacc.yacc(debug=True)

def test_parser(data):
    lexer.input(data)
    for tok in lexer:
        print(tok)
    result = parser.parse(lexer=lexer)
    print(result)

# Example input string
data = """
program Maior3;
var
    num1, num2, num3, maior: Integer;
begin
"""

if __name__ == "__main__":
    test_parser(data)
