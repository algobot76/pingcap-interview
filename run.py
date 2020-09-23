import copy
import random
import string
from typing import List, Tuple


MAX_C_LENGTH = 10
COLUMNS = ["a", "b", "c"]
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


def get_random_condition(column: str) -> Tuple[str, str, str]:
    if column == "c":
        return (column, "=", f"\'{get_random_string(random.randint(1, MAX_C_LENGTH))}\'")
    else:
        operator = random.choice(COMPARISON_OPERATORS)
        value = random.randint(-100, 100)
        return (column, operator, str(value))


def get_random_where_clause() -> str:
    columns = get_random_columns()
    conditions = [get_random_condition(column) for column in columns]
    conditions = [
        f"{condition[0]} {condition[1]} {condition[2]}" for condition in conditions]
    return "WHERE " + f" {random.choice(LOGICAL_OPERATORS)} ".join(conditions)


def get_random_order_by_clause() -> str:
    return f"ORDER BY {','.join(get_random_columns())}"


def get_random_limit_clause(k: int = 10) -> str:
    return f"LIMIT {random.randint(1, k)}"


def get_random_query() -> str:
    q = f"SELECT {','.join(get_random_columns())} FROM t"

    # Generate a WHERE clause?
    if get_random_bool():
        q = f"{q} {get_random_where_clause()}"

    # Generate a random ORDER BY clause?
    if get_random_bool():
        q = f"{q} {get_random_order_by_clause()}"

    # Generate a random LIMIT clause?
    if get_random_bool():
        q = f"{q} {get_random_limit_clause()}"

    return f"{q};"


if __name__ == "__main__":
    q = get_random_query()
    print(q)
