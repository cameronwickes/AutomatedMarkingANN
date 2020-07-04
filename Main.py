from GUI import * #Imports the relevant files
from Processing import *


if __name__ == "__main__": #If it’s the main namespace
  MAXSIZE = 30 #Set the maximum test size
  networkDataStructure = handleNetworkDataInput() #Gets the network data from a json file and parses it into a data structure
  teacherDataStructure = handleTeacherDataInput() #Gets the teacher data from a json file and parses it into a data structure
  questionDataStructure = handleQuestionDataInput() #Gets the question data from a json file and parses it into a data structure
  GUI=GUI(teacherDataStructure,questionDataStructure,networkDataStructure,MAXSIZE) #Creates the GUI by calling it
  GUI.root.mainloop() #MainLoop the GUI to display it to the user

	
