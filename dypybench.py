import argparse
import subprocess
import csv

# argparse for arguments

parser = argparse.ArgumentParser()
parser.add_argument(
    "--list", "-l", action="store_true", help="List all the projects DyPyBench supports"
)

parser.add_argument(
    "--timeout", type=int, help="Specify timeout to be used in seconds for execution of subprocesses", default=(60*10) # default to 60 mins
)

parser.add_argument(
    "--test", "-t", type=int, nargs='+', help="Specify the project number to run the test suite"
)

parser.add_argument(
    "--test_original", "-to", action="store_true", help="Run tests on original code"
)

parser.add_argument(
    "--save", "-s", type=str, help="Specify file name to save the stdout and stderr combined"
)

parser.add_argument(
    "--update_dynapyt_source", action="store_true", help="get dynapyt source code"
)

parser.add_argument(
    "--update_lex_source", action="store_true", help="get LExecutor source code"
)

parser.add_argument(
    "--dynapyt_instrument", "-di", type=int, nargs='+', help="Specify the project no. to run DynaPyt instrumentation"
)

parser.add_argument(
    "--dynapyt_file", "-df", type=str, help="Specify the path to file containing the includes.txt file to run the instrumentation"
)

parser.add_argument(
    "--dynapyt_analysis", "-da", help="Specify DynaPyt analysis to run"
)

parser.add_argument(
    "--dynapyt_run", "-dr", type=int, nargs='+', help="Specify the project no. to run DynaPyt Analysis"
)

parser.add_argument(
    "--lex_instrument", "-li", type=int, nargs='+', help="Specify the project no. to run LExecutor instrumentation"
)

parser.add_argument(
    "--lex_file", "-lf", type=str, help="Specify the path to file containing the includes.txt file to run the instrumentation"
)

parser.add_argument(
    "--lex_test", "-lt", type=int, nargs='+', help="Specify the project no. to run test suite for LExecutor"
)

parser.add_argument(
    "--pycg", "-scg", type=int, nargs='+', help="Specify the project no. to run PyCG for static call graph generation"
)

def printAllProjects():
    """
    Pretty print the list of all the projects in the benchmark.
    """
    print("{:<8} {:<20} {:<50}".format("Number", "Project Name", "Repository URL"))
    print("{:<8} {:<20} {:<50}".format("-------", "--------------", "---------------------------------"))
    for value in data:
        no, name, url = value
        print("{:<8} {:<20} {:<50}".format(no, name, url))

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
Main code for DyPyBench
"""
if __name__ == '__main__':
    args = parser.parse_args()

    # setup project data for use with every option of benchmark
    setupProjects()

    # list the projects in benchmark
    if args.list:
        printAllProjects()

    # update DynaPyt source code
    if args.update_dynapyt_source:
        # print("Downloading the dynapyt source from git")
        if args.save:
            output = subprocess.run(["/DyPyBench/scripts/setup-DynaPyt-src.sh"
            ], shell=True, stdout=open(args.save,'a+',1), stderr=subprocess.STDOUT)
        else:
            output = subprocess.run(["/DyPyBench/scripts/setup-DynaPyt-src.sh"
            ], shell=True, capture_output=True)
            #if output needs to be printed on the console then comment above and uncomment below
            """output = subprocess.run(["/DyPyBench/scripts/setup-DynaPyt-src.sh"
            ], shell=True, stderr=subprocess.STDOUT)"""

    # update Lexecutor source code
    if args.update_lex_source:
        # print("Downloading the LExecutor source from git")
        if args.save:
            output = subprocess.run(["/DyPyBench/scripts/setup-LExecutor-src.sh"
            ], shell=True, stdout=open(args.save,'a+',1), stderr=subprocess.STDOUT)
        else:
            output = subprocess.run(["/DyPyBench/scripts/setup-LExecutor-src.sh"
            ], shell=True, capture_output=True)
            #if output needs to be printed on the console then comment above and uncomment below
            """output = subprocess.run(["/DyPyBench/scripts/setup-LExecutor-src.sh"
            ], shell=True, stderr=subprocess.STDOUT)"""

    # execute tests in benchmark
    if args.test:
        projects = args.test
        if 0 in projects: # execute for all projects in case 0 is provided
            projects = [x for x in range(1,51)]
        for project in projects:
            if(project < 0 or project > 50):
                print("Project number should be between 1 and 50")
            else:
                proj_name = str(data[project - 1][1])
                proj_no = str(data[project - 1][0])
                proj_flags = str(original_data[project - 1][1])
                copy_folder = args.test_original # check if tests to be done on the original folder
                if(proj_flags == "rt"):
                    proj_test_folder = str(original_data[project - 1][3])
                elif(proj_flags == "t"):
                    proj_test_folder = str(original_data[project - 1][2])
                elif(proj_flags == "r"):
                    proj_test_folder = ""

                if args.save:
                    output = subprocess.run(["/DyPyBench/scripts/run-test.sh %s %s %s %s %s" %(proj_name, proj_no, proj_test_folder, copy_folder, args.timeout)
                    ], shell=True, stdout=open(args.save,'a+',1), stderr=subprocess.STDOUT, timeout=args.timeout)
                else:
                    output = subprocess.run(["/DyPyBench/scripts/run-test.sh %s %s %s %s %s" %(proj_name, proj_no, proj_test_folder, copy_folder, args.timeout)
                    ], shell=True, capture_output=True, timeout=args.timeout)
                    #if output needs to be printed on the console then comment above and uncomment below
                    """output = subprocess.run(["/DyPyBench/scripts/run-test.sh %s %s %s %s %s" %(proj_name, proj_no, proj_test_folder, copy_folder, args.timeout)
                    ], shell=True, stderr=subprocess.STDOUT, timeout=args.timeout)"""

    # execute DynaPyt instrumentation
    if args.dynapyt_instrument:
        projects = args.dynapyt_instrument
        if 0 in projects: # execute for all projects in case 0 is provided
            projects = [x for x in range(1,51)]
        for project in projects:
            if(project < 0 or project > 50):
                print("Project number should be between 1 and 50")
            else:
                proj_name = str(data[project - 1][1])
                proj_no = str(data[project - 1][0])
                instr_file = args.dynapyt_file
                analysis = args.dynapyt_analysis

                # read txt file to get the files to instrument
                # file contains the path, file or directory flag and project name
                with open(instr_file, 'r') as inst_file:
                    csvReader = csv.reader(inst_file, delimiter=" ")
                    instr_details = {}
                    for row in csvReader:
                        project_name, flag, path = row
                        project_no = get_project_no(project_name) # map name to number
                        if project_no in instr_details.keys():
                            temp = instr_details[project_no]
                            temp.append((project_no, flag, path))
                            instr_details[project_no] = temp
                        else:
                            instr_details[project_no] = [(project_no, flag, path)]

                # clear the previously instrumented files for the project
                if args.save:
                    output = subprocess.run(["/DyPyBench/scripts/clear-project.sh %s %s" %(proj_name, proj_no)
                            ], shell=True, stdout=open(args.save,'a+',1), stderr=subprocess.STDOUT, timeout=args.timeout)
                else:
                    output = subprocess.run(["/DyPyBench/scripts/clear-project.sh %s %s" %(proj_name, proj_no)
                    ], shell=True, capture_output=True, timeout=args.timeout)
                    #if output needs to be printed on the console then comment above and uncomment below
                    """output = subprocess.run(["/DyPyBench/scripts/clear-project.sh %s %s" %(proj_name, proj_no)
                    ], shell=True, stderr=subprocess.STDOUT, timeout=args.timeout)"""

                # instrument files for each project
                for line in instr_details[proj_no]:
                    project_no, flag, path = line
                    if args.save:
                        output = subprocess.run(["/DyPyBench/scripts/run-dynapyt-instrumentation.sh %s %s %s %s %s %s" %(proj_name, proj_no, path, analysis, flag, args.timeout)
                        ], shell=True, stdout=open(args.save,'a+',1), stderr=subprocess.STDOUT, timeout=args.timeout)
                    else:
                        output = subprocess.run(["/DyPyBench/scripts/run-dynapyt-instrumentation.sh %s %s %s %s %s %s" %(proj_name, proj_no, path, analysis, flag, args.timeout)
                        ], shell=True, capture_output=True, timeout=args.timeout)
                        #if output needs to be printed on the console then comment above and uncomment below
                        """output = subprocess.run(["/DyPyBench/scripts/run-dynapyt-instrumentation.sh %s %s %s %s %s %s" %(proj_name, proj_no, path, analysis, flag, args.timeout)
                        ], shell=True, stderr=subprocess.STDOUT, timeout=args.timeout)"""

    # execute tests for DynaPyt analysis on instrumented code 
    if args.dynapyt_run:
        projects = args.dynapyt_run
        if 0 in projects: # execute for all projects in case 0 is provided
            projects = [x for x in range(1,51)]
        for project in projects:
            if(project < 0 or project > 50):
                print("Project number should be between 1 and 50")
            else:
                proj_name = str(data[project - 1][1])
                proj_no = str(data[project - 1][0])
                analysis = args.dynapyt_analysis
                proj_flags = str(original_data[project - 1][1])
                if(proj_flags == "rt"):
                    proj_test_folder = str(original_data[project - 1][3])
                elif(proj_flags == "t"):
                    proj_test_folder = str(original_data[project - 1][2])
                elif(proj_flags == "r"):
                    proj_test_folder = ""

                if args.save:
                    output = subprocess.run(["/DyPyBench/scripts/run-dynapyt-analysis.sh %s %s %s %s %s" %(proj_name, proj_no, analysis, proj_test_folder, args.timeout)
                    ], shell=True, stdout=open(args.save,'a+',1), stderr=subprocess.STDOUT, timeout=args.timeout)
                else:
                    output = subprocess.run(["/DyPyBench/scripts/run-dynapyt-analysis.sh %s %s %s %s %s" %(proj_name, proj_no, analysis, proj_test_folder, args.timeout)
                    ], shell=True, capture_output=True, timeout=args.timeout)
                    #if output needs to be printed on the console then comment above and uncomment below
                    """output = subprocess.run(["/DyPyBench/scripts/run-dynapyt-analysis.sh %s %s %s %s %s" %(proj_name, proj_no, analysis, proj_test_folder, args.timeout)
                    ], shell=True, stderr=subprocess.STDOUT, timeout=args.timeout)"""

    # execute LExecutor instrumentation
    if args.lex_instrument:
        projects = args.lex_instrument
        if 0 in projects: # execute for all projects in case 0 is provided
            projects = [x for x in range(1,51)]
        for project in projects:
            if(project < 0 or project > 50):
                print("Project number should be between 1 and 50")
            else:
                proj_name = str(data[project - 1][1])
                proj_no = str(data[project - 1][0])
                instr_file = args.lex_file

                # read txt file to get the files to instrument
                # file contains the path and project name
                with open(instr_file, 'r') as inst_file:
                    csvReader = csv.reader(inst_file, delimiter=" ")
                    instr_details = {}
                    for row in csvReader:
                        project_name, path = row
                        project_no = get_project_no(project_name) # map name to number
                        if project_no in instr_details.keys():
                            temp = instr_details[project_no]
                            temp.append((project_no, path))
                            instr_details[project_no] = temp
                        else:
                            instr_details[project_no] = [(project_no, path)]

                # clear the previously instrumented files for the project
                if args.save:
                    output = subprocess.run(["/DyPyBench/scripts/clear-project.sh %s %s" %(proj_name, proj_no)
                            ], shell=True, stdout=open(args.save,'a+',1), stderr=subprocess.STDOUT, timeout=args.timeout)
                else:
                    output = subprocess.run(["/DyPyBench/scripts/clear-project.sh %s %s" %(proj_name, proj_no)
                    ], shell=True, capture_output=True, timeout=args.timeout)
                    #if output needs to be printed on the console then comment above and uncomment below
                    """output = subprocess.run(["/DyPyBench/scripts/clear-project.sh %s %s" %(proj_name, proj_no)
                    ], shell=True, stderr=subprocess.STDOUT, timeout=args.timeout)"""

                # gather files for each project
                files = []
                for line in instr_details[proj_no]:
                    project_no, file_path = line
                    files.append(file_path)

                path = ' '.join([str(path) for path in files])

                # instrument files for each project
                if args.save:
                    output = subprocess.run(["/DyPyBench/scripts/run-lex-instrumentation.sh %s %s %s %s" %(proj_name, proj_no, args.timeout, path)
                    ], shell=True, stdout=open(args.save,'a+',1), stderr=subprocess.STDOUT, timeout=args.timeout)
                else:
                    output = subprocess.run(["/DyPyBench/scripts/run-lex-instrumentation.sh %s %s %s %s" %(proj_name, proj_no, args.timeout, path)
                    ], shell=True, capture_output=True, timeout=args.timeout)
                    #if output needs to be printed on the console then comment above and uncomment below
                    """output = subprocess.run(["/DyPyBench/scripts/run-lex-instrumentation.sh %s %s %s %s" %(proj_name, proj_no, args.timeout, path)
                    ], shell=True, stderr=subprocess.STDOUT, timeout=args.timeout)"""

    # execute tests for LExecutor trace file generation on the instrumented code
    if args.lex_test:
        projects = args.lex_test
        if 0 in projects: # execute for all projects in case 0 is provided
            projects = [x for x in range(1,51)]
        for project in projects:
            if(project < 0 or project > 50):
                print("Project number should be between 1 and 50")
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
                    output = subprocess.run(["/DyPyBench/scripts/run-lex-test.sh %s %s %s %s" %(proj_name, proj_no, proj_test_folder, args.timeout)
                    ], shell=True, stdout=open(args.save,'a+',1), stderr=subprocess.STDOUT, timeout=args.timeout)
                else:
                    output = subprocess.run(["/DyPyBench/scripts/run-lex-test.sh %s %s %s %s" %(proj_name, proj_no, proj_test_folder, args.timeout)
                    ], shell=True, capture_output=True, timeout=args.timeout)
                    #if output needs to be printed on the console then comment above and uncomment below
                    """output = subprocess.run(["/DyPyBench/scripts/run-lex-test.sh %s %s %s %s" %(proj_name, proj_no, proj_test_folder, args.timeout)
                    ], shell=True, stderr=subprocess.STDOUT, timeout=args.timeout)"""

    # execute PyCG to generate call graphs on static code
    if args.pycg:
        projects = args.pycg
        if 0 in projects: # execute for all projects in case 0 is provided
            projects = [x for x in range(1,51)]
        for project in projects:
            if(project < 0 or project > 50):
                print("Project number should be between 1 and 50")
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

                # PyCG searches for all .py files in folder, so restrict in case of only a single test file for test suite. 
                flag = "folder"
                if proj_test_folder.__contains__(".py"):
                    flag = "file"

                if args.save:
                    output = subprocess.run(["/DyPyBench/scripts/run-pycg.sh %s %s %s %s %s" %(proj_name, proj_no, proj_test_folder, flag, args.timeout)
                    ], shell=True, stdout=open(args.save,'a+',1), stderr=subprocess.STDOUT, timeout=args.timeout)
                else:
                    output = subprocess.run(["/DyPyBench/scripts/run-pycg.sh %s %s %s %s %s" %(proj_name, proj_no, proj_test_folder, flag, args.timeout)
                    ], shell=True, capture_output=True, timeout=args.timeout)
                    #if output needs to be printed on the console then comment above and uncomment below
                    """output = subprocess.run(["/DyPyBench/scripts/run-pycg.sh %s %s %s %s %s" %(proj_name, proj_no, proj_test_folder, flag, args.timeout)
                    ], shell=True, stderr=subprocess.STDOUT, timeout=args.timeout)"""
