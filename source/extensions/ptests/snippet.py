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

# from typing import Any, Dict, List

import docutils

class CodeSnippet(object):
    def __init__(self, contents: str, language: str, path: str, line: int, actual: str = None, displayed_lines: str = None):
        self._contents = contents
        self._actual = actual
        self._language = language
        self._displayed_lines = displayed_lines
        self._path = path
        self._line = line

        with open(f"log.txt", "a") as logger:
            logger.write(f":: {language}\n")

    def actual(self) -> str:
        if self.actual_contents_are_different_than_displayed_contents():
            return self._actual
        else:
            return self.contents()

    def actual_contents_are_different_than_displayed_contents(self):
        return not self._actual is None

    def contents(self) -> str:
        return self._contents

    def language(self) -> str:
        return self._language if not self.language is None else 'none'
    
    def location(self) -> str:
        return f"{self._path}:{self._line}"

    def path(self) -> str:
        return self._path

    def line(self) -> str:
        return self._line

    def displayed_lines(self) -> str:
        return self._displayed_lines

    def displayed_contents(self) -> str:
        return self.contents()

    def to_nodes(self) -> 'list[Node]':
        code_block = docutils.nodes.literal_block(
            text = self.displayed_contents(),
            language = self.language(),
        )
        return [ code_block ]