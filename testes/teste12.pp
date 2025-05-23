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
        writeln('É positivo')
    else
        writeln('É negativo');

    b := Positivo(-3);
    if b then
        writeln('É positivo')
    else
        writeln('É negativo');
end.
