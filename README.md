# Setup

Install Python packages

```shell
pip install -r requirement.txt
```

> ANTLR requirers java to generate the parser.

# Usage

```shell
$ python -m cmm -h
usage: cmm [-h] [-o] input

C-- interpreter

positional arguments:
  input       source code

optional arguments:
  -h, --help  show this help message and exit
  -o          python output
```

# To run python3 -m cmm input.cmm

1. pip3 install ast-decompiler
2. pip3 install requests
3. python3 -m cmm input.cmm
