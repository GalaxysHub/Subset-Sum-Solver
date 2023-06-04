import csv, sys
import json
import string
import random

group_camps = "./InputData/EF2023 - Camp Groups.csv"

def getSmallCamps():
    tot = 0
    small_camps = {}

    with open(group_camps, newline='',encoding='utf-8') as f:
        reader = csv.DictReader(f)
        Camps = {}
        totalPeople = 0
        try:
            for row in reader:
                print(row)
                totalPeople += int(row["Size"])
                groupName = row['Group Name']
                printable = set(string.printable)
                groupName = ''.join(filter(lambda x: x in printable, groupName))
                Camps[groupName] = int(row['Size'])

        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(group_camps, reader.line_num, e))

        print(Camps)
        campNames = [camp for camp in Camps]
        print(campNames)

        magicLimit = 80

        while tot<600:
            rand = random.randrange(0, len(campNames))
            camp = campNames[rand]
            camp_size = Camps[camp]
            print(camp)
            print(camp_size)
            if camp_size<magicLimit:
                tot+=camp_size
                small_camps[camp] = camp_size
                campNames.remove(camp)
                del Camps[camp]

    with open('./InputData/EF2023 - Small Camp Groups.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar=',', quoting=csv.QUOTE_MINIMAL)
        
        spamwriter.writerow(['Group Name', 'Size'])
        for camp, size in small_camps.items():
            spamwriter.writerow([camp, size])



getSmallCamps()