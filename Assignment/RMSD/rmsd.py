#!/usr/bin/python3
#github.com/yg19d/BCH5884/Assignment/RMSD

import sys, math

#function defined to read the pdb and return the list of atoms
def readpdb(pdb1,pdb2):

    #open the first pdb file and make the list of atoms
    f=open(pdb1,'r')
    lines=f.readlines()

    #lists are defined globally in order to be accessed when called through 'main' namespace
    global lstlist1, lstlist2

    lstlist1=[]
    for line in lines:
        words=line.split()
        words[1]=int(words[1])
        words[5]=int(words[5])
        words[6]=float(words[6])
        words[7]=float(words[7])
        words[8]=float(words[8])
        words[9]=float(words[9])
        words[10]=float(words[10])
        lstlist1.append(words)

    f.close()
    
    #open the second pdb file and make the list of atoms
    f=open(pdb2,'r')
    lines=f.readlines()

    lstlist2=[]
    for line in lines:
        words=line.split()
        if len(words) == 12:
            words[1]=int(words[1])
            words[5]=int(words[5])
            words[6]=float(words[6])
            words[7]=float(words[7])
            words[8]=float(words[8])
            words[9]=float(words[9])
            words[10]=float(words[10])
            lstlist2.append(words)
        else:
            pass

    f.close()

#function defined to calculate the rmsd value
def rmsd (file1,file2):

    global rmsd_value

    Total=0
    
    #loop to calculate the square of the difference between the respective cordinates 
    for i in range (0, len(file1)):
        x=((file1[i][6] - file2[i][6])**2)
        y=((file1[i][7] - file2[i][7])**2)
        z=((file1[i][8] - file2[i][8])**2)

        Total= Total + x + y + z 
    
    #calculation of the final rmsd value
    rmsd_value=math.sqrt(Total/len(file1))

if __name__=="__main__":
    readpdb(sys.argv[1], sys.argv[2])
    rmsd(lstlist1, lstlist2)
    print ("The root mean square deviation of the two pdb files is %.2f" % (rmsd_value))

