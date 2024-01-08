import requests
import shutil
import tkinter as tk

window = tk.Tk()

zpl = '^XA^LH0,5^CF0,35^FO5,5^GB500,390,5^FS^FO5,65^GB500,65,5^FS^FO5,195^GB500,65,5^FS^FO5,325^GB500,70,5^FS^FO240,5^GB0,390,5^FS^FO35,30^FD New LTP^FS^FO35,90^FD Old LTP^FS^FO35,150^FDUserName^FS^FO35,215^FD Batch^FS^FO35,280^FD Group ID^FS^FO35,345^FD Date^FS^PQ1^XZ'

# adjust print density (8dpmm), label width (4 inches), label height (6 inches), and label index (0) as necessary
url = 'http://api.labelary.com/v1/printers/8dpmm/labels/2.5x2/0/'
files = {'file' : zpl}
headers = {'Accept' : 'application/pdf'} # omit this line to get PNG images back
response = requests.post(url, headers = headers, files = files, stream = True)

if response.status_code == 200:
    response.raw.decode_content = True
    with open('label.pdf', 'wb') as out_file: # change file name for PNG images
        shutil.copyfileobj(response.raw, out_file)
    img = tk.Label(window, text="image").pack()
    

else:
    print('Error: ' + response.text)