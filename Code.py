import random
ProbCrosPar1 = 0.45
ProbCrosPar2 = 0.9

space = ' '
newLine = '\n'

def readInput(testFile) :
    file = open(testFile, 'r+')
    fileList = file.readlines()
    fileList = [s.replace('\n', '') for s in fileList]
    
    [days, doctors] = [int(i) for i in fileList[0].split()]
    maxCapacity = int(fileList[1])
    
    allShifts = []
    for i in range(2, days + 2):
        dayRequirements = fileList[i].split()
        morningReqs = [int(i) for i in dayRequirements[0].split(",")]
        eveningReqs = [int(i) for i in dayRequirements[1].split(",")]
        nightReqs = [int(i) for i in dayRequirements[2].split(",")]
        
        allShifts.append((morningReqs, eveningReqs, nightReqs))

    file.close()
    return [days, list(range(doctors)), maxCapacity, allShifts]



def columnSum(lst, index):
    return list(map(sum, zip(*lst)))[index]



class JobScheduler:
    def __init__(self, fileInfo):
        self.days = fileInfo[0]
        self.doctorsNum = len(fileInfo[1])
        self.doctorsIds = fileInfo[1]
        self.maxCapacity = fileInfo[2]
        self.allShifts = fileInfo[3]
        

        self.POPULATION_SIZE = 300
        self.elitismPercentage = 16
        self.pc = 0.65
        self.pm2 = 0.4
        self.ShiftsNum = self.days * 3
        self.chromosomes = self.generateInitialPopulation()
        


  
    def generateGnom(self):
        DocShifts = []
        for i in range (self.ShiftsNum):
            DocShifts.append(random.choice(range(2)))
        return DocShifts

        
    def generateInitialPopulation(self):
        population = []
        for i in range(self.POPULATION_SIZE):
            table = [[random.choice([0, 1]) for i in range( self.ShiftsNum)] for j in range( self.doctorsNum)]
            tableFit = self.calculateFitness(table)
            population.append([table, tableFit])
        return population
        
    
    def crossOver(self, par1, par2):
        child = []
        for satr in range(self.doctorsNum):
            prob = random.random()
            if prob < ProbCrosPar1:
                child.append(par1[satr])
            elif prob < ProbCrosPar2:
                child.append(par2[satr])
            else:
                child.append(self.generateGnom())
        return child
        
        
    def calculateFitness(self, chromosome):
        fitness = 0
        
        for ColumnIndex in range(self.days):
            dayNum = ColumnIndex
            for i in range(3):
                ColumnInChorom = dayNum * 3 + i
                realDocNum = columnSum(chromosome, ColumnInChorom)
                minimom = self.allShifts[ColumnIndex][i][0]
                maximom = self.allShifts[ColumnIndex][i][1]
                if realDocNum < minimom:
                    fitness += minimom - realDocNum
                elif realDocNum > maximom:
                    fitness += realDocNum - maximom
                    
        for doctor in range(self.doctorsNum):
            for dayNum in range(self.days - 1):
                shab = 3 * dayNum + 2
                farda_sob = 3 * (dayNum + 1) + 0
                farda_asr = 3 * (dayNum + 1) + 1
                if (chromosome[doctor][shab] == 1 and chromosome[doctor][farda_sob] == 1):
                    fitness += 1
                if (chromosome[doctor][shab] == 1 and chromosome[doctor][farda_asr] == 1):
                    fitness += 1
                    
        for doctor in range(self.doctorsNum):
            for dayNum in range(self.days - 2):
                emshab = 3 * dayNum + 2
                fardashab = 3 * (dayNum + 1) + 2
                pasfardashab = 3 * (dayNum + 2) + 2
                if (chromosome[doctor][emshab] == 1 and 
                    chromosome[doctor][fardashab] == 1 and 
                    chromosome[doctor][pasfardashab] == 1):
                    fitness += 1
                    
        for doctor in range(self.doctorsNum):
            if sum(chromosome[doctor]) > self.maxCapacity:
                fitness += sum(chromosome[doctor]) - self.maxCapacity
                    
        return fitness
                    

  
    
    def generateNewPopulation(self, population):
        newGeneration = []
        
        elitismNum = int((self.POPULATION_SIZE * self.elitismPercentage)/100)
        newGeneration.extend(population[:elitismNum])
        
        ConsiderParNum = int(self.pc * self.POPULATION_SIZE)
        restOfNewPop = self.POPULATION_SIZE - elitismNum
        for i in range(restOfNewPop):
            ParSelected = random.sample(range(0, ConsiderParNum), 2)
            par1 = population[ParSelected[0]][0]
            par2 = population[ParSelected[1]][0]
            child = self.crossOver(par1, par2)
            childFit = self.calculateFitness(child)
            newGeneration.append([child, childFit])
            
        return newGeneration
    
    
    
    
    
    
                
    def mutate2(self, chromosome):
        mutingSelected = random.choice(range(self.doctorsNum))
        for i in range(self.ShiftsNum):
            prob = random.random()
            if prob < 0.5:
                chromosome[mutingSelected][i] = 1 - chromosome[mutingSelected][i]
        return chromosome    
    
    
       
    def printTimeTable(self, table):
        fp = ''
        for i in range(self.ShiftsNum):
            if (i % 3 == 0):
                thisShift = self.DoTableFor1shift(table, i)
                fp += thisShift
                
            elif (i % 3 == 1):
                fp += space
                thisShift = self.DoTableFor1shift(table, i)
                fp += thisShift
                
            else:
                fp += space
                thisShift = self.DoTableFor1shift(table, i)
                fp += thisShift
                fp += newLine
        
        print(fp)
                
                
                
                
                
        
        
    def DoTableFor1shift(self, table, ColIndex):
        fp = ''
        for ID in range(self.doctorsNum):
            if table[ID][ColIndex] == 1:
                fp += str(ID)
                fp += ','
        fp = fp[:-1]
        return fp
    
    
    
    
    
    def schedule(self): 
        generation = 1
        found = False
        population = self.generateInitialPopulation()
        
        while not found:
            population = sorted(population, key = lambda x: x[1])            
            if population[0][1] <= 0:
                found = True
                self.printTimeTable(population[0][0])
                break
            newGeneration = self.generateNewPopulation(population)
            population = newGeneration
            generation += 1

            MutationNum2 = int(self.POPULATION_SIZE * self.pm2)
            
            mutingSelected_Indexes = random.sample(range(0 , self.POPULATION_SIZE), MutationNum2)
            
            for index in range(MutationNum2):
                parIndexInPopul = mutingSelected_Indexes[index]
                lastparChrom = population[parIndexInPopul][0]
                newparChrom = self.mutate2(lastparChrom)
                parFit = self.calculateFitness(newparChrom)
                mutingSelected_Indexes[index] = [newparChrom, parFit]



        

    
testFile1 = "test1.txt"

fileInfo1 = readInput(testFile1)

start = time.time()

scheduler = JobScheduler(fileInfo1)
scheduler.schedule()

end = time.time()

print("Test 1: ", '%.2f'%(end - start), 'sec')



testFile1 = "test2.txt"
fileInfo2 = readInput(testFile2)

start = time.time()

scheduler = JobScheduler(fileInfo2)
scheduler.schedule()

end = time.time()

print("Test 2: ", '%.2f'%(end - start), 'sec')


