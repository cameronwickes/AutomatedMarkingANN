import json #Imports the required libraries
from DataStructures import *
import os
import cv2
import numpy as np
import shutil
import random


def handleNetworkDataInput():
    filesInDir = findFilesInTestDirectory(".", ".json")  # Gets the json files in the current directory  
    if "networkData.json" in filesInDir:  # Checks if the network data file exists  
        myNeuralNetwork = handleWeightDataInput()  # Handles the network data input if the file exists  
    else:  # No network file in current directory  
        myNeuralNetwork = neuralNetwork(7, 11, 60, 0.1)  # Creates a new neural network  
        myNeuralNetwork = handleTrainingDataInput(myNeuralNetwork, 10000)  # Trains the neural network  
        handleNetworkDataOutput(myNeuralNetwork)  # Handles the data output and writes the network data to a file  
    return myNeuralNetwork  # Returns the new neural network  


def handleNetworkDataOutput(neuralNetwork):
    # GETS THE DATA INTO A JSON FORMAT  
    finalData = json.dumps(
        dict(learningrate=neuralNetwork.getLearningRate(), numberofhiddennodes=neuralNetwork.getNumberOfHiddenNodes(),
             numberofinputnodes=neuralNetwork.getNumberOfInputNodes(),
             numberofoutputnodes=neuralNetwork.getNumberOfOutputNodes(),
             hiddennodeweights=neuralNetwork.getHiddenNodeWeights().getMatrix(),
             hiddennodeoutputweights=neuralNetwork.getHiddenNodeOutputWeights().getMatrix()))
    fileHandle = open("networkData.json", "w", encoding="utf-8")  # Opens the file to write the new data to  
    print("[" + finalData + "]", file=fileHandle,
          end="")  # Prints the json format opening bracket, data and the closing bracket  
    fileHandle.close()  # Closes the file handle  


def handleTrainingDataOutput(trainingDataSet):
    bigList = []  # Creates the empty data structure to hold the final training data set  
    for data in trainingDataSet:  # Loops through the data set  
        inputData = data[0]  # Gets the input and output data  
        outputData = data[1]
        tempData = dict(pixelValues=inputData, numberValues=outputData)  # Converts the data to a dictionary  
        bigList.append(tempData)  # Appends the bigger list with the data dictionary  
    finalData = json.dumps(bigList)  # Json parses the big list  
    fileHandle = open("trainingData.json", "w", encoding="utf-8")  # Opens the file to write the new data to  
    print(finalData, file=fileHandle, end="")  # Prints the json formatted data  
    fileHandle.close()  # Closes the file handle  


def handleWeightDataInput():
    fileHandle = open("networkData.json", "r", encoding="utf-8")  # Opens the network data file  
    lines = json.load(fileHandle)[0]  # Loads the json data into python  
    myNeuralNetwork = neuralNetwork(lines['numberofinputnodes'], lines['numberofoutputnodes'],
                                    lines['numberofhiddennodes'],
                                    lines['learningrate'])  # Creates a new neural network with the parameters read in  
    myNeuralNetwork.setHiddenNodeWeights(Matrix(lines['hiddennodeweights'], 1))  # Sets the weight matrices  
    myNeuralNetwork.setHiddenNodeOutputWeights(Matrix(lines['hiddennodeoutputweights'], 1))
    fileHandle = open("trainingData.json", "r", encoding="utf-8")  # Opens training data file with utf-8 encoding  
    lines = json.load(fileHandle)  # Reads all lines in with json load function to get to dictionary  
    trainingDataSet = [[line['pixelValues'], line['numberValues']] for line in
                       lines]  # Takes the data into a training data set  
    count = 0  # Sets the count to zero  
    for dataIndex in range(len(trainingDataSet)):  # Loops through the training data set  
        dataOut = myNeuralNetwork.run(trainingDataSet[dataIndex][0])  # Feeds in the value and gets the data out  
        for dataOutIndex in range(len(dataOut)):  # Loops through the length of the output data  
            index = dataOut.index(max(dataOut))  # Gets the index of the maximum value  
            if dataOutIndex == index:
                dataOut[dataOutIndex] = 1  # Sets a one for the maximum value  
            else:
                dataOut[dataOutIndex] = 0  # Sets a zero for anything else  
        if trainingDataSet[dataIndex][1] == dataOut:  # Checks if the trained data value is the same as the label  
            count += 1  # Adds one to the count  
    print((count / len(trainingDataSet)) * 100)  # Prints the accuracy from the file  
    return myNeuralNetwork  # Returns the neural network  


def handleTrainingDataInput(neuralNetwork, epochCount):
    fileHandle = open("trainingData.json", "r", encoding="utf-8")  # Opens training data file with utf-8 encoding  
    lines = json.load(fileHandle)  # Reads all lines in with json load function to get to dictionary  
    trainingDataSet = [[line['pixelValues'], line['numberValues']] for line in
                       lines]  # Takes the data into a training data set  
    for epoch in range(epochCount):  # Loops through each epoch  
        print("Epoch ", epoch)  # Prints the epoch count  
        for dataIndex in range(len(trainingDataSet)):  # Loops through the data set  
            neuralNetwork.train(trainingDataSet[dataIndex][0], trainingDataSet[dataIndex][
                1])  # Trains the neural network with the pixel values and the label  
    count = 0  # Sets the count to zero  
    for secondDataIndex in range(len(trainingDataSet)):  # Loops through the training data set  
        print('Label: {}'.format(trainingDataSet[secondDataIndex][1]))  # Prints the label  
        dataOut = neuralNetwork.run(trainingDataSet[secondDataIndex][0])  # Feeds in the value and gets the data out  
        for dataOutIndex in range(len(dataOut)):  # Loops through the length of the output data  
            index = dataOut.index(max(dataOut))  # Gets the index of the maximum value  
            if dataOutIndex == index:
                dataOut[dataOutIndex] = 1  # Sets a one for the maximum value  
            else:
                dataOut[dataOutIndex] = 0  # Sets a zero for anything else  
        print('Predicted: {}'.format(dataOut))  # Prints the trained data values  
        if trainingDataSet[secondDataIndex][
            1] == dataOut:  # Checks if the trained data value is the same as the label  
            print("SUCCESS")  # Prints success  
            count += 1  # Adds one to the count  
        else:
            print("FAILURE")  # Prints failure as data doesn't match  
    print((count / len(trainingDataSet)) * 100)  # Prints the accuracy from the file  
    return neuralNetwork  # Returns the trained neural network  


def handleTeacherDataInput():  # Procedure for populating data structures from json file  
    fileHandle = open("teacherData.json", "r", encoding="utf-8")  # Opens file with utf-8 encoding  
    lines = json.load(fileHandle)  # Reads all lines in with json load function to get to dictionary  
    myTeacherStructure = Classes()  # Creates an empty Teachers structure  
    for jsonClass in lines:  # Loops through teacher in the read in lines  
        className = jsonClass['name']  # Takes the teacher name, username and password out  
        tempClass = singleClass(className)  # Creates a temporary teacher data structure with the required data  
        for testName, testData in jsonClass['activeTests'].items():  # For each test in the teachers activetests  
            tempTest = Test(testName)  # Creates an empty temporary test with the required data  
            for index in range(len(jsonClass['activeTests'][testName][
                                       'questions'])):  # Loops through the questions and adds the question to the test  
                tempTest.addQuestion(jsonClass['activeTests'][testName]['questions'][index],
                                     jsonClass['activeTests'][testName]['answers'][index],
                                     jsonClass['activeTests'][testName]['categories'][index])
            tempClass.addActiveTest(tempTest)  # Adds the created temporary test to the teacher structures activetests  

        for testName, testData in jsonClass['retiredTests'].items():  # Loops through the teachers retired tests  
            tempTest = Test(testName)  # Creates a temporary test with the required data  
            for index in range(len(jsonClass['retiredTests'][testName][
                                       'questions'])):  # Loops through the questions adding the questions to the test  
                tempTest.addQuestion(jsonClass['retiredTests'][testName]['questions'][index],
                                     jsonClass['retiredTests'][testName]['answers'][index],
                                     jsonClass['retiredTests'][testName]['categories'][index])
                tempTest.addAnswerCountQuestion(jsonClass['retiredTests'][testName]['questions'][index],
                                                jsonClass['retiredTests'][testName]['wrongCount'][index])
            for index in range(len(jsonClass['retiredTests'][testName]['testScores'][
                                       'students'])):  # Loops through the scores, adding them to the test  
                tempTest.addTestScore(jsonClass['retiredTests'][testName]['testScores']['students'][index],
                                      jsonClass['retiredTests'][testName]['testScores']['scores'][index])
            tempClass.addRetiredTest(tempTest)  # Adds the temporary retired test to the teachers retired tests  
        myTeacherStructure.addClass(tempClass)  # Adds the teacher to the teachers structure  
    fileHandle.close()  # Closes the file handle for the teacher data json file  
    return myTeacherStructure


def handleQuestionDataInput():
    myQuestionStructure = allQuestions()  # Creates an empty data structure for holding all the questions  
    fileHandle = open("testQuestions.json", "r", encoding="utf-8")  # Opens the test question file with utf-8 encoding  
    lines = json.load(fileHandle)  # Reads in all the lines from the json file  
    for question in lines:  # Loops through the questions  
        boolValue = eval(question['used'])
        myQuestionStructure.addQuestion(question['question'], question['answer'], question['category'],
                                        boolValue)  # Adds the question to the question data structure  
    fileHandle.close()  # Closes the handle associated with the question data  
    return myQuestionStructure  # Returns the two populated data structures  


def handleQuestionDataOutput(questionDataStructure):
    finalData = []  # Makes the required structure  
    for questionData in questionDataStructure.getQuestions():  # Loops through each question  
        question = questionData.getQuestion()  # Gets the required attributes and forms the relevant dictionaries  
        answer = questionData.getAnswer()
        category = questionData.getCategory()
        isUsed = questionData.getUsed()
        tempQuestion = json.dumps(dict(question=question, answer=answer, category=category, used=str(isUsed)))
        finalData.append(tempQuestion)  # Adds the question  
    fileHandle = open("testQuestions.json", "w", encoding="utf-8")  # Opens the file to write the new data to  
    print("[", file=fileHandle, end="")  # Prints the json format opening bracket  
    print((','.join(finalData)), file=fileHandle, end="")  # Prints the teachers json, joining each one by a comma  
    print("]", file=fileHandle, end="")  # Printing the json format closing bracket  


def handleDataOutput(teacherDataStructure):  # Procedure to handle writing data to the teacher json file  
    finalData = []  # Creates an empty list structure to hold the teacher dictionaries  
    for singleClass in teacherDataStructure.getClasses():  # Loops through each teacher in the data structure  
        activeTests = {}  # Creates two empty dictionaries for the retired and active tests  
        retiredTests = {}
        for test in singleClass.getActiveTests():  # Loops through the tests in the active tests  
            collectedQuestions = []  # Creates empty data structures for holding the questions, answers and categories  
            collectedAnswers = []
            collectedCategories = []
            for question in test.getQuestions():  # Loops through each question in the test  
                collectedQuestions.append(
                    question.getQuestion())  # Appends the question answer and category to the relevant structures  
                collectedAnswers.append(question.getAnswer())
                collectedCategories.append(question.getCategory())
            tempTest = dict([(test.testName, dict(questions=collectedQuestions, answers=collectedAnswers,
                                                  categories=collectedCategories))])
            activeTests.update(
                tempTest)  # Creates a dictionary with all the questions, answers and categories of that test and updates the active tests dictionary with that test  
        for test in singleClass.getRetiredTests():  # Does the same with the retired tests, but with scores as well  
            collectedQuestions = []
            collectedAnswers = []
            collectedCategories = []
            collectedWrongAnswerCounts = []
            astudent = []  # Two empty data structures for holding the students and scores  
            ascore = []
            for question in test.getQuestions():
                collectedQuestions.append(question.getQuestion())
                collectedAnswers.append(question.getAnswer())
                collectedCategories.append(question.getCategory())
                collectedWrongAnswerCounts.append(question.getWrongAnswerCount())
            for score in test.getScores():  # Loops through the scores part of the structure  
                ascore.append(score.studentScore)
                astudent.append(score.studentName)
            tempTest = dict([(test.testName, dict(questions=collectedQuestions, answers=collectedAnswers,
                                                  categories=collectedCategories, wrongCount=collectedWrongAnswerCounts,
                                                  testScores=dict(students=astudent, scores=ascore)))])
            retiredTests.update(tempTest)  # Adds the test to the retiredTests dictionary  
        dictFinal = json.dumps(dict(name=singleClass.name, activeTests=activeTests, retiredTests=retiredTests))
        finalData.append(dictFinal)  # Adds the json dumped dictionary to final data  
    fileHandle = open("teacherData.json", "w", encoding="utf-8")  # Opens the file to write the new data to  
    print("[", file=fileHandle, end="")  # Prints the json format opening bracket  
    print((','.join(finalData)), file=fileHandle, end="")  # Prints the teachers json, joining each one by a comma  
    print("]", file=fileHandle, end="")  # Printing the json format closing bracket  


def createNewClass(teacherDataStructure, className):
    newClass = singleClass(className)  # Creates a new class with the required class name  
    teacherDataStructure.addClass(newClass)  # Adds the class to the data structure  
    handleDataOutput(teacherDataStructure)  # Outputs the data to a file  
    return teacherDataStructure  # Returns the new structure  


def createFolderCheck(dirName, folderName):  # Function for checking if a folder is in a directory  
    folders = []  # Creates the empty list structure for holding names of folders  
    for root, directory, file in os.walk(
            dirName):  # Walks the directory grabbing the root,directory and file of each file  
        for folder in directory:  # Goes through each folder in directory  
            folders.append(folder)  # Appends the folder name to the data structure  
    if folderName not in folders:  # If there is no folder in the dir  
        return "Not in use"  # Return the message saying the file is not in user  
    else:  # Else return appropriate error message  
        return "In use"


def createImagesFolder():  # Procedure for creating the test images folder  
    directory = os.getcwd()  # Gets the working directory of the files  
    if createFolderCheck(directory, "Test Images") == "Not in use":  # Checks if the Test Images folder exists  
        os.mkdir("Test Images")  # Makes the folder if it doesn't exist  

def createClassFolder(className):
    createImagesFolder()  # Creates the image folder if it isn't there already 
    directory = os.getcwd() + "\\" + "Test Images"  # Gets the directory and adds the test images name to it  
    if createFolderCheck(directory, className) == "Not in use":  # Checks if the folder is in use  
        os.mkdir(directory + "\\" + className)  # Makes the teacher testImages Directory if it is not there  

def createTestFolder(folderName, className):  # Procedure for creating the image folder for each test  
    createClassFolder(className) # Creates the class folder if it isn't there already
    directory = os.getcwd() + "\\" + "Test Images" + "\\" + className  # Gets the test image directory  
    if createFolderCheck(directory,folderName) == "Not in use":  # Checks the test image directory for the test folder  
        os.mkdir((directory + "\\" + folderName))  # Makes the folder if there isn't one  
        os.mkdir(directory + "\\" + folderName + "\\" + "testFiles" + "\\")

def deleteTestFolder(folderName, className):
    directory = os.getcwd() + "\\" + "Test Images" + "\\" + className #Gets the test image directory
    if createFolderCheck(directory, folderName) == "In use":  # Checks if the folder is in use  
        shutil.rmtree(directory + "\\" + folderName)  # Deletes the folder if it exists

def renameClassDirectory(oldName, nameChange):
    directory = os.getcwd() + "\\" + "Test Images\\" #Gets the test images directory
    os.rename(directory+oldName, directory+nameChange) #Renames the old directory to the new name changed one

def deleteClassDirectory(className):
    directory = os.getcwd() + "\\" + "Test Images\\" #Gets the test images directory
    shutil.rmtree(directory + className) #Removes the class directory

def findFilesInTestDirectory(directory, extension):
    filesInDirectory = os.listdir(directory)  # Gets all of the files in the directory  
    filesInDirectory = [file for file in filesInDirectory if file.endswith(extension)]
    return filesInDirectory  # Returns the list of files files  

def sortContoursLeftToRight(contours):
    boundingBoxes = [getBoundingBox(cont) for cont in contours]  # Constructs the list of bounding boxes  
    (newContours, boundingBoxes) = zip(*sorted(zip(contours, boundingBoxes), key=lambda x: x[1][0],
                                               reverse=False))  # Sorts the contours and bounding boxes  
    return newContours, boundingBoxes  # Returns the list of sorted contours and bounding boxes  

def getDocumentationImages():
    directory = os.getcwd() + "\\Documentation\\Numbers.jpg" #Gets the image
    return directory #Returns the image

def sortingFunction(contour, img, lowerBound, upperBound):
    previousYValue = 0  # Initialises the counters and lists  
    contourList = []
    lineList = []
    for cont in contour:  # Loops through every contour  
        x, y, w, h = getBoundingBox(cont)  # Gets the x,y,width and height for each contour  
        if (img.shape[0] * 0.78) < h:  # Check for getting the bigger boxes  
            previousYValue = y  # Makes the previous value to be the new y value  
            lineList.append(cont)  # Appends the contour to the list  
        if (w > lowerBound and h > lowerBound) and (
                w < upperBound and h < upperBound):  # Checks for only the digit boxes  
            if y - previousYValue > 150:  # Checks if a new line has been encroached  
                contourList.append(
                    lineList)  # Appends the list of old contours on the previous line to the contour list  
                lineList = list()  # Wipes the line list  
                lineList.append(cont)  # Appends the new contour to the new line list  
            else:
                lineList.append(cont)  # Otherwise, adds the contour to the line list  
            previousYValue = y  # Sets the previous y value to y  
    contourList.append(lineList)  # Appends the last line list to the main contour list  

    for sublist in contourList:  # Loops through the sublists in the contours list (each sublist being a line)  
        sublist.sort(key=lambda x: getBoundingBox(x)[0])  # Sorts each line by x value  

    flatList = [item for sublist in contourList for item in sublist]  # Creates the flattened list of contours  
    return flatList  # Returns the flattened list  


def makeStructuringElement(height, width):
    return [[1 for wIndex in range(width)] for hIndex in
            range(height)]  # Returns the structuring element that the user requests  


def boxExtraction(imagePath, directoryCroppedPath):
    image = cv2.imread(imagePath, 0)  # Reads the image into the variable in greyscale  

    (threshold, binaryImageTemp) = cv2.threshold(image, 128, 255,
                                                 cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholds the image to get it to black and white  
    binaryImage = 255 - binaryImageTemp  # Inverts the image to flip it  

    lengthOfKernel = len(image[0]) // 40  # Creates the kernel length  

    kernelVertical = np.asarray(makeStructuringElement(lengthOfKernel,
                                                       1))  # Creates the vertical kernel with 1 multiplied by the lengthOfKernel variable  
    kernelHorizontal = np.asarray(makeStructuringElement(1,
                                                         lengthOfKernel))  # Creates the horizontal kernel with the kernel length multiplied by 1  
    kernel = np.asarray(makeStructuringElement(3, 3))  # Creates a normal kernel with 3 x 3 ones  

    verticalTempImage = cv2.erode(binaryImage, kernelVertical,
                                  iterations=3)  # Detects the vertical lines through morphological operation  
    verticalLines = cv2.dilate(verticalTempImage, kernelVertical,
                               iterations=3)  # Dilates the erosion done in the previous step with the vertical kernel  
    horizontalTempImage = cv2.erode(binaryImage, kernelHorizontal,
                                    iterations=3)  # Detects the horizontal lines through morphological operations  
    horizontalLines = cv2.dilate(horizontalTempImage, kernelHorizontal,
                                 iterations=3)  # Dilates the previous erosion with the horizontal kernel  

    binaryImageFinal = cv2.addWeighted(verticalLines, 0.5, horizontalLines, 0.5,
                                       0.0)  # Adds the two horizontal and vertical images to get a third image, which is both combined. Uses the specific weight parameters defined earlier.  
    binaryImageFinal = cv2.erode(~binaryImageFinal, kernel, iterations=2)
    (threshold, binaryImageFinal) = cv2.threshold(binaryImageFinal, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(binaryImageFinal, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)  # Finds the contours in the image  
    contours.sort(key=lambda x: getBoundingBox(x)[1])  # Sorts the contours by y value  
    contours = sortingFunction(contours, image, 100, 400)  # Passes the sorted contours into the next sorting function  

    fileNameIndex = 0  # Defines the variables for the file name and previous y value  
    previousYValue = 0
    maxVal = int(image.shape[0] / 23)  # Gets the maximum value of the line

    for cont in contours:  # Loops through the contours  
        x, y, w, h = getBoundingBox(cont)  # Gets the coordinates and resolution of the image  
        if (image.shape[0] * 0.78) < h:  # Checks for larger rectangles  
            previousYValue = y  # Sets the previous y value to the y for the larger rectangle
        if (w > 100 and h > 100) and (
                w < 400 and h < 400):  # Checks that the box is a rectangle that fits the right dimensions
            newImage = image[y:y + h, x:x + w]  # Creates a new image with these dimensions
            if y - previousYValue > maxVal:  # Checks if a new line has been hit
                fileNameIndex += 10  # Adds ten to the file name
                fileNameIndex = roundDown(fileNameIndex, 10)  # Rounds down to the nearest 10
            cv2.imwrite(directoryCroppedPath + "%02d" % fileNameIndex + '.jpg',
                        newImage)  # Writes the new image to the file  
            fileNameIndex += 1  # Adds one to the filename index to point to the next box  
        previousYValue = y  # Sets the previous y value to the y value  


def getBoundingBox(contourArray):
    maxXValue = maxYValue = 0  # Sets the max X and Y values to zero  
    minXValue = minYValue = float("inf")  # Sets the min X and Y values to infinity  
    for contour in contourArray:  # Loops through all the contours in the array  
        xValue = contour[0][0]  # Gets the x value from the contour  
        yValue = contour[0][1]  # Gets the y value from the contour  
        if xValue < minXValue: minXValue = xValue  # Series of checks to determine what the minimum and maximum X co-ords are  
        if xValue > maxXValue: maxXValue = xValue
        if yValue < minYValue: minYValue = yValue  # Series of checks to determine what the minimum and maximum Y co-ords are  
        if yValue > maxYValue: maxYValue = yValue
    return minXValue, minYValue, (maxXValue - minXValue + 1), (
                maxYValue - minYValue + 1)  # Calculates and returns the co-ordinates of the bounding box  


def roundDown(num, divisor):
    return num - (num % divisor)  # Returns the rounded down number to the nearest multiple of the divisor  


def boxExtractionFurther(imagePath):
    image = cv2.imread(imagePath, 0)  # Reads the image into the variable in greyscale  

    (threshold, binaryImage) = cv2.threshold(image, 128, 255,
                                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholds the image to get it to black and white  
    binaryImage = 255 - binaryImage  # Inverts the image to flip it  

    lengthOfKernel = len(image[0]) // 40  # Creates the kernel length  

    kernelVertical = np.asarray(makeStructuringElement(lengthOfKernel,
                                                       1))  # Creates the vertical kernel with one column, and the desired lengthOfKernel number of rows, and converts it to a numpy array  
    kernelHorizontal = np.asarray(makeStructuringElement(1,
                                                         lengthOfKernel))  # Creates the horizontal kernel with the kernel length multiplied by 1  
    kernel = np.asarray(makeStructuringElement(3, 3))  # Creates a normal kernel with 3 x 3 ones  

    verticalTempImage = cv2.erode(binaryImage, kernelVertical,
                                  iterations=3)  # Detects the vertical lines through morphological operation  
    verticalLines = cv2.dilate(verticalTempImage, kernelVertical,
                               iterations=3)  # Dilates the erosion done in the previous step with the vertical kernel  
    horizontalTempImage = cv2.erode(binaryImage, kernelHorizontal,
                                    iterations=3)  # Detects the horizontal lines through morphological operations  
    horizontalLines = cv2.dilate(horizontalTempImage, kernelHorizontal,
                                 iterations=3)  # Dilates the previous erosion with the horizontal kernel  

    binaryImageFinal = cv2.addWeighted(verticalLines, 0.5, horizontalLines, 0.5,
                                       0.0)  # Adds the two horizontal and vertical images to get a third image, which is both combined. Uses the specific weight parameters defined earlier.  
    binaryImageFinal = cv2.erode(~binaryImageFinal, kernel, iterations=2)
    (threshold, binaryImageFinal) = cv2.threshold(binaryImageFinal, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(binaryImageFinal, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)  # Finds the contours in the image  
    (contours, boundingBoxes) = sortContoursLeftToRight(contours)  # Sorts the contours by left to right method  

    averages = []  # Defines the empty averages list  
    for cont in contours:  # Loops through all of the contours  
        x, y, w, h = getBoundingBox(cont)  # Gets the coordinates and resolution of the image  
        if (25 < w < 175) and (25 < h < 175):
            newImage = image[y:y + h, x:x + w]  # Creates a new image with the dimensions  
            average1 = np.average(newImage, axis=0)  # Gets the averages pixel density of the segment  
            average2 = np.average(average1, axis=0)
            averages.append(average2 / 255)  # Appends the average to the list
        try:
            maximumValue = max(averages)  # Works out the maximum and minimum value in the list
            minumumValue = min(averages)
        except:
            print("Couldn't recognise boxes! Please check that there are no digits that are crossed out")
    if maximumValue - minumumValue < (20 / 255):  # Checks that the digits aren't similar  
        if minumumValue > (
                110 / 255):  # Checks that the whitespace of the minumum value is higher than the amount of blackspace  
            os.remove(imagePath)  # Removes the image  
            return False  # Returns false to signal removal of image  
        else:
            return averages  # Returns the averages as number is an 8  
    else:
        return averages  # Returns the averages if the check is passed  


def studentTestFeedInLoop(className, testName):
    directory = os.getcwd() + "\\" + "Test Images" + "\\" + className + "\\" + testName + "\\" + "testFiles" + "\\"  # Defines the two directories  
    boxDirectory = os.getcwd() + "\\" + "Test Images" + "\\" + className + "\\" + testName + "\\" + "boxExtraction" + "\\"
    if createFolderCheck((os.getcwd() + "\\" + "Test Images" + "\\" + className + "\\" + testName + "\\"),
                         "boxExtraction") == "Not in use":  # Checks if there is a box extraction folder  
        os.mkdir(boxDirectory)  # Creates the directory if it doesnt exist  
    files = findFilesInTestDirectory(directory, "jpg")  # Finds all the images in the test images directory  
    if files == []: #Checks that there are test files in the directory
        return 0 #Returns the relevant error
    else: #There are files, but further checking needs to be done
        for file in files: #Loops through the filenames
            try: #Tries to split them up. If any file isn't named correctly, it will break
                nameList = file.replace(".jpg","").split(" ") #Splits the filename up into it's elements
                if len(nameList) != 3:
                    return 1
                else:
                    name = nameList[0] + nameList[1] + str(int(nameList[2])) #Joins the first, second and checks that the third is a number.
            except:
                return 1 #Returns the relevant error if anything anomalous happens
    scoreDataStructure = allScores()  # Creates the empty scoreDataStructure  
    for file in files:  # Loops through the image files in the directory  
        if createFolderCheck(boxDirectory,
                             file) == "Not in use":  # Checks if there is a folder for the file in the boxExtraction directory  
            os.mkdir(boxDirectory + file)  # Makes the directory if it doesn't exist  
        boxExtraction(directory + file, boxDirectory + file + "\\")  # Extracts the box segments in the correct file  
        furtherFiles = findFilesInTestDirectory(boxDirectory + file,
                                                "jpg")  # Finds the newly extracted box segment images  
        for furtherFile in furtherFiles:  # Loops through the files in the box extraction directory  
            numToAdd = 0  # Creates the num to add  
            averages = boxExtractionFurther(
                boxDirectory + file + "\\" + furtherFile)  # Extracts the segments from the images  
            if averages:  # Checks that the file hasn't been removed  
                tempScore = boxDigit(
                    boxDirectory + file + "\\" + furtherFile)  # Creates the boxDigit model with the file name  
                tempScore.setAverages(averages)  # Sets the averages in the model  
                if len(averages) != 7:  # Checks if the digit has been split up properly  
                    tempScore.setCheckFlag(True)  # Makes the teacher check the digit if not  
                tempScore.setStudentName(
                    (file.split(" ")[0] + " " + file.split(" ")[1]))  # Sets the student name in the model  
                if file.split(" ")[2] == "2.jpg":  # Gets the correct numbers for each test based on the test number  
                    numToAdd = 10
                elif file.split(" ")[2] == "3.jpg":
                    numToAdd = 20
                tempScore.setLineNumber(
                    (int(furtherFile[0]) + numToAdd))  # Sets the line number to the digit plus the number to add  
                tempScore.setLinePosition(int(furtherFile[1]))  # Sets the line position on that line  
                scoreDataStructure.addScore(tempScore)  # Adds the score to the score data structure  
    return scoreDataStructure


def calculateQuestionsWrong(test):
    wrongList = []  # Creates the empty data set to hold the numbers of incorrect answers  
    studentsInClass = len(test.getScores())  # Gets the number of students in the class  

    for question in test.getQuestions():  # Loops through all the questions in the test  
        questionList = list()  # Defines the empty question list  
        questionList.append(question.getQuestion())  # Adds the question, wrong answer count and category to the list  
        questionList.append(question.getWrongAnswerCount())
        questionList.append(question.getCategory())
        wrongList.append(questionList)  # Appends the list structure to the bigger list  

    wrongList.sort(key=lambda x: x[1])  # Sorts the bigger list by incorrect answer  
    for question in wrongList:  # Loops through the questions in the sorted list  
        question[1] = int(
            (question[1] / studentsInClass) * 100)  # Calculates the percentage and re-assigns it to the list  

    wrongList.sort(key=lambda x: x[1], reverse=True)  # Sorts by percentage in reverse  

    fullCategoryList = []
    categoryList = ['MENTAL STRATEGIES', 'KEY SKILLS', 'TIMESTABLES']
    for categories in categoryList:  # Loops through each category  
        tempList = list()  # Defines an empty list structure to hold data  
        tempList.append(categories)  # Adds the category to the list structure  
        tempList.append(sum(int(percentage) for question, percentage, category in wrongList if
                            category == categories))  # Loops through the list, and sums the percentages of each category  
        fullCategoryList.append(tempList)  # Appends the category sublist to the bigger category list  

    fullCategoryList.sort(key=lambda x: x[1], reverse=True)  # Sorts the bigger category list in reverse by percentage  

    return wrongList, fullCategoryList[0][
        0]  # Returns the mode incorrect question list plus the category that most students got wrong  


def findBoxesPerBreakdown(scoreStructure):
    bigBoxList = []  # Creates the list that will hold all segments per screen  
    highestVal = -1  # Creates the highest value  
    for boxSegment in range(len(
            scoreStructure.getScores()) // 8):  # 8 segments are displayed per screen, so gets the integer division of the scores by 8  
        boxList = []  # Creates the list that will hold segments for a particular screen  
        for column in range(8):  # Loops through the 8 columns  
            boxList.append(scoreStructure.getScores()[(boxSegment * 8) + column])  # Appends the score of the segment  
            highestVal = boxSegment * 8 + column  # Sets the new highest value  
        bigBoxList.append(boxList)  # Appends the big list with the small one once completed  
    boxList = []  # Clears the box list for the remainder segments  
    for boxSegment in range(
            int(len(scoreStructure.getScores()) % 8)):  # Gets the remainder boxes to display on screen  
        boxList.append(scoreStructure.getScores()[
                           boxSegment + highestVal + 1])  # Appends the score + the highest value to get the correct new segment  
    if boxList: bigBoxList.append(boxList)  # Doesnt append the boxList if there is nothing in it  
    return bigBoxList  # Returns the list of segments per screen  


def scoreStudent(answersList, questionNumbersList, studentNamesList, testName):
    testQ = testName  # Creates the test variable  
    for student in range(len(studentNamesList)):  # Loops through each student in the studentNames list  
        studentScore = 0  # Sets the current student score to 0  
        for questionsAnswered in range(len(
                questionNumbersList[student])):  # Loops through the questions answered in the question numbers list  
            for testQuestion in range(
                    len(testQ.getQuestions())):  # Loops through all of the test questions in the test  
                if testQuestion == questionNumbersList[student][
                    questionsAnswered]:  # If the test question numbers are the same  
                    if testQ.getQuestions()[testQuestion].getAnswer() == answersList[student][
                        questionsAnswered]:  # Compares the answer  
                        studentScore += 1  # Appends one to the student score if it is right  
                    else:
                        testQ.getQuestions()[testQuestion].addWrongAnswerCount()
        testQ.addTestScore(studentNamesList[student],
                           studentScore)  # Once the student has been looped through, adds the test score to the test  


def createAnswer(answerList):
    answer = ""  # Creates the answer string  
    for answerItem in range(len(answerList)):  # Loops through every item in the digit list  
        if answerList[answerItem] == "-" and answerItem != 0:
            answer = "{}{}".format(answer,
                                   0)  # Formats the old answer and a zero together because of rogue minus number  
        elif answerList[answerItem] == "?":  # Checks if there is an anomaly digit  
            continue  # Performs no operation  
        else:
            answer = "{}{}".format(answer,
                                   answerList[answerItem])  # Formats the old answer and the new answer together  
    try:
        answer = int(answer)  # Returns the integer conversion of the string answer  
    except:
        print("Couldn't recognise answer")  # Prints an error if it couldn't recognise certain answers  
    return answer


def mapNumberToXCoord(number, xStart, xStartPixel, xEnd,
                      xEndPixel):  # Function for mapping a data point to a screen x coordinate  
    proportionBetween = (number - xStart) / (
                xEnd - xStart)  # Gets the proportion of the points where it starts and ends  
    distanceFromStart = proportionBetween * (xEndPixel - xStartPixel)  # Gets the distance from the start of screen  
    return math.ceil(distanceFromStart + xStartPixel)  # Returns the x coord  


def createCheckingScoreStructure(scoreDataStructure):
    newCheckingStructure = allScores()  # Creates a new empty score structure  
    for score in scoreDataStructure.getScores():  # Loops through the scores in the current score structure  
        if score.getCheckFlag():  # Checks if the score needs to be checked  
            newCheckingStructure.addScore(score)  # Adds the score to the data structure if it does need to be checked  
    return newCheckingStructure  # Returns the checking structure  


def neuralNetworkRecognition(scoreDataStructure, networkDataStructure):
    for score in scoreDataStructure.getScores():  # Loops through the scores in the data structure  
        if score.getCheckFlag() is None:  # Only does it if a checkFlag hasn't already been assigned  
            outputData = networkDataStructure.run(
                score.getAverages())  # Runs the neural networks on the average pixel data  
            index = outputData.index(max(outputData))  # Gets the index of the maximum data value  
            if index == 10:  # Sets the number recognised to a minus sign if that is what is recognised  
                score.setNumberRecognised("-")
            else:
                score.setNumberRecognised(index)  # Sets the number recognised to the index of the list  
            confidenceLevel = outputData[index]  # Sets the confidence level to the maximum value  
            secondMaximumIndex = outputData.index(max([xIndex for xIndex in outputData if xIndex != outputData[index]]))  # Gets the index of the second maximum value in the data  
            secondMax = outputData[secondMaximumIndex] #Gets the second maximum value
            if confidenceLevel > 0.85 and secondMax < 0.1:  # If the confidence level is over 85% and the secondMaximum is low enough
                score.setCheckFlag(False)  # Doesn't need to be checked  
            else:
                score.setCheckFlag(True)
    return scoreDataStructure  # Returns the score structure  

def retrainNeuralNetwork(neuralNetwork, scoreDataStructure):
    fileHandle = open("trainingData.json", "r",
                      encoding="utf-8")  # Opens training data file with utf-8 encoding  
    lines = json.load(fileHandle)  # Reads all lines in with json load function to get to dictionary  
    fileHandle.close()
    trainingDataSet = [[line['pixelValues'], line['numberValues']] for line in
                       lines]  # Takes the data into a training data set  
    for data in scoreDataStructure:  # Loops through the scores in the score data structure  
        inputData = data.getAverages()  # Sets the input data as the pixel data
        numberCorrected = data.getNumberCorrected()  # Sets the number corrected from the score  
        if numberCorrected == "-":  # Does the relevant checks for the minus signs  
            outputList = [1 if xIndex == 10 else 0 for xIndex in range(11)]
        elif numberCorrected == "?":  # Does the relevant checks for anomaly digits  
            continue
        else:  # Normal digit, do normal operation  
            outputList = [1 if xIndex == numberCorrected else 0 for xIndex in range(11)]  # Gets the target output data from the user input    
        if len(inputData) != 7 or len(outputList) != 11:
            continue
        random.shuffle(trainingDataSet) # Shuffles the data set to maximise training potential
        for epoch in range(150): #Loops 150 times
            if epoch // 15 == 0: #Only trains 10% of the time
                neuralNetwork.train(inputData, outputList)  # Trains the new data once
            neuralNetwork.train(trainingDataSet[epoch][0], trainingDataSet[epoch][1])
        trainingDataSet.append([inputData, outputList])  # Appends the input and target data to the training data set
    handleNetworkDataOutput(neuralNetwork)  # Handles the network output  
    handleTrainingDataOutput(trainingDataSet)  # Handles the training data output  
    return neuralNetwork  # returns the re-trained neural network


def mergeSort(listFedIn):
    if len(listFedIn) > 1:  # Checks that the list length is greater than one  
        midpoint = len(listFedIn) // 2  # Finds the midpoint of the data  
        leftList = listFedIn[:midpoint]  # Gets the left half of the list (up to the midpoint)  
        rightList = listFedIn[midpoint:]  # Gets the right half of the list (from the midpoint)  
        mergeSort(leftList)  # Recursively calls itself with the left half  
        mergeSort(rightList)  # Recursively calls itself with the right half  

        i = j = k = 0  # Sets the pointers of right, left and new sorted list to zero  

        while i < len(leftList) and j < len(rightList):  # Checks that there are more elements  
            if leftList[i] < rightList[
                j]:  # If the element in the right list is greater than the element in the left list  
                listFedIn[k] = leftList[i]  # New sorted list element is the smallest element  
                i += 1  # Increases the pointer to account for the next value in the left list  
            else:  # The element in the left list is greater or equal to the element in the right list  
                listFedIn[k] = rightList[j]  # New sorted list element is the smallest element  
                j += 1  # Increases the pointer to account for the next value in the right list  
            k += 1  # An element has been added, so increase the sorted list pointer  

        while i < len(leftList):  # While there are more elements in the left list  
            listFedIn[k] = leftList[i]  # Puts the remaining elements in the left list into the new sorted list  
            i += 1  # Increases the left pointer  
            k += 1  # Increases the sorted pointer  

        while j < len(rightList):  # While there are more elements in the right list  
            listFedIn[k] = rightList[j]  # Puts the remaining elements in the right list in the sorted list  
            j += 1  # Increases the right pointer  
            k += 1  # Increases the sorted pointer  

    return listFedIn  # Returns the newly sorted list once finished 
