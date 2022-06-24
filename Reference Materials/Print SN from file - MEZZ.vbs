Dim WshShell, oExec
Set wshShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set FileSysObj = CreateObject("Scripting.FileSystemObject")
Set ObjWshNet = CreateObject("WScript.Network")
Set WshShell = CreateObject("Wscript.Shell")

Set objInputFile = objFSO.OpenTextFile("C:\Users\dwilliams4\Desktop\Zebra Label printers\sn.txt",1)

Do until objInputFile.AtEndofStream
	strcomputer = objInputFile.ReadLine
	Set ObjZebra = FileSysObj.CreateTextFile("LPT7:", True)
	
          ZPLText = "^XA"
          ZPLText = ZPLText & "^LH15,0"
          ZPLText = ZPLText & "^FO1,20"
		  ZPLText = ZPLText & "^AsN,25,25"
          ZPLText = ZPLText & "^FD"
          ZPLText = ZPLText & "Serial Number"

          ZPLText = ZPLText & "^FS"
          ZPLText = ZPLText & "^FO03,60"
          ZPLText = ZPLText & "^B3N,N,100,Y,N"
         
          ZPLText = ZPLText & "^FD"
          ZPLText = ZPLText & strcomputer

          ZPLText = ZPLText & "^FS"
          ZPLText = ZPLText & "^XZ"
        
          ObjZebra.Write(ZPLText)
          Wscript.sleep 500
          objZebra.Close
          Set objZebra = Nothing
	
Loop

objInputFile.Close

