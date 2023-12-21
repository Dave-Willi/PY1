from tkinter import messagebox
import re

# is_on = True
import settings

def main():
    pass

def screenSwap(self, screenOn): # To swap between the various screens within the application.
    settings.currentList = screenOn
    frame = self.frames[screenOn]
    frame.tkraise()

def addToList(itemsForList): # To add labels to the currently active list
    settings.currentList.set(itemsForList)

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
    global currentList
    if range1 == "" or range2 =="" or len(range1) != len(range2): # error out of function if one or both range values are empty or they don't match length
        return -1
    rangePrefix1 = ""
    rangeStart = ""
    rangeSuffix1 = "" 
    rangePrefix2 = ""
    rangeEnd = ""
    rangeSuffix2 = ""
    rangeSplit1 = re.split("(\d+)", range1)
    rangeSplit2 = re.split("(\d+)", range2)
    y = 0
    z = 0
    for x in rangeSplit1: #cycles through however many splits exist in the first split
        if rangeSplit1[y] != rangeSplit2[y]:
            z = y + 1
            rangeStart = min(rangeSplit1[y],rangeSplit2[y]) # sets the lowest number entered into the start
            rangeEnd = max(rangeSplit2[y],rangeSplit1[y]) # sets the highest number entered into the end
            for x in rangeSplit1[z:]:
                try:
                    if rangeSplit1[z] == rangeSplit2[z]:
                        rangeSuffix1 += x
                        rangeSuffix2 += x
                        z+=1
                    else:
                        messagebox.showerror("Error", "Problem determining the suffix")
                        return
                except:
                    break
            break
        elif rangeSplit1[y] == rangeSplit2[y]:
            rangePrefix1 += x
            rangePrefix2 += x
        y+=1
    if rangePrefix1 != rangePrefix2:
        messagebox.showerror("Error", "Error detected in the prefix. \nPlease check and try again")
        return
    elif rangeSuffix1 != rangeSuffix2:
        messagebox.showerror("Error", "Error detected in the suffix. \nPlease check and try again")
        return
    else:
            lead_zeros = len(rangeEnd)
            if settings.is_on == True:
                prefixed = str(rangePrefix1).upper()
                suffixed = str(rangeSuffix1).upper()
                pass
            else:
                prefixed = str(rangePrefix1)
                suffixed = str(rangeSuffix1)
            newlist = ""
            for x in range(int(rangeStart), int(rangeEnd)+1):
                y = str(x).zfill(lead_zeros)
                newlist += prefixed + y + suffixed + "\n"
            addToList(newlist)
            clearInputs()

    return

def idleTimer(): # Probably redundant, used to return to the main screen after a timeout event
    pass

def clearInputs(): # To clear temporary inputs but NOT active list
    pass

def backBtn(): # To return to home screen
    pass

def helpBtn():
    pass

def historyBtn():
    pass

def settingsBtn():
    pass

# if __name__ == '__main__':
#     main()