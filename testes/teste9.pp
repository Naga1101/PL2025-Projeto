program OrdCharExample;
var
  ch: string;
  code: integer;
begin
  ch := 'A';
  code := ord(ch); 
  writeln('The ASCII code of ', ch, ' is ', code);
end.