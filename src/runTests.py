import subprocess
import sys
import os

from lexer import lexer
from parser import parser
from semantics import runSemantics

test_files = [
    "./testes/teste1.pp",
    "./testes/teste2.pp",
    "./testes/teste3.pp",
    "./testes/teste4.pp",
    "./testes/teste5.pp",
    "./testes/teste6.pp",
    "./testes/teste7.pp",
    "./testes/teste8.pp",
]

lexer_dir = "outputsLexer"
parser_dir = "outputsParser"
semantics_dir = "outputsSemantics"

def main():
    #text = "Menu to run the tests provided"  
    exit = startTests = False
    runTests = [False, False, False, False, False, False, False, False]

    while not exit:
        while not startTests:
            print("Selecione os testes pretende correr:")
            for i in range(8):
                if runTests[i]:
                    print(f" {i+1}: O teste {i+1} está selecionado;")
                else:
                    print(f" {i+1}: O teste {i+1} não está selecionado;")
            print(" 9: Selecionar todos os testes;")
            print(" 10: Desselecionar todos os testes;")
            print("11: Correr os testes selecionados.")
            option = input("> ")

            try:
                option = int(option)

                if 0 <= option < 9:
                    option -= 1
                    runTests[option] = not runTests[option] 
                elif option == 9:
                    for i in range(8):
                        runTests[i] = True
                elif option == 10:
                    for i in range(8):
                        runTests[i] = False
                elif option == 11:
                    if any(runTests):
                        startTests = True
                    else:
                        print("Selecione pelo menos 1 teste para correr.")
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Por favor, insira um número.")     

            print()
        
        for i in range(8): 
            if runTests[i]:
                print(f"Teste {i+1}...")
                input_file = open(test_files[i], 'r')
                lexer_input = input_file.read()
                lexer.input(lexer_input)

                tokens = []
                lexer_clone = lexer.clone() 
                for tok in lexer_clone:
                    tokens.append(f"{tok.type}({tok.value}) at line {tok.lineno}, position {tok.lexpos}")

                lexer_output_file = f'{lexer_dir}/test{i+1}output.txt'
                os.makedirs(os.path.dirname(lexer_output_file), exist_ok=True)
                with open(lexer_output_file, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(tokens))

                parser_output = parser.parse(lexer=lexer, debug=True)

                parser_output_file = f'{parser_dir}/test{i+1}output.txt'
                os.makedirs(os.path.dirname(parser_output_file), exist_ok=True)
                with open(parser_output_file, 'w', encoding='utf-8') as f:
                        f.write(str(parser_output))

                semantics_output_file = f'{semantics_dir}/test{i+1}output.txt'
                runSemantics(parser_output, semantics_output_file)


            print("-" * 40)
        
        print()
        print()
        print("Selecione a opção: ")
        print("1: Sair;")
        print("2: Voltar a correr os mesmos testes;")
        print("3: Selecionar novos testes para correr.")
        while True:
            option2 = input("> ")

            try:
                option2 = int(option2)

                if option2 == 1:
                    exit = True
                    break
                elif option2 == 2:
                    startTests = True
                    break
                elif option2 == 3:
                    startTests = False
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Por favor, insira um número.")

    print()


if __name__ == "__main__":
    main()
