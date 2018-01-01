import os

def logNotImplementedMethod(name, args):
    if os.getenv('DEBUG') == 'true':
        print("Not implemented method called: " + name, args)

def last(arr):
    return arr[-1] if len(arr) > 0 else None

def dump(path, data):
    handle = open(path, 'wb')
    handle.write(data)
    handle.close()
