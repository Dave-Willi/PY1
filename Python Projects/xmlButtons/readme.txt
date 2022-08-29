External file will need :-

button name = BBC Logo, eBay Windows QR Code
frame = frame label to place button (tab5 is default)
History name = *BBC Tag*, *Ebay MAC QR tag*
type of label to print = 
			label type = 0 plain text label e.g. (0,"plain tag","","Hello World")
			label type = 1 QR code label e.g. (1,"label","https://www.label.com","Hello Earth")
			label type = 2 BarCode label e.g. (2,"Stripes","F1355SV","Asset Tag")
			label type = 3 Image print e.g. (3,"Pretty picture","img.png")
Code for label = Filename or barcode
Optional additional text for label = eBay Windows, QR Code


Example of file

[BBC]
button_name = "BBC"
history = "BBC Tag"
type = 3
code = "data/bbc.png"
text = ""

[ebay_mac]
button_name = "ebay mac"
history = "ebay mac qr"
type = 1
code = "https://azwusenduserguidestorage.blob.core.windows.net/slef-setup-guide/Setup%20Assistant%20-%20Mac.pdf"
text = "eBay MAC","QR Code"

