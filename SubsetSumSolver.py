import random

numSolToGen = 10
bestSolution = None
bestSpread = None
firstTime = True

maxIter = 10000
inc = 5
initBounds = 0
trysPerSect = 50

class CampSorter:

    def __init__(self, maxAttempts = 10000, increment = 5, boundsDifStart = 0, trysPerSection = 25):
        self.maxAttempts = maxAttempts
        self.increment = increment
        self.boundsDifStart = boundsDifStart
        self.trysPerSection = trysPerSection

        self.pieces = [15616,14720,13184,12544,10368,9600,9088,8832,8064,8064,7680,7680,7424,6784,6656,6528,6528,6400,6400,6272,6016,5888,5888,5760,5760,5632,5632,5504,5504,5504,5376,5376,5376,5248,5248,5248,5120,4992,4992,4992,4864,4864,4736,4736,4736,4736,4608,4608,4608,4608,4480,4480,4480,4352,4352,4352,4352,4224,4096,4096,4096,4096,3968,3968,3968,3968,3968,3840,3840,3840,3840,3840,3840,3712,3712,3712,3712,3712,3712,3584,3584,3584,3584,3584,3456,3456,3456,3328,3328,3328,3328,3328,3328,3328,3328,3328,3200,3200,3200,3200,3200,3200,3200,3200,3200,3072,3072,3072,3072,3072,3072,3072,2944,2944,2944,2816,2816,2816,2816,2816,2816,2816,2816,2688,2688,2688,2688,2688,2688,2560,2560,2560,2560,2560,2560,2560,2560,2560,2560,2560,2432,2304,2560]

        self.campSizeKeys = self.pieces[:]
        self.campLeaders = ["AlBe","RaEd","HeJo","NeMe","KeLe","FeHa","JeEl","TiKr","CaGo","DeLi","CoPr","JoPo","KeC","KeBu","SAMC","AlCh","GrMa","KaGr","MeKa","JePe","BrSc","AdDi","AlSe","ChDo","JoJo","AnMa","DuDi","AaJo","BrMe","CaCo","BrCa","JeTr","MeSp","CaMa","JeAl","MiBe","LiBe","AnKi","KhSi","MaKi","LyJo","SaN","AyEr","MeHe","NaBl","PaSc","JaLe","MiDo","RyPi","SaBu","DoKo","MiRa","YoLo","DeHo","DeGu","GiGa","IaMu","MaWr","BrMe","MiAn","NaLe","ScKe","AlPe","KaRa","LeSc","NiSl","shda","BrBi","CaCa","JoCa","LaEl","MaMa","NoSi","AlAl","DeKi","ElSa","JoSe","SaUr","ScVa","ChHi","DaMc","JaHa","JoAr","PaSt","AaSc","LaNg","TySe","AaBu","JeNo","KaWi","MaHa","MiLi","PaHo","SeTh","ShSe","StNi","AlSy","ChFa","ChCh","HaSt","HeSn","JePa","LiNg","NiSt","RiCo","AmCa","AnMi","BrCl","CaWa","ReAr","StCs","TyKa","CoTa","PhRo","SeRe","CoLy","DaEd","JoBe","KaRi","OmVe","SaMe","StWe","StSp","AlSt","JaKo","kali","LiMi","PaMi","ZaCr","AnWe","AuRe","BeRo","ChLa","CoCh","DuCr","KeSm","RyBl","thle","TiBe","VeWa","MiMa","ChNg","BrTh"]

        self.sections = [22790,18550,18550,18550,18550,18550,18550,18550,18550,15890,16030,18690,18690,18690,18690,18690,16020,23630,19460,19460,19460,19460,19460,19460,19460,19460,19460,19460,19460,19460,19460,19460,19460,16680]

        self.sectionKeys = self.sections[:]
        self.sectionNames = ['A1','B1','C1','D1','E1','F1','G1','H1','I1','J1','K1','L1','M1','N1','O1','P1','Q1','A2','B2','C2','D2','E2','F2','G2','H2','I2','J2','K2','L2','M2','N2','O2','P2','Q2']
        self.sectionWidths = [86,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,60,85,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,60]

        self.sectionSolutions = [[] for _ in range(len(self.sections))]
        self.campLeaderSolutions = [[] for _ in range(len(self.sections))]
        self.campLengthsSolutions = []

        self.sectionsSortedNames = []
        self.sectionsSortedWidths = []

        self.dif = []

        self.sections.sort()#sections are solved from smallest to biggest to decrease chance of unsolvable final section
        # Sorts Section Names and Widths lists
        for section in self.sections:
            for i in range(len(self.sectionKeys)):
                if self.sectionKeys[i]==section:
                    self.sectionsSortedNames.append(self.sectionNames[i])
                    self.sectionsSortedWidths.append(self.sectionWidths[i])
                    del self.sectionKeys[i]
                    del self.sectionNames[i]
                    del self.sectionWidths[i]
                    break;

#---------------Begin Function Declarations------------------
#trys to find fit for a section with the campsite self.pieces
    def fit(self, sectionSize, LB, UB, maxNum,minNum=1):
        solution = []
        newPieces = []

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
        sectionSize = self.sections[position]

        s = []
        self.sectionsRemaining = 0

        for section in self.sectionSolutions:
            if section ==[]: self.sectionsRemaining+=1

        targetDif = (sum(self.pieces)-sum(self.sections[position:]))/self.sectionsRemaining

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
                        self.campLeaderSolutions[i].append(self.campLeaders[j])
                        del self.campLeaders[j]
                        del self.campSizeKeys[j]
                        break;

    def generateAndReturnSolution(self):
        self.getFullSolution()
        return spread, self.pieces, self.sectionsSortedNames, self.sectionSolutions, self.dif, self.campLeaderSolutions, self.campLengthsSolutions

    def printFullSolution(self):
        self.getFullSolution()

        print("\nSections")
        print(self.sectionsSortedNames)
        print("\nSolutions: ")
        print(self.sectionSolutions)
        print("\nDifferences between summed camp area and section area: ")
        print(self.dif)
        print("\nCamp Leaders: ")
        print(self.campLeaderSolutions)
        print("\nCamp Lengths: ")
        print(self.campLengthsSolutions)
        print("\nPieces remaining: ")
        print(self.pieces)
        print("\nThe spread is: " + str(spread))
        if(self.pieces!=[]): print("\nUnsolved self.sections. Run program again")

        filename = "Solutions.csv"
        f= open(filename, "w")
        headers = "Section, Solutions, Differences (ft2), Camping Leaders, Camping Lengths"
        f.write(headers+"\n")

        for i in range(len(self.sectionSolutions)):
            f.write(self.sectionsSortedNames[i]+","+str(self.sectionSolutions[i]).replace(",","|")+","+str(self.dif[i])+","+str(self.campLeaderSolutions[i]).replace(",","|")+","+str(self.campLengthsSolutions[i]).replace(",","|")+"\n")
        f.close()

#Generates all solutions and picks best one
for i in range(0,numSolToGen,1):
    print("\nSolving solution "+str(i+1)+" of "+str(numSolToGen))
    solution = CampSorter(maxIter,inc,initBounds,trysPerSect)
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
