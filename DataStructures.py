from scipy.stats import truncnorm #Imports the required libraries
import math


def truncatedNormal(mean=0, standardDeviation=1, lowerBound=0, upperBound=10):
    return truncnorm(
        (lowerBound - mean) / standardDeviation, (upperBound - mean) / standardDeviation, loc=mean,
        scale=standardDeviation)
    # Returns a normal distribution number between bounds (Used for random weight)  


def sigmoid(fedInMatrix):
    result = [[1 / (1 + math.exp(-fedInMatrix[i][j])) for j in range(len(fedInMatrix[0]))] for i in
              range(len(fedInMatrix))]  # Applies the sigmoid equation to every value in the matrix  
    return result  # Returns the result  


def doubleMatrixMultiplication(firstMatrix, secondMatrix, thirdMatrix):
    firstResult = matrixMatrixOperation(firstMatrix, secondMatrix,
                                        "*")  # Stores the result of the first two matrices multiplied together  
    return matrixMatrixOperation(firstResult.getMatrix(), thirdMatrix,
                                 "*")  # Does a matrix multiplication with the result of the first and the third matrix  


def dotProduct(firstMatrix, secondMatrix):
    result = [[sum(x * y for x, y in zip(i, j)) for j in zip(*secondMatrix)] for i in
              firstMatrix]  # Does the dot product of the two matrices  
    result = Matrix(result, 1)  # Converts the result to a matrix  
    return result  # Returns the matrix that is the dot product  


def matrixMatrixOperation(firstMatrix, secondMatrix, operatorFlag):
    if operatorFlag == "+":
        result = [[firstMatrix[i][j] + secondMatrix[i][j] for j in range(len(firstMatrix[0]))] for i in
                  range(len(firstMatrix))]  # Applies a matrix-matrix addition  
    elif operatorFlag == "-":
        result = [[firstMatrix[i][j] - secondMatrix[i][j] for j in range(len(firstMatrix[0]))] for i in
                  range(len(firstMatrix))]  # Applies a matrix-matrix subtraction  
    elif operatorFlag == "*":
        result = [[firstMatrix[i][j] * secondMatrix[i][j] for j in range(len(firstMatrix[0]))] for i in
                  range(len(firstMatrix))]  # Applies a matrix-matrix multiplication  
    elif operatorFlag == "/":
        result = [[firstMatrix[i][j] / secondMatrix[i][j] for j in range(len(firstMatrix[0]))] for i in
                  range(len(firstMatrix))]  # Applies a matrix-matrix division  
    result = Matrix(result, 1)  # Converts the resulting list into a matrix  
    return result  # Returns the result  


def matrixNumberOperation(number, fedInMatrix, operatorFlag):
    if operatorFlag == "-":
        result = [[number - fedInMatrix[i][j] for j in range(len(fedInMatrix[0]))] for i in
                  range(len(fedInMatrix))]  # Applies a number-matrix subtraction  
    elif operatorFlag == "*":
        result = [[number * fedInMatrix[i][j] for j in range(len(fedInMatrix[0]))] for i in
                  range(len(fedInMatrix))]  # Applies a number-matrix multiplication  
    elif operatorFlag == "/":
        result = [[number / fedInMatrix[i][j] for j in range(len(fedInMatrix[0]))] for i in
                  range(len(fedInMatrix))]  # Applies a number-matrix division  
    elif operatorFlag == "+":
        result = [[number + fedInMatrix[i][j] for j in range(len(fedInMatrix[0]))] for i in
                  range(len(fedInMatrix))]  # Applies a number-matrix addition  
    result = Matrix(result, 1)  # Converts the resulting list into a matrix  
    return result  # Returns the matrix  


class Classes:  # Data structure for holding all information about classes  
    def __init__(self):  # Constructor method initialises the empty classes list  
        self.classes = []

    def addClass(self, classToAdd):  # Procedure to add a class  
        self.classes.append(classToAdd)  # Appends the class object to the classes list structure  

    def getLength(self):
        return len(self.classes)  # Returns the length of the list structure holding all objects  

    def getClass(self, classToGet):  # Function to get class object in classes list  
        return self.classes[classToGet]  # Returns the newly acquired class  

    def getClassIndex(self, className):
        for index in range(len(self.classes)):  # Loops through class structure  
            if self.classes[index].getName() == className:  # Checks if the class name is equal to the one entered  
                return index  # Returns the index of the class  

    def getClasses(self):  # Function for getting all classes  
        return self.classes

    def removeClass(self, classIndex):  # Procedure to remove a class  
        self.classes.pop(classIndex)  # Remove that class from the list  


class singleClass:  # Single Class Class  
    def __init__(self, name):  # Constructor method takes the name when creating a class  
        self.name = name  # Sets the name  
        self.activeTests = []  # Creates empty data structures for holding class test objects  
        self.retiredTests = []  # Retired and active tests for viewing and uploading results  

    def getName(self):  # Function to return name of the class  
        return self.name

    def setName(self, name):  # Function to set the name of the class  
        self.name = name

    def getActiveTests(self):  # Function to get the list of active tests for a class  
        return self.activeTests

    def getActiveTest(self, index):  # Function for getting a certain active test at an index  
        return self.activeTests[index]

    def getRetiredTest(self, index):  # Function for getting a certain retired test at an index  
        return self.retiredTests[index]

    def getRetiredTests(self):  # Function to get the list of retired tests for a class  
        return self.retiredTests

    def addActiveTest(self, testToAdd):  # Procedure to add an active test object to the active test list structure  
        self.activeTests.append(testToAdd)

    def addRetiredTest(self, testToAdd):  # Procedure to add a retired test object to the retired test list structure  
        self.retiredTests.append(testToAdd)

    def removeTest(self, testToRemove):  # Procedure to remove test from the active tests structure  
        self.activeTests.pop(testToRemove)

    def retireTest(self, testToRetire):  # Procedure to retire an active test  
        indexFound = -1
        for testIndex in range(len(self.activeTests)):  # Loops through the length of the active tests list structure  
            if self.activeTests[
                testIndex].getTestName() == testToRetire:  # Checks if the name of the test is equal to the one entered  
                self.retiredTests.append(
                    self.activeTests[testIndex])  # Appends the activeTest to the retired test list structure  
                indexFound = testIndex
        if indexFound != -1: self.activeTests.pop(indexFound)  # Removes the test from the active tests list structure  


class Test:  # Test Class  
    def __init__(self, testName):  # Constructor method takes the test name as a parameter  
        self.testName = testName  # Assigns the test name to the required attribute  
        self.testQuestions = []  # Defines empty structures for the question objects and the test scores objects  
        self.testScores = []

    def getTestName(self):  # Function for getting the name of a test  
        return self.testName

    def getQuestions(self):  # Function for getting all questions associated with a test  
        return self.testQuestions

    def getScores(self):  # Function for getting the scores associated with a test  
        return self.testScores

    def getScore(self, index):  # Function for getting a score of a certain student at a certain index  
        return self.testScores[index]

    def addQuestion(self, questionToAdd, answerToAdd, categoryToAdd):  # Procedure for adding a question to the test  
        testQuestionToAdd = Question(questionToAdd, answerToAdd, categoryToAdd,
                                     True)  # Creates the question object with the required attributes  
        self.testQuestions.append(
            testQuestionToAdd)  # Appends the question object to the testQuestions list structure  

    def addAnswerCountQuestion(self, questionToAdd, answerCount):
        for index in range(len(self.testQuestions)):  # Loops through the test questions  
            if self.testQuestions[index].getQuestion() == questionToAdd:  # Compares the question to the question  
                self.testQuestions[index].setWrongAnswerCount(answerCount)  # Adds one to the wrong answer count  

    def getQuestion(self, indexOfQuestion):  # Function for getting a question of a test  
        return self.testQuestions[indexOfQuestion].question

    def removeQuestion(self, questionToRemove):  # Procedure for removing a question of a test  
        for question in range(
                len(self.testQuestions)):  # Loops through the length of the test questions list structure  
            if self.getQuestion(question) == questionToRemove:  # Checks if the questions are equal  
                self.testQuestions.pop(question)  # Removes the question if they are  

    def addTestScore(self, studentName, studentScore):  # Procedure for adding a test score to the test  
        scoreToAdd = testScore(studentName, studentScore)  # Creates the testScore object  
        self.testScores.append(scoreToAdd)  # Appends it to the testScores list structure  


class Question:  # Question Class  
    def __init__(self, question, answer, category,
                 isUsed):  # Constructor method with question answer and category as required parameters  
        self.question = question  # Sets the default attributes  
        self.answer = answer
        self.category = category
        self.wrongAnswerCount = 0
        self.isUsed = isUsed

    def getWrongAnswerCount(self):  # Function for getting the wrong answer count  
        return self.wrongAnswerCount

    def addWrongAnswerCount(self):  # Procedure for incrementing the wrong answer count  
        self.wrongAnswerCount += 1

    def setWrongAnswerCount(self, number):  # Procedure for setting the wrong answer count  
        self.wrongAnswerCount = number

    def getCategory(self):  # Function for getting the category of a question  
        return self.category

    def getQuestion(self):  # Function for getting the question of a question  
        return self.question

    def getAnswer(self):  # Function for getting the answer of a question  
        return self.answer

    def getUsed(self):  # Function for getting the used status of a question  
        return self.isUsed

    def setUsed(self):  # Procedure for setting the isUsed attribute to True when the question is added to a test  
        self.isUsed = True

    def setUnused(self):  # Procedure for setting the isUsed attribute to False when all questions are used  
        self.isUsed = False


class allQuestions:  # Class containing all the questions  
    def __init__(self):  # Constructor method defines an empty questions list structure  
        self.questions = []

    def addQuestion(self, questionToAdd, answerToAdd, categoryToAdd, isUsed):  # Procedure for adding a question  
        testQuestionToAdd = Question(questionToAdd, answerToAdd, categoryToAdd,
                                     isUsed)  # Creates the question object with the required attributes  
        self.questions.append(
            testQuestionToAdd)  # Appends the newly created question object to the questions list structure  

    def findAndSetQuestionUsed(self,
                               questionToSet):  # Procedure for finding a question by name and setting the isUsed attribute to true  
        for question in range(len(self.questions)):  # Loops through the length of all questions  
            if self.questions[
                question].getQuestion() == questionToSet:  # Checks if the question text is equal to the parameter  
                self.questions[question].setUsed()  # If they are the same, set the question to used  

    def getQuestion(self, index):  # Function for getting the question associated with an index  
        return self.questions[index]

    def getQuestions(self):  # Function for getting all the questions so the program can iterate over them  
        return self.questions

    def setAllQuestionsUnused(self):  # Procedure for setting all questions as unused  
        for question in range(len(self.questions)):  # Loops through the length of the question structure  
            self.questions[question].setUnused()  # Sets the question unused  


class testScore:  # Class for Test Score  
    def __init__(self, name, score):  # Constructor method with name and score as required parameters  
        self.studentName = name
        self.studentScore = score

    def getStudentName(self):  # Function for getting the student name  
        return self.studentName

    def getStudentScore(self):  # Function for getting the student score  
        return self.studentScore


class boxDigit:  # Class for  
    def __init__(self, filename):  # Initialisation method for the box digit class  
        self.filename = filename  # Sets the file name  
        self.averages = []
        self.numberRecognised = -1  # Sets the number recognised and corrected to -1 because they haven't been corrected yet  
        self.numberCorrected = -1
        self.studentName = ""
        self.lineNumber = -1  # Sets the line number and position to -1 because they haven't been recognised yet  
        self.linePosition = -1
        self.checkFlag = None

    def getCheckFlag(self):  # Getter method for the checking flag  
        return self.checkFlag

    def setCheckFlag(self, value):  # Setter method for the checking flag  
        self.checkFlag = value

    def getLinePosition(self):  # Getter method for the line position  
        return self.linePosition

    def setLinePosition(self, linePosition):  # Setter method for changing the line position  
        self.linePosition = linePosition

    def getLineNumber(self):  # Getter method for the line number  
        return self.lineNumber

    def setLineNumber(self, lineNumber):  # Setter method for changing the line number  
        self.lineNumber = lineNumber

    def getStudentName(self):  # Getter method for the student name  
        return self.studentName

    def setStudentName(self, studentName):  # Setter method for changing the student name  
        self.studentName = studentName

    def getFilename(self):  # Getter method for the file name  
        return self.filename

    def setAverages(self, averages):  # Setter method for changing the averages  
        self.averages = averages

    def getAverages(self):  # Getter method for getting the averages  
        return self.averages

    def setNumberRecognised(self, numberRecognised):  # Setter method for changing the number recognised  
        self.numberRecognised = numberRecognised

    def getNumberRecognised(self):  # Getter method for getting the number recognised  
        return self.numberRecognised

    def setNumberCorrected(self, numberCorrected):  # Setter method for changing the number corrected  
        self.numberCorrected = numberCorrected

    def getNumberCorrected(self):  # Getter method for getting the number corrected  
        return self.numberCorrected


class allScores:  # Class for holding all box digits  
    def __init__(self):  # Constructor method defining the scores attribute  
        self.scores = []

    def getScores(self):  # Getter method for the scores attribute  
        return self.scores

    def changeScores(self, newScores):  # Setter method for the scores attribute  
        self.scores = newScores

    def findAndChangeScores(self, newScores):
        filenameList = [score.getFilename() for score in newScores]  # Gets the list of filename's from the new scores  
        newScores.extend(score for score in self.scores if
                         score.getFilename() not in filenameList)  # Extends the new scores with the score data structure, making sure there are no duplicates  
        self.changeScores(newScores)  # Changes the scores  

    def addScore(self, scoreObject):  # Procedure for adding a score to the scores attribute.  
        self.scores.append(scoreObject)


class neuralNetwork:
    def __init__(self, inputNodeNumber, outputNodeNumber, hiddenNodeNumber, learningRate):
        self.numberOfInputNodes = inputNodeNumber  # Sets the required attributes  
        self.numberOfOutputNodes = outputNodeNumber
        self.numberOfHiddenNodes = hiddenNodeNumber
        self.learningRate = learningRate
        self.weightMatrices()  # Calls the function to initialise the weight matrices  

    def getNumberOfInputNodes(self):  # Function for getting the number of input nodes  
        return self.numberOfInputNodes

    def getNumberOfOutputNodes(self):  # Function for getting the number of output nodes  
        return self.numberOfOutputNodes

    def getNumberOfHiddenNodes(self):  # Function for getting the number of hidden nodes  
        return self.numberOfHiddenNodes

    def getLearningRate(self):  # Function for getting the learning rate  
        return self.learningRate

    def getHiddenNodeWeights(self):  # Function for getting the hidden node weight matrix  
        return self.hiddenNodeWeights

    def getHiddenNodeOutputWeights(self):  # Function for getting the hidden node output weight matrix  
        return self.hiddenNodeOutputWeights

    def setHiddenNodeWeights(self, newWeights):  # Procedure for setting the hidden node weight matrix  
        self.hiddenNodeWeights = newWeights

    def setHiddenNodeOutputWeights(self, newWeights):  # Procedure for setting the hidden node output weight matrix  
        self.hiddenNodeOutputWeights = newWeights

    def weightMatrices(self):
        bounds = 1 / math.sqrt(
            self.getNumberOfInputNodes())  # Gets the bounds for the truncated normal function using the number of input nodes  
        truncatedNorm = truncatedNormal(mean=0, standardDeviation=1, lowerBound=-bounds,
                                        upperBound=bounds)  # Applies the truncated norm function to get a value  
        self.hiddenNodeWeights = truncatedNorm.rvs((self.getNumberOfHiddenNodes(),
                                                    self.getNumberOfInputNodes())).tolist()  # Applies the rvs function to get a random variable within the shape parameters  
        self.hiddenNodeWeights = Matrix(self.getHiddenNodeWeights(), 1)  # Converts the weights to a matrix  

        bounds = 1 / math.sqrt(
            self.getNumberOfHiddenNodes())  # Gets the bounds for the truncated normal function using the number of input nodes  
        truncatedNorm = truncatedNormal(mean=0, standardDeviation=1, lowerBound=-bounds,
                                        upperBound=bounds)  # Applies the truncated norm function to get a value  
        self.hiddenNodeOutputWeights = truncatedNorm.rvs((self.getNumberOfOutputNodes(),
                                                          self.getNumberOfHiddenNodes())).tolist()  # Applies the rvs function to get a random variable within the shape parameters  
        self.hiddenNodeOutputWeights = Matrix(self.hiddenNodeOutputWeights, 1)  # Converts the weights to a matrix  

    def train(self, inputData, targetData):
        # GETTING CURRENT OUTPUT  
        inputData = Matrix(inputData,
                           2).transposeMatrix()  # Converts the input data into a matrix in 2 dimensions and transposes it  
        targetData = Matrix(targetData,
                            2).transposeMatrix()  # Converts the target data into a matrix in 2 dimensions and transposes it  

        outputDataNew = dotProduct(self.getHiddenNodeWeights().getMatrix(),
                                   inputData.getMatrix())  # Gets the dot product of the hidden node weight matrix and input matrix  
        outputDataHidden = Matrix(sigmoid(outputDataNew.getMatrix()),
                                  1)  # Gets the 1 dimensional matrix of the sigmoid product of the output data matrix  

        outputDataFinal = dotProduct(self.getHiddenNodeOutputWeights().getMatrix(),
                                     outputDataHidden.getMatrix())  # Gets the dot product of the hidden node output matrix and the sigmoid input matrix  
        outputDataNetwork = Matrix(sigmoid(outputDataFinal.getMatrix()),
                                   1)  # Gets the 1d matrix sigmoid product of the previous dot product  

        outputLoss = matrixMatrixOperation(targetData.getMatrix(), outputDataNetwork.getMatrix(),
                                           "-")  # Calculates the output loss by subtracting the target data matrix from the output data matrix  

        # UPDATING WEIGHTS  
        tempWeight = doubleMatrixMultiplication(outputLoss.getMatrix(), outputDataNetwork.getMatrix(),
                                                (matrixNumberOperation(1.0, outputDataNetwork.getMatrix(),
                                                                       "-").getMatrix()))  # Gets the double matrix multiplication of outputLoss, outputData and subtraction of the outputHidden from 1  
        tempDotProduct = dotProduct(tempWeight.getMatrix(),
                                    outputDataHidden.transposeMatrix().getMatrix())  # Gets the dot product of the tempWeight and the outputHiddenData transposed  
        tempWeight = matrixNumberOperation(self.getLearningRate(), tempDotProduct.getMatrix(),
                                           "*")  # Multiplies the learning rate by the tempDotProduct  

        self.hiddenNodeOutputWeights = matrixMatrixOperation(self.getHiddenNodeOutputWeights().getMatrix(),
                                                             tempWeight.getMatrix(),
                                                             "+")  # Sets the new hidden output weights by the addition of the temp weight and previous hidden output weights  

        # CALCULATES HIDDEN ERROR  
        hiddenLoss = dotProduct(self.getHiddenNodeOutputWeights().transposeMatrix().getMatrix(),
                                outputLoss.getMatrix())  # Through the dot product of the transposed hidden node output weights and the output loss  

        # UPDATES THE WEIGHTS  
        temp = doubleMatrixMultiplication(hiddenLoss.getMatrix(), outputDataHidden.getMatrix(),
                                          (matrixNumberOperation(1.0, outputDataHidden.getMatrix(),
                                                                 "-").getMatrix()))  # Double matrix multiplication with hiddenLoss, outputHiddenData and subtracted outputHiddenData from 1  

        tempPartialCalc = dotProduct(temp.getMatrix(),
                                     inputData.transposeMatrix().getMatrix())  # Gets dot product of previous temp and the transposed input data  
        tempWeightCopy = matrixNumberOperation(self.getLearningRate(), tempPartialCalc.getMatrix(),
                                               "*")  # Multiplies the learning rate by the temp matrix  
        self.hiddenNodeWeights = matrixMatrixOperation(self.getHiddenNodeWeights().getMatrix(),
                                                       tempWeightCopy.getMatrix(),
                                                       "+")  # Appends the tempWeight to the previous hidden node weights  

    def run(self, inputData):
        inputDataMatrix = Matrix(inputData, 2).transposeMatrix()  # Turns the input data to a column matrix  
        outputData = dotProduct(self.getHiddenNodeWeights().getMatrix(),
                                inputDataMatrix.getMatrix())  # Takes the dot product of the hidden node weights and input matrix  
        outputData = Matrix(sigmoid(outputData.getMatrix()), 1)  # Gets the 1d matrix of the sigmoid of the outputData  

        outputData = dotProduct(self.getHiddenNodeOutputWeights().getMatrix(),
                                outputData.getMatrix())  # Gets the dot product of the hidden node output weights and calculated output data  
        outputData = Matrix(sigmoid(outputData.getMatrix()),
                            1)  # Gets the 1d matrix of the sigmoid of the new outputData  

        outputData = outputData.transposeMatrix()  # Transposes the output data matrix, turning it back from a column  

        result = outputData.getMatrix()[0]
        return result  # Returns the output data result  


class Matrix:
    def __init__(self, matrix, minimumDimensions):
        self.matrix = matrix  # Sets the required attributes  
        self.size = 0
        self.max = 0
        self.min = float('inf')
        self.shape = []
        self.minimumDimensions = minimumDimensions
        self.calculateDimensions()  # Calculates the minimum dimensions  

    def getMatrix(self):  # Function to get matrix  
        return self.matrix

    def getMax(self):  # Function to get the maximum  
        return self.max

    def calculateDimensions(self):
        dimensionsList = self.getDimensions(self.matrix)  # Gets the dimensions list from feeding in the list  
        dimensionsCount = len(
            dimensionsList)  # Gets the number of the dimensions from the length of the list, which is 1,2,3,4...  
        if self.minimumDimensions > dimensionsCount:  # Checks if the minimum dimensions is greater than the current dimensions  
            difference = (
                        self.minimumDimensions - dimensionsCount)  # Takes the difference to see how many dimensions to add  
            for dimension in range(difference):  # Loops through the dimensions to add  
                listBox = list()  # Takes an empty list  
                listBox.append(self.matrix)  # Appends the matrix to the list  
                self.matrix = listBox  # Sets the matrix to the new dimension list  
        if dimensionsCount == 1:  # Checks if the matrix is 1d  
            self.size = dimensionsList[0]  # Sets the size to the length of the list  
            self.shape = [None, dimensionsList[0]]  # Sets the size to none, and the column count  
        else:  # It is a 2d list or more  
            self.size = self.calculateSize(
                dimensionsList)  # Sets the size to the size calculated from the dimensions list  
            self.shape = dimensionsList  # Sets the shape to the dimensions list  
        self.max = self.calculateMaxAndMin(self.matrix, "max")  # Calculates the minimum and maximum of the matrix  
        self.min = self.calculateMaxAndMin(self.matrix, "min")

    def calculateSize(self, listToCalculate):
        total = 1  # Sets the total size to 1  
        for dataItem in range(0, len(listToCalculate)):  # Loops through the length of the list  
            total *= listToCalculate[dataItem]  # Multiplies the current total by the list size  
        return total  # Returns the total size  

    def transposeMatrix(self):
        dimensions = len(self.getDimensions(self.matrix))  # Gets the dimension of the matrix  
        if dimensions > 1:  # If the dimensions are greater than one, you need to transpose the matrix  
            temp = Matrix([[self.matrix[j][i] for j in range(len(self.matrix))] for i in range(len(self.matrix[0]))],
                          1)  # Transposes the matrix and creates it as a new matrix  
            return temp  # Returns the transposed matrix  

    def getDimensions(self, listFedIn):
        if not type(listFedIn) == list:  # Checks if the item fed in is not a list  
            return []  # Returns a blank list  
        return [len(listFedIn)] + self.getDimensions(
            listFedIn[0])  # Returns the length of the current list, plus the recursive result of the sublist item  

    def calculateMaxAndMin(self, listFedIn, minOrMaxFlag):
        length = len(listFedIn)  # Calculates the length of the list  
        if length > 1:  # Checks if the length is greater than one  
            midpoint = length // 2  # Finds the midpoint of the length  
            firstHalfValue = self.calculateMaxAndMin(listFedIn[:midpoint],
                                                     minOrMaxFlag)  # Recursively calculates the max/min of the first half  
            secondHalfValue = self.calculateMaxAndMin(listFedIn[midpoint:],
                                                      minOrMaxFlag)  # Recursively calculates the max/min of the second half  
            if minOrMaxFlag == "max":  # If you are calculating the maximum  
                if firstHalfValue > secondHalfValue:  # Finds which value is bigger and returns it  
                    return firstHalfValue
                else:
                    return secondHalfValue
            elif minOrMaxFlag == "min":  # If you are calculating the minimum  
                if firstHalfValue < secondHalfValue:  # Finds which value is smaller and returns it  
                    return firstHalfValue
                else:
                    return secondHalfValue
        elif length < 1:  # If the length is less than one, not an item and returns None  
            return None
        else:  # Item is of length one  
            if isinstance(listFedIn[0], list):  # Checks if it is a list  
                return self.calculateMaxAndMin(listFedIn[0], minOrMaxFlag)  # Feeds in the list  
            else:
                return listFedIn[0]  # Returns the first value of the list  
