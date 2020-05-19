import sys
import os
from IPython.display import HTML, display
import nbformat

# Collecting the Command Line Inputs

Where = sys.argv[1] # OPTIONS: code, markdown, heading, heading_pp, property, all 

if Where == 'all': # If you selected "all" you want a list of all of the files in the directory 
    if len(sys.argv) == 3: # If a root is not given the root is assumed to be the current dir.
        root = sys.argv[2]
    else:
        root = '.'
        
if Where == 'heading_pp': # This is if you want a pretty print output of the headings in a notebook
    file_name = sys.argv[2]
        
if Where != 'all' and 'heading_pp':
    root = sys.argv[2]
    string_pattern = sys.argv[3:]

if Where == 'property':
    x = ''.join(string_pattern)
    if 'and' in x:
        List_of_desired_props = x.split('and')
    else:
        List_of_desired_props = string_pattern

    
# Some helpful functions

def search_util(root='.'):
    """Recursively find all ipynb files in a directory.
    root - This is the directory you would like to find the files in, defaults to cwd""" 
    nb_files = []
    for r, d, f in os.walk(root):
        for file in f:
            if file.endswith('.ipynb') and 'checkpoint.ipynb' not in file:
                nb_files += [os.path.join(r, file)]
    return nb_files

def show_files(nb_files):
    [display(HTML(f'<a href="{f}">{f}</a>')) for f in nb_files]

def search_notebook_util(pattern,cell_type,root='.'):
    """ This function searches all the markdown or code cells  
    in the notebooks in the directory and returns the notebooks
    that include the patter input in one or more of the markdown 
    or code cells"""
    
    files = search_util(root)
    file_list = []
    for file in files:
        nb = nbformat.read(file,as_version=4)
        for i in nb['cells']:
            if i['cell_type'] == cell_type:
                text = i['source']
                if pattern in text:
                    file_list.append(file)
                    break
    return file_list

def search_heading_util(pattern,root):
    import nbformat
    
    files = search_util(root)
    file_list = []
    for file in files:
        nb = nbformat.read(file,as_version=4)
        for i in nb['cells']:
            if i['cell_type'] == 'markdown':
                text = i['source']
                for i in text.split('\n'):
                    try:
                        if i.strip()[0] == '#' and pattern in i:
                            file_list.append(file)
                            break
                    except:
                        None
    return set(file_list)

def heading_list(file):
    """ This function searches all the headings in the notebooks 
    in the directory and returns the notebooks that include the patter 
    input in one or more of the markdown cells"""
    import nbformat

    heading_list = []

    nb = nbformat.read(file,as_version=4)
    for i in nb['cells']:
        if i['cell_type'] == 'markdown':
            text = i['source']
            for i in text.split('\n'):
                try:
                    if i.strip()[0] == '#':
                        heading_list.append(i.strip())
                except:
                    None
    return heading_list

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def pretty_print_headings(heading_list):
    for i in heading_list:
        heading_level = len(i.strip().split()[0])
        print(color.BOLD + color.GREEN + '\t'*(heading_level-1) + f'{i.strip()[heading_level+1:]}\n' + color.END)
       
def search_data_util(props,root='.'):
    """ This function searches the properties cells of the HER notebooks for specific"""
    
    requirements = len(props)
    
    files = search_util(root)
    file_list = []
    for file in files:
        nb = nbformat.read(file,as_version=4)
        for i in nb['cells']:
            if i['cell_type'] == 'code':
                if i['source'].startswith('%%properties'):
                    Metal_A = i['source'].split('\n')[1].split()[-1]
                    Metal_B = i['source'].split('\n')[2].split()[-1]
                    Max_H = float(i['source'].split('\n')[3].split()[-1])
                    require = 0
                    for prop in props:
                        if '<' in prop:
                            if Max_H < float(prop.split('<')[-1].strip()):
                                require += 1
                        elif '>' in prop:
                            if Max_H > float(prop.split('>')[-1].strip()):
                                require += 1
                        else: # Assumed the user entered a metal name
                            if prop.upper() == Metal_A.upper() or prop.upper() == Metal_B.upper():
                                require += 1
                    if require == requirements:
                        file_list.append(file)
                        break
    return file_list


# The Main Functions 

def search_files(root='.'):
    nb_files = search_util(root)
    show_files(nb_files)
    
def search_notebook(string_pattern,cell_type,root='.'):
        """ Cell_type can be 'code' or 'markdown' """
        nb_files = search_notebook_util(string_pattern,cell_type,root)
        show_files(nb_files)
        
def search_heading(pattern,root='.'):
    """ This function searches all the headings in the notebooks 
    in the directory and returns the notebooks that include the patter 
    input in one or more of the markdown cells"""
    nb_files = search_heading_util(pattern,root)
    show_files(nb_files)

def headings_pprint(file):
    """ This function produces an indented (based on heading level) "pretty print" of the headings in the file given """
    List = heading_list(file)
    pretty_print_headings(List)

def search_data(props,root='.'):
    """ This function searches all the headings in the notebooks 
    in the directory and returns the notebooks that include the patter 
    input in one or more of the markdown cells"""
    nb_files = search_data_util(props,root)
    show_files(nb_files)

# --------------------------------------------------------------------------------
if Where == 'all': # If you selected "all" you want a list of all of the files in the directory 
    search_files(root)
elif Where == 'code' or Where == 'markdown':
    search_notebook(string_pattern[0],Where,root)
elif Where == 'heading':
    search_heading(string_pattern[0],root)
elif Where == 'heading_pp':
    headings_pprint(file_name)
elif Where == 'property':
    search_data(List_of_desired_props,root)
    