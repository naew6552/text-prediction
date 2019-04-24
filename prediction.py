'''
prediction.py
Written by: Nate Ewan

This is a python program that will fulfill a couple functions. It can be used as
a command line utility to generate sentences, take in corpuses, and run accuracy
tests on a langauge prediction model. It can also be run as a CLI utility, where
when using tab-complete, the model will try to predict the next world you will
type.

CLI Arguments:
    - t
    - c

'''
import readline


def read_cli():
    print("Enter 'quit' to quit")
    while True:
        text = input()
        if text == "quit":
            break


#def completer(text, state):
#    options = [i for i in commands if i.startswith(text)]
#    if state < len(options):
#        return options[state]
#    else:
#        return None

#def completer(text, state):
#    return "test"

def completer(text,state):
    results = ["example",None]
    return results[state]

readline.set_completer(completer)
readline.parse_and_bind('tab: complete') #set the parser to use tab complete
read_cli()
