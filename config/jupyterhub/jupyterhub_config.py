c.JupyterHub.port = 8001
c.JupyterHub.proxy_api_port = 8003
c.Authenticator.admin_users = {'pfe'}
c.NotebookApp.allow_origin = '*'
c.JupyterHub.admin_access = True
c.NotebookApp.terminals_enabled = False
c.LatexConfig.run_times = 2
c.LatexConfig.latex_command = 'pdflatex'
