program SumExample;

function Add(a: integer; b: integer): integer;
begin
    Add := a + b;
end;

var
    num1, num2, result: integer;
begin
    num1 := 5;
    num2 := 3;
    result := Add(num1, num2);
    writeln(result);
end.