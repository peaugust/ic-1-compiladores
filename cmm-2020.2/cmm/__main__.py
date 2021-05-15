from antlr4 import FileStream, CommonTokenStream
from os import path
import argparse

try:
    from .parser.cmmLexer import cmmLexer
    from .parser.cmmParser import cmmParser
except ImportError:
    # Generate ANTLR parser from g4 file
    from .generate_parser import generate_parser
    generate_parser(path.join(path.dirname(__file__), 'parser/cmm.g4'))

    from .parser.cmmLexer import cmmLexer
    from .parser.cmmParser import cmmParser

# import astVisitor after the try-except
from .globVisitor import globVisitor


def main():

    # Argument parser
    parser_args = argparse.ArgumentParser(prog='cmm', description='C-- interpreter')
    parser_args.add_argument('input', type=str, help='source code')

    args = parser_args.parse_args() 
    #################################

    input_stream = FileStream(args.input)

    lexer = cmmLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = cmmParser(stream)

    tree = parser.start() # Get AST

    visitor = globVisitor(args.input)
    glob = visitor.visitStart(tree)

    glob['main'](glob=glob)
    
if __name__ == '__main__':
    main()