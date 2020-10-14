#!/usr/bin/python3
#Yashika Garg
import sys

pdbname=sys.argv[1]
f=open(pdbname,'r')
lines=f.readlines()

lstlist=[]
for line in lines:
    words=line.split()
    words[1]=int(words[1])
    words[5]=int(words[5])
    words[6]=float(words[6])
    words[7]=float(words[7])
    words[8]=float(words[8])
    words[9]=float(words[9])
    words[10]=float(words[10])
#    result=(words[0:11])
#    lstlist.append(result)
#    print(lstlist)
    lstlist.append(words)
#    print(lstlist)
f.close()

f=open("newfile.out",'w')
s= "The list of lists is %s\n" % (lstlist)
f.write(str(s))
f.close()



