Set FileSysObj = CreateObject("Scripting.FileSystemObject")
Set ObjWshNet = CreateObject("WScript.Network")
Set WshShell = CreateObject("WScript.Shell")

LabelSku = UCase(InputBox("Type McDonald's Store Number or Q to Quit", "McDonald's oDMB label utility"))
If LabelSku = "Q" or LabelSku = "X" Then
	Wscript.Quit
ElseIf LabelSku <> "" Then
	ScreenType = Array("DT Price Menu Board","DT PreSell 1 Left","DT PreSell 1 Right","DT Order COD 1 Left","DT Order COD 1 Right","DT Order COD 2 Left","DT Order COD 2 Right","DT Mini Screen 1","DT PreSell 2 Right","DT PreSell 2 Left")
	ScreenType1 = Array("DT Price Menu Board SOC","DT PreSell 1 Left SOC","DT PreSell 1 Right SOC","DT Order COD 1 Left SOC","DT Order COD 1 Right SOC","DT Order COD 2 Left SOC","DT Order COD 2 Right SOC","DT PreSell 2 Right SOC","DT PreSell 2 Left SOC")
	Dim Stypes, item, ip
	For Each item In ScreenType
		Set re = New RegExp
		With re
			.Pattern    = "(?:SOC)"
			.IgnoreCase = True
			.Global     = False
		End With
		
		If re.Test( item ) Then
			ip = "Yes"
		Else
			ip = "No"
		End If
		
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
		ZPLText = ZPLText & "^PQ2"
		ZPLText = ZPLText & "^FS"
		ZPLText = ZPLText & "^XZ"
		ObjZebra.Write(ZPLText)
		objZebra.Close
		Set objZebra = Nothing
	Next
	For Each item In ScreenType1
		Set re = New RegExp
		With re
			.Pattern    = "(?:SOC)"
			.IgnoreCase = True
			.Global     = False
		End With
		
		If re.Test( item ) Then
			ip = "Yes"
		Else
			ip = "No"
		End If
		
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
		ZPLText = ZPLText & "^PQ3"
		ZPLText = ZPLText & "^FS"
		ZPLText = ZPLText & "^XZ"
		ObjZebra.Write(ZPLText)
		objZebra.Close
		Set objZebra = Nothing
	Next
End If