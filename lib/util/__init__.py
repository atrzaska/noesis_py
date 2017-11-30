import os

def logNotImplementedMethod(name, args):
    if os.environ.get('DEBUG') == 'true':
        print("Not implemented method called: " + name, args)

def last(arr):
    return arr[-1] if len(arr) > 0 else None
