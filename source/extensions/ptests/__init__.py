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
from typing import Any, Dict

import sphinx

# from .builder import PTestBuilder
# from .nodes.ptest import ptest
# from .directives.ptest import PTest
# from sphinx.util.typing import ExtensionMetadata

import ptests
from ptests.command import command
from ptests.example import example
from ptests.domain import PTests
from ptests.builder import Builder
from ptests import utils

def rewrite_ptest_nodes(app, doctree):
    # with open("rewrite.txt", "a") as logger:
    #     logger.write(str(f"doctree {doctree}\n"))

    for node in doctree.traverse(PTestNode):
        cb = node.as_code_blocks()
        with open("rewrite.txt", "a") as logger:
            logger.write(f"node {node}\n{cb}\n\n")
        
        node.replace_self(cb)
    

def setup(app: sphinx.application.Sphinx) -> Dict[str, Any]:
    # app.add_directive('command', Command)
    app.add_domain(PTests)
    app.add_builder(Builder)

    app.add_node(command,
        html=(utils.ignore_node, utils.ignore_node),
        latex=(utils.ignore_node, utils.ignore_node),
        text=(utils.ignore_node, utils.ignore_node),
    )

    app.add_node(example,
        html=(utils.ignore_node, utils.ignore_node),
        latex=(utils.ignore_node, utils.ignore_node),
        text=(utils.ignore_node, utils.ignore_node),
    )

    #app.connect('doctree-read', rewrite_ptest_nodes)
    #app.connect('doctree-resolved', process_todo_nodes)

    return {
        'version': '1.0',
        'parallel_read_safe': False,
        'parallel_write_safe': False,
    }
