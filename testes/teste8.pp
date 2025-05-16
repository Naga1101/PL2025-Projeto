program TesteBinOp;

var
    soma, sub, mult, divi: integer;
    somaFloat, subFloat, multFloat, diviFloat: float;
    igual, diferente, menor, maior, menorIgual, maiorIgual: boolean;
    conjuncao, disjuncao: boolean;
begin
    somaFloat := 10 + 2.3;
    subFloat := 23 - somaFloat;
    multFloat := 3 * 7.6;
    diviFloat := 2.754 / 3.5;

    igual := 12 = 21;
    diferente := 32 <> 2;
    menor := 90 < 110;
    maior := 1 > 0;
    menorIgual := 0.0 <= 0.0;
    maiorIgual := 12 >= 9;

    conjuncao := 0 and 1;
    disjuncao := 0 or 1;
end.