# Learning Preferences with Asprin
An answer set programming (ASP) system for learning preferences.

### Dependencies
***
clingo: https://potassco.org/clingo/ python3: https://www.python.org/downloads/

### Overview
***
Given as input: 
	- a list of examples pairs as facts with labels (file name containing the substring "examples")
	- a file detailing the domain of the input facts (file name containing substring "domain")
	- a library containing preference type definitions (file name containing substring "lib")
	-  choice rule(s) specifying the potential preference types and instances to choose from (file name containing substring "generation")

The system outputs: 
	- the learned preference statement(s) that best fits the input data. 

### Usage
*** 
`python3 asprin_learn6.lp <domain.lp> <examples.lp> <generation.lp> <lib.lp> <backend.lp>` 