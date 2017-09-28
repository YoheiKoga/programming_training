from ipykernel.kernelbase import Kernel
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import urllib, base64

def _to_png(fig):
    """Return a base64-encoded PNG from a
    matplotlib figure."""
    imgdata = BytesIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)
    return urllib.parse.quote(
        base64.b64encode(imgdata.getvalue()))

_numpy_namespace = {n: getattr(np, n) for n in dir(np)}

def _parse_function(code):
    """Return a NumPy function from a string 'y=f(x)'."""
    return lambda x: eval(code.split('=')[1].strip(), _numpy_namespace, {'x': x})

class PlotKernel(Kernel):
    implementation = 'Plot'
    implementation_version = '1.0'
    banner = "Simple plotting"
    language_info = {
        'name': 'python',
        'version': '',
        'file_extension': '.plot',
        'mimetype': 'text/x-python'
    }
    language = language_info['name']
    language_version = language_info['version']
    
    def do_execute(self, code, silent,
                  store_history=True,
                  user_expressions=None,
                  allow_stdin=False):
        
        fig = plt.figure(figsize=(6,4), dpi=100)
        x = np.linspace(-5., 5., 200)
        functions = code.split('\n')
        for fun in functions:
            f = _parse_function(fun)
            y = f(x)
            plt.plot(x, y)
        plt.xlim(-5, 5)
        
        png = _to_png(fig)
        
        if not silent:
            self.send_response(self.iopub_socket,
                              'stream', {
                                  'name': 'stdout',
                                  'data': 'Plotting {n} function(s)'. \
                                      format(n=len(functions))
                              })
            
            content = {
                'source': 'kernel',
                
                'data': {
                    'image/png': png
                },
                
                'metadata': {
                    'image/png': {
                        'width': 600,
                        'height': 400
                    }
                }
            }
            
            self.send_response(self.iopub_socket, 'display_data', content)
        
        return {'status': 'ok',
               'execution_count': self.execution_count,
               'payload': [],
               'user_expressions': {},
               }

if __name__ == '__name__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=PlotKernel)