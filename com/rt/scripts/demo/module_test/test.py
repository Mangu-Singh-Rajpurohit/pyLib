import sys
print "\n".join(sys.path)
import site
#import os   #   it'll import os.py present in current directory, rather than importing standard os.py
            #   because, directory containing running script is placed before standard library path in
            #   sys.path list. So, current directory is searched first and thus, our os.py is loaded.
            #   to check, run this program from command line(not from pyscripter).
#print dir(os)
def fTest():
    print globals().keys()

temp = 23

print __name__, __package__, __file__

#fd = open("ABC.txt", "w")
#fd.write("python started")
#fd.close()