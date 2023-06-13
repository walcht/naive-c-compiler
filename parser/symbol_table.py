from os import path
from typing import List, Iterator, NamedTuple, Dict, Literal
from statemachine import StateMachine, State

Token = NamedTuple("Token", [("kind", str), ("value", str | None), ("line_nbr", int)])
Reference = NamedTuple("Reference", [("line", int), ("ref", str), ("declaration", int)])


def _generate_tokens(file_path: str) -> Iterator[Token]:
    """Generates tokens out of a token file.

    Each line in the provided file should be of the following format:
        <KIND,VALUE,LINE>
    or value can be omitted for trivial kinds (such as '{' and '}'):
        <KIND,LINE>
    KIND is the token's kind (example: KEYWORD).
    VALUE is the token's value (example: function_name).
    LINE is the token's line number in the source file.

    Parameters:
    -----------
    file_path: str
        absolute filepath to the file containing string tokens.

    Yields:
    -------
    Token:
        next token in the file if there is any.
    """
    if not path.isfile(file_path):
        file_path = path.abspath(file_path)
        if not path.isfile(file_path):
            raise ValueError(
                """
    Supplied path is not a valid file path.
    Please supply either a valid absolute or relative filepath."""
            )
    with open(file_path, "r", encoding="utf8") as tokens:
        for line in tokens:
            values: List[str] = line[1:-1].split(",")
            if len(values) == 3:
                yield Token(values[0], values[1], int(values[2]))
            elif len(values) == 2:
                yield Token(values[0], None, int(values[1]))


class SymbolTableFST(StateMachine):
    enter = State(initial=True)
    dec = State()
    undecided_dec = State()
    fun_params = State()
    before_fun_body = State()
    ref = State()

    TYPE = enter.to(dec)
    ID = enter.to(ref) | dec.to(undecided_dec)
    COMA = undecided_dec.to(dec)
    SEMICOLON = undecided_dec.to(enter)
    OPEN_PAR = undecided_dec.to(fun_params)
    CLOSE_PAR = fun_params.to(before_fun_body)
    OPEN_BRACE = before_fun_body.to(enter)
    CLOSE_BRACE = enter.to(enter)

    def __init__(
        self,
    ) -> None:
        self.symbol_table_stack: List[Dict[str, int]] = []
        self.references_table: List[Reference] = []
        super(SymbolTableFST, self).__init__()

    def on_enter_undecided_dec(self, value: str, line: int) -> None:
        self.last_id = (value, line)

    def on_exit_undecided_dec(self, kind: str) -> None:
        if kind == "OPEN_PAR":
            self.symbol_table_stack[-1][self.last_id[0]] = self.last_id[1]
            self.symbol_table_stack.append(dict())
        elif kind in ["SEMICOLON", "COMA"]:
            self.symbol_table_stack[-1][self.last_id[0]] = self.last_id[-1]

    def on_ref_enter(self, value: str, line: int) -> None:
        for i in range(len(self.symbol_table_stack), -1, -1):
            if value in self.symbol_table_stack[i]:
                self.references_table.append(Reference(line, value, self.symbol_table_stack[i][value]))
                return
        raise Exception(f"Reference to a non declared variable {value} at line: {line}")

    def after_CLOSE_BRACE(self) -> None:
        self.symbol_table_stack.pop()


if __name__ == "__main__":
    pass
