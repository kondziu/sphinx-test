# from docutils import nodes
# from docutils.parsers.rst import Directive
# from docutils.parsers.rst import directives

# from sphinx import addnodes
# from sphinx.application import Sphinx
# from sphinx.directives import ObjectDescription
# from sphinx.domains import Domain, Index
# from sphinx.roles import XRefRole
# from sphinx.util.nodes import make_refnode
# from sphinx.application import Sphinx
# from sphinx.builders import Builder
# from sphinx.util import logging
# from sphinx.util.docutils import SphinxDirective

from typing import List
import os

import docutils 
import sphinx
import textwrap

from ptests.snippet import CodeSnippet
from ptests import utils

class Example(sphinx.util.docutils.SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        'name': docutils.parsers.rst.directives.unchanged_required,
        'description': docutils.parsers.rst.directives.unchanged_required,
        'skip-markup': docutils.parsers.rst.directives.unchanged,
    }

    def _name(self) -> str:
        return self.options['name']

    def _description(self) -> str:
        return self.options['description']

    def _path(self) -> str:
        return self.env.doc2path(self.env.docname, base=False)

    def _skip_markup(self) -> str:
        return utils.option_is_true(self.options, 'skip-markup')

    def _text(self) -> str: 
        return "\n".join(self.content)

    def to_example(self) -> 'command':
        example_node = example(
            name = self._name(),
            description = self._description(),
            path = self._path(),
            line = self.lineno,
            markup = not self._skip_markup(),
            content = self._text(),
        )

        return example_node

    def to_nodes(self) -> 'list[Node]':
        return [ self.to_example() ]

    def run(self) -> 'list[Node]':
        node = self.to_example()
        utils.register(self.env, 'ptest_examples', self._name(), node)
        return [ node ]

class example(docutils.nodes.General, docutils.nodes.Element):
    def __init__(self, name: str, description: str, path: str, line: int, content: str, markup: bool = True):
        self.name = name
        self.description = description
        self.path = path
        self.line = line
        self.markup = markup
        self.content = content

        super(docutils.nodes.General, self).__init__()
        super(docutils.nodes.Element, self).__init__()       

    @classmethod
    def visit(node_class, translator, node):
        pass

    @classmethod
    def depart(node_class, translator, node):
        pass

    def __str__(self) -> str:
        props = [
            ('name', self.name),
            ('description', utils.quoted(self.description)),
            ('path', self.path),
            ('line', self.line),
            ('markup', self.markup),
        ]
        displayed_props = [ f'{name}="{utils.quoted(prop)}"' for (name, prop) in props if prop != None ]
        
        return f'<ptest:example {" ".join(displayed_props)}>{utils.quoted(self.content)}</ptest:example>'

    def to_nodes(self) -> 'list[Node]':
        # def with_classes(node: 'Node', *classes) -> 'Node':
        #     utils.attach_classes(node, *classes)
        #     return node

        # container = with_classes(docutils.nodes.container(), "ptest")
        # container += [ with_classes(node, "ptest-command-block") for node in self.command.to_nodes() ]
        # container += [ with_classes(node, "ptest-output-block") for node in self.output.to_nodes() ]

        return [ docutils.nodes.Text("**Example**") ]

    def to_driver(self) -> 'str':
        pass