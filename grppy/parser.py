import logging
import os

from lark import Lark, common, Transformer
from lark.tree import Visitor, Tree

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


class Proto3InitialVisitor(Visitor):

    def header(self, tree):
        tree.children = [child for child in tree.children if child is not None]

        if len(tree.children) == 1:
            tree = tree.children[0]


_transformers = [
    Proto3InitialTransformer,
    Proto3InitialVisitor,
]


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


def _apply_next_transformer(transformer, tree):
    if issubclass(transformer, Transformer):
        return transformer().transform(tree)
    elif issubclass(transformer, Visitor):
        return transformer().visit(tree)


"""
Cleaners
"""
def _remove_heading_nodes(tree):
    if isinstance(tree.children[0], Tree) and len(tree.children) == 1 and tree.data == 'header':
        return _remove_heading_nodes(tree.children[0])

    return tree


def _remove_node(tree, name):
    if isinstance(tree.children[0], Tree) and len(tree.children) == 1 and tree.data == name:
        return tree.children[0]

    if isinstance(tree.children[0], Tree):
        for i, node in enumerate(tree.children):
            tree.children[i] = _remove_node(node, name)
    return tree


def _remove_leaf_nodes(tree):

    if not isinstance(tree, Tree):
        return

    def is_removable(child):
        return isinstance(child, Tree) and len(child.children) == 0

    tree.children = [node for node in tree.children if not is_removable(node)]

    for child in tree.children:
        _remove_leaf_nodes(child)


def build_grpc_module(input_file):
    tree = _parse(input_file)
    if tree is None:
        return None

    _parse_tree_to_png(tree, input_file + "2.png")

    for transformer in _transformers:
        tree = _apply_next_transformer(transformer, tree)

    tree = _remove_heading_nodes(tree)
    tree = _remove_node(tree, 'start')
    tree = _remove_node(tree, 'definition_unit')
    _remove_leaf_nodes(tree)

    _parse_tree_to_png(tree, input_file + ".png")


if __name__ == '__main__':
    import sys

    build_grpc_module(sys.argv[1])
