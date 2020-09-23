import copy
import random
import string
from typing import List, Tuple


MAX_C_LENGTH = 10
COLUMNS = ["a", "b", "c"]
ARITHMETIC_OPERATORS = ["+", "-", "*", "/"]
COMPARISON_OPERATORS = ["<", ">", "="]
LOGICAL_OPERATORS = ["AND", "OR"]


def get_random_bool() -> bool:
    return random.choice([True, False])


def get_random_string(k: int = 1) -> str:
    return ''.join([random.choice(string.ascii_letters) for _ in range(k)])


def get_random_columns() -> List[str]:
    columns = copy.deepcopy(COLUMNS)
    random.shuffle(columns)
    return columns[0:random.randint(1, len(columns))]


def get_random_arithmetic_expr() -> Tuple[str, str, str]:
    left = random.choice(["a", "b"])
    right = "b" if left == "a" else "a"
    return (left, random.choice(ARITHMETIC_OPERATORS), right)


def choose_random_columns(columns: List[str]) -> List[str]:
    temp = copy.deepcopy(columns)
    random.shuffle(temp)
    return temp[0:random.randint(1, len(temp))]


def get_random_condition(column: str) -> Tuple[str, str, str]:
    if column == "c":
        return (column, "=", f"\'{get_random_string(random.randint(1, MAX_C_LENGTH))}\'")
    else:
        operator = random.choice(COMPARISON_OPERATORS)
        value = random.randint(-100, 100)
        return (column, operator, str(value))


def get_random_where_clause(columns: List[str]) -> str:
    random_columns = choose_random_columns(columns)
    conditions = [get_random_condition(column) for column in random_columns]
    conditions = [
        f"{condition[0]} {condition[1]} {condition[2]}" for condition in conditions]
    return "WHERE " + f" {random.choice(LOGICAL_OPERATORS)} ".join(conditions)


def get_random_order_by_clause(columns: List[str]) -> str:
    random_columns = choose_random_columns(columns)
    return f"ORDER BY {','.join(random_columns)}"


def get_random_limit_clause(k: int = 10) -> str:
    return f"LIMIT {random.randint(1, k)}"


def get_random_query() -> str:
    columns = get_random_columns()
    arithmetic_exprs = [get_random_arithmetic_expr()
                        for _ in range(random.randint(0, 2))]
    arithmetic_exprs = [
        f"{expr[0]}{expr[1]}{expr[2]}" for expr in arithmetic_exprs]
    columns.extend(arithmetic_exprs)
    columns = [f"\"{column}\"" for column in columns]

    # Has nested query?
    if get_random_bool():
        inner_q, new_columns = _get_random_query(columns, "t")
        q, _ = _get_random_query(new_columns, inner_q)
    else:
        q, _ = _get_random_query(columns, "t")

    return f"{q};"


def _get_random_query(columns: List[str], table: str,) -> str:
    output_columns = choose_random_columns(columns)
    q = f"SELECT {','.join(output_columns)} FROM ({table})"

    # Generate a WHERE clause?
    if get_random_bool():
        q = f"{q} {get_random_where_clause(columns)}"

    # Generate a random ORDER BY clause?
    if get_random_bool():
        q = f"{q} {get_random_order_by_clause(columns)}"

    # Generate a random LIMIT clause?
    if get_random_bool():
        q = f"{q} {get_random_limit_clause()}"

    return q, output_columns
