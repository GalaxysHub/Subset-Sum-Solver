from SubsetSumSolver import CampSorter

import json
from formatInput import FormatInputData

group_camps = 'EF2023 - Camping Groups.csv'
camp_section = 'EF2023 - Camp Sections.csv'

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
    numSolToGen = 10
    bestSolution = None
    bestSpread = None
    firstTime = True

    maxIter = 10000
    inc = 5
    initBounds = 5
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
    writeJsonSolution(bestSolution)



run()