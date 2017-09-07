"""
    This file is used to generate a selection, it expects two arguments: the percentage of lines to select from each file
    and the location that the results should be stored, this should be a txt file
"""
from selection.parser.file_parser import *
from selection.window import *

import sys

perc = float(sys.argv[1])
result_location = sys.argv[2]

line_scores = get_line_score("./selection/data/cha_files", "./selection/data/first_round",
                             "./selection/data/second_round")
selection = get_file_selection(line_scores, perc)


def prepend_zeros(length, string):
    """
    Prepend zeros to the string until the desired length is reached
    :param length: the length that the string should have
    :param string: the string that we should appends 0's to
    :return: A string with zeros appended
    """
    return "{}{}".format("0" * (length - len(string)), string)


def get_nr_to_check(selection, line_scores):
    """
    Gets the number of checks the annotators should do given a selection and a line_score
    :param selection: selection of the lines to check
    :param line_scores: the lines with the given score
    :return: the number of checks that still need to be performed
    """
    total_checks = 0
    maximum_checks = 0
    for (name, lines), (name2, (lines_with_score)) in zip(selection, line_scores):
        score = sum([score for (line, score) in lines_with_score if line in lines])
        max_score = len(lines) * 2
        total_checks += score
        maximum_checks += max_score
    return maximum_checks - total_checks


print("Number of checks to perform: {}".format(get_nr_to_check(selection, line_scores)))

# Sorting the selection for convenience
selection = sorted(selection, key=lambda name_lines: name_lines[0])

# Storing the names of the files the names to a file
file_names = []
for (name, lines) in selection:
    file_names = file_names + ["VanKampen_{}_u{}.xml".format(name, prepend_zeros(11, str(line))) for line in lines]

with open(result_location, "w") as f:
    for file_name in file_names:
        f.write("{}\n".format(file_name))
