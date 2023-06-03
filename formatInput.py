import csv, sys
import json
import string

group_camps = 'EF2023 - Camping Groups.csv'
camp_section = 'EF2023 - Camp Sections.csv'


formatedInputData = {}
totalArea = 0
totalPeople = 0

def getCampingData():
    with open(camp_section, newline='',encoding='utf-8') as f:
        reader = csv.DictReader(f)
        CampSectionData = {}
        try:
            for row in reader:
                print(row)
                global totalArea
                totalArea = totalArea + int(row["Size Ft2"])
                CampSectionData[row["Camp section"]] = {
                    "size": int(row["Size Ft2"]),
                    "width": int(row["Width"])
                }
            formatedInputData["CampSectionData"] = CampSectionData
                

        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(group_camps, reader.line_num, e))

def getGroupCampsData():
    with open(group_camps, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        Camps = {}
        try:
            for row in reader:
                print(row)
                global totalPeople
                totalPeople = totalPeople + int(row["Size"])
                groupName = row['Group Name']
                printable = set(string.printable)
                groupName = ''.join(filter(lambda x: x in printable, groupName))
                Camps[groupName] = int(row['Size'])
            formatedInputData["Camps"] = Camps
            

        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(group_camps, reader.line_num, e))


def calculateAreaPerCamp():
    areaPerPerson = totalArea/totalPeople
    for key, value in formatedInputData["Camps"].items():
        formatedInputData["Camps"][key] = round(value * areaPerPerson,0)



def specialCases():
    OmittedCamps = {}
    Camps = formatedInputData["Camps"]
    CampSectionData = formatedInputData["CampSectionData"]

    #move slippery saucy sloots & Cabbage Pash Kids to B32 (ADA)
    CampSectionData["B32"]["size"] = CampSectionData["B32"]["size"] - Camps["slippery saucy sloots"]
    CampSectionData["B32"]["size"] = CampSectionData["B32"]["size"] - Camps["cabbage pash kids"]
    OmittedCamps["slippery saucy sloots"]=Camps["slippery saucy sloots"]
    OmittedCamps["cabbage pash kids"]=Camps["cabbage pash kids"]
    del Camps["slippery saucy sloots"]
    del Camps["cabbage pash kids"]

    #move M3ga St3llar Ali3ns and Camp Schwifty 2020! to C32 (ADA)
    CampSectionData["C32"]["size"] = CampSectionData["C32"]["size"] - Camps["M3ga St3llar Ali3ns"]
    CampSectionData["C32"]["size"] = CampSectionData["C32"]["size"] - Camps["Camp Schwifty 2020!"]
    OmittedCamps["M3ga St3llar Ali3ns"]=Camps["M3ga St3llar Ali3ns"]
    OmittedCamps["Camp Schwifty 2020!"]=Camps["Camp Schwifty 2020!"]
    del Camps["M3ga St3llar Ali3ns"]
    del Camps["Camp Schwifty 2020!"]

    #copmbine Camp Ohanas
    Camps["Camp Ohana x2"] = Camps["Camp Ohana 1"] + Camps["Camp Ohana 2"]
    OmittedCamps["Camp Ohana 1"]=Camps["Camp Ohana 1"]
    OmittedCamps["Camp Ohana 2"]=Camps["Camp Ohana 2"]
    del Camps["Camp Ohana 1"]
    del Camps["Camp Ohana 2"]

    #combine TEAM BLAST OFF & Camp Wurder
    Camps["TEAM BLAST OFF & Camp Wurder"] = Camps["TEAM BLAST OFF"] + Camps["Camp Wurder"]
    OmittedCamps["TEAM BLAST OFF"] = Camps["TEAM BLAST OFF"]
    OmittedCamps["Camp Wurder"]=Camps["Camp Wurder"]
    del Camps["TEAM BLAST OFF"]
    del Camps["Camp Wurder"]

    formatedInputData["OmittedCamps"] = OmittedCamps

def writeJsonInputs():
    with open("InputData.json", "w") as outfile:
        json.dump(formatedInputData, outfile)

def formatInput():
    getCampingData()      
    getGroupCampsData()
    calculateAreaPerCamp()
    # specialCases()
    writeJsonInputs()



sys.modules[__name__] = formatInput


