program TesteFuncIf;
function Positivo(x: integer): boolean;
begin
    Positivo := x > 0;
end;

var
    a, b: Boolean;

begin
    a := Positivo(5);
    if a then
        writeln('Positivo')
    else
        writeln('Negativo');

    b := Positivo(3);
    if b then
        writeln('Positivo')
    else
        writeln('Negativo');
end.
