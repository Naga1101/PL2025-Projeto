program TestaLoops;
var
    i, soma: integer;
begin
    soma := 0;

    { loop crescente }
    for i := 1 to 3 do
    soma := soma + i;

    { loop decrescente }
    for i := 3 downto 1 do
    soma := soma + i;

    { deve imprimir 12 }
    writeln(soma);  
end.
