import requests
import tkinter as tk
from PIL import ImageTk

window = tk.Tk()
# greeting = tk.Label(text="Hello, Tkinter")
# greeting.pack()

zpl = '^XA^LH0,5^CF0,35^FO5,5^GB500,390,5^FS^FO5,65^GB500,65,5^FS^FO5,195^GB500,65,5^FS^FO5,325^GB500,70,5^FS^FO240,5^GB0,390,5^FS^FO35,30^FD New LTP^FS^FO35,90^FD Old LTP^FS^FO35,150^FDJury Rigged^FS^FO35,215^FD Batch^FS^FO35,280^FD Group ID^FS^FO35,345^FD Date^FS^PQ1^XZ'

# adjust print density (8dpmm), label width (4 inches), label height (6 inches), and label index (0) as necessary
url = 'http://api.labelary.com/v1/printers/8dpmm/labels/2.5x2/0/'
files = {'file' : zpl}
response = requests.post(url, files = files, stream = True)
eatme = response.content
qrPreviewImg = ImageTk.PhotoImage(data=eatme)

img = tk.Label(text="image", image=qrPreviewImg).pack()
btn = tk.Button(text="truth", command=lambda:window.destroy()).pack()



window.mainloop()