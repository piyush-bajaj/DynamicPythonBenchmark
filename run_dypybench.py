import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument(
    "--list", "-l", action="store_true", help="List all the projects DyPyBench supports")

def printAllProjects():
    print("{:<8} {:<20} {:<50}".format("Number", "Project Name", "Repository URL"))
    print("{:<8} {:<20} {:<50}".format("-------", "--------------", "---------------------------------"))
    for value in data:
        no, name, url = value
        print("{:<8} {:<20} {:<50}".format(no, name, url))

def setupProjects():
    global data
    global original_data
    data = []
    original_data = []
    with open("./github-url.txt", "r") as csv_file:
        csvReader = csv.reader(csv_file, delimiter=" ")
        for index, row in enumerate(csvReader):
            temp=[]
            temp.append(index + 1)
            temp.append(row[0].split("/")[-1].split(".git")[0])
            temp.append(row[0])
            data.append(temp)
            original_data.append(row)
