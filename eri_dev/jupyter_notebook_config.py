import os
from IPython.lib import passwd
from IPython.lib.security import hashlib

c = c  # pylint:disable=undefined-variable
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = int(os.getenv('PORT', 8888))
c.NotebookApp.open_browser = False

# sets a password if PASSWORD is set in the environment
if 'PASSWORD' in os.environ:
    password = os.environ['PASSWORD']
    salt = str(os.getenv('PORT', 8888))
    if password:
        c.NotebookApp.password = passwd(password)
        h = hashlib.new('sha1')
        h.update(password.encode() + salt.encode())
        c.NotebookApp.token = h.hexdigest()
    else:
        c.NotebookApp.password = ''
        c.NotebookApp.token = ''
    del os.environ['PASSWORD']
