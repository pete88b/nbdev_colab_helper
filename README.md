# nbdev / colab helper
> Tools and tutorials to help working with nbdev in google colab.


## Install in colab

Run the following code cell in a colab notebook:

`!pip install git+https://github.com/pete88b/nbdev_colab_helper.git`

TODO: Create pip package or move to nbdev?

## How to use

The goal of this project is to make it as easy as possible to work with nbdev and github without leaving colab.
 
## Regular nbdev notebooks
 
As you can see from [this notebook](https://github.com/pete88b/nbdev_colab_helper/blob/master/00_core.ipynb), you don't have to `!pip install nbdev` in every notebook.
 
You can use the following pattern to avoid running colab specific things in non-colab environments, like mounting your google drive:
 
```python
IN_COLAB = 'google.colab' in str(get_ipython())
if IN_COLAB:
  from google.colab import drive
```
 
or installing nbdev:
 
```python
if IN_COLAB:
  !pip install git+https://github.com/fastai/nbdev.git
```
 
Now that nbdev is available to the runtime, you can `from nbdev import *` and start using [magic flags](https://pete88b.github.io/fastpages/nbdev/fastai/jupyter/2020/06/02/nbdev-magic.html), `show_doc` etc.
 
## The colab helper notebook
 
Having a colab helper notebook gives you a place to do the things you would do from the command line in a non-colab environment (like running nbdev or git commands). Feel free to use [this notebook](https://colab.research.google.com/github/pete88b/nbdev_colab_helper/blob/master/_colab_helper.ipynb) as a starter.
 
Before we can run nbdev or git commands in a colab helper notebook, we need to set-up the colab runtime via a call to `nbdev_colab_helper.core.setup_project`.
 
After mounting your google drive to `/content/drive`, `setup_project` looks for `/content/drive/My Drive/nbdev_colab_projects.ini`: which must have a section for the project you are setting up.
 
**Warning:** Your nbdev_colab_projects.ini should live outside your nbdev projects. Please don't share this file, or push to githib etc
 
Here's an example `nbdev_colab_projects.ini` with sections for 2 projects:
 
```
[DEFAULT]
project_parent = /content/drive/My Drive/Colab Notebooks/github
 
git_user_name = **changeme**
git_user_email = **changeme**@gmail.com
git_user_password = **changeme**
 
[nbdev_colab_helper]
git_url = https://github.com/pete88b/nbdev_colab_helper.git
git_branch = master
 
[nbdev_demo]
git_url = https://github.com/pete88b/nbdev_demo.git
git_branch = main
```
 
See [ConfigParser](https://docs.python.org/3/library/configparser.html) for details on how this file can be formatted.
 
The name of the colab helper notebook is not important and it doesn't have to be part of your nbdev project - you could manage any number of nbdev projects from a single colab helper notebook.
