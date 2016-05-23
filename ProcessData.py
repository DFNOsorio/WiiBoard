import matplotlib


def uploadData(data):
    lines = data.readlines()

    for line in lines:
        print (line)



Data = open('/home/danielosorio/PycharmProjects/WiiBoard/Raw_Mon_16:22:19')

uploadData(Data)