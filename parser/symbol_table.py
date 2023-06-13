import os
import sys
import re
from typing import List, Iterator, NamedTuple, Dict, Literal
from statemachine import StateMachine, State

Token = NamedTuple("Token", [("kind", str), ("value", str | None), ("line_nbr", int)])
Reference = NamedTuple("Reference", [("line", int), ("ref", str), ("declaration", int)])


def _generate_tokens() -> Iterator[Token]:
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
    reg_pat = re.compile(r"[<>,\s]")
    for line in sys.stdin:
        values: List[str] = [t for t in reg_pat.split(line) if t]
        if len(values) == 3:
            yield Token(values[0], values[1], int(values[2]))
        elif len(values) == 2:
            yield Token(values[0], None, int(values[1]))
        else:
            print("Token in wrong string format. Ignoring token...")


class SymbolTableFST(StateMachine):
    """Finite state machine for generating a symbol table."""

    enter = State(initial=True)
    dec = State()
    undecided_dec = State()
    fun_params = State()
    before_fun_param_var_dec = State()
    fun_param_var_dec = State()
    before_fun_body = State()
    ref = State()

    TYPE = enter.to(dec) | fun_params.to(before_fun_param_var_dec)
    ID = enter.to(ref) | dec.to(undecided_dec) | before_fun_param_var_dec.to(fun_param_var_dec)
    COMA = undecided_dec.to(dec) | fun_param_var_dec.to(fun_params)
    SEMICOLON = undecided_dec.to(enter)
    OPAR = undecided_dec.to(fun_params)
    CPAR = fun_params.to(before_fun_body) | fun_param_var_dec.to(before_fun_body)
    OBRACE = before_fun_body.to(enter)
    CBRACE = enter.to(enter)
    AUTOMATIC_TRANSITION = ref.to(enter)

    def __init__(
        self,
    ) -> None:
        """Initializes and starts symbol table and references table construction process.

        Parameters:
        -----------
        """
        self.symbol_table_stack: List[Dict[str, int]] = []
        self.references_table: List[Reference] = []
        self.symbol_table_stack.append({})
        self.persistent_symbol_tables: List[Dict[str, int]] = []
        super(SymbolTableFST, self).__init__(allow_event_without_transition=True)

    def on_enter_undecided_dec(self, *, value: str, line: int) -> None:
        self.last_id = (value, line)

    def on_exit_undecided_dec(self, *, kind: str) -> None:
        if kind == "OPAR":
            self.symbol_table_stack[-1][self.last_id[0]] = self.last_id[1]
            self.symbol_table_stack.append(dict())
        elif kind in ["SEMICOLON", "COMA"]:
            self.symbol_table_stack[-1][self.last_id[0]] = self.last_id[1]

    def on_enter_ref(self, *, value: str, line: int) -> None:
        for i in range(len(self.symbol_table_stack) - 1, -1, -1):
            if value in self.symbol_table_stack[i]:
                self.references_table.append(Reference(line, value, self.symbol_table_stack[i][value]))
                self.AUTOMATIC_TRANSITION()
                return
        raise Exception(f"Reference to a non declared variable {value} at line: {line}")

    def on_enter_fun_param_var_dec(self, *, value: str, line: int) -> None:
        self.symbol_table_stack[-1][value] = line

    def after_CBRACE(self) -> None:
        self.persistent_symbol_tables.append(self.symbol_table_stack.pop())

    def save_diagram_image(self, path: str | None = None) -> None:
        diag_img_path: str
        if path is None:
            diag_img_path = os.path.abspath(
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "media", "diag_img.png")
            )
        else:
            diag_img_path = path
        self._graph().write_png(diag_img_path)

    def get_references_table(self) -> List[Reference]:
        return self.references_table

    def pretty_print_references_table(self) -> None:
        print("{0:10}{1:20}{2:20}".format("LINE", "REFERENCE", "DECLARATION"))
        for entry in self.references_table:
            print(f"{str(entry.line):10}{entry.ref:20}{str(entry.declaration):20}")

    def pretty_print_symbol_table(self) -> None:
        print("{0:20}{1}".format("OUTER SCOPE", self.symbol_table_stack[0]))
        for st in self.persistent_symbol_tables:
            print("{0:20}{1}".format("NAME UNK CURRENTLY", st))


if __name__ == "__main__":
    fst = SymbolTableFST()
    fst.save_diagram_image()
    for token in _generate_tokens():
        fst.send(
            token.kind,
            kind=token.kind,
            value=token.value,
            line=token.line_nbr,
        )
    fst.pretty_print_symbol_table()
    fst.pretty_print_references_table()
