import argparse
import subprocess
import csv

parser = argparse.ArgumentParser()
parser.add_argument(
    "--list", "-l", action="store_true", help="List all the projects DyPyBench supports")
parser.add_argument(
    "--test", "-t", type=int, nargs='+', help="Specify the project number to run test suite of the project")
parser.add_argument(
    "--save", "-s", type=str, help="Specify file name to save the stdout and stderr combined")

#subparsers = parser.add_subparsers()
#dynapyt_parser = subparsers.add_parser("dynapyt")
parser.add_argument(
    "--instrument", "-i", type=int, nargs='+', help="Specify the project no. to run DynaPyt instrumentation"
)
parser.add_argument(
    "--directory", "-d", help="Specify the directory path to run the instrumentation"
)
parser.add_argument(
    "--files", "-f", help="Specify the file path to run the instrumentation"
)
parser.add_argument(
    "--analysis", "-a", help="Specify DynaPyt analysis to run"
)
parser.add_argument(
    "--entry", "-e", help="Specify entry file DynaPyt analysis"
)
parser.add_argument(
    "--run", "-r", type=int, nargs='+', help="Specify the project no. to run DynaPyt Analysis"
)

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

if __name__ == '__main__':
    args = parser.parse_args()

    setupProjects()

    if args.list:
        printAllProjects()
    
    if args.test:
        projects = args.test
        for project in projects:
            if(project < 0 or project > 10):
                print("Project number should be between 1 and 10")
            else:
                proj_name = str(data[project - 1][1])
                proj_no = str(data[project - 1][0])
                proj_flags = str(original_data[project - 1][1])
                if(proj_flags == "rt"):
                    proj_test_folder = str(original_data[project - 1][3])
                elif(proj_flags == "t"):
                    proj_test_folder = str(original_data[project - 1][2])
                elif(proj_flags == "r"):
                    proj_test_folder = ""
                
                if args.save:
                    output = subprocess.run(["./run-test.sh %s %s %s" %(proj_name, proj_no, proj_test_folder)
                    ], shell=True, stdout=open(args.save,'w+',1), stderr=subprocess.STDOUT)
                else:
                    output = subprocess.run(["./run-test.sh %s %s %s" %(proj_name, proj_no, proj_test_folder)
                    ], shell=True, capture_output=True)
                    #if output needs to be printed on the console then comment above and uncomment below
                    """output = subprocess.run(["./run-test.sh %s %s %s" %(proj_name, proj_no, proj_test_folder)
                    ], shell=True, stderr=subprocess.STDOUT)"""
    
    if args.instrument:
        projects = args.instrument
        for project in projects:
            if(project < 0 or project > 10):
                print("Project number should be between 1 and 10")
            else:
                proj_name = str(data[project - 1][1])
                proj_no = str(data[project - 1][0])
                inst_dir = args.directory
                analysis = args.analysis

                if args.save:
                    output = subprocess.run(["./run-dynapyt-instrumentation.sh %s %s %s %s" %(proj_name, proj_no, inst_dir, analysis)
                    ], shell=True, stdout=open(args.save,'w+',1), stderr=subprocess.STDOUT)
                else:
                    output = subprocess.run(["./run-dynapyt-instrumentation.sh %s %s %s %s" %(proj_name, proj_no, inst_dir, analysis)
                    ], shell=True, capture_output=True)
                    #if output needs to be printed on the console then comment above and uncomment below
                    """output = subprocess.run(["./run-dynapyt-instrumentation.sh %s %s %s %s" %(proj_name, proj_no, inst_dir, analysis)
                    ], shell=True, stderr=subprocess.STDOUT)"""

    if args.run:
        projects = args.run
        for project in projects:
            if(project < 0 or project > 10):
                print("Project number should be between 1 and 10")
            else:
                proj_name = str(data[project - 1][1])
                proj_no = str(data[project - 1][0])
                entry_file = args.entry
                analysis = args.analysis
                proj_flags = str(original_data[project - 1][1])
                if(proj_flags == "rt"):
                    proj_test_folder = str(original_data[project - 1][3])
                elif(proj_flags == "t"):
                    proj_test_folder = str(original_data[project - 1][2])
                elif(proj_flags == "r"):
                    proj_test_folder = ""

                if args.save:
                    output = subprocess.run(["./run-dynapyt-analysis.sh %s %s %s %s %s" %(proj_name, proj_no, entry_file, analysis, proj_test_folder)
                    ], shell=True, stdout=open(args.save,'w+',1), stderr=subprocess.STDOUT)
                else:
                    output = subprocess.run(["./run-dynapyt-analysis.sh %s %s %s %s %s" %(proj_name, proj_no, entry_file, analysis, proj_test_folder)
                    ], shell=True, capture_output=True)
                    #if output needs to be printed on the console then comment above and uncomment below
                    """output = subprocess.run(["./run-dynapyt-analysis.sh %s %s %s %s %s" %(proj_name, proj_no, entry_file, analysis, proj_test_folder)
                    ], shell=True, stderr=subprocess.STDOUT)"""
