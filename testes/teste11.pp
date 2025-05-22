program Maior3;
var
    num1, num3, maior: Integer;
    num2 : Float;
begin
    writeln('Ola, Mundo!');
    write('Ola, Mundo!');

    num1 := 5;
    num2 := 7.5;
    num3 := 15;

    if num1 > 0 then
        writeln('num1 is positive');

    if num1 > 0 then
    begin
        writeln('num1 is positive');
        num2 := num2 + 1;
        num3 := num3 * 2;
    end
    else
        writeln('num1 is negative');

    for num2 := 1 to 5 do
        write(num2);
end.