program TesteBinOp;

function SomaF(soma: float): float;
begin
    SomaF := 10 + 2.3;
end;

function SubF(soma: float): float;
begin
    SubF := 23 - soma;
end;

function MultF(soma: float): float;
begin
    MultF := 3 * 7.6;
end;

function DivF(soma: float): float;
begin
    DivF := 2.754 div 3.5;
end;

function Igual(a: boolean): boolean;
begin
    Igual := 12 = 21;
end;

function Diferente(a: boolean): boolean;
begin
    Diferente := 32 <> 2;
end;

function Menor(a: boolean): boolean;
begin
    Menor := 90.5 < 110;
end;

function Maior(a: boolean): boolean;
begin
    Maior := 1 > 0;
end;

function MenorIgual(a: boolean): boolean;
begin
    MenorIgual := 0.0 <= 0.0;
end;

function MaiorIgual(a: boolean): boolean;
begin
    MaiorIgual := 12 >= 9;
end;

function Conjuncao(a: boolean): boolean;
begin
    Conjuncao := 0 and 1;
end;

function Disjuncao(a: boolean): boolean;
begin
    Disjuncao := 0 or 1;
end;

var
    b, sF, suF, mF, dF: float;
    a, b1, b2, b3, b4, b5, b6, b7, b8: boolean;

begin
    b := 1;
    a := 1;

    sF := SomaF(b);
    suF := SubF(sF);
    mF := MultF(b);
    dF := DivF(b);

    writeln('Soma: ', sF);
    writeln('Subtracao: ', suF);
    writeln('Multiplicacao: ', mF);
    writeln('Divisao: ', dF);

    b1 := Igual(a);
    b2 := Diferente(a);
    b3 := Menor(a);
    b4 := Maior(a);
    b5 := MenorIgual(a);
    b6 := MaiorIgual(a);
    b7 := Conjuncao(a);
    b8 := Disjuncao(a);

    writeln('12 = 21? ', b1);
    writeln('32 <> 2? ', b2);
    writeln('90 < 110? ', b3);
    writeln('1 > 0? ', b4);
    writeln('0.0 <= 0.0? ', b5);
    writeln('12 >= 9? ', b6);
    writeln('0 and 1? ', b7);
    writeln('0 or 1? ', b8);
end.
