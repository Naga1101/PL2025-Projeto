# PL2025-Projeto

## Introdução


## Análise Léxica

A primeira etapa deste projeto foi identificar todos os tokens existentes na linguagem Pascal de forma a que ao forneceremos um ficheiro e código este seja analisado e convertido numa lista de tokens.
Para tal foi necessário seguir uma organização na declaração estes padrões, pois quando um token pode ser apanhado por mais de um padrão, o que se encontra declarado será o que vai definir o token. Devido a esteproblema o padrão que apanha os identificadores ```r'\b[a-zA-Z_]{1}[a-zA-Z0-9_]*\b'``` teve de ser o último a ser definido pois este vai ao encontro de keywords pré existentes na lingaugem Pascal.
O lexer que obtivemos encontra-se localizado no ficheio _lexer.py_.

## Análise Sintática

Após a definição dos tokens, definimos as regras que a nossa gramática iria seguir...

```
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
```

O parser que obtivemos encontra-se localizado no ficheio _parser.py_.

## Análise Semântica

Na análise semântica
A análise semântica foi realizada no ficheio _semantics.py_.

## Geração de Código

Nesta etapa optamos por converter o código Passcal em código da máquina virtual seguindo uma tradução dirigida pela sintaxe
Tal como a análise semântica a geração de código foi realizada no ficheio _semantics.py_.

## Correr testes

De forma a facilitar o processo de teste do programa foi realizado um script (_runTests.py_) que mostra os testes existentes e irá corre-los de forma a que o ficheiro Pascal chegue até ao ficheiro formato final, um output em formato txt com os comandos que podem ser corridos na máquina virtual.
Os ficheiros teste encontram-se na pasta _testes_ e os outputs encontram-se divididos por 3 pastas diferentes(_outputsParser_, _outputsLexer_ e _outputsSemantics_) com o nome do teste que estão a realizar.