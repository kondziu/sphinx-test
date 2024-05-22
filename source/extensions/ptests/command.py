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

class Command(sphinx.util.docutils.SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        'example': docutils.parsers.rst.directives.unchanged_required, 
        'name': docutils.parsers.rst.directives.unchanged_required,
        'command': docutils.parsers.rst.directives.unchanged_required,
        'command-language': docutils.parsers.rst.directives.unchanged,
        'executed-command': docutils.parsers.rst.directives.unchanged,
        'language': docutils.parsers.rst.directives.unchanged,
        'show-output': docutils.parsers.rst.directives.unchanged,
        'capture-stderr': docutils.parsers.rst.directives.unchanged,
        'capture-stdout': docutils.parsers.rst.directives.unchanged,
        'filter': docutils.parsers.rst.directives.unchanged,
    }

    def _check_and_get(self, option) -> str:
        if option not in self.options:
            raise utils.MissingRequiredOption(f"{self._relative_path()}:{self.lineno}: Required option `{option}` missing from command directive.")
        value = self.options[option]
        if not value:
            raise utils.MissingRequiredOption(f"{self._relative_path()}:{self.lineno}: Required option `{option}` cannot be empty in command directive.")
        return value

    def _command(self): 
        return self._check_and_get('command')

    def _executed_command(self):
        return self.options.get('executed-command')

    def _command_language(self):
        return self.options.get('command-language')

    def _output(self):
        return "\n".join(self.content)

    def _output_language(self):
        return self.options.get('language')

    def _has_output_block(self) -> bool:
        return utils.option_is_true(self.options, 'show-output')

    def _relative_path(self):
        return self.env.doc2path(self.env.docname, base=False) # Path relative to conf.py

    def _name(self):
        return self._check_and_get('name')

    def _example(self):
        return self._check_and_get('example')

    def _capture_stdout(self):
        return utils.option_is_true(self.options, 'capture-stdout')
    
    def _capture_stderr(self):
        return utils.option_is_true(self.options, 'capture-stderr')

    def _filter(self):
        return self.options.get('filter')

    def _command_snippet(self) -> CodeSnippet:
        return CodeSnippet(
            contents = self._command(),
            actual = self._executed_command(),
            language = self._command_language(),
            path = self._relative_path(),
            line = self.lineno,
        )

    def _output_snippet(self) -> CodeSnippet:
        return CodeSnippet(
            contents = self._output(), 
            language = self._output_language(),
            path = self._relative_path(),
            line = self.lineno,
        )

    def to_command(self) -> 'command':
        with open(f"log.txt", "a") as logger:
            logger.write(f"@ {self.options}\n")
            logger.write(f">> {self.env.docname}\n")
            logger.write(f">>> {self.env.doc2path(self.env.docname)}\n")    

        command_node = command(
            example = self._example(),
            name = self._name(),
            command = self._command_snippet(),
            output = self._output_snippet(),
            capture_stderr = self._capture_stderr(),
            capture_stdout = self._capture_stdout(),
            filter = self._filter(),
        )

        return command_node

    def to_nodes(self) -> 'list[Node]':
        command = self.to_command()
        code_blocks = command.to_nodes()
        return [ command ] + code_blocks

    def run(self) -> 'list[Node]':
        return self.to_nodes() 

class command(docutils.nodes.General, docutils.nodes.Element):
    def __init__(self, example, name, command: CodeSnippet, output: CodeSnippet, filter: str = None, capture_stdout: bool = True, capture_stderr: bool = True, show_output: bool = True):
        self.example = example
        self.name = name
        self.command = command
        self.output = output
        self.filter = filter
        self.capture_stdout = capture_stdout
        self.capture_stderr = capture_stderr

        super(docutils.nodes.General, self).__init__()
        super(docutils.nodes.Element, self).__init__()       

    @classmethod
    def visit(node_class, translator, node):
        pass

    @classmethod
    def depart(node_class, translator, node):
        pass

    def __str__(self) -> str:     
        return self.__repr__()  

    def __repr__(self) -> str:    
        def snippet_to_str(name, snippet) -> str:
            props = [
                ('language', snippet.language()),
                ('location', snippet.location()),
                ('contents', snippet.contents()),
                ('actual', snippet.actual()),
            ]
            displayed_props = [ f'{name}="{utils.quoted(prop)}"' for (name, prop) in props if prop != None ]
            return f'<{name} {" ".join(displayed_props)}/>'

        subnodes = [
            snippet_to_str('command', self.command),
            snippet_to_str('output', self.output),
        ]

        props = [
            ('example', self.example),
            ('capture-stderr', self.capture_stderr),
            ('capture-stdout', self.capture_stdout),
            ('filter', self.filter)
        ]
        displayed_props = [ f'{name}="{utils.quoted(prop)}"' for (name, prop) in props if prop != None ]
        
        return f'<ptest:command {"".join(displayed_props)}>{"".join(subnodes)}</ptest:command>'

    def to_nodes(self) -> 'list[Node]':
        def with_classes(node: 'Node', *classes) -> 'Node':
            utils.attach_classes(node, *classes)
            return node

        container = with_classes(docutils.nodes.container(), "ptest")
        container += [ with_classes(node, "ptest-command-block") for node in self.command.to_nodes() ]
        container += [ with_classes(node, "ptest-output-block") for node in self.output.to_nodes() ]

        return container

    def to_executable(self) -> 'str':
        warning = f"""
        # WARNING! THIS FILE IS AUTOMATICALLY GENERATED
        # 
        # This file is part of an automatically-generated executable ptests example
        # found at location: 
        #
        #    {self.command.location()}
        #
        # To edit this file, update the example in the documentation (and the
        # surrounding text). To re-generate the file, run:
        #
        #    make clean ptests
        #
        """

        optional_addendum = f"""
        # The command executed by the script differs from the command displayed in the
        # documentation. The command displayed in the documentation is:
        #
        #    {self.command.displayed_contents()}
        #
        """

        about_oracle = f"""
        # The script is a part of the following PTESTS files:
        #
        #    {self.command.path()}/{self.example}/{self.name}.ptests   
        #    {self.command.path()}/{self.example}/{self.name}.oracle   
        #  
        """

        sections = []
        sections += [ utils.prefix_strip(warning, True) ]
        if self.command.actual_contents_are_different_than_displayed_contents():
            sections += [ utils.prefix_strip(optional_addendum, True) ]
        sections += [ utils.prefix_strip(about_oracle, True) ]
        sections += [ os.linesep, self.command.actual() ]

        return "".join(sections)

    def to_ptest(self) ->str:
        comment = f"""
        COMMENT: This EXECNOW corresponds to command:
        COMMENT:
        COMMENT:    {self.command.displayed_contents()}
        COMMENT:
        COMMENT: Located in the documentation at location:
        COMMENT:
        COMMENT:    {self.command.location()}
        COMMENT:
        """

        # TODO extract method
        directory_path = os.path.join("build", "ptests", self.example)

        # TODO extract method
        extension = utils.language_to_extenstion(self.command.language())
        filename = f"{self.name}.{extension}"
        filepath = os.path.join(directory_path, filename)

        log_file = f"{self.command.path()}/{self.example}/{self.name}.log"
        interpreter = utils.language_to_interpreter(self.command.language())

        execnow = " ".join([
            f"EXECNOW:",
            f"LOG {log_file}",
            f"{interpreter} \"{filepath}\"",
            f"2> {log_file}",
            f"1> {log_file}",
        ])

        sections = [
            utils.prefix_strip(comment, True), 
            execnow,
            "\n",
        ]
        
        return "".join(sections)