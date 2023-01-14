import argparse
import subprocess
import csv
import os

parser = argparse.ArgumentParser()
parser.add_argument(
    "--list", "-l", action="store_true", help="List all the projects DyPyBench supports")
parser.add_argument(
    "--test", "-t", type=int, nargs='+', help="Specify the project number to run test suite of the project")
parser.add_argument(
    "--original", action="store_true", help="Run tests on original code")
parser.add_argument(
    "--save", "-s", type=str, help="Specify file name to save the stdout and stderr combined")

#subparsers = parser.add_subparsers()
#dynapyt_parser = subparsers.add_parser("dynapyt")
parser.add_argument(
    "--instrument", "-i", type=int, nargs='+', help="Specify the project no. to run DynaPyt instrumentation"
)
parser.add_argument(
    "--file", "-f", type=str, help="Specify the path to file containing the includes.txt file to run the instrumentation"
)
parser.add_argument(
    "--analysis", "-a", help="Specify DynaPyt analysis to run"
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
    with open("./text/github-url.txt", "r") as csv_file:
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
            if(project < 0 or project > 50):
                print("Project number should be between 1 and 50")
            else:
                proj_name = str(data[project - 1][1])
                proj_no = str(data[project - 1][0])
                proj_flags = str(original_data[project - 1][1])
                copy_folder = args.original
                if(proj_flags == "rt"):
                    proj_test_folder = str(original_data[project - 1][3])
                elif(proj_flags == "t"):
                    proj_test_folder = str(original_data[project - 1][2])
                elif(proj_flags == "r"):
                    proj_test_folder = ""
                
                if args.save:
                    output = subprocess.run(["./scripts/run-test.sh %s %s %s %s" %(proj_name, proj_no, proj_test_folder, copy_folder)
                    ], shell=True, stdout=open(args.save,'a+',1), stderr=subprocess.STDOUT)
                else:
                    output = subprocess.run(["./scripts/run-test.sh %s %s %s %s" %(proj_name, proj_no, proj_test_folder, copy_folder)
                    ], shell=True, capture_output=True)
                    #if output needs to be printed on the console then comment above and uncomment below
                    """output = subprocess.run(["./scripts/run-test.sh %s %s %s %s" %(proj_name, proj_no, proj_test_folder, copy_folder)
                    ], shell=True, stderr=subprocess.STDOUT)"""

    if args.instrument:
        projects = args.instrument
        for project in projects:
            if(project < 0 or project > 50):
                print("Project number should be between 1 and 50")
            else:
                proj_name = str(data[project - 1][1])
                proj_no = str(data[project - 1][0])
                instr_file = args.file
                analysis = args.analysis

                with open(instr_file, 'r') as inst_file:
                    csvReader = csv.reader(inst_file, delimiter=" ")
                    instr_details = {}
                    for row in csvReader:
                        project_no, flag, path = row
                        if project_no in instr_details.keys():
                            temp = instr_details[project_no]
                            temp.append(row)
                            instr_details[project_no] = temp
                        else:
                            instr_details[project_no] = [row]

                    if args.save:
                        output = subprocess.run(["./scripts/clear-project.sh %s %s" %(proj_name, proj_no)
                                ], shell=True, stdout=open(args.save,'a+',1), stderr=subprocess.STDOUT)
                    else:
                        output = subprocess.run(["./scripts/clear-project.sh %s %s" %(proj_name, proj_no)
                        ], shell=True, capture_output=True)
                        #if output needs to be printed on the console then comment above and uncomment below
                        """output = subprocess.run(["./scripts/clear-project.sh %s %s" %(proj_name, proj_no)
                        ], shell=True, stderr=subprocess.STDOUT)"""

                    for line in instr_details[proj_no]:
                        project_no, flag, path = line
                        if args.save:
                            output = subprocess.run(["./scripts/run-dynapyt-instrumentation.sh %s %s %s %s %s" %(proj_name, proj_no, path, analysis, flag)
                            ], shell=True, stdout=open(args.save,'a+',1), stderr=subprocess.STDOUT)
                        else:
                            output = subprocess.run(["./scripts/run-dynapyt-instrumentation.sh %s %s %s %s %s" %(proj_name, proj_no, path, analysis, flag)
                            ], shell=True, capture_output=True)
                            #if output needs to be printed on the console then comment above and uncomment below
                            """output = subprocess.run(["./scripts/run-dynapyt-instrumentation.sh %s %s %s %s %s" %(proj_name, proj_no, path, analysis, flag)
                            ], shell=True, stderr=subprocess.STDOUT)"""

    if args.run:
        projects = args.run
        for project in projects:
            if(project < 0 or project > 50):
                print("Project number should be between 1 and 50")
            else:
                proj_name = str(data[project - 1][1])
                proj_no = str(data[project - 1][0])
                analysis = args.analysis
                proj_flags = str(original_data[project - 1][1])
                if(proj_flags == "rt"):
                    proj_test_folder = str(original_data[project - 1][3])
                elif(proj_flags == "t"):
                    proj_test_folder = str(original_data[project - 1][2])
                elif(proj_flags == "r"):
                    proj_test_folder = ""

                if args.save:
                    # os.system("./scripts/run-dynapyt-analysis.sh %s %s %s %s >> %s 2>&1" %(proj_name, proj_no, analysis, proj_test_folder, args.save))
                    output = subprocess.run(["./scripts/run-dynapyt-analysis.sh %s %s %s %s" %(proj_name, proj_no, analysis, proj_test_folder)
                    ], shell=True, stdout=open(args.save,'a+',1), stderr=subprocess.STDOUT)
                else:
                    # os.system("./run-dynapyt-analysis.sh %s %s %s %s" %(proj_name, proj_no, analysis, proj_test_folder))
                    output = subprocess.run(["./scripts/run-dynapyt-analysis.sh %s %s %s %s" %(proj_name, proj_no, analysis, proj_test_folder)
                    ], shell=True, capture_output=True)
                    #if output needs to be printed on the console then comment above and uncomment below
                    """output = subprocess.run(["./scripts/run-dynapyt-analysis.sh %s %s %s %s" %(proj_name, proj_no, analysis, proj_test_folder)
                    ], shell=True, stderr=subprocess.STDOUT)"""
