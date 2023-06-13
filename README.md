# About

This is a very naive attempt at implementing a C frontend compiler.
The implemented frontend architecture is described in the following diagram:

![Compiler FrontEnd Design](https://raw.githubusercontent.com/walcht/naive-c-compiler/master/media/frontend_compiler.png)

## Symbol Table

The symbol table is implemented using a finite state machine as described below:

![symbol table finite state machine diagram](https://raw.githubusercontent.com/walcht/naive-c-compiler/master/media/diag_img.png)

## Know Limitations

- [ ] Preprocessor should be run on source C code before attempting to tokenize it. Not doing so will result in a lot of undefined-variable errors
- [ ] Name of scope isn't specified (should be implemented easily).
- [ ] Pointers are not yet properly handled.
- [ ] String literal tokenizer
- [ ] Ignore single line comments
- [ ] Ignore multiple line comments

## License

MIT License as specified in the ```LICENSE.txt``` file.
