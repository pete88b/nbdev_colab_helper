# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['IN_COLAB', 'setup_git', 'git_push', 'read_config', 'setup_project', 'init_notebook']

# Cell
IN_COLAB = 'google.colab' in str(get_ipython())

# Cell
import os, subprocess, urllib, shlex

def _run_commands(commands, password=None):
  "Run a list of commands making sure we mask `password` when printing commands"
  for cmd in commands:
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    output, err = process.communicate()
    if password: cmd = cmd.replace(password, '*****')
    print(cmd)
    if output or err:
      print('  ', output.decode('utf8').strip() if output else '', err or '')

def setup_git(git_url:str, git_branch:str, name:str, password:str, email:str):
  "Link your mounted drive to GitHub"
  password = urllib.parse.quote(password)
  _run_commands([
      f"git config --global user.email {email}",
      f"git config --global user.name {name}",
      f"git init",
      f"git remote rm origin",
      f"git remote add origin {git_url.replace('://git', f'://{name}:{password}@git')}",
      f"git pull origin {git_branch}", # TODO: do we need --allow-unrelated-histories?
      f"git checkout {git_branch}",
      f"git push --set-upstream origin {git_branch}"],
      password)

def git_push(git_branch:str, message:str):
  "Convert notebooks to scripts and then push to the library"
  _run_commands([
      f'nbdev_install_git_hooks',
      f'nbdev_build_lib',
      f'git add *', # TODO: allow specific files to be pushed
      f'git commit -m "{message}"',
      f'git push origin {git_branch}']) # TODO: show message when push fails!

# Cell
from configparser import ConfigParser
from pathlib import Path

def read_config(project_name):
  config_path = Path('/content/drive/My Drive/nbdev_colab_projects.ini')
  config = ConfigParser()
  config.read(config_path)
  if project_name not in config:
    print(f'Error: [{project_name}] section not found in {config_path}')
    print(f'Please add a section for [{project_name}] and run `setup_project` again')
    print('See https://pete88b.github.io/nbdev_colab_helper/core.html for details')
    return config, None
  return config, config[project_name]

# Cell
def setup_project(project_name):
  "Set-up the colab runtime for `project_name`"
  assert IN_COLAB, "You do not appear to be running in Colab"
  if not Path('/content/drive/My Drive').exists():
    print('Connecting to google drive')
    from google.colab import drive
    drive.mount('/content/drive')
  config, project_config = read_config(project_name)
  if project_config is None: return config, project_config
  project_path = Path(project_config['project_parent'])/project_name
  git_url, git_branch = project_config['git_url'], project_config['git_branch']
  if project_path.is_dir():
    print(f'Clone of {project_name} already exists in {project_path.parent}')
  else:
    project_path.parent.mkdir(parents=True, exist_ok=True)
    _run_commands([f'git clone {git_url} "{project_path}"'])
  get_ipython().magic(f'cd {project_path}')
  _run_commands(['pip install fastscript==1.0.0 fastcore==1.0.8 nbdev==1.0.14'])
  setup_git(git_url, git_branch, project_config['git_user_name'],
            project_config['git_user_password'], project_config['git_user_email'])
  return config, project_config

# Cell
def init_notebook(project_name):
  print('Connecting to google drive')
  from google.colab import drive
  drive.mount('/content/drive')
  config, project_config = read_config(project_name)
  if project_config is None: return config, project_config
  project_path = Path(project_config['project_parent'])/project_name
  get_ipython().magic(f'cd {project_path}')
  _run_commands(['pip install fastscript==1.0.0 fastcore==1.0.8 nbdev==1.0.14'])
  from nbdev.imports import Config
  get_ipython().magic(f'cd {Config().nbs_path}') # TODO is there a better way to know which dir the nb is in?
  # TODO: de-duplicate with setup_project
  # TODO: Read `requirements` section in `settings.ini` and install all reqs here

