from .token import Token, TokenType

class LexerException(Exception):
    pass

class Lexer():

    def __init__(self):
        self._pos: int = 0
        self._current_char: str = ''
        self._text: str = ''

    def next_(self) -> Token:
        while self._current_char != None:
            if self._current_char == " ":
                self._skip()
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
            if self._current_char == "*":
                char = self._current_char
                self._forward()
                return Token(TokenType.MUL, char)
            if self._current_char == "/":
                char = self._current_char
                self._forward()
                return Token(TokenType.DIV, char)
            raise LexerException(f"Bad token {self._current_char}")
        return Token(TokenType.EOS, None)

    def _skip(self):
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

    def init(self, _text: str) -> int:
        self._text = _text
        self._pos = -1
        self._forward()