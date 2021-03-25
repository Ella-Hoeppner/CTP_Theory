# CTP_Theory
An implementation of CTP Theory, a Critical Rationalist approach to Artificial General Intelligence.

See [this blog post](https://www.ellahoeppner.com/ctp-theory-a-critical-rationalist-approach-to-agi/) for a description of CTP Theory.

This repository contains an implementation of CTP Theory using a format for A-Claims that consists of a boolean and a list of integers, stored together in a 2-tuple. A-Claims are defined to be contradictory if they have identical lists of integers and opposite boolean values.

The theory language that this implementation uses is defined in the language.py file. In the language, programs consist of lists of tuples of integers, where the first integer in each tuple indicates some instruction, and the rest of the integers in the tuple are arguments to the instruction. While a program in the language is running the program state consists of two elements: a stack of integers (called the int-stack) and a stack of either claims or lists of claims (called the claim-stack). Note: I call these elements "stacks", despite the fact that they are just implemented as python lists, because the theory language mostly treats them like stacks.

Some instructions require that the top element of the claim-stack be a claim, rather than a set of claims. When one of these claims is encountered, and the top element of the claim-stack is a list of claims, rather than just a claim, execution will be forked into multiple branches, one for each element in the list. In each branch, the top list of claims on the top of the claim-stack will be replaced with one of the elements in the list, so that each branch has a different claim on the top of its stack. Each path of execution then continues independently. The instructions that cause this kind of forking are listed in the "forking_functions" list in language.py.

The file tests.py contains four functions that demonstrate different aspects of this implementation's capabilities.
