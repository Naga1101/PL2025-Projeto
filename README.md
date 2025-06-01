# PL2025-Projeto

## Introdução


## Análise Léxica

A primeira etapa deste projeto foi identificar todos os tokens existentes na linguagem Pascal de forma a que ao forneceremos um ficheiro e código este seja analisado e convertido numa lista de tokens.
Para tal foi necessário seguir uma organização na declaração estes padrões, pois quando um token pode ser apanhado por mais de um padrão, o que se encontra declarado será o que vai definir o token. Devido a esteproblema o padrão que apanha os identificadores ```r'\b[a-zA-Z_]{1}[a-zA-Z0-9_]*\b'``` teve de ser o último a ser definido pois este vai ao encontro de keywords pré existentes na lingaugem Pascal.
O lexer que obtivemos encontra-se localizado no ficheio _lexer.py_.

## Análise Sintática

Após a definição dos tokens, definimos as regras que a nossa gramática iria seguir. 

### Estrutura definida
Começamos por definir uma estrutura principal com estes **tokens não terminais = {const_decls; func_decls; var_decl; begin_progr}** que consistem nos blocos existentes na liguagem pascal. Cada uma destas produções contêm uma lista de tokens não terminais que definem a parte de código correspondente(por exemplo: ```const_decls → CONST const_decl_list``` que irá identificar todas as constantes definidas pelo código). 

### Statements definidos
De forma a identificar o corpo principal da função definimos todos os tipos de statements que podem aparecer numa função pascal:


```
P18: statement → simple_statement ';'
               | compound_statement ';'
               | selection_statement
               | while_statement
               | for_statement
               | COMMENT
``` 

Os *simple_statement* correspondem a todas as linhas de código pascal que acabam com ';' e têm apenas 1 linha. 

De seguida os *compound_statement* correspondem a uma lista de statements que se encontra entre um ```BEGIN ... END```, foi realizada uma decisão de dividir a chamada do *compound_statement* em duas produções diferentes sendo uma delas a ```P18: statement``` que ocorre quando o *compound_statement* se encontra dentro de uma função e o segundo caso na produção ```P15: begin_progr → compound_statement '.'``` que corresponde ao ```BEGIN ... END``` principal que acaba com um '.' para sinalizar o fim da função.

O *selection_statement* corresponde aos casos ```if ... then``` ou ```if ... then ... else```.

O *while_statement* e o *for_statement* correspondem aos loops existentes em pascal, while loop e for loop respetivamente.

Por fim o statement *COMMENT* corresponde ao token terminal correspondente aos comentários escritos pelo código.

### Gramática completa
Por fim a gramática definida foi a seguinte:

```
P1: init → PROGRAM program_name

P2: program_name → ID ';' program_body

P3: program_body → const_decls func_decls var_decl begin_progr
                 | func_decls var_decl begin_progr
                 | const_decls var_decl begin_progr
                 | const_decls func_decls begin_progr
                 | const_decls begin_progr
                 | func_decls begin_progr
                 | var_decl begin_progr
                 | begin_progr

P4: const_decls → CONST const_decl_list

P5: const_decl_list → const_decl
                    | const_decl_list const_decl

P6: const_decl → ID '=' expression ';'

P7: func_decls → func_decl
               | func_decls func_decl

P8: func_decl → FUNCTION ID '(' var_decl_lines ')' ':' type ';' begin_func

P9: begin_func → var_decl compound_statement ';'
               | compound_statement ';'

P10: var_decl → VAR var_decl_lines

P11: var_decl_lines → var_decl_line
                    | var_decl_lines var_decl_line

P12: var_decl_line → id_list ':' type ';'
                   | id_list ':' type

P13: id_list → ID
             | id_list ',' ID

P14: type → INTEGERTYPE
          | FLOATTYPE
          | BOOLEANTYPE
          | STRINGTYPE
          | ARRAY '[' NUMBER '..' NUMBER ']' OF type

P15: begin_progr → compound_statement '.'

P16: compound_statement → BEGIN statement_list END

P17: statement_list → statement
                    | statement_list statement

P18: statement → COMMENT
               | simple_statement ';'
               | compound_statement ';'
               | selection_statement
               | while_statement
               | for_statement

P19: simple_statement → ID ASSIGN expression
                      | WRITEFUNC '(' expression_list ')'
                      | WRITEFUNCLN '(' expression_list ')'
                      | READFUNC expression
                      | READFUNCLN expression
                      | BREAK

P20: selection_statement →
     IF expression THEN statement
   | IF expression THEN inside_statement ELSE statement

P21: inside_statement → simple_statement
                      | compound_statement
                      | inside_selection_statement

P22: inside_selection_statement → IF expression THEN inside_statement
                                | IF expression THEN inside_statement ELSE inside_statement

P23: while_statement → WHILE expression DO statement

P24: for_statement → FOR ID ASSIGN expression TO expression DO statement
                   | FOR ID ASSIGN expression DOWNTO expression DO statement

P25: expression → expression '+' expression
                | expression '-' expression
                | expression '*' expression
                | expression '/' expression
                | expression MOD expression
                | expression AND expression
                | expression GT expression
                | expression LT expression
                | expression GE expression
                | expression LE expression
                | expression EQ expression
                | expression NE expression
                | expression OR expression
                | ORDFUNC expression
                | PREDFUNC expression
                | SUCCFUNC expression
                | LENGTHFUNC expression
                | ID '[' expression ']'
                | ID '(' expression_list ')'
                | '(' expression ')'
                | ID '(' ')'
                | NOT expression
                | STRING
                | NUMBER
                | FLOAT
                | FALSE
                | TRUE
                | CHAR
                | ID
                | <empty>

P26: expression_list → expression
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