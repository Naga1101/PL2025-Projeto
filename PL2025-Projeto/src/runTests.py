import subprocess
import sys
import os

test_files = [
    "./testes/teste1.pp",
    "./testes/teste2.pp",
    "./testes/teste3.pp",
    "./testes/teste4.pp",
    "./testes/teste5.pp",
    "./testes/teste6.pp",
    "./testes/teste7.pp"
]

expected_result = [ # Pode vir a mudar
    "Ola, Mundo!",
    "O maior é: 9",
    "", # são precisos inputs para estes testes
    "", # são precisos inputs para estes testes
    "", # são precisos inputs para estes testes
    "", # são precisos inputs para estes testes
    ""  # são precisos inputs para estes testes
]

test_inputs = [
    None,                
    "5\n9\n2\n", # input para teste2
    "", # faltam inputs para este teste
    "", # faltam inputs para este teste
    "", # faltam inputs para este teste
    "", # faltam inputs para este teste
    "", # faltam inputs para este teste
    ""  # faltam inputs para este teste
]

def main():
    #text = "Menu to run the tests provided"  
    exit = startTests = False
    runTests = [False, False, False, False, False, False, False]

    while not exit:
        while not startTests:
            print("Selecione os testes pretende correr:")
            for i in range(7):
                if runTests[i]:
                    print(f" {i+1}: O teste {i+1} está selecionado;")
                else:
                    print(f" {i+1}: O teste {i+1} não está selecionado;")
            print(" 8: Selecionar todos os testes;")
            print(" 9: Desselecionar todos os testes;")
            print("10: Correr os testes selecionados.")
            option = input("> ")

            try:
                option = int(option)

                if 0 <= option < 8:
                    option -= 1
                    runTests[option] = not runTests[option] 
                elif option == 8:
                    for i in range(7):
                        runTests[i] = True
                elif option == 9:
                    for i in range(7):
                        runTests[i] = False
                elif option == 10:
                    if any(runTests):
                        startTests = True
                    else:
                        print("Selecione pelo menos 1 teste para correr.")
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Por favor, insira um número.")     

            print()
        
        for i in range(7): # Atualmente não testa nada sendo que esta estrutura pode mudar
            if runTests[i]:
                print(f"Teste {i+1}...")

                process = subprocess.run(
                    ["python", "nome_do_ficheiro_que_vai_correr_o_codigo", test_files[i]],  # Chamar o interpretador do codigo aqui
                    input=test_inputs[i],
                    capture_output=True,
                    text=True
                )

                output_lines = process.stdout.strip().splitlines()

                filtered_output = "\n".join(
                    line for line in output_lines
                    if not line.startswith("Introduza") and not line.startswith("Write")
                )

                expected_output = expected_result[i].strip()

                if filtered_output == expected_output:
                    print(f"Teste {i+1} passou!")
                else:
                    print(f"Teste {i+1} falhou.")
                    print(f"Output esperado: {expected_output}")
                    print(f"Output recebido: {filtered_output}")
        
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
