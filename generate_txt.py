import glob
import argparse
import os
import csv


parser = argparse.ArgumentParser()
parser.add_argument(
    "--dir", "-d", type=str, help="Specify directory to list all python files")
parser.add_argument(
    "--name", "-n", type=str, help="Specify project name")

def setupProjects():
    global data
    data = []
    with open("./text/github-url.txt", "r") as csv_file:
        csvReader = csv.reader(csv_file, delimiter=" ")
        for index, row in enumerate(csvReader):
            temp=[]
            temp.append(index + 1)
            temp.append(row[0].split("/")[-1].split(".git")[0])
            temp.append(row[0])
            data.append(temp)

def get_files(dir, name):
    files = []
    dir_content = os.listdir(dir)
    for content in dir_content:
        path = os.path.join(os.path.abspath(dir), content)
        if os.path.isdir(path):
            files_arr = get_files(path, name)
            for file_path in files_arr:
                files.append(file_path)
        elif path[-3:] == ".py":
            if not ( path.__contains__("/vm") or path.__contains__("/build") or path.__contains__("setup.py") or path.__contains__("config.py") or path.__contains__("conftest.py")) :
                with open('includes_lex.txt', 'a') as f:
                    f.write(name)
                    f.write(' ')
                    print(root_dir)
                    f.write(path.replace(os.path.abspath(root_dir), '.'))
                    f.write('\n')
                    files.append(path)
    return files

if __name__ == '__main__':
    setupProjects()
    global root_dir
    global number
    number = 0
    for value in data:
        no, name, _ = value
        number = no
        root_dir = '/DyPyBench/Project/project' + str(number)
        get_files('Project/project' + str(no), name)
