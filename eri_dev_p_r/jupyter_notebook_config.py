import os

c = c  # pylint:disable=undefined-variable
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = int(os.getenv('PORT', 8888))
c.NotebookApp.open_browser = False
c.NotebookApp.allow_password_change=False

# sets a password if PASSWORD is set in the environment
if 'PASSWORD' in os.environ:
    c.NotebookApp.password = os.environ['PASSWORD']

if 'JUPYTERTOKEN' in os.environ:
    c.NotebookApp.password = os.environ['JUPYTERTOKEN']

