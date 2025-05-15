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
    'float': 'PUSHF',
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
    lines = evaluate_expression(output)
    lines.append('\t// writeln')
    print("aqui" ,output)
    # TODO forma de descobrir o tipo de write que é preciso
    if isinstance(output, str):
        var_type = 'string'
    elif isinstance(output, (int, float)):
        var_type = 'integer' if isinstance(output, int) else 'float'
    else:
        var_type = 'integer'  # assume literal string or fallback

    if var_type.lower() == 'string':
        lines.append('\tWRITES')
    else:
        lines.append('\tWRITEI')  # default for numeric values (you can customize for float)
    
    lines.append('\tWRITELN\n')
    return lines

def handle_write(output):
    lines = evaluate_expression(output)
    lines.append('\t// write')
    print("aqui" ,output)
    print_tables()
    # TODO forma de descobrir o tipo de write que é preciso
    if isinstance(output, str) and output in tabela_simbolos_global:
        var_type = tabela_simbolos_global[output].get('type', 'string')
    elif isinstance(output, (int, float)):
        var_type = 'integer' if isinstance(output, int) else 'float'
    else:
        var_type = 'integer'  # assume literal string or fallback

    if var_type.lower() == 'string':
        lines.append('\tWRITES')
    else:
        lines.append('\tWRITEI')  # default for numeric values (you can customize for float)
    
    lines.append('\tWRITELN\n')
    return lines

def handle_assign(var, value):  # passar o atributo que diz se é main ou func
    global free_gp
    my_gp = free_gp
    free_gp += 1

    tabela_simbolos_global[var]['value'] = value
    tabela_simbolos_global[var]['gp'] = my_gp
    
    expr_lines = evaluate_expression(value, var)

    lines = [
        f'\t// assign {value} to {var}',
        *expr_lines,
        f'\tSTOREL {my_gp}\n'
    ]

    return lines

def handle_binop(input):
    update_value = None
    left_value = None
    right_value = None
    if(isinstance(input, tuple)):
        #print(input[0])
        #print(input[1]) # value where it is going to be assigned
        binop = input[0]
        update_value = input[1]
    else:
        binop = input

    expr_lines = evaluate_expression(binop)
    print(expr_lines)

    op_type = binop['type']
    left_operand = binop['left']
    right_operand = binop['right']

    lines = []
    if op_type == '+':
        print(op_type)
        lines.append(f'\t// binop +')
        print("lines", lines)
    elif op_type == '-':
        lines.append(f'\t// binop -')
    elif op_type == '*':
        lines.append(f'\t// binop *')
    elif op_type == '/':
        lines.append(f'\t// binop /')
    else:
        return f"; Unsupported operation: {op_type}"
    
    left_push = None
    left_type = None
    if left_operand in tabela_simbolos_global:
        if update_value is not None: 
            left_value = tabela_simbolos_global[left_operand]['value']
        left_push = tabela_simbolos_global[left_operand]['gp']
        left_type = 'PUSHL'
    elif tabela_simbolos_global[update_value]['kind'] == 'function':
        func_params = tabela_funcoes[update_value]['parameters']
        for param in func_params:
            if left_operand == param[0]:
                left_push = param[2]
            left_type = 'PUSHL'
    else:
        if isinstance(left_operand, int): 
            left_push = left_operand
            left_type = tipo_de_push['integer']
        elif isinstance(left_operand, float):  
            left_push = left_operand
            left_type = tipo_de_push['float']
        elif isinstance(left_operand, str):  
            if left_operand.isdigit():  
                left_push = int(left_operand)
                left_type = tipo_de_push['integer']
            else:
                try:
                    float_value = float(left_operand)  
                    left_push = float_value
                    left_type = tipo_de_push['float']
                except ValueError:
                    left_push = left_operand
                    left_type = tipo_de_push['string']

    right_push = None
    right_type = None
    if right_operand in tabela_simbolos_global:
        if update_value is not None: 
            right_value = tabela_simbolos_global[right_operand]['value']
        right_push = tabela_simbolos_global[right_operand]['gp']
        right_type = 'PUSHL'
    elif tabela_simbolos_global[update_value]['kind'] == 'function':
        func_params = tabela_funcoes[update_value]['parameters']
        for param in func_params:
            if right_operand == param[0]:
                right_push = param[2]
            right_type = 'PUSHL'
        update_value = None
    else:
        if isinstance(right_operand, int):  
            right_push = right_operand
            right_type = tipo_de_push['integer']
        elif isinstance(right_operand, float): 
            right_push = right_operand
            right_type = tipo_de_push['float']
        elif isinstance(right_operand, str):  
            if right_operand.isdigit(): 
                right_push = int(right_operand)
                right_type = tipo_de_push['integer']
            else:
                try:
                    float_value = float(right_operand)  
                    right_push = float_value
                    right_type = tipo_de_push['float']
                except ValueError:
                    right_push = right_operand
                    right_type = tipo_de_push['string']
        
    lines.append(f'\t{left_type} {left_push}')
    lines.append(f'\t{right_type} {right_push}')

    if left_value is None:
        left_value = left_push
    if right_value is None:
        right_value = right_push

    if op_type == '+':
        if update_value is not None: 
            tabela_simbolos_global[update_value]['value'] = left_value + right_value
        lines.append('\tADD\n')
    elif op_type == '-':
        if update_value is not None: 
            tabela_simbolos_global[update_value]['value'] = left_value - right_value
        lines.append('\tSUB\n')
    elif op_type == '*':        
        if update_value is not None: 
            tabela_simbolos_global[update_value]['value'] = left_value * right_value
        lines.append('\tMUL\n')
    elif op_type == '/':        
        if update_value is not None: 
            tabela_simbolos_global[update_value]['value'] = left_value / right_value
        lines.append('\tDIV\n')
    else:
        return f"; Unsupported operation: {op_type}"

    # print_tables()
    return lines

# TODO assumir que ord vai ser sempre um char ou uma var
def handle_ord(ord_input):
    lines = ['\t// ord']
    input_value = None
    update_value = None
    if(isinstance(ord_input, tuple)):
        #print(ord_input[0])
        #print(ord_input[1]) value where it is going to be assigned
        input_value = ord_input[0]
        update_value = ord_input[1]
        if ord_input[0] in tabela_simbolos_global:
            input_value = tabela_simbolos_global[ord_input[0]]['value']
    else:
        input_value = ord_input
        if ord_input in tabela_simbolos_global:
            input_value = tabela_simbolos_global[ord_input]['value']

    output = ord(input_value)

    if update_value is not None:
        tabela_simbolos_global[update_value]['value'] = output

    lines.append(f'\tPUSHI {output}')
    # print_tables()
    return lines

def handle_function_call(input):
    func_name = input["name"].lower()
    params = input["args"]
    lines = [f'\t// Call da {func_name} com os parametros {params}']


    for param in params:
        if param in tabela_simbolos_global:
            mygp = tabela_simbolos_global[param]['gp']
            lines.append(f'\tPUSHL {mygp}')
        elif isinstance(param, int): 
            lines.append(f'\tPUSHI {param}')
        elif isinstance(param, float): 
            lines.append(f'\tPUSHF {param}')
        else:
            lines.append(f'\tPUSHS {param}')

    lines.append(f'\tPUSHA {func_name}\n\tCALL')
    return lines

def handle_return(func_name, return_input):
    expr_lines = evaluate_expression(return_input, None, func_name)
    lines = expr_lines
    lines.append(f'\tRETURN\n')
    return lines

instruction_handlers = {
    'writeln': handle_writeln,
    'write': handle_write,
    'assign': handle_assign,
    'binop': handle_binop,
    'ord': handle_ord,
    'return': handle_return,
    'Function_call': handle_function_call,
    # Add other instruction types here
}

def evaluate_expression(expr, isAssign=None, isFunc=None):
    if isinstance(expr, tuple):
        instr_type = expr[0]
        args = expr[1:]
        if(isAssign is not None and instr_type in ['binop', 'ord']):
            args = (*args, isAssign)
        elif(isFunc is not None):
            args = (*args, isFunc)
        elif len(expr[1:]) == 1:
            args = args[0]
        handler = instruction_handlers.get(instr_type)
        print(len(expr[1:]))
        return handler(args) if handler else [f"// Unsupported expression: {instr_type}"]

    if isinstance(expr, str) and expr in tabela_simbolos_global:
        var_info = tabela_simbolos_global[expr]
        var_type = var_info.get('type', 'string')
        push_instr = tipo_de_push.get(var_type, 'PUSHS')
        return [f'{push_instr} {expr}'] if push_instr == 'PUSHS' else [f'{push_instr}L {var_info["fp"]}']

    # Literal values
    if isinstance(expr, int):
        return ['\tPUSHI ' + str(expr)]
    elif isinstance(expr, float):
        return ['\tPUSHL ' + str(expr)]
    elif isinstance(expr, str):
        return [f'\tPUSHS "{expr}"']

    return [f"// Unhandled expression type: {expr}"]

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
            fp = -len(raw_parameters)
            for (vars_tuple, type_tuple) in raw_parameters:
                var_names = vars_tuple[1]
                var_type = type_tuple[1]
                myfp = fp
                fp += 1 
                for var in var_names:
                    parameters.append((var, var_type, myfp))

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

def convert_func(func):
    func_name = func[0]
    func_lines = [f'{func_name.lower()}:']

    func_instructions = func[1]
    for instr in func_instructions:
        instr_type = instr[0]
        args = instr[1:]
        if(instr_type == 'assign' and args[0] == func_name):
            instr_type = 'return'

        handler = instruction_handlers.get(instr_type)

        if handler:
            lines = handler(*args)  # Should return a list of strings
            for line in lines:
                print(line)
                func_lines.append(line)
        else:
            msg = f"; Unsupported instruction: {instr_type}"
            print(msg)
    return func_lines

def read_code(func_instructions, main_instructions):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        f.write("JUMP main\n\n")
        print(func_instructions)
        if len(func_instructions) > 0:
            for func in func_instructions:
                lines = convert_func(func)
                if len(lines) > 0:
                    for line in lines:
                        print(line)
                        f.write(line + '\n')
                else:
                    msg = f"; Unsupported instruction: {instr_type}"
                    print(msg)

        f.write("\nmain:\n\tSTART\n\n")
        print("Converter Pascal para Assembly:")
        print(main_instructions)

        for instr in main_instructions:
            instr_type = instr[0]
            args = instr[1:]
            handler = instruction_handlers.get(instr_type)

            if handler:
                lines = handler(*args)  # Should return a list of strings
                for line in lines:
                    print(line)
                    f.write(line + '\n')
            else:
                msg = f"; Unsupported instruction: {instr_type}"
                print(msg)

        f.write("\tSTOP\n")

################################################################

data1 = """
('program', {'program_name': 'Maior3', 'program_body': {'var_declaration': ('var_decl_lines', [(('vars', ['num1', 'num2', 'num3', 'maior']), ('type', 'Integer')), (('vars', ['bol1', 'bol2']), ('type', 'Boolean'))]), 'program_code': ('compound', [('writeln', 'Ola, Mundo!'),('writeln', 'Adeus, Mundo!')])}})
"""

data5 = """
('program', {'program_name': 'Maior3', 'program_body': {'var_declaration': ('var_decl_lines', [(('vars', ['num1', 'num2', 'num3', 'maior']), ('type', 'Integer')), (('vars', ['bol1', 'bol2']), ('type', 'Boolean'))]), 'program_code': ('compound', [('assign', 'num1', 5), ('assign', 'num2', 7), ('write', ('binop', {'type': '+', 'left': 'num1', 'right': 'num2'}))])}})"""

data6 = """
('program', {'program_name': 'Maior3', 'program_body': {'var_declaration': ('var_decl_lines', [(('vars', ['num1', 'num2', 'num3', 'maior']), ('type', 'Integer')), (('vars', ['bol1', 'bol2']), ('type', 'Boolean'))]), 'program_code': ('compound', [('assign', 'num2', 7), ('assign', 'num1', ('binop', {'type': '+', 'left': 5, 'right': 'num2'})), ('write', ('binop', {'type': '+', 'left': 'num1', 'right': 'num2'}))])}})
"""

data7 = """
('program', {'program_name': 'OrdCharExample', 'program_body': {'var_declaration': ('var_decl_lines', [(('vars', ['ch']), ('type', 'string')), (('vars', ['code']), ('type', 'integer'))]), 'program_code': ('compound', [('assign', 'ch', 'A'), ('assign', 'code', ('ord', 'ch')), ('write', ['The ASCII code of ', 'ch', ' is ', 'code'])])}})
"""

data8 = """
('program', {'program_name': 'SumExample', 'program_body': {'functions': [('function', {'name': 'Add', 'parameters': [(('vars', ['a']), ('type', 'integer')), (('vars', ['b']), ('type', 'integer'))], 'return_type': 'integer', 'body': ('compound', [('assign', 'Add', ('binop', {'type': '+', 'left': 'a', 'right': 'b'}))])})], 'var_declaration': ('var_decl_lines', [(('vars', ['num1', 'num2', 'result']), ('type', 'integer'))]), 'program_code': ('compound', [('assign', 'num1', 5), ('assign', 'num2', 3), ('assign', 'result', ('Function_call', {'name': 'Add', 'args': ['num1', 'num2']})), ('write', ['result'])])}})
"""

def main():
    ast_tree = ast.literal_eval(data8)

    _, program_data = ast_tree
    body = program_data["program_body"]
    consts = body.get("consts", [])
    functions = body.get("functions", [])
    var_decl = body.get("var_declaration", ())
    code_tuple = body.get("program_code", ())

    create_symbol_table(consts, functions, var_decl)

    functions_body = []
    for function in functions:
        func_name = function[1]['name']
        func_body = function[1]['body'][1]
        functions_body.append((func_name, func_body))

    read_code(functions_body, code_tuple[1])

if __name__ == "__main__":
    main()