"""
 Contains functions to parse and get info about the cha files and xml files that corresponds to the checked lines in the cha files
"""

import os
import codecs
import time
from datetime import datetime, date
import re
import zipfile
import json

dates = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12
}


def create_info_file():
    """"
        Creates the information for each cha files. This information includes: "name, time_stamp, nr_of_lines. nr_of_first_checked, nr_of_second_checked"
        :return information: Returns the information as specified above
        :rtype dict
    """
    path = "selection/data/cha-files"

    first_round = get_lines_checked("selection/data/1. eerste ronde")
    second_round = get_lines_checked("selection/data/2. afgerond")

    count = 0
    for k in second_round:
        for entry in second_round[k]:
            if (entry not in first_round[k] and entry[0] != "sarah46"):
                count += 1
                print(entry)
    print(count)
    results = []

    # Count the lines and get the dates out of the files
    for file in os.listdir(path):
        date = ""
        with codecs.open(os.path.join(path, file), "r", "utf-8") as f:
            count = 0
            for line in f.readlines():
                if ("*" == line[0]):
                    count += 1
                if ("@Date" in line):
                    date = date_to_timestamp(get_date(line))

        # Remove the .cha extension
        file = file[:-4]
        info = {
            "name": file,
            "time_stamp": date,
            "nr_of_lines": count,
            "first_check": len(first_round[file]) if file in first_round else 0,
            "second_check": len(second_round[file]) if file in second_round else 0
        }

        results.append(info)
    return results

def get_lines_of_cha_files(path):
    """
    Gets the lines in the cha files in the given path
    :param path: The path that is looked at, this includes the subfolders
    :return: a list of cha files with the lines
    """
    results = []
    for file in os.listdir(path):

        with codecs.open(os.path.join(path, file), "r", "utf-8") as f:
            count = 0
            for line in f.readlines():
                if ("*" == line[0]):
                    count += 1
            results.append((file[:-4], [i for i in range(count)]))
    return results

def list_all_files_with_extension(path, extension):
    """"
        Lists all the files in the path with the given extension, when there is a zip folder it unzips it and removes the zip folder
        :param path: The path that we list all the files in, this includes the subfolders and zip files
        :param extension: The extension that we look at
        :return the files in the path with the given extension
        :rtype string[]
    """
    files = []
    for file in os.listdir(path):
        if file.endswith(extension):
            files.append(file)
        if file.endswith(".zip"):
            new_path = unzip(os.path.join(path, file))
            os.remove(os.path.join(path, file))
            files = files + list_all_files_with_extension(new_path, extension)
        # Dive into subfolders.
        if os.path.isdir(os.path.join(path, file)):
            files = files + list_all_files_with_extension(os.path.join(path, file), extension)
    return files


def list_cha_files(path):
    """"
         List all the cha files in a given path
        :param path: The path that we list all the files in, this includes the subfolders and zip files
    """
    return list_all_files_with_extension(path, ".cha")


def clean_file_name(file_name):
    """"
        Cleans a file such that it only contains the name of the session.
        :param file_name: the name that should be cleaned.
        :return the cleaned file name.
    """
    file_name = file_name.replace("VanKampen_", "")
    file_name = file_name.replace("uttfiles2_", "")
    i = file_name.find("_")
    return file_name[0:i]


def get_number_from_file(file_name):
    """"
        Get the line number that this file annotates
        :param file_name: the name of the file that we want to look get the number from
        :return the number of the line that this file annotates
    """

    # First delete everything before the numbers
    occurences = [m.start() for m in re.finditer('_', file_name)]

    number = file_name[occurences[-1] + 1:]
    # some sort of side_case
    if ("u" in file_name):
        number = number[1:]
    number = int(number)

    return number


def file_to_name_and_number(file_name):
    """
    Splits the file in a name and a line number
    :param file_name: the file name that we want to splitup
    :return: a tuple containing the name (e.g. laura47) and the line number
    """

    # Examplaar is a file that we do not need to concern ourselfs with.
    if ("Exemplaar" in file_name):
        return ("", -1)
    name = clean_file_name(file_name[:-4])
    number = get_number_from_file(file_name[:-4])
    return (name, number)


def get_line_score(files_path, first_checked_path, second_checked_path):
    """
    Gets the line score
    :param files_path:
    :param first_checked_path:
    :param second_checked_path:
    :return:
    """
    first_checked = get_lines_checked(first_checked_path)
    second_checked = get_lines_checked(second_checked_path)
    #Clean file name
    files_and_lines = get_lines_of_cha_files(files_path)
    result = []
    for (file, lines) in files_and_lines:
        file_result = [file]

        for line in lines:
            score = 0
            if file in first_checked:
                if line in first_checked[file]:
                    score = 1
            if file in second_checked:
                if line in second_checked[file]:
                    score = 2
            line_results = (line, score)
            file_result.append(line_results)

        result.append(file_result)
    print(result)
    return result



def get_lines_checked(path):
    """
    Get all the lines checked in the given path.
     It expects a path pointing to xml files which contain files that describes which line is checked
    :param path:
    :return: A dictionary containing file names and the lines that are checked
    """
    files = list_all_files_with_extension(path, ".xml")
    result = {}
    found = set()
    for file in files:
        name_number = file_to_name_and_number(file)
        if name_number in found:
            pass
        else:
            found.add(name_number)
        if (not "uttfiles2_" in file):
            file = clean_file_name(file)
            if file in result.keys():
                result[file].add(name_number[1])
            else:
                result[file] = set([name_number[1]])
    return result


def count_line_files(path):
    """
    Counts the line files in a given path e.g laura47_00001.xml and laura47_000002.xml
    :param path:
    :return:
    """
    files = list_all_files_with_extension(path, ".xml")
    result = {}
    # to make sure there are no duplicates
    found = set()
    for file in files:
        name_number = file_to_name_and_number(file)
        if name_number in found:
            pass
        else:
            found.add(name_number)
            if (not "uttfiles2_" in file):
                file = clean_file_name(file)
                if file in result.keys():
                    result[file] += 1
                else:
                    result[file] = 1
            else:
                print(file)
    return result


def normalize_xml_files(path):
    files = list_all_files_with_extension(path, ".xml")
    result = set([])
    for file in files:
        file = clean_file_name(file)
        result.add(file)
    return result



# Get the date out of a date string from a cha file
def get_date(string):
    return string[7:-1]


def date_to_timestamp(date_string):
    ar = date_string.split("-")
    d = date(int(ar[2]), dates[ar[1]], int(ar[0]))
    return time.mktime(d.timetuple())


def store_info(info, location):
    """"
        Stores the given info in the given location
    """
    with open(location, "w") as f:
        for entry in info:
            json.dump(entry, f)
            f.write("\n")


def load_info(location):
    """"
        Loads the info from the given location
    """
    info = []
    with open(location, "r") as f:
        for line in f.readlines():
            info.append(json.loads(line))
    return info


def unzip(path):
    """
    Unzips a zip folder and creates a folder containing the results
    :param path: The path to the folder to zip
    :return: The new name fo the path
    """
    zip_ref = zipfile.ZipFile(path, 'r')
    new_path = path[:-3]
    zip_ref.extractall(new_path)
    zip_ref.close()
    return new_path