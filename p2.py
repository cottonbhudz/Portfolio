"""
Author: Vir Chuy Darm
Date: 11/18/2022
Description:  This code evalutes data dictionaries, uses a variety of functions to differentiate and evaluate. sample data: data["Ince, Ryan"] = ['09:45:00, 11/2/2022', '09:45:00, 11/4/2022']
"""

# Comment the line below out if your have the load_dictionary function working!!
# Comment the line below out if your have the load_dictionary function working!!

from dataEntryP2 import fillAttendanceData

# Comment the line above out if your have the load_dictionary function working!!
# Comment the line above out if your have the load_dictionary function working!!

def print_list(xlist):
    for element in xlist:
        print(element)

def list_students_attendance_count(data):
    #values and lists
    first_class = []
    second_class = []
    count = 0

    #checks if the values are unique or seen before
    for i in data:
        first_name = str(i)
        if first_name not in first_class:
            first_class.append(first_name)
        else:
            second_class.append(first_name)
    
    #counts list
    for i in second_class:
        count += 1

    print('there were',count, 'records for this query')

def load_roster(roster_file_name):
    #values and lists
    dataRoster = []

    roster_file_name = open('rosters.txt','r')

    #it appends files into a list
    for i in roster_file_name:
        dataRoster.append(i)
    return dataRoster

def load_dictionary(infile):
    #values and lists
    data = {}

    file1 = open(infile, 'r')
    Lines = file1.readlines()

    #separates the lines of string
    for line in Lines:
        line = line.strip()
        name = line.split(', ')[0] + ', ' + line.split(', ')[1]
        time = line.split(', ')[2] + ', ' + line.split(', ')[3]

    if name not in data:
        data[name] = []

    data[name].append(time)

    return data

def connect_to_data_file(filename):
    # will return connection to data file
    infile = open(filename, "r")

    try:
        #infile = open("data.txt", "r")
        #infile = open("dataAllShow1stClass.txt", "r")
        #infile = open("dataAllShow1stAnd2ndClass.txt", "r")
        infile = open(filename, "r")
    except FileNotFoundError:
        print("file was not found, try again")

    return infile  # connection with the file

def get_first_student_to_enter(date,data):
    #values and lists
    student_one = False

    for name in data.keys():
        times = data[name]


        #splits the data into elements
        for i in times:
            token = i.split(', ')
            date = token[1]
            timing = token[0]
            if date == date:
                comps = timing.split(':')
                time_in_seconds = 0

                #turns everything into seconds
                time_in_seconds += int(comps[0])*60*60
                time_in_seconds += int(comps[1])*60
                time_in_seconds += int(comps[2])
                
                #if student one is similar it changes to true
                if student_one == False:
                    earliest_student = name
                    earliest_time = time_in_seconds
                    student_one = True

                #if the new time is lower than previous it changes to the new value
                else:
                    if time_in_seconds < earliest_time:
                        earliest_time = time_in_seconds
                        earliest_student = name

    return(earliest_student)

def is_present(name,date,data):
    #values
    datestime_present = data[name]

    #splits the names
    for i in datestime_present:
        date_present = i.split(', ')[1]

        #if they are present on date prints true
        if date == date_present:
            return True

    return False

def list_all_students_checked_in(date, data):
    #values and lists
    old_date = date
    data_list = data
    date_list = []
    checked_in_list = []

    #checks if date is in elements
    for i in data_list:
        for i in data_list[i]:
            if old_date in (i[:]):
                date_list.append(i)

    #checks which keys has the element date and puts it into list
    for i in date_list:
        new_date = i
        for i in data_list:
            if new_date in (data_list[i]):
                checked_in_list.append(i)  

    return checked_in_list

def print_dictionary(data):
    print(data)
    return data

def display_attendance_data_for_student(name, data):
    #values and lists
    attend_list = []
    second_attend_list = {}
    value = name

    #if the name is in keys appends to list
    for i in data:
        if value in (i[:]):
            attend_list.append(i)

    if name not in data:
        print("No student of this name in the attendance log") 
    
    #if name in data elements it makes a dictionary
    for i in attend_list:
        name = i
        for i in data:
            if name in (i[:]):
                second_attend_list[name] = data[name]
        
    for i in second_attend_list:
        print (i, second_attend_list[i])



def list_all_students_checked_in_before(date, time, data):
    #my values and lists
    first_list = []
    name_list = []

    #splits time into its parts
    new_time = time.split(':')
    hour = (new_time[0])
    minute = (new_time[1])
    seconds = (new_time[2])

    #checks if time is equal to the data time and appends
    for i in data:
            for i in data[i]:
                value = i.split(',')[0]
                if (value[0:2] <= hour) and (value[3:5] <= minute) and (value[6:8] < seconds) and (date in i):
                    first_list.append(i)

    #if the values of the list are the same it appends the original list values
    for i in first_list:
        second_value = i
        for i in data:
            if second_value in data[i]:
                name_list.append(i)

    return(name_list) 


if __name__ == '__main__':

    infile = connect_to_data_file("dataEntryP2.py")
    if(infile):
        print("connected to data file...")
    else:
        print("issue with data file... STOP")
        exit(1)

    # data = load_dictionary(infile)
    # ************************
    # OR MANUALLY!!!
    # ************************

    # just making sure the data collected is good
    print_dictionary(data)

    print("********* Looking up Student Attendance Data ***********")
    display_attendance_data_for_student("Morrison, Simon", data)
    display_attendance_data_for_student("Arsenault, Al", data)

    print("********* Looking to see if Student was present on date ***********")
    print(is_present("Bower, Amy", "11/5/2022", data))
    print(is_present("Bower, Amy", "11/17/2022", data))

    # display when students first signed in
    print("**** Students present on this date ****")
    result = list_all_students_checked_in("11/5/2022", data)
    print_list(result)
    print_count(result)

    print("**** Those present on date & before a time assigned ****")
    result = list_all_students_checked_in_before("11/5/2022", "08:55:04", data)
    print_list(result)
    print_count(result)

    # list the good students that showed up both days
    print("**** Those who attended BOTH classes ****")

    # list the  students that showed up ONE of the days
    print("**** Those who attended ONE class ****")

    # list the  students that have not shown up
    print("**** Those who have NOT attended a SINGLE class ****")
