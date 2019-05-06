import os

c = c  # pylint:disable=undefined-variable
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = int(os.getenv('PORT', 8888))
c.NotebookApp.open_browser = False
c.NotebookApp.allow_password_change=False
c.NotebookApp.password = os.getenv('PASSWORD', '')
c.NotebookApp.token = os.getenv('PASSWORD', '')

