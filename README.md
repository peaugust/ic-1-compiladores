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

# Run inside parser file

1. antlr4 cmm.g4 -o build
2. cd build
3. javac \*.java
4. grun cmm start -gui < ../../../../cmm-2020.2/input.cmm
