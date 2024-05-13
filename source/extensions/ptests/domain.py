from typing import Iterable

import sphinx

from ptests.command import Command
from ptests.example import Example

class PTests(sphinx.domains.Domain):
    name = 'ptests'
    label = 'PTests Executable Examples'
    directives = {
        'command': Command,
        'example': Example,
    }
    initial_data = {
        'examples': []
    }
    
    def get_full_qualified_name(self, node):
        return f'{name}.{node.arguments[0]}'

    # Object descriptions are tuples with six items:
    #
    # 1. name: fully qualified name.
    # 2. dispname: name to display when searching/linking.
    # 3. type: object type, a key in self.object_types.
    # 4. docname: the document where it is to be found.
    # 5. anchor: the anchor name for the object.
    # 6. priority: how “important” the object is (determines placement in search
    #    results):
    #
    #    - 1   Default priority (placed before full-text matches).
    #    - 0   Object is important (placed before default-priority objects).
    #    - 2   Object is unimportant (placed after full-text matches).
    #    - -1  Object should not show up in search at all.
    #
    def get_objects(self) -> Iterable[tuple[str, str, str, str, str, int]]:
        yield from self.data['examples']