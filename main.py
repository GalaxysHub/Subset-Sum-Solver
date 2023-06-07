from helpers.SubsetSumSolver import CampSorter
from helpers.formatInput import FormatInputData

import json

global inputData
with open('InputData.json', 'r') as f:
  inputData = json.load(f)


def writeJsonSolution(solution):
    data = {
        "Sections": solution.sectionsSortedNames,
        "CampAreas": solution.sectionSolutions,
        "Camps":solution.campsSolutions,
        "CampLengths":solution.campLengthsSolutions,
    }
    with open("solution.json", "w") as outfile:
        json.dump(data, outfile)

def run():

    camp_section_dict = {
        # 'InputData/EF2023 - Small Camp Sections.csv':'InputData/EF2023 - Small Camp Groups.csv',
        # 'InputData/EF2023 - Camp Sections.csv':'InputData/EF2023 - Camp Groups.csv',
        # 'InputData/EF2023 - Large Camp Sections.csv':'InputData/EF2023 - Large Camp Groups.csv',
        # 'InputData/EF2023 - Small Camp Sections.csv':'InputData/EF2023 - Small Camp Groups.csv',
        'InputData/EF2023 - Activities Camp Sections.csv':'InputData/EF2023 - Activities Camp Groups.csv',
    }

    for camp_section, group_camps in camp_section_dict.items():
        numSolToGen = 7
        bestSolution = None
        bestSpread = None
        firstTime = True

        maxIter = 10000
        inc = 15
        initBounds = 15
        trysPerSect = 50

        formatter = FormatInputData(camp_section, group_camps)
        formatter.formatInput()
        inputData = formatter.getFormattedInput()
        #Generates all solutions and picks best one
        for i in range(0,numSolToGen,1):
            print("\nSolving solution "+str(i+1)+" of "+str(numSolToGen))
            solution = CampSorter(maxIter,inc,initBounds,trysPerSect,inputData)
            fullSolution = solution.generateAndReturnSolution()
            print("Spread: " + str(fullSolution[0]))
            print("Unsorted pieces: " + str(fullSolution[1]))
            #replaces old solution if better one is found
            if (firstTime or fullSolution[0]<bestSpread) and fullSolution[1]==[]:
                bestSpread = fullSolution[0]
                bestSolution = solution
                firstTime = False
                print("The best spread has been updated to "+str(bestSpread))

        print(bestSolution.printFullSolution())

        #todo: combine solutions from different inputs

        writeJsonSolution(bestSolution)


run()