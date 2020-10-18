#!/usr/bin/python3
#Yashika Garg
import sys

# Open file (.pdb) from user input
pdbname=sys.argv[1]
f=open(pdbname,'r')
lines=f.readlines()

# Save rows of .pdb file to lists 
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

#Make list of lists
f=open("listoflist",'w')
s= "The list of lists is %s \n" %(lstlist)
f.write(str(s))
f.close()

f=open("center",'w')

#Make list of all x,y,z cordinates separately
x=[]
y=[]
z=[]

for line in lines:
    words=line.split()
    xvalue=float(words[6])
    yvalue=float(words[7])
    zvalue=float(words[8])
    x.append(xvalue)
    y.append(yvalue)
    z.append(zvalue)

#Make list of mass according to the atom data
mass=[]
 
for element in lstlist:
    if element[11] == "N":
        mass.append(14)
    elif element[11] == "O":
        mass.append(16)
    elif element[11] == "C":
        mass.append(12)
    else:
        mass.append(32)

#Multiplication of mass by x-, y-, and z- cordinates and saving them to a list
mx=[]
my=[]
mz=[]

for i in range (0, len(mass)):
     massx=round(mass[i]*x[i],2)
     mx.append(massx)
     massy=round(mass[i]*y[i],2)
     my.append(massy)
     massz=round(mass[i]*z[i],2)
     mz.append(massz)

#Addition of all multiplied data and saving them to a list
sm=sum(mass)
sx=sum(mx)
sy=sum(my)
sz=sum(mz)

#Calculation of X-, Y-, Z- cordinate of center of mass
X_cordinate=sx/sm
Y_cordinate=sy/sm
Z_cordinate=sz/sm

#Calculation of centered mass of all the atoms and saving them to a list with respect to their cordinates
centeredmassx=[]
centeredmassy=[]
centeredmassz=[]
for i in range (0, len(x)):
    centermassx=round(x[i]-X_cordinate,2)
    centeredmassx.append(centermassx)
for i in range (0, len(y)):
    centermassy=round(y[i]-Y_cordinate,2)
    centeredmassy.append(centermassy)
for i in range (0, len(z)):
    centermassz=round(z[i]-Z_cordinate,2)
    centeredmassz.append(centermassz)

#Addition of x-, y- and z- cordinates for calculation of geometric center and saving them to a list
addx=[]
addy=[]
addz=[]

addx=sum(x)
addy=sum(y)
addz=sum(z)

#Calculation of geometric center
average_x=[]
average_y=[]
average_z=[]

average_x=addx/(len(x))
average_y=addy/(len(y))
average_z=addz/(len(z))

f.close()

#Get user input for choice of center of mass or geometric center 
#Print the output according to user's input
#Give error message if the user doesn't follow the instructions
f=open("finaloutput",'w')
center=int(input("Please enter your choice, Geometric centre [0] or Centre of Mass [1]: "))
if center==0:
    print ("The geometric center is at %.2f, %.2f, %.2f" % (average_x, average_y, average_z))
elif center==1:
    print ("The center of mass is at %.2f, %.2f, %.2f" % (X_cordinate, Y_cordinate, Z_cordinate))
else:
    print ("Invalid input. Enter 0 or 1")

#Format new (.pdb) file
for i in range(len(centeredmassx)):
    f.write("%6.2f %6.2f %6.2f\n" % (centeredmassx[i], centeredmassy[i], centeredmassz[i]))

f.close()


