import random
import json

with open('InputData.json', 'r') as f:
  data = json.load(f)
class CampSorter:

    def __init__(self, maxAttempts = 10000, increment = 5, boundsDifStart = 0, trysPerSection = 25):
        self.pieces = data["pieces"]
        self.maxAttempts = maxAttempts
        self.increment = increment
        self.boundsDifStart = boundsDifStart
        self.trysPerSection = trysPerSection

        self.campSizeKeys = self.pieces[:]
        self.campLeaders = ["AlBe","RaEd","HeJo","NeMe","KeLe","FeHa","JeEl","TiKr","CaGo","DeLi","CoPr","JoPo","KeC","KeBu","SAMC","AlCh","GrMa","KaGr","MeKa","JePe","BrSc","AdDi","AlSe","ChDo","JoJo","AnMa","DuDi","AaJo","BrMe","CaCo","BrCa","JeTr","MeSp","CaMa","JeAl","MiBe","LiBe","AnKi","KhSi","MaKi","LyJo","SaN","AyEr","MeHe","NaBl","PaSc","JaLe","MiDo","RyPi","SaBu","DoKo","MiRa","YoLo","DeHo","DeGu","GiGa","IaMu","MaWr","BrMe","MiAn","NaLe","ScKe","AlPe","KaRa","LeSc","NiSl","shda","BrBi","CaCa","JoCa","LaEl","MaMa","NoSi","AlAl","DeKi","ElSa","JoSe","SaUr","ScVa","ChHi","DaMc","JaHa","JoAr","PaSt","AaSc","LaNg","TySe","AaBu","JeNo","KaWi","MaHa","MiLi","PaHo","SeTh","ShSe","StNi","AlSy","ChFa","ChCh","HaSt","HeSn","JePa","LiNg","NiSt","RiCo","AmCa","AnMi","BrCl","CaWa","ReAr","StCs","TyKa","CoTa","PhRo","SeRe","CoLy","DaEd","JoBe","KaRi","OmVe","SaMe","StWe","StSp","AlSt","JaKo","kali","LiMi","PaMi","ZaCr","AnWe","AuRe","BeRo","ChLa","CoCh","DuCr","KeSm","RyBl","thle","TiBe","VeWa","MiMa","ChNg","BrTh"]

        self.sections = [22790,18550,18550,18550,18550,18550,18550,18550,18550,15890,16030,18690,18690,18690,18690,18690,16020,23630,19460,19460,19460,19460,19460,19460,19460,19460,19460,19460,19460,19460,19460,19460,19460,16680]

        self.sectionKeys = self.sections[:]
        self.sectionNames = ['A1','A2','A3','A4','A5','A6','B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','B11','B12','B13','B14','B15','B16','B17','B18','B19','B20','B21','B22','B23','B24','B25','B26','B27','B28', "B29", "B30"]
        self.sectionWidths = [70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,60,85,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,60]

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
                    break

#---------------Begin Function Declarations------------------
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


