import subprocess
import csv
import os

def setupProjects():
    """
    Read the text file containing the list of projects and their flags, and save it for local usage
    """
    global data
    global original_data
    data = []
    original_data = []
    with open("/DyPyBench/text/github-url.txt", "r") as csv_file:
        csvReader = csv.reader(csv_file, delimiter=" ")
        for index, row in enumerate(csvReader):
            temp=[]
            temp.append(index + 1)
            temp.append(row[0].split("/")[-1].split(".git")[0])
            temp.append(row[0])
            data.append(temp)
            original_data.append(row)

def get_project_name(proj_no:int) -> str:
    """
    Get project name from project number as shown in the list

    Args:
        proj_no (int): Project Number

    Returns:
        str: Project Name
    """
    for value in data:
        no, name, _ = value
        if(proj_no == no):
            return name

def get_project_no(proj_name:str) -> str:
    """
    Get project number from project name as shown in the list

    Args:
        proj_name (str): Project Name

    Returns:
        str: Project Number in String format
    """
    for value in data:
        no, name, _ = value
        if(proj_name == name):
            return str(no)

"""
Utility for overwriting the test files
"""
if __name__ == '__main__':

    setupProjects()
    path = '/DyPyBench/overwrite_files' # pick files from here for overwriting
    override_folder = os.listdir(path)

    # for each directory in overwrite folder, replace the original files
    for dir in override_folder:
        p1 = os.path.join(path, dir) 
        p2 = '/DyPyBench/../Project/project' + get_project_no(dir)
        command = 'cp -r ' + p1 + '/. ' + p2 + '/.'
        print(command)
        output = subprocess.run([command
            ], shell=True, stderr=subprocess.STDOUT)
