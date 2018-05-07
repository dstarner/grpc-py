import logging
import os

from lark import Lark, common, Transformer

logger = logging.getLogger(__name__)

"""
Utils
"""


def _strip_quotes(quote_str):
    def starts_and_ends(x, y): return x.startswith(y) and x.endswith(y)

    if starts_and_ends(quote_str, "'") or starts_and_ends(quote_str, '"'):
        return quote_str[1:-1]
    return quote_str


class Proto3InitialTransformer(Transformer):

    def syntax(self, matches):
        if _strip_quotes(matches[0].value) != "proto3":
            raise AttributeError("Only supports Proto3 syntax.")
        return None

    def option(self, matches):
        return None


def _read(fn, *args):
    kwargs = {'encoding': 'iso-8859-1'}
    with open(fn, *args, **kwargs) as f:
        return f.read()


def _build_parser(file_name='grammar.g'):
    with open(file_name, 'r') as grammar_file:
        parser = Lark(grammar_file, parser='lalr', lexer='standard', start='start')
    return parser


def _parse(input_file, parser=None):
    if not parser:
        parser = _build_parser()
    try:
        return parser.parse(_read(input_file) + '\n')
    except common.UnexpectedToken as exc:
        logger.error(f"Error parsing file: {exc}")
        return None


def _parse_tree_to_png(tree, file):
    from lark.tree import pydot__tree_to_png
    pydot__tree_to_png(tree, file)


def build_grpc_module(input_file):
    parse_tree = _parse(input_file)
    if parse_tree is None:
        return None

    transformed = Proto3InitialTransformer().transform(parse_tree)
    print(transformed.pretty())
    _parse_tree_to_png(transformed, input_file + ".png")


if __name__ == '__main__':
    import sys

    build_grpc_module(sys.argv[1])
