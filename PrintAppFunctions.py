def screenSwap(screenOn): # To swap between the various screens within the application.
    pass

def addToList(itemsForList): # To add labels to the currently active list
    currentList += itemsForList

def printList(): # To send the currently active list to be printed
    pass

def BCU_Label(): # To create a BCU label
    pass

def printerSelect(): # For selecting printers appropriate for the current action, as set by settings window
    pass

def clearVars(): # To empty local variables
    pass

def saveToConfig(): # To save settings to a config file
    pass

def rangeToList(range1,range2): # To take 2 points of a range and create a list going from one to the other
    if range1 == "" or range2 =="" or len(range1) != len(range2): # error out of function if one or both range values are empty or they don't match length
        return -1
    


def idleTimer(): # Probably redundant, used to return to the main screen after a timeout event
    pass