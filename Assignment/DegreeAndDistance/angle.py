#!/usr/bin/python3

# link to the repository- github.com/yg19d/BCH5884

import math

x1=int(input("Enter the x-cordinate of point A: "))
y1=int(input("Enter the y-cordinate of point A: "))
x2=int(input("Enter the x-cordinate of point B: "))
y2=int(input("Enter the y-cordinate of point B: "))
x3=int(input("Enter the x-cordinate of point C: "))
y3=int(input("Enter the y-cordinate of point C: "))

# distance between the points

a=math.sqrt((x2-x1)**2+(y2-y1)**2)
b=math.sqrt((x3-x2)**2+(y3-y2)**2)
c=math.sqrt((x1-x3)**2+(y1-y3)**2)

print("The distance between point A and B is", a)
print("The distance between point B and C is", b)
print("The distance between point A and C is", c)

# angle determination by cosine law

alpha=math.acos((a*a+b*b-c*c)/(2*a*b))
beta=math.acos((b*b+c*c-a*a)/(2*b*c))
gamma=math.acos((a*a+c*c-b*b)/(2*a*c))

# converting into degrees

pi=22/7
alpha1=alpha*(180/pi)
beta1=beta*(180/pi)
gamma1=gamma*(180/pi)

print("Alpha, Beta and Gamma angles in degrees are", alpha1, beta1, gamma1)
