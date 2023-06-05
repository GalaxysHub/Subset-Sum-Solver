import random


class CampSorter:

    def __init__(self, maxAttempts = 10000, increment = 5, boundsDifStart = 0, trysPerSection = 25, inputData={}):
        campdata = list(inputData['CampSectionData'].values())
        self.maxAttempts = maxAttempts
        self.increment = increment
        self.boundsDifStart = boundsDifStart
        self.trysPerSection = trysPerSection

        self.pieces = list(inputData["Camps"].values())
        self.campSizeKeys = self.pieces[:]
        self.camps =  list(inputData["Camps"].keys())
        self.sectionSizes = [d['size'] for d in campdata]

        self.sectionKeys = self.sectionSizes[:] #section sizes are later mapped to the section

        self.sectionNames = list(inputData["CampSectionData"].keys())
        self.sectionWidths =  [d['width'] for d in campdata]

        self.sectionSolutions = [[] for _ in range(len(self.sectionSizes))]
        self.campsSolutions = [[] for _ in range(len(self.sectionSizes))]
        self.campLengthsSolutions = []

        self.sectionsSortedNames = []
        self.sectionsSortedWidths = []

        self.dif = []

        self.sectionSizes.sort()#sectionSizes are solved from smallest to biggest to decrease chance of unsolvable final section
        # Sorts Section Names and Widths lists
        for section in self.sectionSizes:
            for i in range(len(self.sectionKeys)):
                if self.sectionKeys[i]==section:
                    self.sectionsSortedNames.append(self.sectionNames[i])
                    self.sectionsSortedWidths.append(self.sectionWidths[i])
                    del self.sectionKeys[i]
                    del self.sectionNames[i]
                    del self.sectionWidths[i]
                    break

#trys to find fit for a section with the campsite self.pieces
    def fit(self, sectionSize, LB, UB, maxNum,minNum=1):
        solution = []

        random.shuffle(self.pieces)

        for i in range(len(self.pieces)):
            for j in range(i+minNum,len(self.pieces)+1):
                if(j-1>maxNum):
                    break

                if(LB<sum(self.pieces[i:j])-sectionSize<UB):
                    solution = self.pieces[i:j] #adds solution for section to list
                    break
            else:
                continue
            break

        for i in range(len(solution)):
            self.pieces.remove(solution[i]) #removes campsites from the list

        difference = sum(solution)-sectionSize #difference between section size and area occupied
        return solution, difference

    #finds a fit based on campsite self.pieces and section number
    def findSectionFit(self, position):
        x = 0
        attempt = 1
        sectionSize = self.sectionSizes[position]

        s = []
        self.sectionsRemaining = 0

        for section in self.sectionSolutions:
            if section ==[]: self.sectionsRemaining+=1

        targetDif = (sum(self.pieces)-sum(self.sectionSizes[position:]))/self.sectionsRemaining

        LB = (targetDif) - self.boundsDifStart
        UB = (targetDif) + self.boundsDifStart

        maxNum = len(self.pieces)
        # reduces max number of pieces a section can have
        self.pieces.sort()
        tot = 0
        for i in range(len(self.pieces)):
            tot += self.pieces[i]
            if(tot>sectionSize):
                maxNum = i
                break

        minNum = 1
        tot = 0
        # incrase min number of pieces a section can have
        c = 0
        for i in range(len(self.pieces),0,-1):
            tot += self.pieces[i-1]
            c+=1
            if(tot>sectionSize):
                minNum = c
                break

        while(s==[]):
            s, d = self.fit(sectionSize, LB, UB, maxNum, minNum)

            if(s==[]):
                random.shuffle(self.pieces)
                attempt += 1
            else:
                self.sectionSolutions[position]=s
                self.dif.append(d)

            # Adjusts the error bounds if solution not found after trysPerSection attempts
            if(attempt%self.trysPerSection==0):
                LB -= self.increment
                UB += self.increment

            if(attempt>self.maxAttempts):
                break

    def getSomeAns(self):
        for i in range(len(self.sectionSolutions)):
            if(self.sectionSolutions[i]==[]): #solves all empty solution sets
                self.findSectionFit(i)

    def getFullSolution(self):
        self.getSomeAns()
        global spread
        spread = max(self.dif)-min(self.dif)#the best overal fit will have the smallest spread
        # Matches the Camp Leader and calculates the length of the camp
        for i in range(len(self.sectionSolutions)):
            self.campLengthsSolutions.append([round(x/self.sectionsSortedWidths[i],0) for x in self.sectionSolutions[i]])

            for solution in self.sectionSolutions[i]:

                for j in range(len(self.campSizeKeys)):
                    if(self.campSizeKeys[j]==solution):
                        self.campsSolutions[i].append(self.camps[j])
                        del self.camps[j]
                        del self.campSizeKeys[j]
                        break

    def generateAndReturnSolution(self):
        self.getFullSolution()
        return spread, self.pieces, self.sectionsSortedNames, self.sectionSolutions, self.dif, self.campsSolutions, self.campLengthsSolutions

    def printFullSolution(self):
        self.getFullSolution()

        print("\nSections")
        print(self.sectionsSortedNames)
        print("\nSolutions: ")
        print(self.sectionSolutions)
        print("\nDifferences between summed camp area and section area: ")
        print(self.dif)
        print("\nCamps: ")
        print(self.campsSolutions)
        print("\nCamp Lengths: ")
        print(self.campLengthsSolutions)
        print("\nPieces remaining: ")
        print(self.pieces)
        print("\nThe spread is: " + str(spread))
        if(self.pieces!=[]): print("\nUnsolved self.sectionSizes. Run program again")

        filename = "./Solutions.csv"
        f= open(filename, "w")
        headers = "Section, Solutions, Differences (ft2), Camping Leaders, Camping Lengths"
        f.write(headers+"\n")

        for i in range(len(self.sectionSolutions)):
            f.write(self.sectionsSortedNames[i]+","+str(self.sectionSolutions[i]).replace(",","|")+","+str(self.dif[i])+","+str(self.campsSolutions[i]).replace(",","|")+","+str(self.campLengthsSolutions[i]).replace(",","|")+"\n")
        f.close()


