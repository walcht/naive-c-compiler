# About

This is a very naive attempt at implementing a C frontend compiler.
The implemented frontend architecture is described in the following diagram:

![Compiler FrontEnd Design](https://raw.githubusercontent.com/walcht/naive-c-compiler/master/media/frontend_compiler.png)

## Symbol Table

The symbol table is implemented using a finite state machine as described below:

![symbol table finite state machine diagram](https://raw.githubusercontent.com/walcht/naive-c-compiler/master/media/diag_img.png)

## Instructions

1. make sure ```flex``` is installed in your machine
2. make sure to have python 3.8+ installed and install package dependancies in ```requirements.txt```
3. generate C lexer code from ```lexer.lex```

  ```
  flex lexer/lexer.lex
  ```
  
3. compile previously generated C code file (make sure you have a C compiler installed in your machine):

  ```
  gcc lex.yy.c -lfl
  ```
  
4. pipe a C source code into the previously compiled lexer then pipe the output of the lexer to the Python parser:

  ```
  cat examples/example3.c | ./a.out | python3 parser/symbol_table.py
  ```
  
## Know Limitations

- [ ] Preprocessor should be run on source C code before attempting to tokenize it. Not doing so will result in a lot of undefined-variable errors
- [ ] Name of scope isn't specified (should be implemented easily).
- [ ] Pointers are not yet properly handled.
- [ ] String literal tokenizer
- [ ] Ignore single line comments
- [ ] Ignore multiple line comments

## License

MIT License as specified in the ```LICENSE.txt``` file.
