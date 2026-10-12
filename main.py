"""Entry point for the Nova interpreter."""

import sys
from pathlib import Path

from evaluator import evaluate
from lexer import Lexer
from parser import parse


def run_source(source: str):
    lexer = Lexer(source)
    tokens = []
    while True:
        token = lexer.next_token()
        tokens.append(token)
        if token.type.name == "EOF":
            break
    ast = parse(tokens)
    return evaluate(ast)


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: python main.py <file.myext>")
        return 1

    path = Path(argv[0])
    source = path.read_text(encoding="utf-8")
    run_source(source)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
