# Examples

```{ptests:example}
:name: my-example-2
:description: This is an example containing some commands.

This is a short description with additional test and **markup**.
```

```{ptests:command}
:example: my-example-2
:name: my-snippet-2
:command: cat "example.c"
:command-language: bash
:language: c

printf("Hello, world!\n");
````

```{ptests:command}
:example: my-example-2
:name: my-snippet-2
:command: gcc "example.c" && a.out
:command-language: bash
:language: none

Hello, world!
````
