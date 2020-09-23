# pingcap-interview

## Introduction

This is a demo about how to implement a random SQL query generator and how it can be used to do a fuzz test. Note that the code is still immature and please don't use it in production.

## Usage

Make sure you have Python installed on your computer and the version is at least 3.8. This demo is shipped with two handy command line tools: `seed` and `fuzz`. To install them, please follow these steps:

1. `git clone https://github.com/algobot76/pingcap-interview.git`
2. `cd pingcap-interview`
3. `pip install -e .`

### `seed`

`seed` is a command line tool that generates a database with random data. The database contains only one table called `t` and `t` has tree columns: `a` (INTEGER), `b` (INTEGER), and `c` (VARCHAR(10)).

```bash
seed example.db 100
```

- This command creates a database called `example.db` and it contains 100 random entries.

### `fuzz`

`fuzz` is a command line tool that runs a large number of random SQL queries against a database (it only supports SQLite for now).

```bash
fuzz example.db 1000
```

- `fuzz` runs 1000 random SQL queries against the `example.db` database.
- It reports the number of queries and the execution time of each query.

## Notes on Implementation of `rqg`

The implementation of the random SQL query generator resides in `packages/rqg.py`. Please take a look at the source code for details. This section only provides you an overview of the implementation.

```
<query> ::= <select-statement>
<select-statement> ::= SELECT <column>+ FROM <table> <where-clause>? <order-by-clause>? <limit-clause>?;
<where-clause> ::= WHERE <condition>+
<order-by-clause> ::= ORDER BY <column>+
<limit-clause> ::= LIMIT <number>
<column> ::= <column-name> | <arithmetic-expr>
<column-name> ::= <string>
<arithmetic-expr> ::= <column-name> <arithmetic-operator> <column-name>
<table> ::= <string> | <query>
<condition> ::= <column> <comparison-operator> (<number> | <string>)
<comparison-operator> ::= "<" | ">" | "="
<arithmetic-operator> ::= "+" | "-" | "*" | "/"
```

The generator is implemented according to the BNF syntax of SQL query. Functions, such as `get_random_where_clause`, along with other helper functions work together to create different entities that make up a SQL query.
