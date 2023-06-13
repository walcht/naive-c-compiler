%{
    #define PRINT_TOKEN(NAME, VALUE, LINE) (printf("<%s,%s,%d>\n", NAME, VALUE, LINE))
    #define PRINT_TOKEN_NOVAL(NAME, LINE) (printf("<%s,%d>\n", NAME, LINE))
%}
    int num_lines = 0;
DIGIT           [0-9]
%%
void                        |
char                        |
short                       |
int                         |        
long                        |
float                       |
double                      |
unsigned                    |
signed                      PRINT_TOKEN("TYPE", yytext, num_lines);
"+"                         |
"-"                         |
"*"                         |
"/"                         |
"++"                        |
"--"                        |
"%"                         PRINT_TOKEN("ARITHMETIC", yytext, num_lines);
"~"                         |
"&"                         |
"|"                         |
"^"                         |
"<<"                        |
">>"                        PRINT_TOKEN("BITWISE", yytext, num_lines);
"=="                        |
"!="                        |
">"                         |
">="                        |
"<"                         |
"<="                        PRINT_TOKEN("RELATIONAL", yytext, num_lines);
"!"                         |
"&&"                        |
"||"                        PRINT_TOKEN("LOGICAL", yytext, num_lines);
"="                         |
"+="                        |
"-="                        |
"*="                        |
"/="                        |
"%="                        |
"&="                        |
"|="                        |
"^="                        |
"<<="                       |
">>="                       PRINT_TOKEN("ASSIGNMENT", yytext, num_lines);
"auto"                      |
"const"                     |
"struct"                    |
"break"                     |
"continue"                  |
"else"                      |
"for"                       |
"switch"                    |
"case"                      |
"default"                   |
"enum"                      |
"goto"                      |
"register"                  |
"sizeof"                    |
"typedef"                   |
"volatile"                  |
"do"                        |
"extern"                    |
"if"                        |
"return"                    |
"static"                    |
"union"                     |
"while"                     PRINT_TOKEN("KEYWORD", yytext, num_lines);
[_a-zA-Z][_a-zA-Z0-9]*      PRINT_TOKEN("ID", yytext, num_lines);
{DIGIT}+"."{DIGIT}*         PRINT_TOKEN("LITERAL_FLOAT", yytext, num_lines);
{DIGIT}+                    PRINT_TOKEN("LITERAL_INT", yytext, num_lines);
"("                         PRINT_TOKEN_NOVAL("OPAR", num_lines);
")"                         PRINT_TOKEN_NOVAL("CPAR", num_lines);
"{"                         PRINT_TOKEN_NOVAL("OBRACE", num_lines);
"}"                         PRINT_TOKEN_NOVAL("CBRACE", num_lines);
";"                         PRINT_TOKEN_NOVAL("SEMICOLON", num_lines);
","                         PRINT_TOKEN_NOVAL("COMA", num_lines);
\n                          ++num_lines;
[\t ]+                      ;
%%
int main() {
    yylex();
}
