program Maior3;
var
    num1, maior : Integer;
    num2, num3 : Float;
begin
    writeln('Ola, Mundo!');

    num1 := 5;
    num2 := -7.5;
    num3 := num1 * num2;

    if num1 > 0 then
        writeln('num1 is positive');

    if num3 > 0 then
        writeln('num3 is positive')
    else
        writeln('num1 is negative');
end.