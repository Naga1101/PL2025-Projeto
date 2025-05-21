import ast

import os
## Global vars

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
    try:
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
    except Exception as e:
        print("Erro ao imprimir as tabelas de simbolos e funcoes:", e)

### Handlers

def handle_writeln(output):
    lines = evaluate_expression(output)
    lines.append('\t// writeln')

    if isinstance(output, list):
        for item in output:
            lines.extend(process_write_item(item))
    else:
        lines.extend(process_write_item(output))

    lines.append('\tWRITELN\n')
    return lines

def handle_write(output):
    lines = evaluate_expression(output)
    lines.append('\t// write')
    print("aqui" ,output)
    print_tables()
    # TODO forma de descobrir o tipo de write que é preciso
    if isinstance(output, list):
        for item in output:
            lines.extend(process_write_item(item))
    else:
        lines.extend(process_write_item(output))
    return lines

def process_write_item(item):
    lines = []

    # Se for variável conhecida
    if isinstance(item, str) and item in tabela_simbolos_global:
        var_info = tabela_simbolos_global[item]
        var_type = var_info['type']
        gp = var_info.get('gp')

        if var_type == 'boolean':
            # Load valor booleano da memória
            lines.append(f'\tPUSHL {gp}')
            # Se for 0 escreve 'false', se for 1 escreve 'true'
            lines.append('\tDUP 1')
            lines.append('\tPUSHI 0')
            lines.append('\tEQUAL')
            lines.append('\tJZ label_true')
            lines.append('\tPUSHS "false"')
            lines.append('\tWRITES')
            lines.append('\tJUMP label_endbool')
            lines.append('label_true:')
            lines.append('\tPUSHS "true"')
            lines.append('\tWRITES')
            lines.append('label_endbool:')
        elif var_type == 'integer':
            lines.append(f'\tPUSHL {gp}')
            lines.append('\tWRITEI')
        elif var_type == 'float':
            lines.append(f'\tPUSHL {gp}')
            lines.append('\tWRITEF')
        elif var_type == 'string':
            lines.append(f'\tPUSHL {gp}')
            lines.append('\tWRITES')

    # Literal booleano direto (True/False)
    elif isinstance(item, bool):
        str_val = 'true' if item else 'false'
        lines.append(f'\tPUSHS "{str_val}"')
        lines.append('\tWRITES')

    # Literal string
    elif isinstance(item, str):
        lines.append(f'\tPUSHS "{item}"')
        lines.append('\tWRITES')

    # Literal inteiro
    elif isinstance(item, int):
        lines.append(f'\tPUSHI {item}')
        lines.append('\tWRITEI')

    # Literal float
    elif isinstance(item, float):
        lines.append(f'\tPUSHF {item}')
        lines.append('\tWRITEF')

    # Expressão complexa (ex: binop, função, etc)
    else:
        expr_lines = evaluate_expression(item)
        lines.extend(expr_lines)
        lines.append('\tWRITEI')

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
    elif op_type == 'div':
        lines.append(f'\t// binop div')
    elif op_type == 'mod':
        lines.append(f'\t// binop mod')
    elif op_type == 'and':
        lines.append(f'\t// binop and')
    elif op_type == 'or':
        lines.append(f'\t// binop or')
    elif op_type == '>':
        lines.append(f'\t// binop >')
    elif op_type == '<':
        lines.append(f'\t// binop <')
    elif op_type == '>=':
        lines.append(f'\t// binop >=')
    elif op_type == '<=':
        lines.append(f'\t// binop <=')
    elif op_type == '=':
        lines.append(f'\t// binop =')
    elif op_type == '<>':
        lines.append(f'\t// binop <>')
    else:
        return f"; Unsupported operation: {op_type}"
    
    left_push = None
    left_type = None
    if left_operand in tabela_simbolos_global:
        if update_value is not None: 
            left_value = tabela_simbolos_global[left_operand]['value']
        type =  tabela_simbolos_global[left_operand]['type']
        left_push = tabela_simbolos_global[left_operand]['gp']
        left_type = 'PUSHL'
    elif tabela_simbolos_global[update_value]['kind'] == 'function':
        func_params = tabela_funcoes[update_value]['parameters']
        for param in func_params:
            if left_operand == param[0]:
                left_push = param[2]
            type =  param[1]
            left_type = 'PUSHL'
    else:
        if isinstance(left_operand, int): 
            left_push = left_operand
            type = 'integer'
            left_type = tipo_de_push['integer']
        elif isinstance(left_operand, float):  
            left_push = left_operand
            type = 'float'
            left_type = tipo_de_push['float']
        elif isinstance(left_operand, str):  
            if left_operand.isdigit():  
                left_push = int(left_operand)
                left_type = tipo_de_push['integer']
                type = 'integer'
            else:
                try:
                    float_value = float(left_operand)  
                    left_push = float_value
                    left_type = tipo_de_push['float']
                    type = 'float'
                except ValueError:
                    left_push = left_operand
                    left_type = tipo_de_push['string']
                    type = 'string'

    right_push = None
    right_type = None
    if right_operand in tabela_simbolos_global:
        print(tabela_simbolos_global[right_operand])
        if update_value is not None: 
            right_value = tabela_simbolos_global[right_operand]['value']
        right_push = tabela_simbolos_global[right_operand]['gp']
        right_type = 'PUSHL'
        if type != 'float' and tabela_simbolos_global[right_operand]['type'] == 'float':
            type =  'float'
    elif tabela_simbolos_global[update_value]['kind'] == 'function':
        func_params = tabela_funcoes[update_value]['parameters']
        for param in func_params:
            if right_operand == param[0]:
                right_push = param[2]
            if type != 'float':
                type =  param[1]
            right_type = 'PUSHL'
        update_value = None
    else:
        if isinstance(right_operand, int):  
            right_push = right_operand
            right_type = tipo_de_push['integer']
        elif isinstance(right_operand, float):
            if type != 'float':
                type =  'float'
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
                    if type != 'float':
                        type =  param[1]
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
        if type == 'integer': 
            lines.append('\tADD\n')
        elif type == 'float':
            lines.append('\tFADD\n')
    elif op_type == '-':
        if update_value is not None: 
            tabela_simbolos_global[update_value]['value'] = left_value - right_value
        if type == 'integer': 
            lines.append('\tSUB\n')
        elif type == 'float':
            lines.append('\tFSUB\n')
    elif op_type == '*':        
        if update_value is not None: 
            tabela_simbolos_global[update_value]['value'] = left_value * right_value
        if type == 'integer': 
            lines.append('\tMUL\n')
        elif type == 'float':
            lines.append('\tFMUL\n')
    elif op_type == 'div':        
        if update_value is not None: 
            tabela_simbolos_global[update_value]['value'] = left_value / right_value
        if type == 'integer': 
            lines.append('\tDIV\n')
        elif type == 'float':
            lines.append('\tFDIV\n')
    elif op_type == 'mod':        
        if update_value is not None: 
            tabela_simbolos_global[update_value]['value'] = left_value % right_value
        lines.append('\tMOD\n')
    elif op_type == 'and':
        if update_value is not None: 
            tabela_simbolos_global[update_value]['value'] = left_value and right_value
        lines.append('\tAND\n')
    elif op_type == 'or':
        if update_value is not None: 
            tabela_simbolos_global[update_value]['value'] = left_value or right_value
        lines.append('\tOR\n')
    elif op_type == '>':
        if update_value is not None: 
            tabela_simbolos_global[update_value]['value'] = left_value > right_value
        if type == 'integer':
            lines.append('\tSUP\n')
        elif type == 'float':
            lines.append('\tFSUP\n')
    elif op_type == '<':
        if update_value is not None: 
            tabela_simbolos_global[update_value]['value'] = left_value < right_value
        if type == 'integer':
            lines.append('\tINF\n')
        elif type == 'float':
            lines.append('\tFINF\n')
    elif op_type == '>=':
        if update_value is not None: 
            tabela_simbolos_global[update_value]['value'] = left_value >= right_value
        if type == 'integer':
            lines.append('\tSUPEQ\n')
        elif type == 'float':
            lines.append('\tFSUPEQ\n')
    elif op_type == '<=':
        if update_value is not None: 
            tabela_simbolos_global[update_value]['value'] = left_value <= right_value
        if type == 'integer':
            lines.append('\tINFEQ\n')
        elif type == 'float':
            lines.append('\tFINFEQ\n')
    elif op_type == '=':
        if update_value is not None: 
            tabela_simbolos_global[update_value]['value'] = left_value == right_value
        lines.append('\tEQUAL\n')
    elif op_type == '<>':
        if update_value is not None: 
            tabela_simbolos_global[update_value]['value'] = left_value != right_value
        lines.append('\tEQUAL')
        lines.append('\tNOT\n')
    else:
        return f"; Unsupported operation: {op_type}"

    print_tables()
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
    elif isinstance(expr, list):
        return []

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

def read_code(func_instructions, main_instructions, output_file):
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
[
  "program",
  {
    "program_name": "TesteBinOp",
    "program_body": {
      "functions": [
        [
          "function",
          {
            "name": "SomaF",
            "parameters": [
              [
                [
                  "vars",
                  [
                    "soma"
                  ]
                ],
                [
                  "type",
                  "float"
                ]
              ]
            ],
            "return_type": "float",
            "body": [
              "compound",
              [
                [
                  "assign",
                  "SomaF",
                  [
                    "binop",
                    {
                      "type": "+",
                      "left": 10,
                      "right": 2.3
                    }
                  ]
                ]
              ]
            ]
          }
        ],
        [
          "function",
          {
            "name": "SubF",
            "parameters": [
              [
                [
                  "vars",
                  [
                    "soma"
                  ]
                ],
                [
                  "type",
                  "float"
                ]
              ]
            ],
            "return_type": "float",
            "body": [
              "compound",
              [
                [
                  "assign",
                  "SubF",
                  [
                    "binop",
                    {
                      "type": "-",
                      "left": 23,
                      "right": "soma"
                    }
                  ]
                ]
              ]
            ]
          }
        ],
        [
          "function",
          {
            "name": "MultF",
            "parameters": [
              [
                [
                  "vars",
                  [
                    "soma"
                  ]
                ],
                [
                  "type",
                  "float"
                ]
              ]
            ],
            "return_type": "float",
            "body": [
              "compound",
              [
                [
                  "assign",
                  "MultF",
                  [
                    "binop",
                    {
                      "type": "*",
                      "left": 3,
                      "right": 7.6
                    }
                  ]
                ]
              ]
            ]
          }
        ],
        [
          "function",
          {
            "name": "DivF",
            "parameters": [
              [
                [
                  "vars",
                  [
                    "soma"
                  ]
                ],
                [
                  "type",
                  "float"
                ]
              ]
            ],
            "return_type": "float",
            "body": [
              "compound",
              [
                [
                  "assign",
                  "DivF",
                  [
                    "binop",
                    {
                      "type": "div",
                      "left": 2.754,
                      "right": 3.5
                    }
                  ]
                ]
              ]
            ]
          }
        ],
        [
          "function",
          {
            "name": "Igual",
            "parameters": [
              [
                [
                  "vars",
                  [
                    "a"
                  ]
                ],
                [
                  "type",
                  "boolean"
                ]
              ]
            ],
            "return_type": "boolean",
            "body": [
              "compound",
              [
                [
                  "assign",
                  "Igual",
                  [
                    "binop",
                    {
                      "type": "=",
                      "left": 12,
                      "right": 21
                    }
                  ]
                ]
              ]
            ]
          }
        ],
        [
          "function",
          {
            "name": "Diferente",
            "parameters": [
              [
                [
                  "vars",
                  [
                    "a"
                  ]
                ],
                [
                  "type",
                  "boolean"
                ]
              ]
            ],
            "return_type": "boolean",
            "body": [
              "compound",
              [
                [
                  "assign",
                  "Diferente",
                  [
                    "binop",
                    {
                      "type": "<>",
                      "left": 32,
                      "right": 2
                    }
                  ]
                ]
              ]
            ]
          }
        ],
        [
          "function",
          {
            "name": "Menor",
            "parameters": [
              [
                [
                  "vars",
                  [
                    "a"
                  ]
                ],
                [
                  "type",
                  "boolean"
                ]
              ]
            ],
            "return_type": "boolean",
            "body": [
              "compound",
              [
                [
                  "assign",
                  "Menor",
                  [
                    "binop",
                    {
                      "type": "<",
                      "left": 90,
                      "right": 110
                    }
                  ]
                ]
              ]
            ]
          }
        ],
        [
          "function",
          {
            "name": "Maior",
            "parameters": [
              [
                [
                  "vars",
                  [
                    "a"
                  ]
                ],
                [
                  "type",
                  "boolean"
                ]
              ]
            ],
            "return_type": "boolean",
            "body": [
              "compound",
              [
                [
                  "assign",
                  "Maior",
                  [
                    "binop",
                    {
                      "type": ">",
                      "left": 1,
                      "right": 0
                    }
                  ]
                ]
              ]
            ]
          }
        ],
        [
          "function",
          {
            "name": "MenorIgual",
            "parameters": [
              [
                [
                  "vars",
                  [
                    "a"
                  ]
                ],
                [
                  "type",
                  "boolean"
                ]
              ]
            ],
            "return_type": "boolean",
            "body": [
              "compound",
              [
                [
                  "assign",
                  "MenorIgual",
                  [
                    "binop",
                    {
                      "type": "<=",
                      "left": 0.0,
                      "right": 0.0
                    }
                  ]
                ]
              ]
            ]
          }
        ],
        [
          "function",
          {
            "name": "MaiorIgual",
            "parameters": [
              [
                [
                  "vars",
                  [
                    "a"
                  ]
                ],
                [
                  "type",
                  "boolean"
                ]
              ]
            ],
            "return_type": "boolean",
            "body": [
              "compound",
              [
                [
                  "assign",
                  "MaiorIgual",
                  [
                    "binop",
                    {
                      "type": ">=",
                      "left": 12,
                      "right": 9
                    }
                  ]
                ]
              ]
            ]
          }
        ],
        [
          "function",
          {
            "name": "Conjuncao",
            "parameters": [
              [
                [
                  "vars",
                  [
                    "a"
                  ]
                ],
                [
                  "type",
                  "boolean"
                ]
              ]
            ],
            "return_type": "boolean",
            "body": [
              "compound",
              [
                [
                  "assign",
                  "Conjuncao",
                  [
                    "binop",
                    {
                      "type": "and",
                      "left": 0,
                      "right": 1
                    }
                  ]
                ]
              ]
            ]
          }
        ],
        [
          "function",
          {
            "name": "Disjuncao",
            "parameters": [
              [
                [
                  "vars",
                  [
                    "a"
                  ]
                ],
                [
                  "type",
                  "boolean"
                ]
              ]
            ],
            "return_type": "boolean",
            "body": [
              "compound",
              [
                [
                  "assign",
                  "Disjuncao",
                  [
                    "binop",
                    {
                      "type": "or",
                      "left": 0,
                      "right": 1
                    }
                  ]
                ]
              ]
            ]
          }
        ]
      ],
      "var_declaration": [
        "var_decl_lines",
        [
          [
            [
              "vars",
              [
                "b",
                "sF",
                "suF",
                "mF",
                "dF"
              ]
            ],
            [
              "type",
              "float"
            ]
          ],
          [
            [
              "vars",
              [
                "a",
                "b1",
                "b2",
                "b3",
                "b4",
                "b5",
                "b6",
                "b7",
                "b8"
              ]
            ],
            [
              "type",
              "boolean"
            ]
          ]
        ]
      ],
      "program_code": [
        "compound",
        [
          [
            "assign",
            "b",
            1
          ],
          [
            "assign",
            "a",
            1
          ],
          [
            "assign",
            "sF",
            [
              "Function_call",
              {
                "name": "SomaF",
                "args": [
                  "b"
                ]
              }
            ]
          ],
          [
            "assign",
            "suF",
            [
              "Function_call",
              {
                "name": "SubF",
                "args": [
                  "sF"
                ]
              }
            ]
          ],
          [
            "assign",
            "mF",
            [
              "Function_call",
              {
                "name": "MultF",
                "args": [
                  "b"
                ]
              }
            ]
          ],
          [
            "assign",
            "dF",
            [
              "Function_call",
              {
                "name": "DivF",
                "args": [
                  "b"
                ]
              }
            ]
          ],
          [
            "writeln",
            [
              "Soma: ",
              "sF"
            ]
          ],
          [
            "writeln",
            [
              "Subtracao: ",
              "suF"
            ]
          ],
          [
            "writeln",
            [
              "Multiplicacao: ",
              "mF"
            ]
          ],
          [
            "writeln",
            [
              "Divisao: ",
              "dF"
            ]
          ],
          [
            "assign",
            "b1",
            [
              "Function_call",
              {
                "name": "Igual",
                "args": [
                  "a"
                ]
              }
            ]
          ],
          [
            "assign",
            "b2",
            [
              "Function_call",
              {
                "name": "Diferente",
                "args": [
                  "a"
                ]
              }
            ]
          ],
          [
            "assign",
            "b3",
            [
              "Function_call",
              {
                "name": "Menor",
                "args": [
                  "a"
                ]
              }
            ]
          ],
          [
            "assign",
            "b4",
            [
              "Function_call",
              {
                "name": "Maior",
                "args": [
                  "a"
                ]
              }
            ]
          ],
          [
            "assign",
            "b5",
            [
              "Function_call",
              {
                "name": "MenorIgual",
                "args": [
                  "a"
                ]
              }
            ]
          ],
          [
            "assign",
            "b6",
            [
              "Function_call",
              {
                "name": "MaiorIgual",
                "args": [
                  "a"
                ]
              }
            ]
          ],
          [
            "assign",
            "b7",
            [
              "Function_call",
              {
                "name": "Conjuncao",
                "args": [
                  "a"
                ]
              }
            ]
          ],
          [
            "assign",
            "b8",
            [
              "Function_call",
              {
                "name": "Disjuncao",
                "args": [
                  "a"
                ]
              }
            ]
          ],
          [
            "writeln",
            [
              "12 = 21? ",
              "b1"
            ]
          ],
          [
            "writeln",
            [
              "32 <> 2? ",
              "b2"
            ]
          ],
          [
            "writeln",
            [
              "90 < 110? ",
              "b3"
            ]
          ],
          [
            "writeln",
            [
              "1 > 0? ",
              "b4"
            ]
          ],
          [
            "writeln",
            [
              "0.0 <= 0.0? ",
              "b5"
            ]
          ],
          [
            "writeln",
            [
              "12 >= 9? ",
              "b6"
            ]
          ],
          [
            "writeln",
            [
              "0 and 1? ",
              "b7"
            ]
          ],
          [
            "writeln",
            [
              "0 or 1? ",
              "b8"
            ]
          ]
        ]
      ]
    }
  }
]"""
data6 = """
('program', {'program_name': 'Maior3', 'program_body': {'var_declaration': ('var_decl_lines', [(('vars', ['num1', 'num2', 'num3', 'maior']), ('type', 'Integer')), (('vars', ['bol1', 'bol2']), ('type', 'Boolean'))]), 'program_code': ('compound', [('assign', 'num2', 7), ('assign', 'num1', ('binop', {'type': '+', 'left': 5, 'right': 'num2'})), ('write', ('binop', {'type': '+', 'left': 'num1', 'right': 'num2'}))])}})
"""

data7 = """
('program', {'program_name': 'OrdCharExample', 'program_body': {'var_declaration': ('var_decl_lines', [(('vars', ['ch']), ('type', 'string')), (('vars', ['code']), ('type', 'integer'))]), 'program_code': ('compound', [('assign', 'ch', 'A'), ('assign', 'code', ('ord', 'ch')), ('write', ['The ASCII code of ', 'ch', ' is ', 'code'])])}})
"""

data8 = """
('program', {'program_name': 'SumExample', 'program_body': {'functions': [('function', {'name': 'Add', 'parameters': [(('vars', ['a']), ('type', 'integer')), (('vars', ['b']), ('type', 'integer'))], 'return_type': 'integer', 'body': ('compound', [('assign', 'Add', ('binop', {'type': '+', 'left': 'a', 'right': 'b'}))])})], 'var_declaration': ('var_decl_lines', [(('vars', ['num1', 'num2', 'result']), ('type', 'integer'))]), 'program_code': ('compound', [('assign', 'num1', 5), ('assign', 'num2', 3), ('assign', 'result', ('Function_call', {'name': 'Add', 'args': ['num1', 'num2']})), ('write', ['result'])])}})
"""

data10 = """
('program', {'program_name': 'TesteBinOp', 'program_body': {'var_declaration': ('var_decl_lines', [(('vars', ['soma', 'sub', 'mult', 'divi']), ('type', 'integer')), (('vars', ['somaFloat', 'subFloat', 'multFloat', 'diviFloat']), ('type', 'float')), (('vars', ['igual', 'diferente', 'menor', 'maior', 'menorIgual', 'maiorIgual']), ('type', 'boolean')), (('vars', ['conjuncao', 'disjuncao']), ('type', 'boolean'))]), 'program_code': ('compound', [('assign', 'somaFloat', ('binop', {'type': '+', 'left': 10, 'right': 2.3})), ('assign', 'subFloat', ('binop', {'type': '-', 'left': 23, 'right': 'somaFloat'})), ('assign', 'multFloat', ('binop', {'type': '*', 'left': 3, 'right': 7.6})), ('assign', 'diviFloat', ('binop', {'type': '/', 'left': 2.754, 'right': 3.5})), ('assign', 'igual', ('binop', {'type': '=', 'left': 12, 'right': 21})), ('assign', 'diferente', ('binop', {'type': '<>', 'left': 32, 'right': 2})), ('assign', 'menor', ('binop', {'type': '<', 'left': 90, 'right': 110})), ('assign', 'maior', ('binop', {'type': '>', 'left': 1, 'right': 0})), ('assign', 'menorIgual', ('binop', {'type': '<=', 'left': 0.0, 'right': 0.0})), ('assign', 'maiorIgual', ('binop', {'type': '>=', 'left': 12, 'right': 9})), ('assign', 'conjuncao', ('binop', {'type': 'and', 'left': 0, 'right': 1})), ('assign', 'disjuncao', ('binop', {'type': 'or', 'left': 0, 'right': 1}))])}})
"""

def runSemantics(input, outputFileName):
    try:
        ast_tree = input

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

        read_code(functions_body, code_tuple[1], outputFileName)

        global free_fp
        global free_gp
        free_fp = 0
        free_gp = 0
    except Exception as e:
        print(e)
        print("Erro na criação do ficheiro ", outputFileName)

def main():
    ast_tree = ast.literal_eval(data5)

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

    read_code(functions_body, code_tuple[1], "outputsSemantics/output.txt")

if __name__ == "__main__":
    main()