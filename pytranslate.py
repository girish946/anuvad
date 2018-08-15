import os
import sys
import polib
from googletrans import Translator
translator = Translator()

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

def TranslateData(data):
    #print("translatting {0}".format(data.encode('utf-8')))
    tData = translator.translate(data, dest='mr')
    #print("translatted to {0}".format(tData.text.encode('utf8')))
    return tData.text

def printAllMsgStrs(data):
    lines = data.split("\n")
    start = len("msgid")
    transKeys = []
    for i in lines:
        contents = i.strip()
        if contents.startswith("msgid"):
            #print(contents[start+1:])
            if contents[start+1:]:
                transKeys.append(contents[start+1:])
    return transKeys

def writeToFile(key, val):
    with open("some.po", "w+") as transFile:
        for (i, j) in zip(key, val):
            transFile.write("{0}:\t{1}\n".format(i.encode('utf-8'), j.encode('utf8')))


if __name__  == '__main__':
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            #print("exists")
            #data = open(sys.argv[1]).read()
            #if data:
            #    keys = printAllMsgStrs(data)
            po = polib.pofile(sys.argv[1])
            keys = []
            for i in po:
                keys.append(i.msgid)
            print("\n\n\n\n")
            total = len(keys)
            vals = []
            for i in range(len(keys)):
                percent = round(100 * (float(i)/float(total)), 2)
                sys.stdout.write(ERASE_LINE)
                sys.stdout.write(CURSOR_UP_ONE*5)
                sys.stdout.write(ERASE_LINE)
                sys.stdout.write('\rTranslatting: {0:.2f} % done\n'.format(percent))
                sys.stdout.write("\rKey is: {0}".format(keys[i].replace("\n"," ").encode('utf-8')))
                sys.stdout.flush()
                if keys[i]:
                    vals.append(TranslateData(keys[i]))
            percent = round(100, 2)
            sys.stdout.write("\r                                      ")
            sys.stdout.write('\rTranslatting: {0:.2f} % done'.format(percent))
            sys.stdout.flush()

            #print(len(vals))
            for i in range(len(po)):
                po[i].msgstr = vals[i]
                #print(po[i])

            po.save("output.po")
            #writeToFile(keys, vals)

