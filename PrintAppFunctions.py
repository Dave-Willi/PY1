from tkinter import messagebox
from 

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
        total_print = 1 + int(rangeEnd) - int(rangeStart)
        if total_print <= 0:
            messagebox.showerror("Error", "Please sure you have the first and last tags the correct way around")
            return
        answer = messagebox.askyesno("Question","This will print " + str(total_print) + " labels.\nDo you wish to continue?")
        if answer == True:
            lead_zeros = len(rangeEnd)
            prefixed = str(rangePrefix1).upper()
            suffixed = str(rangeSuffix1).upper()
            full_range = ""
            pre_label = "^XA^LH" + str(15+(cfg.horz_label_mod.get() * 5)) + "," + str(10 + (cfg.label_mod.get() * 8)) + "^FO1,20^ASN,25,25^FDDevice Asset Tag^FS^FO3,60^BCN,80,Y,N^FD"
            suf_label = "^FS^PQ1^XZ"
            for x in range(int(rangeStart), int(rangeEnd)+1):
                y = str(x).zfill(lead_zeros)
                log = prefixed + y + suffixed
                full_range += pre_label + log + suf_label


def idleTimer(): # Probably redundant, used to return to the main screen after a timeout event
    pass