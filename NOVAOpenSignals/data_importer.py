import numpy as np


def open_reader(name_of_file):

    data = open(name_of_file + ".txt")
    lines = data.readlines()
    print lines[1]



