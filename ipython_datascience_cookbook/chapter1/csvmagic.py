import pandas as pd
from io import StringIO

def csv(line, cell):
    sio = StringIO(cell)
    return pd.read_csv(sio)

def load_ipython_extension(ipython):
    """this is function is called when the extension
    is loaded. it accepts an
    IPython InteractiveShell instance.
    We can register the magic with the
    `register_magic_function` method.
    """
    ipython.register_magic_function(csv, 'cell')