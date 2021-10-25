from .token import Token, TokenType

class InterpreterException(Exception):
    pass

class Interpreter():
    def __init__(self):
        self._pos: int = 0
        self._current_token: Token = None
        self._current_char: str = ''
        self._text: str = ''

    def _next_token(self) -> Token:
        while self._current_char != None:
            if self._current_char == " ":
                self.skip()
                continue
            if self._current_char.isdigit():
                return Token(TokenType.INTEGER, self._integer())
            if self._current_char == "+":
                char = self._current_char
                self._forward()
                return Token(TokenType.PLUS, char)
            if self._current_char == "-":
                char = self._current_char
                self._forward()
                return Token(TokenType.MINUS, char)
            raise InterpreterException(f"Bad token {self._current_char}")
        return Token(TokenType.EOS, None)

    def skip(self):
        while self._current_char and self._current_char == " ":
            self._forward()

    def _integer(self):
        result: list = []
        while self._current_char and self._current_char.isdigit():
            result.append(self._current_char)
            self._forward()
        return "".join(result)

    def _forward(self):
        self._pos += 1
        if self._pos >= len(self._text):
            self._current_char = None
        else:
            self._current_char = self._text[self._pos]

    def _check_token_type(self, type_: TokenType):
        if self._current_token.type_ == type_:
            self._current_token = self._next_token()
        else:
            raise InterpreterException(f"Invalid token order {type_}")

    def _expr(self) -> int:
        self._current_token = self._next_token()
        left = self._current_token
        self._check_token_type(TokenType.INTEGER)

        op = self._current_token
        if op.type_ == TokenType.PLUS:
            self._check_token_type(TokenType.PLUS)
        elif op.type_ == TokenType.MINUS:
            self._check_token_type(TokenType.MINUS)
        
        right = self._current_token
        self._check_token_type(TokenType.INTEGER)

        if op.type_ == TokenType.PLUS:
            return int(left.value) + int(right.value)
        elif op.type_ == TokenType.MINUS:
            return int(left.value) - int(right.value)
        else:
            raise InterpreterException("Bad operator")

    def __call__(self, _text: str) -> int:
        return self.interpret(_text)

    def interpret(self, _text: str) -> int:
        self._text = _text
        self._pos = -1
        self._forward()
        return self._expr()