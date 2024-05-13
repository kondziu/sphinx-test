import os
import itertools
# from docutils import nodes
# from docutils.parsers.rst import Directive
# from docutils.parsers.rst import directives
import docutils

import sphinx
# from sphinx import addnodes
# from sphinx.application import Sphinx
# from sphinx.directives import ObjectDescription
# from sphinx.domains import Domain, Index
# from sphinx.roles import XRefRole
# from sphinx.util.nodes import make_refnode
# from sphinx.application import Sphinx

from ptests.command import command
from ptests.example import example

from ptests import utils

class Builder(sphinx.builders.Builder): 
    name = 'ptests'
    # format = '.ptests'
    # file_suffix = '.ptests'
    # link_suffix = None  # defaults to file_suffix

    # @classmethod
    # def is_command(node):
    #     if node.tagname != "container":
    #         return False
        
    #     with open("build/ptests/log.txt", "a") as logger:
    #         logger.write(str(f"node {node.attributes}"))
        
    #     return 'ptest' in node.attributes['classes']

    def get_target_uri(self, docname, typ=None): 
        return docname + f".ptests"

    # def init(self):
    #     pass

    def prepare_writing(self, docnames):
        pass

    def get_outdated_docs(self):
        return "all documents"

    def write_doc(self, docname, doctree):
        # https://github.com/sphinx-contrib/restbuilder/blob/master/sphinxcontrib/builders/rst.py
        # https://github.com/sphinx-contrib/spelling/blob/51debaa98520145f6debce8f5a6c6d220359f54c/sphinxcontrib/spelling/builder.py#L34
        commands = list(doctree.findall(lambda node: isinstance(node, command)))
        examples = list(doctree.findall(lambda node: isinstance(node, example)))
        example_registry = utils.get_registered(self.env, 'ptest_examples')

        for node in commands:
            if not node.example in example_registry:
                raise utils.UnknownRegistryKey(f"{node.location}: Unknown example {node.example}")

            directory_path = os.path.join("build", "ptests", node.example)
            if not os.path.isdir(directory_path):
                os.makedirs(directory_path)

            extension = utils.language_to_extenstion(node.command.language())
            filename = f"{node.name}.{extension}"
            filepath = os.path.join(directory_path, filename)

            with open(filepath, "w") as logger:
                logger.write(f"{node.to_executable()}\n")        

        # TODO check if all the commands from one example sequence are in the same file

        sorted_commands = sorted(commands, key=lambda c: c.example)
        groupped_commands = itertools.groupby(sorted_commands, lambda c: c.example) 
        examples_and_commands = { exmpl: sorted(cmds, key = lambda c: c.command.location()) for exmpl, cmds in groupped_commands }

        x = open("xxx.txt", "w")
        x.write(str(sorted_commands))

        for exmpl_name, constituent_commands in examples_and_commands.items():
            exmpl = example_registry[exmpl_name]

            directory_path = os.path.join("build", "ptests", exmpl.name)
            if not os.path.isdir(directory_path):
                os.makedirs(directory_path)

            filename = f"{exmpl.name}.ptests"
            filepath = os.path.join(directory_path, filename)

            with open(filepath, "w") as logger:
                for cmd in constituent_commands:
                    logger.write(f"{cmd.to_ptest()}\n") # TODO


    def finish(self):
        pass
    
