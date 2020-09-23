import copy
import random
from packages.utils import get_random_string
from typing import List, Tuple


MAX_C_LENGTH = 10
COLUMNS = ["a", "b", "c"]
ARITHMETIC_OPERATORS = ["+", "-", "*", "/"]
COMPARISON_OPERATORS = ["<", ">", "="]
LOGICAL_OPERATORS = ["AND", "OR"]


def get_random_bool() -> bool:
    """Returns a random boolean value.

    Returns:
        A boolean value.
    """

    return random.choice([True, False])


def get_random_columns() -> List[str]:
    """Returns a list of randomly chosen columns.

    The columns are randomly chosen from a, b, and c.

    Returns:
        A list of column names.
    """

    columns = copy.deepcopy(COLUMNS)
    random.shuffle(columns)
    return columns[0:random.randint(1, len(columns))]


def get_random_arithmetic_expr() -> Tuple[str, str, str]:
    """Returns a tuple that represents an arithmetic expression.

    The first/last element of the tuple is either a or b. And the second
    element is an arithmetic operator, e.g. +.

    Returns:
        An arithmetic expression.
    """

    left = random.choice(["a", "b"])
    right = "b" if left == "a" else "a"
    return (left, random.choice(ARITHMETIC_OPERATORS), right)


def choose_random_columns(columns: List[str]) -> List[str]:
    """Returns a list of randomly chosen columns.

    Args:
        columns: A list of columns.

    Returns:
        A list of randomly chosen columns.
    """

    temp = copy.deepcopy(columns)
    random.shuffle(temp)
    return temp[0:random.randint(1, len(temp))]


def get_random_condition(column: str) -> Tuple[str, str, str]:
    """Returns a tuple that represents a condition.

        A condition can be a < 10, which is represented by the tuple
        ("a", "<", "10).

    Args:
        column: A column name.

    Returns:
        A condition represented by a tuple.
    """

    if column == "c":
        return (column, "=", f"\'{get_random_string(random.randint(1, MAX_C_LENGTH))}\'")
    else:
        operator = random.choice(COMPARISON_OPERATORS)
        value = random.randint(-100, 100)
        return (column, operator, str(value))


def get_random_where_clause(columns: List[str]) -> str:
    """Returns a random WHERE clause.

    Args:
        columns: A list of columns.

    Returns:
        A WHERE clause.
    """

    random_columns = choose_random_columns(columns)
    conditions = [get_random_condition(column) for column in random_columns]
    conditions = [
        f"{condition[0]} {condition[1]} {condition[2]}" for condition in conditions]
    return "WHERE " + f" {random.choice(LOGICAL_OPERATORS)} ".join(conditions)


def get_random_order_by_clause(columns: List[str]) -> str:
    """Returns a random ORDER BY clause.

    Args:
        columns: A list of columns.

    Returns:
        A ORDER BY clause.
    """

    random_columns = choose_random_columns(columns)
    return f"ORDER BY {','.join(random_columns)}"


def get_random_limit_clause(k: int = 10) -> str:
    """Returns a random LIMIT clause.

    Args:
        columns: A list of columns.

    Returns:
        A LIMIT clause.
    """

    return f"LIMIT {random.randint(1, k)}"


def get_random_query() -> str:
    """Returns a random SQL query.

    Returns:
        A random SQL query.
    """

    # Generate a list of random columns.
    columns = get_random_columns()
    arithmetic_exprs = [get_random_arithmetic_expr()
                        for _ in range(random.randint(0, 2))]
    arithmetic_exprs = [
        f"{expr[0]}{expr[1]}{expr[2]}" for expr in arithmetic_exprs]
    columns.extend(arithmetic_exprs)
    columns = [f"\"{column}\"" for column in columns]

    # Generate a nested query?
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
