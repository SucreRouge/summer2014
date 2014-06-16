# Linear Temporal Logic to Büchi Automaton Translation in OCaml

Based on [Specification and Verification using Temporal Logics](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.217.7298) by Stéphane Demri & Paul Gastin.

Provides a basic tool for the translation of LTL expressions into Büchi Automaton Acceptors with the goal of program specification and synthesis.

## Usage
```sh
$ ./build
$ ltl2ba <ltl expression> <out file>.dot
$ dot -Tpng -o <out file>.png <out file>.dot
```