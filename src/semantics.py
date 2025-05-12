import ast

import os
## Global vars

output_file = "outputs/output.txt"

conversor_tipos = {
    'int': 'integer',
    'float': 'float',
    'str': 'string',
    'bool': 'boolean',
    'NoneType': 'void',
}

tipo_de_push = {
    'Integer': 'PUSHI',
    'integer': 'PUSHI',
    'float': 'PUSHL',
    'string': 'PUSHS'
}
free_fp = 0
free_gp = 0

tabela_simbolos_global = {}
tabela_funcoes = {}

def print_tables():
    label1 = "Nome"
    label2 = "Kind"
    label3 = "Tipo"
    label4 = "Valor de Retorno"
    label5 = "Parametros de entrada"
    label6 = "Corpo da Função"
    label7 = "Valor"
    print("Tabela de Simbolos:")
    print(f"{label1:10} | {label2:8} | {label3:7} | {label7}")
    for name, info in tabela_simbolos_global.items():
        print(f"{name:10} | {info['kind']:8} | {info['type']:7} | {info['value']}")
    
    print()
    print("Tabela de Funções:")
    print(f"{label1:10} | {label4:14} | {label5:38} | {label6}")
    for name, info in tabela_funcoes.items():
        print(f"{name:10} | {info['return_type']:16} | {str(info['parameters']):38} | {info['func_body']}")
    print()

### Handlers

def handle_writeln(output):
    if isinstance(output, tuple):
        print(output)
        # TODO estou a assumir que é um binop não vai dar caso não seja
        lines = handle_binop(output[1])
        lines.append('// write\nWRITEI\n') 
    else:  # senão for tuple é sinal que é uma string
        lines = [
            '// write',
            f'PUSHS "{output}"',
            'WRITES',
            'WRITELN\n'
        ]
    return lines

def handle_write(output):
    if isinstance(output, tuple):
        print(output)
        # TODO estou a assumir que é um binop não vai dar caso não seja
        lines = handle_binop(output[1])
        lines.append('// write\nWRITEI\n') 
    else:
        lines = [
            '// write',
            f'PUSHS "{output}"',
            'WRITES',
            'WRITELN\n'
        ]
    return lines

def handle_assign(var, value):
    global free_fp
    my_fp = free_fp
    free_fp += 1
    tabela_simbolos_global[var]['value'] = value
    tabela_simbolos_global[var]['fp'] = my_fp
    
    # print_tables()
    # print(tabela_simbolos_global[var]['fp'])

    push = tipo_de_push[tabela_simbolos_global[var]['type']]

    lines = [
        f'// assign {value} to {var}',
        f'{push} {value}',
        f'STOREL {my_fp}\n'
    ]

    return lines

def handle_binop(binop):
    op_type = binop['type']
    left_operand = binop['left']
    right_operand = binop['right']

    lines = []
    # TODO por enquanto está a assumir que os binops só vao ter numeros e estão na tabela vai ter de se mudar
    if op_type == '+':
        lines = [
            f'// binop +',
            f'PUSHL {tabela_simbolos_global[left_operand]['fp']}', 
            f'PUSHL {tabela_simbolos_global[right_operand]['fp']}\nADD\n'
        ]
    elif op_type == '-':
        lines = [
            f'// binop -',
            f'PUSHL {tabela_simbolos_global[left_operand]['fp']}',
            f'PUSHL {tabela_simbolos_global[right_operand]['fp']}\nSUB\n'
        ]
    elif op_type == '*':
        lines = [
            f'// binop *',
            f'PUSHL {tabela_simbolos_global[left_operand]['fp']}',
            f'PUSHL {tabela_simbolos_global[right_operand]['fp']}\nMUL\n'
        ]
    elif op_type == '/':
        lines = [	
            f'// binop /',
            f'PUSHL {tabela_simbolos_global[left_operand]['fp']}',
            f'PUSHL {tabela_simbolos_global[right_operand]['fp']}\nDIV\n'
        ]
    else:
        return f"; Unsupported operation: {op_type}"
    
    return lines


instruction_handlers = {
    'writeln': handle_writeln,
    'write': handle_write,
    'assign': handle_assign,
    'binop': handle_binop,
    # Add other instruction types here
}

### Basic structure functions

def create_symbol_table(consts, functions, var_decl):
    if consts:
        for kind, const_content in consts:
            if kind == 'const':
                const_name = const_content['name']
                const_value = const_content['value']
                tabela_simbolos_global[const_name] = {
                    'kind': 'const',
                    'type': conversor_tipos.get(type(const_value).__name__, type(const_value).__name__),
                    'value': const_value,
                    'gp' : '',
                    'fp' : ''
                }

    if var_decl and var_decl[0] == 'var_decl_lines':
        for decl in var_decl[1]:
            vars_list = decl[0][1] 
            var_type = decl[1][1] 
            for var in vars_list:
                tabela_simbolos_global[var] = {
                    'kind': 'var',
                    'type': var_type,
                    'value': '',
                    'gp' : '',
                    'fp' : ''
                }

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
                'type': return_type,
                'value': ''
            }

            tabela_funcoes[func_name] = {
                'return_type': return_type,
                'parameters': parameters,
                'func_body': body
            }

    print_tables()

def read_main_code(instructions):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        f.write("START\n\n")
        print("Converter Pascal para Assembly:")
        print(instructions)

        for instr in instructions:
            instr_type = instr[0]
            handler = instruction_handlers.get(instr_type)

            if handler:
                lines = handler(*instr[1:])  # Should return a list of strings
                for line in lines:
                    print(line)
                    f.write(line + '\n')
            else:
                msg = f"; Unsupported instruction: {instr_type}"
                print(msg)

        f.write("STOP\n")

################################################################

data1 = """
('program', {'program_name': 'Maior3', 'program_body': {'var_declaration': ('var_decl_lines', [(('vars', ['num1', 'num2', 'num3', 'maior']), ('type', 'Integer')), (('vars', ['bol1', 'bol2']), ('type', 'Boolean'))]), 'program_code': ('compound', [('writeln', 'Ola, Mundo!'),('writeln', 'Adeus, Mundo!')])}})
"""

data5 = """
('program', {'program_name': 'Maior3', 'program_body': {'var_declaration': ('var_decl_lines', [(('vars', ['num1', 'num2', 'num3', 'maior']), ('type', 'Integer')), (('vars', ['bol1', 'bol2']), ('type', 'Boolean'))]), 'program_code': ('compound', [('assign', 'num1', 5), ('assign', 'num2', 7), ('write', ('binop', {'type': '+', 'left': 'num1', 'right': 'num2'}))])}})"""

def main():
    ast_tree = ast.literal_eval(data5)

    _, program_data = ast_tree
    body = program_data["program_body"]
    consts = body.get("consts", [])
    functions = body.get("functions", [])
    var_decl = body.get("var_declaration", ())
    code_tuple = body.get("program_code", ())

    create_symbol_table(consts, functions, var_decl)

    read_main_code(code_tuple[1])

    
if __name__ == "__main__":
    main()