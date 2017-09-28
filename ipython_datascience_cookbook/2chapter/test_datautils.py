from urllib.request import (HTTPHandler, install_opener, build_opener, addinfourl)
import os
import shutil
import tempfile
from io import StringIO
from datautils import download

TEST_FOLDER = tempfile.mkdtemp()
ORIGINAL_FOLDER = os.getcwd()

class TestHTTPHandler(HTTPHandler):
    """Mock HTTP handler."""
    def http_open(self, req):
        resp = addinfourl(StringIO('test'), '', req.get_full_url(), 200)
        resp.msg = 'OK'
        return resp

def setup():
    """install the mock HTTP handler for unit tests."""
    install_opener(build_opener(TestHTTPHandler))
    os.chdir(TEST_FOLDER)
    
def teardown():
    """Restore the normal HTTP handler."""
    install_opener(build_opener(HTTPHandler))
    # go back to the original folder.
    os.chdir(ORIGINAL_FOLDER)
    # delete the test folder.
    shutil.rmtree(TEST_FOLDER)


def test_download1():
    file = download("http://example.com/file.txt")
    # check that the file has been downloaded.
    assert os.path.exists(file)
    # check that the file contains the contents of the remote file
    with open(file, 'r') as f:
        contents = f.read()
    print(contents)
    assert contents == 'test'
def test_download2():
    file = download("http://example.com/")
    assert os.path.exists(file)