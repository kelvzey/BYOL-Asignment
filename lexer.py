"""Lexer implementation for Nova (.myext) language.

Week 1 lexer solution prepared by Kelvin omonigho Erhiaworon (Ug/22/5790). This version keeps the same logic but uses a slightly different coding style.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, List


class TokenType(Enum):
    LET = auto()
    PRINT = auto()
    IDENT = auto()
    INTEGER = auto()
    STRING = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQUAL = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()
    ILLEGAL = auto()


KEYWORDS = {
    "let": TokenType.LET,
    "print": TokenType.PRINT,
}


@dataclass
class Token:
    type: TokenType
    literal: str

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.literal!r})"


class Lexer:
    def __init__(self, script: str):
        self.input = script
        self.position = 0       # current pos in input (points to current char)
        self.advance_pos = 0  # current reading position in input (after current char)
        self.ch: Optional[str] = None
        self.move_on()

    def move_on(self):
        if self.advance_pos >= len(self.input):
            self.ch = None
        else:
            self.ch = self.input[self.advance_pos]
        self.position = self.advance_pos
        self.advance_pos += 1

    def preview(self) -> Optional[str]:
        if self.advance_pos >= len(self.input):
            return None
        return self.input[self.advance_pos]

    def clear_space(self):
        while self.ch is not None and self.ch.isspace():
            self.move_on()

    def take_name(self) -> str:
        start = self.position
        while self.ch is not None and (self.ch.isalpha() or self.ch.isdigit() or self.ch == '_'):
            self.move_on()
        return self.input[start:self.position]

    def take_number(self) -> str:
        start = self.position
        while self.ch is not None and self.ch.isdigit():
            self.move_on()
        return self.input[start:self.position]

    def take_text(self) -> str:
        # consume opening quote
        self.move_on()
        value_chars: List[str] = []
        while self.ch is not None and self.ch != '"':
            if self.ch == '\\' and self.preview() in ('"', '\\'):
                # handle simple escapes: \" and \\
                self.move_on()
                value_chars.append(self.ch)
                self.move_on()
                continue
            value_chars.append(self.ch)
            self.move_on()
        # consume closing quote
        if self.ch == '"':
            self.move_on()
        return ''.join(value_chars)

    def scan_token(self) -> Token:
        self.clear_space()

        if self.ch is None:
            return Token(TokenType.EOF, "")

        # comments
        if self.ch == '/' and self.preview() == '/':
            # consume both slashes
            self.move_on()
            self.move_on()
            while self.ch is not None and self.ch != '\n':
                self.move_on()
            return self.scan_token()

        if self.ch.isalpha() or self.ch == '_':
            lit = self.take_name()
            ttype = KEYWORDS.get(lit, TokenType.IDENT)
            return Token(ttype, lit)

        if self.ch.isdigit():
            lit = self.take_number()
            return Token(TokenType.INTEGER, lit)

        if self.ch == '"':
            lit = self.take_text()
            return Token(TokenType.STRING, lit)

        ch = self.ch
        if ch == '+':
            tok = Token(TokenType.PLUS, ch)
        elif ch == '-':
            tok = Token(TokenType.MINUS, ch)
        elif ch == '*':
            tok = Token(TokenType.STAR, ch)
        elif ch == '/':
            tok = Token(TokenType.SLASH, ch)
        elif ch == '=':
            tok = Token(TokenType.EQUAL, ch)
        elif ch == '(':
            tok = Token(TokenType.LPAREN, ch)
        elif ch == ')':
            tok = Token(TokenType.RPAREN, ch)
        else:
            tok = Token(TokenType.ILLEGAL, ch)

        self.move_on()
        return tok


if __name__ == "__main__":
    sample = 'let x = 10\nprint x + 5\n'
    lexer = Lexer(sample)
    toks = []
    while True:
        t = lexer.scan_token()
        toks.append(t)
        if t.type == TokenType.EOF:
            break
    for t in toks:
        print(t)
