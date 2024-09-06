"""
Author:  Vir Chuy Darm
Date:    December 9, 2022
E-mail:  vjchuydarm@gmail.com
Description: This program runs a simple shell server, and contains functions related to ones found in a gl server.
"""


#Simple Shell Values
DIRECTORIES_KEY = 'directories'
FILES_KEY = 'files'
ROOT_DIRECTORY_NAME = 'main'

def Simple_Shell_System():
    """
    This is the main shell function, used to make the 3d dictionary
    param: None
    """
    #fresh system
    my_file_system = {
        ROOT_DIRECTORY_NAME: {
            DIRECTORIES_KEY: {},
            FILES_KEY: []
        }
    }

    return my_file_system

def Command_line(input_string, file_system, PWD):
    """
    This is a helper function that excecutes all functions for the program
    param: user_input
    param: file_system
    param: PWD
    """

    #my values
    retVal = 1
    user_input = input_string.strip().split(' ')
    command = user_input[0]
    directory = ROOT_DIRECTORY_NAME
    current_directory = {}

    #executes mkdir function
    if (command == 'mkdir'):
        mkdir(file_system, user_input, PWD)

    #executes cd function
    elif (command == 'cd'):
        PWD = cd(file_system, user_input, PWD)

    #executes ls function
    elif (command == 'ls'):
        ls(file_system, user_input, PWD)

    #executes pwd function
    elif (command == 'pwd'):
        pwd(file_system, PWD)

    #executes rm function
    elif (command == 'rm'):
        rm(file_system, user_input, PWD)

    #executes touch function
    elif (command == 'touch'):
        touch(file_system, user_input, PWD)

    #executes locate function
    elif (command == 'locate'):
        locate(file_system, PWD, user_input)
    
    #used to exit program
    elif (command == 'exit'):
        retVal = 0
        print("Exit Simple Shell")

    #prints if a command is not recognized
    else:
        print('Command Unknown')

    return retVal, PWD


def run_file_system():
    """
    This is the main shell program, and takes no arguments
    param: None
    """
    #This starts the file system
    my_file_system = Simple_Shell_System()

    #PWD shows where you are and updates when cd function is used
    PWD = '/' + ROOT_DIRECTORY_NAME 

    #used to exit the simple shell
    exit = 1
    while (exit != 0):
        command = input("Enter Command: ")
        exit, PWD = Command_line(command, my_file_system, PWD,)

def determine_location(directory, key_name, PWD, route):
    """
    This is a helper function used to look for files recursively, also used in locate function
    param: directory
    param: key_name
    param: PWD
    param: route
    """
    
    #used to see if file is in the directory
    if key_name in directory[FILES_KEY]:
        #appends if in
        route.append(PWD + '/' + key_name)

    # loops in all directories
    for dir_name in directory[DIRECTORIES_KEY]:

        #puts in route
        newPWD = PWD + '/' + dir_name
        
        # will find the directory
        dir_ref = directory[DIRECTORIES_KEY][dir_name]
        
        #recursive case
        determine_location(dir_ref, key_name, newPWD, route)

def locate(file_system, PWD, user_input):
    """
    This is the main locate function, used to find where a file is and prints the PWD or route
    param: file_system
    param: PWD
    param: user_input
    """
    #values
    filename = user_input[1]
    route = []

    #checks if incorrect input
    if '/' in filename:
        print('Incorrect Input')
    
    #used to find the reference directory
    current = getDirectory(file_system, PWD)

    # used to search for a file infinitely
    determine_location(current, filename, PWD, route)
    for i in route:
        print(i)

    #return the route all files were in
    return route

def touch(file_system, user_input, PWD):
    """
    Touch Function used to make a file in a directory
    param: file_system
    param: user_input
    param: PWD
    """
    #checks to see if there is an inputted name
    if len(user_input) == 1:
        print("No Directory Name")
        return False

    #finds the directory
    file_name = user_input[1]
    currentDir = getDirectory(file_system, PWD)

    #sees if there is a file in the directory
    if file_name in currentDir[FILES_KEY]:
        print('File already exists')
        return

    #creates file
    currentDir[FILES_KEY].append(file_name)
    print('File created')
    return

def rm(file_system, user_input, PWD):
    """
    This is a function that will remove a file from file_system
    param: file_system
    param: user_input
    param: PWD
    """
    # checks if there is a name to the file
    if len(user_input) == 1:
        print("Missing file name")
        return False

    file_name = user_input[1]

    #gets the current directory and checks if it exists
    current_directory = getDirectory(file_system, PWD)
    if file_name in current_directory.get(FILES_KEY):
        current_directory.get(FILES_KEY).remove(file_name)
    
    #if file is not found
    else:
        print("File not found")

def cd(file_system, user_input, PWD):
    """
    This is a change directory function used to locate as well as change the current directory.
    param: file_system
    param: user_input
    param: PWD
    """
    #values
    directory_route = user_input[1]


    #if no name was inputted
    if len(user_input) == 1:
        print("No Directory Name")
        return PWD

    

    #if / was inputted
    if directory_route == '/':
        PWD = '/' + ROOT_DIRECTORY_NAME
        return PWD

    #used so a blank is not returned
    if directory_route[-1] == '/':
        directory_route = directory_route[:-1]

    if len(directory_route.split('/')) == 1:

        #checks if '' or ' ' was inputted
        if directory_route == '' or directory_route == '.':
            return PWD  ## do nothing, you moved no where

        #checks if .. was inputted
        if directory_route == '..':

            if PWD == '/' + ROOT_DIRECTORY_NAME:
                return PWD

            #used to removed the last directory from the pwd
            part = PWD.split('/')
            all_but_current = part[:-1]
            PWD = all_but_current[0]
            for i in all_but_current[1:]:
                PWD += '/' + i
            return PWD

        #Checks if the directory exists
        currentDir = getDirectory(file_system, PWD)
        if directory_route not in currentDir[DIRECTORIES_KEY]:
            print('Directory not found')
            return PWD
        else:
            PWD = PWD + '/' + directory_route
            return PWD



    else:
        #used if a path was given
        if directory_route[0] == '/':
            string = directory_route[1:]
            direct = string.split('/')
            new_pwd = '/' + ROOT_DIRECTORY_NAME

            #loops through the direct
            for i in direct[1:]:
                if i in getDirectory(file_system, new_pwd)[DIRECTORIES_KEY]:
                    new_pwd += '/' + i

                # if a route does not exist
                else:
                    print('Route does not exist')
                    return PWD  # return old path

            PWD = new_pwd
            return PWD

        #used if a relative path was given
        else:
            #splits and makes a new pwd
            string = directory_route
            direct = string.split('/')
            new_pwd = PWD

            #loops through direct
            for i in direct:
                if i in getDirectory(file_system, new_pwd)[DIRECTORIES_KEY]:
                    new_pwd += '/' + i

                #if a route doesnt exist, it will return previous route
                else:
                    print('Route does not exist')
                    return PWD

            PWD = new_pwd
            return PWD

def mkdir(file_system, user_input, PWD):
    """
    This function makes a new directory inside the current directory
    param: file_system
    param: user_input
    param: PWD
    """
    #values
    directory_name = user_input[1]

    #if there is no inputted directory name
    if len(user_input) == 1:
        print("No Directory Name")
        return False

    

    #check if inputted name is allowed
    if '/' in directory_name:
        print('Invalid Character Inputted')
        return False

    #check if it exists in the directory
    current_directory = getDirectory(file_system, PWD)
    if directory_name in current_directory[DIRECTORIES_KEY]:
        print("Directory already exists")
        return False

    # creates directory
    current_directory[DIRECTORIES_KEY][directory_name] = {DIRECTORIES_KEY: {}, FILES_KEY: []}
    print(file_system)
    return True

def pwd(file_system, PWD):
    """
    This function is the pwd, is used to make the route to current directory
    param: file_system
    param: pwd
    """

    #used to display what current directory is shown
    directory_contents = PWD
    
    print("Current working directory is: " + str(directory_contents))

def getDirectory(file_system, route):
    """
    This is a helper function used to get the current directory
    param: file_system
    param: route
    """
    if route == '/':
        return file_system[ROOT_DIRECTORY_NAME]

    #used to remove the first /
    string = route.strip()
    if route[0] == '/':
        string = string[1:]

    #used to remove remaining /s
    if string[-1] == '/':
        string = string[:-1]

    #strips to parts
    parts = string.strip().split('/')
    directory = file_system.get(parts[0])

    #loops through the parts
    for i in parts[1:]:
        directory = directory.get(DIRECTORIES_KEY).get(i)

    return directory

def ls(file_system, user_input, PWD):
    """
    This function displays directories and files in the current directory
    param: file_system
    param: user_input
    param: PWD
    """
    #used to look in the current directory
    if len(user_input) == 1:
        route = PWD

    #gets the route
    else:
        directory_route = user_input[1]
        new_route = cd(file_system, ['cd', directory_route], PWD)
        route = new_route

    #finds what directory is being used
    currentDir = getDirectory(file_system, route)
    print('contents for ' + route)

    #prints the directories and files
    for i in currentDir[DIRECTORIES_KEY]:
        print(i)
    for i in currentDir[FILES_KEY]:
        print(i)

    return



if __name__ == '__main__':
    run_file_system()
