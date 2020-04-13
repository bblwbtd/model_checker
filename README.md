# Model Checker

## Introduction

Inspired by this [paper](https://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CJFQ&dbname=CJFDLAST2019&filename=RJXB201909004&v=MTczOTBkc0Z5L21WTHJMTnlmVGJMRzRIOWpNcG85RllJUjhlWDFMdXhZUzdEaDFUM3FUcldNMUZyQ1VSN3FmWSs=)
,which indicates that the contract in our real-life can be converted into the smart contract. At the end of this paper, it
purposes that the next step of their work is making a visual tool for building models. So this project is a simple 
demonstration of this kind of tool and supports users to verify their model.

## Installation
1. Make sure that [python3](https://www.python.org) has already installed on your computer properly.
2. Clone this project and get into the project directory.
3. Run `pip3 install pipenv` if you don't have pipenv.
4. Run `pipenv install` to install dependence.
5. Run `pipenv run python3 Main.py` to start the program.

## Usage

### Add Template
1. Click 'Add Template' button on the left of the page.
2. Enter the template name.
3. Click add template variables. The program support part of the basic variable type of python3
4. Click add states and enter the state name and code.
5. Click add events and enter the event name and code.
6. Enter the validator code.
7. Click save button at the lower right corner.

### Template verification
1. Select the template.
2. Change the initial value of variables.
3. Click the run button at the lower right corner. Then you will see the report.

### About coding
There are several places that need python code to control the model. In the code, you can access the 
[model](https://github.com/bblwbtd/model_checker/blob/master/src/model_checker/MagicTemplate.py) 
by using `model` variable. So you can alter the variable of the model or invoke the function of the model 
or monitor the running status of the model. If the code discovers something wrong, just raise an exception and the program 
will catch it and add to the report.In this way, the program can discover logic vulnerabilities.

## Warning
This program is only designed for personal study and research. It has execution vulnerabilities due to the use of build-in
`exec()` function.