"""Tests for the Nova evaluator."""

from lexer import Lexer
from parser import parse
from evaluator import evaluate


def tokenize(src: str):
    lexer = Lexer(src)
    tokens = []
    while True:
        token = lexer.next_token()
        tokens.append(token)
        if token.type.name == "EOF":
            break
    return tokens


def test_arithmetic_evaluation():
    src = """
let x = 10
let y = 5
let result = x + y * 2
"""
    env = evaluate(parse(tokenize(src)))
    assert env["x"] == 10
    assert env["y"] == 5
    assert env["result"] == 20


def test_string_and_identifier_evaluation():
    src = """
let name = "Daniel"
let greeting = "Hi " + name
"""
    env = evaluate(parse(tokenize(src)))
    assert env["name"] == "Daniel"
    assert env["greeting"] == "Hi Daniel"


def test_grouped_expression_evaluation():
    src = "let total = (2 + 3) * 4"
    env = evaluate(parse(tokenize(src)))
    assert env["total"] == 20


if __name__ == "__main__":
    test_arithmetic_evaluation()
    test_string_and_identifier_evaluation()
    test_grouped_expression_evaluation()
    print("All evaluator tests passed")
