program TesteFuncao;

function Dobro(x: integer): integer;
begin
    Dobro := x * 2;
end;

begin
    writeln(Dobro(5));
    writeln(Dobro(10));
end.
