"""Evaluator for the Nova language."""

from __future__ import annotations

from typing import Any, Dict


class EvaluationError(RuntimeError):
    """Raised when the runtime cannot evaluate a Nova expression."""


def evaluate(ast):
    """Evaluate a parsed Nova program and return the final environment."""
    env: Dict[str, Any] = {}
    for statement in ast.statements:
        evaluate_statement(statement, env)
    return env


def evaluate_statement(statement, env: Dict[str, Any]):
    statement_type = type(statement).__name__

    if statement_type == "Assignment":
        value = evaluate_expression(statement.value, env)
        env[statement.name] = value
        return value

    if statement_type == "PrintStatement":
        value = evaluate_expression(statement.expr, env)
        print(value)
        return value

    raise EvaluationError(f"Unsupported statement type: {statement_type}")


def evaluate_expression(expr, env: Dict[str, Any]):
    expr_type = type(expr).__name__

    if expr_type == "IntegerLiteral":
        return int(expr.value)

    if expr_type == "StringLiteral":
        return expr.value

    if expr_type == "Identifier":
        if expr.name not in env:
            raise NameError(f"Undefined variable: {expr.name}")
        return env[expr.name]

    if expr_type == "GroupedExpression":
        return evaluate_expression(expr.expr, env)

    if expr_type == "BinaryOp":
        left = evaluate_expression(expr.left, env)
        right = evaluate_expression(expr.right, env)

        if expr.op == "+":
            return left + right
        if expr.op == "-":
            return left - right
        if expr.op == "*":
            return left * right
        if expr.op == "/":
            return left / right

        raise EvaluationError(f"Unsupported operator: {expr.op}")

    raise EvaluationError(f"Unsupported expression type: {expr_type}")
