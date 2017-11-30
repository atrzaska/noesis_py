import os

def logNotImplementedMethod(name, args):
    if os.environ.get('DEBUG') == 'true':
        print("Not implemented method called: " + name, args)
