Set FileSysObj = CreateObject("Scripting.FileSystemObject")
Set ObjWshNet = CreateObject("WScript.Network")
Set WshShell = CreateObject("WScript.Shell")

LabelSku = UCase(InputBox("Type Starbuck's Store Number or Q to Quit", "Starbuck's media player label utility"))
If LabelSku = "Q" or LabelSku = "X" Then
	Wscript.Quit
ElseIf LabelSku <> "" Then
	ScreenType = Array("BackOfBar 1", "DailyOrderBoard 1", "Menuboard 1", "Menuboard 2", "Menuboard 3")
	Dim Stypes, item, ip
	For Each item In ScreenType		
		'Set re = New RegExp
		'With re
		'	.Pattern    = "(?:SOC)"
		'	.IgnoreCase = True
		'	.Global     = False
		'End With
		
		'If re.Test( item ) Then
			ip = "Yes"
		'Else
		'	ip = "No"
		'End If
		
		Set ObjZebra = FileSysObj.CreateTextFile("LPT3:", True)
		ZPLText = "^XA"
		ZPLText = ZPLText & "^LH020,20"
		ZPLText = ZPLText & "^F01,10"
		ZPLText = ZPLText & "^A0N,40,40"
		ZPLText = ZPLText & "^FD"
		ZPLText = ZPLText & "Store Number:"
		ZPLText = ZPLText & "^FS"
		ZPLText = ZPLText & "^FO1,60"
		ZPLText = ZPLText & "^A0N,40,40"
		ZPLText = ZPLText & "^FD"
		ZPLText = ZPLText & LabelSku
		ZPLText = ZPLText & "^FS"
		ZPLText = ZPLText & "^FO1,130"
		ZPLText = ZPLText & "^A0N,40,40"
		ZPLText = ZPLText & "^FD"
		ZPLText = ZPLText & "Screen:"
		ZPLText = ZPLText & "^FS"
		ZPLText = ZPLText & "^FO1,180"
		ZPLText = ZPLText & "^A0N,40,40"
		ZPLText = ZPLText & "^FD"
		ZPLText = ZPLText & item
		ZPLText = ZPLText & "^FS"
		ZPLText = ZPLText & "^FD"
		ZPLText = ZPLText & "^FS"
		ZPLText = ZPLText & "^FO1,250"
		ZPLText = ZPLText & "^A0N,40,40"
		ZPLText = ZPLText & "^FD"
		ZPLText = ZPLText & "IP Assigned:"
		ZPLText = ZPLText & "^FS"
		ZPLText = ZPLText & "^FO1,300"
		ZPLText = ZPLText & "^A0N,40,40"
		ZPLText = ZPLText & "^FD"
		ZPLText = ZPLText & ip
		ZPLText = ZPLText & "^FS"
		ZPLText = ZPLText & "^FD"
		ZPLText = ZPLText &"^PQ2"
		ZPLText = ZPLText & "^FS"
		ZPLText = ZPLText & "^XZ"
		ObjZebra.Write(ZPLText)
		objZebra.Close
		Set objZebra = Nothing
	Next
End If