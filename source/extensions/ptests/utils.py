def attach_classes(node: 'docutils.nodes.Node', *classes: 'list[str]'):
    node.update_basic_atts({
        'classes': classes
    })

def option_is_true(options, key: str):
    return options.get(key, "true").strip().lower() == "true"

def prefix_strip(string: str, remove_empty_lines_from_beginning: bool):
    import os
    if remove_empty_lines_from_beginning:
        output = []
        drop = True
        for line in string.splitlines():
            if drop and line.strip() == "":
                output
            else:
                drop = False
                output.append(line.lstrip())
        return os.linesep.join(output)
    else:
        return os.linesep.join([line.lstrip() for line in string.splitlines()])

class DuplicateRegistryKey(Exception):
    pass

class UnknownRegistryKey(Exception):
    pass

# TODO trancation
def register(env, registry, name, element):
    if not hasattr(env, registry):
        setattr(env, registry, {})
    registry = getattr(env, registry)
    registry[name] = element

# TODO trancation
def register_unique(env, registry, name, element):
    if not hasattr(env, registry):
        setattr(env, registry, {})
    registry = getattr(env, registry)
    if name in registry:
        raise DuplicateRegistryKey(name)
    registry[name] = element

# TODO transaction
def get_registered(env, registry) -> dict:
    if not hasattr(env, registry):
        setattr(env, registry, {})
    return getattr(env, registry)

class MissingRequiredOption(Exception):
    pass

# TODO move to sphinx env
languages = {
    'bash': {
        'interpreter': 'bash',
        'extension': 'sh',
    }
}

# TODO move to command
def language_to_extenstion(language) -> str:
    language = language.lower()
    return languages.get(language, language)['extension']

# TODO move to command
def language_to_interpreter(language) -> str:
    language = language.lower()
    return languages.get(language, language)['interpreter']

def ignore_node(translator, node):
    pass

def quoted(s: str) -> str:
    return str(s).replace('"','\\"').replace('\n','\\n')