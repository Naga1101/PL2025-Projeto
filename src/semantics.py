import ast

def test_parser(data):
    ast_tree = ast.literal_eval(data)

    _, program_content = ast_tree
    program_body = program_content['program_body']

    tabela_simbolos_global = {}
    tabela_funcoes = {}

    var_decl = program_body.get('var_declaration')
    if var_decl and var_decl[0] == 'var_decl_lines':
        for decl in var_decl[1]:
            vars_list = decl[0][1] 
            var_type = decl[1][1] 
            for var in vars_list:
                tabela_simbolos_global[var] = {
                    'kind': 'var',
                    'type': var_type
                }

    functions = program_body.get('functions')
    if functions:
        for func in functions:
            kind, func_content = func 
            func_name = func_content['name']
            return_type = func_content['return_type']
            raw_parameters = func_content['parameters']
            body = func_content['body'][1]

            parameters = []
            for (vars_tuple, type_tuple) in raw_parameters:
                var_names = vars_tuple[1]
                var_type = type_tuple[1]
                for var in var_names:
                    parameters.append((var, var_type))

            tabela_simbolos_global[func_name] = {
                'kind': kind,
                'type': return_type
            }

            tabela_funcoes[func_name] = {
                'return_type': return_type,
                'parameters': parameters,
                'func_body': body
            }


    label1 = "Nome"
    label2 = "Kind"
    label3 = "Tipo"
    label4 = "Valor de Retorno"
    label5 = "Parametros de entrada"
    label6 = "Corpo da Função"
    print("Tabela de Simbolos:")
    print(f"{label1:10} | {label2:8} | {label3}")
    for name, info in tabela_simbolos_global.items():
        print(f"{name:10} | {info['kind']:8} | {info['type']}")
    
    print()
    print("Tabela de Funções:")
    print(f"{label1:10} | {label4:14} | {label5:38} | {label6}")
    for name, info in tabela_funcoes.items():
        print(f"{name:10} | {info['return_type']:16} | {str(info['parameters']):38} | {info['func_body']}")

    

data5 = """
('program',{'program_name':'SumExample','program_body':{'functions':[('function',{'name':'Add','parameters':[(('vars', ['a']), ('type', 'integer')),(('vars', ['b']), ('type', 'integer'))],'return_type':'integer','body':('compound',[('writeln', 'num1 is positive')])}),('function',{'name': 'Add','parameters':[(('vars', ['a']), ('type', 'integer')),(('vars', ['b']), ('type', 'integer'))],'return_type': 'integer','body':('compound',[('Assign','x',('binop', '+', 'a', 'b'))])})],'var_declaration':('var_decl_lines',[(('vars', ['num1', 'num2', 'result']),('type', 'integer'))]),'program_code':('compound',[('Assign', 'num1', 5),('Assign', 'num2', 3),('Assign','result',('Function_call',{'name': 'Add','args': ['num1', 'num2']})),('writeln', 'The sum is: ')])}})
"""

test_parser(data5)
