program TesteFuncao;

function Dobro(x: integer): integer;
begin
    Dobro := x * 2;
end;

var
    valor, counter: Integer;
begin
    Write('Introduza um número menor que 10: ');
    ReadLn(valor);
    counter := 1;
    while valor < 10 do
    begin
        valor := Dobro(valor);
        writeln('O ciclo ', counter, ' têm o valor: ', valor);
        if valor < 10 then
            counter := counter + 1;
    end;
    writeln('Foram preciso ', counter, ' ciclos e o valor final foi ', valor);
end.