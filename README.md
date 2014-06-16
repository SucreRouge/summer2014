# Linear Temporal Logic to Büchi Automaton Translation in OCaml

Based on [Specification and Verification using Temporal Logics](citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.217.7298) by Stéphane Demri & Paul Gastin.

Provides a basic tool for the translation of LTL expressions into Büchi Automaton Acceptors with the goal of program specification and synthesis.

## LTL Syntax
In order to reduce the size and complexity of the resulting automata the standard syntax of temporal logic was extended with several redundant notations to include:

The standard operators for propositional logic: AND, OR, NOT
The basic notions of linear temporal logic: X (next), U (until) as well as:
* F p := true U p
* G p := not F not p
* a R b := not (not a U not b)

## Graph Output
When run the program produces a visual representation of the resulting automaton in png format. Each state is represented by a node labelled with a set of formulas which have not yet been satisfied. Transitions are represented by labelled edges where the label is a positive boolean expression over the atoms and their complements. The start state is denoted by an ungrounded arrow and accepting states are doubly circled.

## Usage
```sh
$ ./build
$ ltl2ba <ltl expression> <out file>
$ eog <out file>
```