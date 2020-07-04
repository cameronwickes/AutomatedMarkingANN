from tkinter import * #Imports the required libraries
from PIL import Image, ImageTk
import tkinter.messagebox as tm
from random import randint
from Processing import *
import math


class GUI:
    def __init__(self, teacherDataStructure, questionDataStructure, networkDataStructure,
                 maximumTestSize):  # Constructor method for the GUI class  
        self.MAXIMUMTESTSIZE = maximumTestSize  # Defines the maximum question size per test  
        self.CATEGORYBOUNDARY = math.trunc(len(questionDataStructure.questions) / 3)
        self.root = Tk()  # Creates the root window  
        self.width = self.root.winfo_screenwidth()  # Grabs the width and height of the screen  
        self.height = self.root.winfo_screenheight()
        self.root.geometry(
            f'{self.width}x{self.height}')  # Uses the grabbed dimensions to resize the root window to be on the screen  
        self.root.title("ANN for Automated Marking")  # Titles the window  
        self.root.state('zoomed')  # Sets the window state to maximised by default  
        self.frame = Frame(self.root)  # Creates a frame inside of the root window  
        self.createChoiceScreen()  # Creates the login screen  
        self.classLoggedIn = -1  # Sets the class logged in variable to -1 to tell the computer that no class is logged in yet  
        self.teacherDataStructure = teacherDataStructure  # Passes the GUI class the teacher and question data structures that have been parsed in  
        self.questionDataStructure = questionDataStructure
        self.networkDataStructure = networkDataStructure

    def showError(self, error):
        tm.showerror("Error", error)  # Show the error  

    def createChoiceScreen(self):
        self.destroyScreen()  # Destroys the previous screen  

        mainMessageLabel = Label(self.frame,
                                 text="Please select an option from the choices below!")  # Creates all the options  
        createClassButton = Button(self.frame, text="Create a new class", command=self.createNewClassScreen)
        selectClassButton = Button(self.frame, text="Login with an existing class",
                                   command=lambda: self.createExistingClassScreen("login"))
        editClassButton = Button(self.frame, text="Edit an existing class",
                                 command=lambda: self.createExistingClassScreen("edit"))

        mainMessageLabel.grid(row=0, columnspan=3, pady=10)  # Packs the buttons and text to the screen  
        createClassButton.grid(row=1, column=0, pady=10, padx=5)
        selectClassButton.grid(row=1, column=1, pady=10, padx=5)
        editClassButton.grid(row=1, column=2, pady=10, padx=5)
        self.frame.pack() #Packs the frame

    def createExistingClassScreen(self, option):
        self.destroyScreen()  # Destroys the previous screen  
        if option == "login":  # Checks if the user is trying to login or edit a class  
            nextButton = Button(self.frame, text="Next",
                                command=lambda: self.classSelectionPressed(
                                    listOfClasses.curselection()))  # Packs the login option to the next button  
        else:
            nextButton = Button(self.frame, text="Next",
                                command=lambda: self.editClassSelection(
                                    listOfClasses.curselection()))  # Packs the edit option to the next button  
        mainMessageLabel = Label(self.frame,
                                 text="Select a class from the list below")
        scrollbar = Scrollbar(self.frame, orient=VERTICAL)  # Creates the scrollbar at the side of the listbox  
        listOfClasses = Listbox(self.frame, selectmode=SINGLE, width=50,
                                yscrollcommand=scrollbar.set)  # Creates the listbox, sets the select mode so teacher cant select more than one test and makes sure the scrollbar is bound to the listbox  
        scrollbar.config(command=listOfClasses.yview)  # Config the scrollbar to change the listbox view when pressed  

        backButton = Button(self.frame, text="Back", command=self.createChoiceScreen)
        mainMessageLabel.grid(row=0, columnspan=2, pady=35)  # Formats the grid and layout of widgets  
        listOfClasses.grid(row=2, columnspan=2)
        scrollbar.grid(row=2, column=3, sticky=NS)
        backButton.grid(row=3, column=0, pady=35)
        nextButton.grid(row=3, column=1, pady=35)

        listBoxCount = 0  # Item listbox count  
        for singleClass in self.teacherDataStructure.getClasses():  # Loops through all classes  
            listOfClasses.insert(listBoxCount, singleClass.getName())  # Inserts the class with the index and name  
            listBoxCount += 1  # Adds one to point to next line of listbox  

        self.frame.pack()

    def editClassSelection(self, cs):
        self.destroyScreen()
        if cs != ():  # If the cursor selection is not nothing then:  
            if type(cs) == tuple:
                cs = int(cs[0])  # Create the test selection index  
            if type(cs) == int:
                self.classLoggedIn = cs  # Sets the class logged in for editing purposes  
                mainMessageLabel = Label(self.frame,
                                         text="Edit the details of your class here: ")  # Creates the main screen options  
                nameLabel = Label(self.frame, text="Name: ")
                nameEntry = Entry(self.frame)
                nameEntry.insert(END, self.teacherDataStructure.getClass(
                    self.classLoggedIn).getName())  # Passes the test name for editing  
                deleteButton = Button(self.frame, text="Delete Class (Irreversible)",
                                      command=lambda: self.removingClass(self.classLoggedIn), fg='white', bg='red')
                deleteTestButton = Button(self.frame, text="Delete specific test",
                                          command=lambda: self.createTestListBox("Delete Test"))
                backButton = Button(self.frame, text="Done",
                                    command=lambda: self.existingClassBackPressed(nameEntry.get()))
                mainMessageLabel.grid(row=0, columnspan=2,
                                      pady=10)  # Packs all the options to the screen in required format/order  
                nameLabel.grid(row=1, column=0, pady=10)
                nameEntry.grid(row=1, column=1, pady=10)
                deleteTestButton.grid(row=2, columnspan=2, pady=10)
                backButton.grid(row=3, columnspan=2, pady=10)
                deleteButton.grid(columnspan=2, pady=self.height // 3)
                self.frame.pack() #Packs the frame
        else:
            self.createExistingClassScreen("edit")  # Cursor Selection invalid, gets the user to try again  
            self.showError("Please select a valid class to edit")
            
    def existingClassBackPressed(self, nameChange):
        if nameChange in ["", " ", "\n"] or nameChange[0] == " " or nameChange.replace(' ','').isalnum() == False:  # If the user entered a blank string or space or newline button  
            self.showError("Please enter a valid name for your class! - Make sure you have entered a name with no invalid characters e.g. a space at the beginning")  # Show the error  
        else:
            checkFlag = False  # Sets the checkflag to false  
            for singleClass in self.teacherDataStructure.getClasses():  # Loops through all the classes in the structure  
                if singleClass.getName().lower() == nameChange.lower() and singleClass != self.teacherDataStructure.getClasses()[self.classLoggedIn]:  # Gets the name of the class and compares it to ones entered  
                    checkFlag = True  # Sets the checkflag if there is already a class at that name  
            if not checkFlag:  # If there isn't already a class by that name
                currentName = self.teacherDataStructure.getClasses()[self.classLoggedIn].getName()
                renameClassDirectory(currentName,nameChange)
                self.teacherDataStructure.getClass(self.classLoggedIn).setName(nameChange)  # Sets the new name to the one in the entry box  
                handleDataOutput(self.teacherDataStructure)  # Outputs the change to files
                self.createChoiceScreen()  # Creates the login screen again  
            else:
                self.showError("There is already a class with that name!")  # Shows the error if required  

    def removingClass(self, cs):
        className = self.teacherDataStructure.getClasses()[cs].getName()
        deleteClassDirectory(className)
        self.teacherDataStructure.removeClass(cs)  # Removes the class from the data structure  
        handleDataOutput(self.teacherDataStructure)  # Outputs the change to the files  
        self.createExistingClassScreen("edit")  # Creates the edit selection screen  

    def deleteTest(self, cs):
        if cs != ():  # If the cursor selection is not nothing then:  
            if type(cs) == tuple:
                cs = int(cs[0])  # Create the test selection index
                testName = self.teacherDataStructure.getClass(self.classLoggedIn).getActiveTest(cs).getTestName()
                className = self.teacherDataStructure.getClass(self.classLoggedIn).getName()
                self.teacherDataStructure.getClass(self.classLoggedIn).removeTest(cs)  # Removes the test from the structure  
                handleDataOutput(self.teacherDataStructure)  # Handles the data output  
                deleteTestFolder(testName, className)
                self.editClassSelection(self.classLoggedIn)  # Sends the user back to the previous screen  
        else:
            self.showError("Please select a valid test to delete") #Shows the error


    def createNewClassScreen(self):  # Procedure to create the teacher class login screen  
        self.destroyScreen()  # Destroy the previous frame and create a new one  

        classLabel = Label(self.frame, text="Class Name: ")  # Creates the required labels  
        loginButton = Button(self.frame, text="Create",
                             command=lambda: self.createClassButtonPressed(classEntry.get()))  # Login button  
        backButton = Button(self.frame, text="Back", command=self.createChoiceScreen)
        classEntry = Entry(self.frame)  # Creates the class entry box  

        classLabel.grid(row=0, sticky=E, pady=10)  # Forms the layout of all screen widgets  
        classEntry.grid(row=0, column=1, pady=10)
        backButton.grid(row=1, column=0, pady=10)
        loginButton.grid(row=1, column=1, pady=10)

        self.frame.pack()  # Packs the frame and widgets onto the screen  

    def createClassButtonPressed(self, classEntered):
        if classEntered in ["", " ", "\n","'"] or classEntered[
            0] == " " or classEntered.replace(' ','').isalnum() == False:  # If the user entered a blank string or space or newline button  
            self.showError(
                "Please enter a valid name for your class! - Make sure you have entered a name with no invalid characters e.g. a space at the beginning")  # Show the error  
        else:
            checkFlag = False  # Sets the checkflag to false  
            for singleClass in self.teacherDataStructure.getClasses():  # Loops through all the classes in the structure  
                if singleClass.getName().lower() == classEntered.lower():  # Gets the name of the class and compares it to ones entered  
                    checkFlag = True  # Sets the checkflag if there is already a class at that name  
            if not checkFlag:  # If there isn't already a class by that name  
                self.teacherDataStructure = createNewClass(self.teacherDataStructure,
                                                           classEntered)  # Creates the new class  
                createClassFolder(classEntered) # Creates the class folder
                self.classLoggedIn = self.teacherDataStructure.getLength() - 1  # Sets the class logged in to the new entry  
                self.createTeacherScreen()  # Creates the main menu interface  
            else:
                self.showError("There is already a class with that name!")  # Shows the error if required  

    def classSelectionPressed(self, cs):  # Function for logging in the teacher  
        if cs != ():  # If the cursor selection is not nothing then:  
            if type(cs) == tuple:
                cs = int(cs[0])  # Create the test selection index  
                self.classLoggedIn = cs  # Sets the teacherLoggedIn variable to the index of the teacher with that username and password for future reference  
                self.createTeacherScreen()  # Creates the teacher interface screen  
        else:
            self.showError("Please select a valid class to login with")
            self.createExistingClassScreen("login")

    def createTeacherScreen(self):  # Procedure for creating the main teacher interface  
        self.destroyScreen()  # Destroys the previous frame and creates a new one  

        welcomeLabel = Label(self.frame, text="Class: " + self.teacherDataStructure.getClass(
            self.classLoggedIn).getName())  # Takes the teacher name and splits it, taking and displaying the first name  
        mainMessageLabel = Label(self.frame, text="What would you like to do?")
        createTestButton = Button(self.frame, text="Create a Test",
                                  command=self.createTestMakingScreen)  # Button for creating a new test  
        displayQuestionsButton = Button(self.frame, text="Display Questions", command=lambda: self.createTestListBox(
            "DisplayQuestions"))  # Button for displaying the questions of a test on the board  
        uploadTestButton = Button(self.frame, text="Upload Test Images", command=lambda: self.createTestListBox(
            "UploadImages"))  # Button for uploading test results  
        viewResultButton = Button(self.frame, text="View Results", command=lambda: self.createTestListBox(
            "ViewResults"))  # Button for viewing test results  
        logoutButton = Button(self.frame, text="Logout",
                              command=self.createChoiceScreen)  # Button for logging teacher out  

        welcomeLabel.grid(row=0, columnspan=6, pady=25)  # Forms the layout grid for all widgets in the screen  
        mainMessageLabel.grid(row=1, columnspan=6, pady=25)
        createTestButton.grid(column=1, row=2, pady=25, padx=25)
        displayQuestionsButton.grid(column=2, row=2, pady=25, padx=25)
        uploadTestButton.grid(column=3, row=2, pady=25, padx=25)
        viewResultButton.grid(column=4, row=2, pady=25, padx=25)
        logoutButton.grid(column=5, row=2, pady=25, padx=25)

        self.frame.pack()  # Packs the frame and associated widgets onto the screen  

    def createTestListBox(self, index):  # Procedure for displaying tests in a listbox  
        self.destroyScreen()  # Destroys the previous frame and creates a new one  

        if index == "UploadImages":  # If the upload images tag is passed  
            mainMessageLabel = Label(self.frame,
                                     text="Select a test to upload images from")  # Create the main message and next,back buttons  
            nextButton = Button(self.frame, text="Next",
                                command=lambda: self.uploadTestData(listOfTests.curselection()))
            backButton = Button(self.frame, text="Back", command=self.createTeacherScreen)
        elif index == "ViewResults":
            mainMessageLabel = Label(self.frame,
                                     text="Select a test to view the results")  # Create the main message and next,back buttons  
            nextButton = Button(self.frame, text="Next",
                                command=lambda: self.createBoxandWhiskerDiagram(listOfTests.curselection()))
            backButton = Button(self.frame, text="Back", command=self.createTeacherScreen)
        elif index == "DisplayQuestions":
            mainMessageLabel = Label(self.frame,
                                     text="Select a test to display the questions")  # Create the main message and next,back buttons  
            nextButton = Button(self.frame, text="Next", command=lambda: self.viewQuestions(listOfTests.curselection()))
            backButton = Button(self.frame, text="Back", command=self.createTeacherScreen)
        elif index == "Delete Test":
            mainMessageLabel = Label(self.frame,
                                     text="Select a test to delete")  # Create the main message and next,back buttons  
            nextButton = Button(self.frame, text="Delete", command=lambda: self.deleteTest(listOfTests.curselection()))
            backButton = Button(self.frame, text="Back", command=lambda: self.editClassSelection(self.classLoggedIn))

        scrollbar = Scrollbar(self.frame, orient=VERTICAL)  # Creates the scrollbar at the side of the listbox  
        listOfTests = Listbox(self.frame, selectmode=SINGLE, width=50,
                              yscrollcommand=scrollbar.set)  # Creates the listbox, sets the select mode so teacher cant select more than one test and makes sure the scrollbar is bound to the listbox  
        scrollbar.config(command=listOfTests.yview)  # Config the scrollbar to change the listbox view when pressed  

        mainMessageLabel.grid(row=0, columnspan=2, pady=35)  # Formats the grid and layout of widgets  
        listOfTests.grid(row=2, columnspan=2)
        scrollbar.grid(row=2, column=3, sticky=NS)
        backButton.grid(row=3, column=0, pady=35)
        nextButton.grid(row=3, column=1, pady=35)

        listBoxCount = 0  # Item listbox count  
        if index == "UploadImages" or index == "DisplayQuestions" or index == "Delete Test":  # Upload images, Display questions and Delete Test are displaying the same set of tests  
            for test in self.teacherDataStructure.getClass(
                    self.classLoggedIn).getActiveTests():  # Loops through all tests (active)  
                listOfTests.insert(listBoxCount, test.testName)  # Inserts the test with the index and test name  
                listBoxCount += 1  # Adds one to point to next line of listbox  
        elif index == "ViewResults":
            for test in self.teacherDataStructure.getClass(
                    self.classLoggedIn).getRetiredTests():  # Loops through all tests (retired)  
                listOfTests.insert(listBoxCount, test.testName)  # Inserts the test with the index and test name  
                listBoxCount += 1  # Adds one to point to next line of listbox  

        self.frame.pack()  # Packs the frame and widgets to the screen  

    def uploadTestData(self, cs):  # Procedure for uploading the test data (File searching and ANN network algorithm)  
        if cs != ():  # If the cursor selection is not nothing then:  
            cs = int(cs[0])  # Create the test selection index  
            test = self.teacherDataStructure.getClass(self.classLoggedIn).getActiveTest(
                cs)  # Gets the test for easy access  
            self.scoreDataStructure = studentTestFeedInLoop(
                (self.teacherDataStructure.getClass(self.classLoggedIn).getName()),
                test.getTestName())  # Feeds in the student tests
            if self.scoreDataStructure == 0:
                self.showError("No jpg files in test upload directory!")
                self.createTestListBox("UploadImages")
            elif self.scoreDataStructure == 1:
                self.showError("Check the files are named correctly and try again.")
                self.createTestListBox("UploadImages")
            self.scoreDataStructure = neuralNetworkRecognition(self.scoreDataStructure,
                                                               self.networkDataStructure)  # Gets the neural network to recognise the digits  
            checkingScoreStructure = createCheckingScoreStructure(
                self.scoreDataStructure)  # Creates the data structure if the neural network is unsure  
            if checkingScoreStructure.getScores():
                listCreation = findBoxesPerBreakdown(
                    checkingScoreStructure)  # Finds the boxes per screen and the remainder boxes  
                self.displaySegments(listCreation, 0, test)  # Displays the segments with the list of segments  
            else:
                self.displaySegments(checkingScoreStructure.getScores(), 0, test)  # Displays the segments  
            self.teacherDataStructure.getClass(self.classLoggedIn).retireTest(test.getTestName())  # Retires the test  
            handleDataOutput(self.teacherDataStructure)  # Writes the score data to the file  
        else:
            self.showError("Please select a valid test") #Shows the error
            self.createTestListBox("UploadImages")  # Cursor selection invalid, creates previous screen  

    def displaySegments(self, boxesPerSegment, screenNumber, testName):
        if len(boxesPerSegment) == screenNumber:  # Checks if there are no more screens to display  
            flatList = [data1 for data2 in boxesPerSegment for data1 in data2]  # Gets the flatList of boxSegments  
            self.networkDataStructure = retrainNeuralNetwork(self.networkDataStructure,
                                                             flatList)  # Retrains the neural network based on the corrected digits  
            self.scoreDataStructure.findAndChangeScores(flatList)  # Feeds in and changes the scores  
            self.scoreModelStudentMark(testName)  # Marks the student based on test scores  
            self.createTeacherScreen()  # Returns to teacher screen  
        else:
            self.destroyScreen()  # Destroys the previous screen  
            messageLabel = Label(self.frame,
                                 text="Make sure each digit has been recognised correctly and correct it if it isn't...\n Enter a '-' for a minus number, and a '?' if you don't recognise the digit or it is blank.")
            messageLabel.grid(row=0, columnspan=8, pady=35)  # Creates and formats the message text  
            for column in range(len(boxesPerSegment[screenNumber])):  # Loops through the segments in screen list  
                image = Image.open(boxesPerSegment[screenNumber][
                                       column].getFilename())  # Opens and parses the image from the boxList  
                img = image.resize((int(self.width / 9), int(self.width / 9)),
                                   Image.ANTIALIAS)  # Resizes the image to fit on the screen  
                photo = ImageTk.PhotoImage(img)  # Makes it into a tkinter photo  
                label = Label(self.frame, image=photo)  # Adds and formats the photo to a label  
                label.image = photo
                label.grid(row=1, column=column, pady=5)
                entryLabel = Entry(self.frame)  # Creates the entry box for the user to add the corrected digit  
                entryLabel.config(width=5)
                entryLabel.grid(row=2, column=column, pady=15)
            nextButton = Button(self.frame, text="Next",
                                command=lambda: self.getValueAllEntryWidgets(self.frame, boxesPerSegment, screenNumber,
                                                                             testName))
            nextButton.grid(row=3, columnspan=8, pady=35)  # Creates and formats the next button  
            self.frame.pack()  # Formats the screen  

    def getValueAllEntryWidgets(self, frame, boxesPerSegment, screenNumber, testName):
        listContents = []  # Defines the list for holding the values of entry widgets  
        childWidgets = frame.winfo_children()  # Gets the child widgets in the current frame  
        for child in childWidgets:  # Loops through the aquired child widgets  
            if child.winfo_class() == 'Entry':  # If the child widget is an entry box  
                listContents.append(child.get())  # Adds the entry contents to the list  
        digitVerification = True  # Boolean value for purpose of digit verification  
        for index in range(len(listContents)):  # Loops through the contents of the entry widgets on the screen  
            try:
                digitIn = int(listContents[index])
                if listContents[index] != "" and digitIn in [1, 2, 3, 4, 5, 6, 7, 8, 9,
                                                             0]:  # Checks that the correct format is entered (one digit and not blank)  
                    boxesPerSegment[screenNumber][index].setNumberCorrected(
                        digitIn)  # Sets the number corrected to the number entered  
                else:
                    digitVerification = False  # One or more of the entry widgets is not in the correct format  
            except:
                if listContents[index] == "-" or listContents[index] == "?":
                    boxesPerSegment[screenNumber][index].setNumberCorrected(
                        listContents[index])  # Sets the number corrected to the number entered  
                else:
                    digitVerification = False
        if digitVerification:  # Only displays the next screen if all of the data entered is in the correct form  
            self.displaySegments(boxesPerSegment, screenNumber + 1, testName)
        else:
            self.showError("Digits entered must be single integers (0-9)")

    def createBoxandWhiskerDiagram(self, cs):  # Procedure for creating a box and whisker diagram  
        if cs != ():  # If the cursor selection is not nothing then:  
            if type(cs) == tuple:
                cs = int(cs[0])  # Create the test selection index  
            test = self.teacherDataStructure.getClass(self.classLoggedIn).retiredTests[cs]  # Takes the test selection  

            self.destroyScreen()  # Destroys the previous frame and creates a new one  

            studentScores = []  # Creates an empty data set which will hold all the student scores  
            for student in range(len(test.testScores)):  # Loops through the length of the testScores  
                studentScores.append(test.testScores[student].studentScore)  # Adds each student score to the data set  

            studentScores = mergeSort(
                studentScores)  # Sorts the student score dataset for the box and whisker diagram to be created  
            uniqueScores = list(set(studentScores))
            if len(studentScores) == 0:  # Checks to make sure that there are scores  
                self.createTestListBox(
                    "ViewResults")  # Creates the previous screen if there are no scores to operate on  
                self.showError("No results to display information for.")
            elif len(uniqueScores) > 2 and len(
                    studentScores) > 2:  # Else, if there are the right amount of scores (no few)  
                canvas = Canvas(self.frame, width=self.width,
                                height=200)  # Creates a canvas, the size of the screen and with a height of 200  
                canvas.grid(row=0,
                            columnspan=8)  # Creates the canvas grid (columnspan 8 to nicely format the buttons)  
                # Calculates the quartiles by getting the indexes and putting them in a data structure  
                quartileIndexes = [math.ceil(len(studentScores) / 4), math.ceil(2 * len(studentScores) / 4),
                                   math.ceil(3 * len(studentScores) / 4)]
                quartiles = [studentScores[index - 1] for index in quartileIndexes]

                # Finds the iqr by taking the third quartile from the first quartile  
                interQuartileRange = quartiles[2] - quartiles[0]
                lowerAnomalyBoundary = quartiles[
                                           0] - 1.5 * interQuartileRange  # Calculates the two anomaly bounds by doing 1.5*iqr  
                higherAnomalyBoundary = quartiles[2] + 1.5 * interQuartileRange

                # Calculates outliers and other studentScores  
                anomalyDataPoints = [score for score in studentScores if
                                     score < lowerAnomalyBoundary or score > higherAnomalyBoundary]  # Adds it to the anomaly data set if any scores are lower than the low anomaly bound and vice versa for higher  
                validDataPoints = [score for score in studentScores if
                                   not score in anomalyDataPoints]  # Loops through student scores and adds it to valid if its not in the anomaly data set  

                firstPoint = studentScores[0]  # Takes the first point from the student data set  
                lastPoint = studentScores[-1]  # Takes the last point from the student data set  
                firstPointPixel = 100  # Creates the first point pixel  
                lastPointPixel = self.width - 100  # Creates the last point pixel (to take up full width)  

                # Maps the box start and end to x coordinates with the first and third quartile  
                boxStart = mapNumberToXCoord(quartiles[0], firstPoint, firstPointPixel, lastPoint, lastPointPixel)
                boxEnd = mapNumberToXCoord(quartiles[2], firstPoint, firstPointPixel, lastPoint, lastPointPixel)

                canvas.create_rectangle(boxStart, 100, boxEnd,
                                        200)  # Creates the main box rectangle with the correct pixel width and height  

                # Maps the lowest and highest point (if not anomaly)  
                lowestPointLine = mapNumberToXCoord(validDataPoints[0], firstPoint, firstPointPixel, lastPoint,
                                                    lastPointPixel)
                highestPointLine = mapNumberToXCoord(validDataPoints[-1], firstPoint, firstPointPixel, lastPoint,
                                                     lastPointPixel)
                canvas.create_rectangle(lowestPointLine, 100, lowestPointLine, 200,
                                        outline='skyblue')  # Creates the lowest extreme line  
                canvas.create_rectangle(highestPointLine, 100, highestPointLine, 200,
                                        outline='skyblue')  # Creates the highest extreme line  

                # Maps the horizontal lines  
                canvas.create_rectangle(lowestPointLine, 150, boxStart,
                                        150)  # Creates the solid horizontal line going from the lowest point to the box  
                canvas.create_rectangle(boxEnd, 150, highestPointLine,
                                        150)  # Creates the solid horizontal line going from the box to the highest point  

                # Maps the median line  
                midlinexCoordinate = mapNumberToXCoord(quartiles[1], firstPoint, firstPointPixel, lastPoint,
                                                       lastPointPixel)  # Gets the median x coordinate  
                canvas.create_rectangle(midlinexCoordinate, 100, midlinexCoordinate,
                                        200)  # Creates the median line on the x coordinate  

                # Maps anomaly points  
                for anomaly in anomalyDataPoints:  # Loops through anomaly points  
                    xCoordinate = mapNumberToXCoord(anomaly, firstPoint, firstPointPixel, lastPoint,
                                                    lastPointPixel)  # Maps the x coord  
                    canvas.create_line(xCoordinate - 5, 145, xCoordinate + 5, 155,
                                       fill="red")  # Creates the lines to make a cross  
                    canvas.create_line(xCoordinate - 5, 155, xCoordinate + 5, 145, fill="red")
                    canvas.create_text(xCoordinate, 130,
                                       text=str(anomaly))  # Creates the text with the score of the anomaly point  

                keyPoints = [validDataPoints[0]] + quartiles + [validDataPoints[
                                                                    -1]]  # Takes the key data points (first data non anomaly, quartiles and last data non anomaly)  

                for point in keyPoints:  # For each key point  
                    xCoordinate = mapNumberToXCoord(point, firstPoint, firstPointPixel, lastPoint,
                                                    lastPointPixel)  # Gets the x coordinate of where the text should go  
                    canvas.create_text(xCoordinate, 60,
                                       text=str(point))  # Creates the text with the score of the point  

                meanData = round((sum(studentScores) / (len(studentScores))),
                                 2)  # Gathers the mean of the student scores and rounds it to 2 decimal place  
                medianData = quartiles[1]  # Gets the median from the quartiles data set  
                modeData = max(studentScores, key=studentScores.count)  # Gathers the mode through a max function  
                rangeData = studentScores[-1] - studentScores[
                    0]  # Gathers the range by subtracting the first data point from the last data point (including anomalies)  

                backButton = Button(self.frame, text="Back", command=lambda: self.createTestListBox(
                    "ViewResults"))  # Creates the next and back buttons  
                nextButton = Button(self.frame, text="Next", command=lambda: self.createBarChartScreen(cs))
                meanLabel = Label(self.frame, text="Mean: " + str(meanData))  # Creates the mean data label  
                medianLabel = Label(self.frame, text="Median: " + str(medianData))  # Creates the median data label  
                modeLabel = Label(self.frame, text="Mode: " + str(modeData))  # Creates the mode data label  
                rangeLabel = Label(self.frame, text="Range: " + str(rangeData))  # Createst the range data label  

                meanLabel.grid(row=3, columnspan=8, pady=10)  # Create and format the grid of buttons and labels  
                medianLabel.grid(row=4, columnspan=8, pady=10)
                modeLabel.grid(row=5, columnspan=8, pady=10)
                rangeLabel.grid(row=6, columnspan=8, pady=10)
                backButton.grid(row=7, column=3, pady=35)
                nextButton.grid(row=7, column=4, pady=35)

                self.frame.pack()  # Packs the frame and widgets onto the screen  
            else:
                mainMessageLabel = Label(self.frame,
                                         text="There are too few unique results to display a box and whisker diagram correctly.")
                backButton = Button(self.frame, text="Back", command=lambda: self.createTestListBox(
                    "ViewResults"))  # Creates the next and back buttons  
                nextButton = Button(self.frame, text="Next", command=lambda: self.createBarChartScreen(cs))

                mainMessageLabel.grid(row=1, columnspan=8)  # Packs the required attributes to the screen  
                backButton.grid(row=7, column=3, pady=35)
                nextButton.grid(row=7, column=4, pady=35)

                self.frame.pack()
        else:
            self.createTestListBox("ViewResults")  # Creates the previous screen if invalid  
            self.showError("Please select a valid test to view results") # Shows the error

    def createBarChartScreen(self, cs):
        newColours = ['LightSteelBlue1', 'cornflower blue', 'SteelBlue3', 'DeepSkyBlue3', 'DeepSkyBlue2', 'SteelBlue1',
                      'LightSteelBlue2', 'alice blue', 'LightBlue3', 'LightSkyBlue3', 'LightBlue2', 'SkyBlue2',
                      'dodger blue', 'midnight blue', 'RoyalBlue1', 'LightSkyBlue1', 'powder blue', 'SlateBlue4',
                      'SteelBlue4', 'SteelBlue2', 'SlateBlue3', 'dark slate blue', 'DodgerBlue3', 'SlateBlue1', 'blue4',
                      'light sky blue', 'SkyBlue4', 'LightSkyBlue2', 'LightSteelBlue4', 'DeepSkyBlue4', 'light blue',
                      'sky blue', 'medium slate blue', 'RoyalBlue3', 'LightBlue4', 'deep sky blue', 'SkyBlue1',
                      'LightBlue1', 'royal blue', 'RoyalBlue2', 'CadetBlue2', 'DodgerBlue2', 'SlateBlue2', 'cadet blue',
                      'medium blue', 'steel blue', 'SkyBlue3', 'CadetBlue4', 'blue2', 'CadetBlue3',
                      'slate blue']  # Creates the colours for the bar chart to distinguish between users  

        test = self.teacherDataStructure.getClass(self.classLoggedIn).getRetiredTest(cs)  # Gets the relevant test  

        self.destroyScreen()  # Destroys the previous frame and creates a new one  

        canvas = Canvas(self.frame, width=self.width,
                        height=self.height - 200)  # Creates a new canvas the width of the screen and the height -200 to make sure all points fit on the screen  
        canvas.grid(row=0,
                    columnspan=8)  # Formats the canvas in a grid with columnspan 8 to format the buttons nicely  

        numbers = []  # Creates two new empty data structures to hold the student scores and names associated with scores  
        students = []
        for score in test.getScores():  # Loops through the length of the test scores  
            numbers.append(
                score.getStudentScore())  # Appends the score associated with that set to the score data set  
            students.append(str(score.getStudentName().split(" ")[0][0] + score.getStudentName().split(" ")[1][
                0]))  # Same for the student name, but grabs the initials by splitting the name by space  

        # The variables below size the bar graph  
        canvasHeight = self.height - 200  # Height of canvas  
        yStretchValue = 15  # The highest y = max_data_value * yStretchValue  
        yGapValue = 20  # The gap between lower canvas edge and x axis  
        xStretchValue = 10  # Stretch x wide enough to fit the variables  
        xWidthValue = 40  # The width of the x-axis  
        xGapValue = 60  # The gap between left canvas edge and y axis  

        # A quick for loop to calculate the rectangle  
        xy0 = (canvasHeight - yGapValue)

        for x, y in enumerate(numbers):  # Loops through each data point  
            # Creates the y score coordinates   
            canvas.create_text(10, (canvasHeight - (y * yStretchValue + yGapValue)), anchor=SW,
                               text=('{:>6}'.format(str(y) + " - ")))

            x0 = x * xStretchValue + x * xWidthValue + xGapValue  # Bottom left coordinate  
            y0 = canvasHeight - (y * yStretchValue + yGapValue)  # Top left coordinate   
            x1 = x * xStretchValue + x * xWidthValue + xWidthValue + xGapValue  # Bottom right coordinate  
            y1 = canvasHeight - yGapValue  # Top right coordinate  

            canvas.create_rectangle(x0, y0, x1, y1, fill=newColours[x])  # Draws the rectangle/bar for the data point  
            canvas.create_text(x0 + 2, y0, anchor=SW,
                               text=('{:^8}'.format(students[x])))  # Adds the student initials to the top of the bar  

        canvas.create_rectangle(35, 35, 35, xy0)  # Creates the Y axis  
        canvas.create_rectangle(x1, xy0, 35, xy0)  # Creates the X axis, (size of the rightmost data point)  

        nextButton = Button(self.frame, text="Next",
                            command=lambda: self.createWrongAnswersScreen(cs))  # Creates the next and back buttons  
        backButton = Button(self.frame, text="Back", command=lambda: self.createBoxandWhiskerDiagram(cs))

        backButton.grid(row=1, column=3, pady=55)  # Formats the next and back buttons in the grid  
        nextButton.grid(row=1, column=4, pady=55)

        self.frame.pack()  # Packs the frame and widgets onto the screen  

    def createWrongAnswersScreen(self, cs):
        test = self.teacherDataStructure.getClass(self.classLoggedIn).getRetiredTest(cs)  # Gets the relevant test  
        wrongList, categoryMostWrong = calculateQuestionsWrong(test)
        self.destroyScreen()  # Destroys the previous frame and creates a new one  
        mainLabel = Label(self.frame, text="Commonly Wrong Questions")
        mainLabel.grid(row=0, columnspan=8, pady=35) 
        row = 1 #Creates the labels needed for the questions
        for index in range(3):
            question = Label(self.frame,
                             text="{}% of people scored poorly on the question '{}' - {}".format(wrongList[index][1],wrongList[index][0],wrongList[index][2]))
            question.grid(row=row, columnspan=8, pady=15)
            row += 1
        mostWrongLabel = Label(self.frame, text="The category that students found the most difficult was {}".format(
            categoryMostWrong))
        mostWrongLabel.grid(row=row, columnspan=8, pady=45)
        
        nextButton = Button(self.frame, text="Next",
                            command=self.createTeacherScreen)  # Creates the next and back buttons  
        backButton = Button(self.frame, text="Back", command=lambda: self.createBarChartScreen(cs))
        backButton.grid(row=row + 1, column=3, pady=35)  # Formats the next and back buttons in the grid  
        nextButton.grid(row=row + 1, column=4, pady=35)

        self.frame.pack()

    def createTestMakingScreen(self):  # Procedure to create the test screen  
        self.destroyScreen()  # Destroys the previous frame and creates a new one  

        mainMessageLabel = Label(self.frame,
                                 text="Create a test and give it a name")  # Creates the main message label at the top  
        testName = Label(self.frame, text="Test Name: ")  # Creates the test name label  
        testNameEntry = Entry(self.frame)  # Creates the entry for the test name  
        questionLabel = Label(self.frame, text="How many questions?: ")
        questionSlider = Scale(self.frame, from_=3, to=self.MAXIMUMTESTSIZE, resolution=3, orient=HORIZONTAL)
        questionSlider.config(length=120)
        nextButton = Button(self.frame, text="Next", command=lambda: self.createTestButtonPressed(testNameEntry.get(),
                                                                                                  questionSlider.get()))  # Creates the next and back buttons  
        backButton = Button(self.frame, text="Back", command=self.createTeacherScreen)

        mainMessageLabel.grid(row=0, columnspan=2, pady=55)  # Formats all widgets in grid nicely  
        testName.grid(row=1, columnspan=2)
        testNameEntry.grid(row=2, columnspan=2, pady=10)
        questionLabel.grid(row=3, columnspan=2, pady=20)
        questionSlider.grid(row=4, columnspan=2, pady=10)
        backButton.grid(row=5, column=0, pady=55)
        nextButton.grid(row=5, column=1, pady=55)

        self.frame.pack()  # Packs the frame and widgets onto the screen  

    def createTestButtonPressed(self, testName,
                                questionNumber):  # Procedure for when the create test button is pressed (name checking)  
        activeTests = self.teacherDataStructure.getClass(self.classLoggedIn).getActiveTests()
        retiredTests = self.teacherDataStructure.getClass(self.classLoggedIn).getRetiredTests()
        tests = activeTests + retiredTests
        if testName in ["", " ", "\n","'"] or testName[
            0] == " " or testName.replace(' ','').isalnum() == False:  # If the user entered a blank string or space or newline button  
            self.showError("Please enter a valid name for your test!")  # Show the error  
        else:  # Checking there is not a test with the same name  
            testNames = []  # Creates the empty structure for holding test names  
            for test in tests:  # Iterates through the active and retired tests  
                testNames.append(test.getTestName().lower())  # Appends the names to the data structures  
            if testName.lower() in testNames:  # Checks if the test name is in the structure and already a test (takes account of capitals)  
                self.showError(
                    "Test name already in use. Please try another name!")  # Shows an error if there is a test  
            else:
                self.makeTest(testName, questionNumber)  # Create the test if a valid name is entered  

    def makeTest(self, testName, questionNumber):  # Procedure for creating a test and adding it to the database  
        self.checkQuestionCount()  # Calls the question count to check that there is enough questions for a test  
        newTest = Test(testName)  # Creates an empty test structure with the test name  

        for category in range(3):  # Loops through each category  
            for questions in range(int(
                    questionNumber / 3)):  # Loops through the amount of questions per category by using the maximum test size variable  
                questionNotFound = True  # Marks the question not found variable to True by default  
                boundaryOne = category * self.CATEGORYBOUNDARY  # Marks the lower boundary by multiplying category number by the category boundary  
                boundaryTwo = (
                                          category + 1) * self.CATEGORYBOUNDARY  # Marks the upper boundary by multiplying category +1 by the category boundary  
                while questionNotFound:  # While a question hasn't been found  
                    randomQuestionDigit = randint(boundaryOne,
                                                  boundaryTwo)  # Create a random question number between the two category bounds  
                    question = self.questionDataStructure.getQuestion(
                        randomQuestionDigit)  # Get the question object of that index and store it seperately  
                    if not question.isUsed:  # If the question hasn't been used in a test before  
                        newTest.addQuestion(question.question, question.answer,
                                            question.category)  # Add the question to the test variable  
                        self.questionDataStructure.findAndSetQuestionUsed(
                            question.question)  # Sets the added question to used  
                        questionNotFound = False  # Marks that the question has been found and it should move onto the next question  
        self.teacherDataStructure.getClass(self.classLoggedIn).addActiveTest(
            newTest)  # Add the test to the active tests once a complete test has been created  
        self.createTeacherScreen()  # Create the teacher screen to signifty test has been added  
        handleDataOutput(
            self.teacherDataStructure)  # Write the teacherData to the file so it can handle program reboot  
        handleQuestionDataOutput(
            self.questionDataStructure)  # Writes the questionData to the file so it can handle program reboot  
        createTestFolder(newTest.getTestName(), (self.teacherDataStructure.getClass(
            self.classLoggedIn).getName()))  # Creates the test folder with the name of the test so teacher can upload images to it  

    def checkQuestionCount(self):  # Procedure to check that there are enough unused questions to populate a test  
        questionUnusedCount = 0  # Set the question unused count to zero  
        for question in self.questionDataStructure.getQuestions():  # Loops through all the questions  
            if not question.getUsed():  # Checks if the question has been unused  
                questionUnusedCount += 1  # Adds one to the count if it hasn't been used  
        if questionUnusedCount < self.MAXIMUMTESTSIZE:  # Once it has looped through entirety of questions, does a comparison to see if there are enough unused questions to populate a test  
            self.questionDataStructure.setAllQuestionsUnused()  # If there are not enough questions to populate a test, it resets all questions to unused to allow more tests to be created  

    def viewQuestions(self, cs):  # Procedure to view the questions of a test  
        if cs != ():  # If the cursor selection is not nothing then:  
            cs = int(cs[0])  # Create the test selection index  
            self.destroyScreen()  # Destroys the previous frame and creates a new one  

            test = self.teacherDataStructure.getClass(self.classLoggedIn).getActiveTest(cs)  # Gets the relevant test  
            mentalStrategiesLabel = Label(self.frame, text="MENTAL STRATEGIES",font=("Verdana",16))  # Creates the three category labels  
            timestablesLabel = Label(self.frame, text="TIMESTABLES",font=("Verdana",16))
            keySkillsLabel = Label(self.frame, text="KEY SKILLS",font=("Verdana",16))

            mentalStrategiesLabel.grid(row=0, column=0, padx=50, pady=20,
                                       sticky=W)  # Formats the three category labels in a grid  
            timestablesLabel.grid(row=0, column=1, padx=50, pady=20, sticky=W)
            keySkillsLabel.grid(row=0, column=2, padx=50, pady=20, sticky=W)

            questionPerColumn = int(len(test.testQuestions) / 3)  # Gets the number of questions per column  
            for column in range(3):  # Loops through the columns  
                for row in range(1, (
                        questionPerColumn + 1)):  # Goes through every row in the amount of questions per column  
                    questionText = "Question " + str((column * questionPerColumn) + row) + ":     " + test.getQuestion((
                                                                                                                                   (
                                                                                                                                               column * questionPerColumn) + row - 1))  # Get the label text which is the question number plus the question index  
                    Label(self.frame, text=u"{}".format(questionText),wraplength=350,font=("Verdana",13)).grid(row=row, column=column, pady=5, padx=50,
                                                                            sticky=W)  # Formats the question text in unicode on the screen  

            nextButton = Button(self.frame, text="Next",
                                command=self.createTeacherScreen)  # Creates the next button and formats in a grid  
            nextButton.grid(row=(questionPerColumn + 2), columnspan=3, pady=35)

            image = Image.open(getDocumentationImages()) # Opens and parses the image from the list
            img = image.resize((int(self.width - 250), int(self.height  / 7)),Image.ANTIALIAS)  # Resizes the image to fit on the screen
            photo = ImageTk.PhotoImage(img)  # Makes it into a tkinter photo
            label = Label(self.frame, image=photo)  # Adds and formats the photo to a label
            label.image = photo
            label.grid(row=(questionPerColumn + 3), pady=2,columnspan=3) #Packs the photo to the screen

            self.frame.pack()  # Packs the frame and widgets onto the screen  
        else:
            self.showError("Please select a valid test to view questions")
            self.createTestListBox("DisplayQuestions")

    def scoreModelStudentMark(self, testName):
        studentNames = []  # Creates three empty list variables to hold the various data items  
        lineNumbers = []
        answerQuestions = []
        for score in self.scoreDataStructure.getScores():  # Loops through all of the scores of the scoremodel  
            if score.getStudentName() not in studentNames:  # Adds the student name associated with the digit if it is not already in the list  
                studentNames.append(score.getStudentName())

        for student in studentNames:  # Loops through the newly aquired student names  
            tempLines = []  # Creates the empty structure to hold the questions answered  
            for score in self.scoreDataStructure.getScores():  # Loops through all of the digits in the scoreModel  
                if score.getStudentName() == student:  # Checks if the name is equal to the student we want to gain the scores for  
                    if score.getLineNumber() not in tempLines:  # Checks if the question number is already in the numbers list  
                        tempLines.append(score.getLineNumber())  # Adds the question number if its not in the list  
            lineNumbers.append(
                tempLines)  # Adds the students questions answered to the main list as a sublist to separate students  

        for student in range(len(studentNames)):  # Loops through every student in the student names list  
            answerList = []  # Creates the answer list to hold the students answers  
            for question in range(
                    len(lineNumbers[student])):  # Loops through the question numbers answered by the student  
                answerDigitList = []  # Creates the answer digit list to hold the digits  
                for score in self.scoreDataStructure.getScores():  # Loops through the scores in the scoremodel  
                    if score.getStudentName() == studentNames[student]:  # Checks the name  
                        if score.getLineNumber() == lineNumbers[student][question]:  # Checks the question number  
                            if score.getNumberCorrected() == -1:  # Accounts for the Neural Network correction  
                                answerDigitList.append(
                                    score.getNumberRecognised())  # Adds the number to the question list if the digit hasn't been corrected  
                            else:
                                answerDigitList.append(
                                    score.getNumberCorrected())  # Adds the number to the question list if the digit has been corrected  
                answer = createAnswer(answerDigitList)  # Creates the integer answer from all of the digits  
                answerList.append(answer)  # Adds it to the answer list  
            answerQuestions.append(
                answerList)  # Appends the student answers for each question to the large answer list  
        scoreStudent(answerQuestions, lineNumbers, studentNames, testName)  # Scores the student based on the answers  

    def destroyScreen(self):  # Procedure to destroy and create frame  
        self.frame.destroy()  # Destroys the current frame  
        self.frame = Frame(self.root)  # Creates a new frame in the root window  
