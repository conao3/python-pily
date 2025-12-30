# pily

A Lisp reader and REPL implementation written in Python. Pily parses S-expressions into a structured AST using Pydantic models, providing type-safe representations of Lisp data structures.

## Features

- Interactive REPL for exploring S-expressions
- Full S-expression reader supporting atoms, cons cells, and nested lists
- Type-safe AST representation using Pydantic models
- Support for common Lisp syntax including:
  - Integers and floating-point numbers
  - Strings (double-quoted)
  - Symbols
  - Quote syntax (`'expr`)
  - Comments (semicolon-style)
  - Dotted pairs

## Installation

```bash
pip install pily
```

Or install from source using Poetry:

```bash
git clone https://github.com/conao3/python-pily.git
cd python-pily
poetry install
```

## Usage

### Interactive REPL

Start the REPL:

```bash
pily
```

Example session:

```
pily> (+ 1 2)
car=ValueSymbol(name='+') cdr=car=ValueInteger(value=1) cdr=car=ValueInteger(value=2) cdr=ValueSymbol(name='nil')

pily> 'hello
car=ValueSymbol(name='quote') cdr=car=ValueSymbol(name='hello') cdr=ValueSymbol(name='nil')

pily> "a string"
value='a string'
```

### Programmatic Usage

```python
from pily import rep

# Read and evaluate an expression
result = rep.read("(a b c)")
print(result)
```

## Requirements

- Python 3.10+
- pydantic
- more-itertools

## License

Apache-2.0
