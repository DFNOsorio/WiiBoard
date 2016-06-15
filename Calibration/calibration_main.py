import seaborn
import matplotlib as plt
import config


def file_reader(name_of_file):
    tl = []
    tr = []
    bl = []
    br = []
    tw = []
    time = []

    data = open(name_of_file)
    lines = data.readlines()[1:]

    for line in lines:
        temp_line = line.split(';')
        if len(temp_line) < 5:
            tl.append(float(temp_line[0]))
            tr.append(float(temp_line[1]))
            bl.append(float(temp_line[2]))
            br.append(float(temp_line[3]))
            time.append(float(temp_line[4]))
        else:
            tl.append(float(temp_line[0]))
            tr.append(float(temp_line[1]))
            bl.append(float(temp_line[2]))
            br.append(float(temp_line[3]))
            tw.append(float(temp_line[4]))
            time.append(float(temp_line[5]))

    return [tl, tr, bl, br, tw, time]


folder_name = 'Calibration/data'