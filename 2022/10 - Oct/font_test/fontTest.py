font_num = 0
total_print = ""
while font_num < 11:
    test_print = ""
    test_print += "^XA"
    test_print += "^LH15,15"
    test_print += "^A" + str(font_num) + "N,60"
    test_print += "^FO10,10"
    test_print += "^FD"
    test_print += "This is font " + str(font_num)
    test_print += "^FS"
    test_print += "^XZ"
    total_print += test_print
    font_num += 1

chisel = open("LPT1", "w")
chisel.write(total_print)
chisel.close()