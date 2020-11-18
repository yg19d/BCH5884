#!/usr/bin/python3
#github.com/yg19d/BCH5884/Assignment/ProjectII

import numpy
from scipy.signal import find_peaks 
from matplotlib import pyplot

#Read the file
f=open("superose6_50.asc")
lines=f.readlines()
f.close()

#Make lists of time and absorbance values
#Convert the list into array
time=[]
absrb=[]

for line in lines[3:]:
    words=line.split()
    try:
        time.append(float(words[0]))
        absrb.append(float(words[1]))
    except:
        print("Parsed",line)
        continue

time=numpy.array(time)
absrb=numpy.array(absrb)

#Find the peaks

threshold=75
peaks_absrb=[]
peaks_time=[]
peaks_cordinate=[]
index=[]

for i in range ((len(absrb))-1):
    l=absrb[i-1]
    m=absrb[i]
    n=absrb[i+1]
    if m>=l and m>=n and m>threshold:
        peaks_absrb.append(absrb[i])
        peaks_time.append(time[i])
        peaks_cordinate.append((time[i],absrb[i]))
        index.append(i)
        
#Find the slopes

slope=[]

for i in range((len(absrb))-1):
    x_diff=time[i+1]-time[i]
    y_diff=absrb[i+1]-absrb[i]
    slope.append(y_diff/x_diff)

#Find the boundaries of the peaks by concept of dips
dip_time=[]
dip_absrb=[]

for i in range(len(index)-1):
    list_time=time[index[i]:index[i+1]]
    list_absrb=absrb[index[i]:index[i+1]]
    list_absrb_array=numpy.array(list_absrb)
    inv_data=1/list_absrb_array
    dips, _ =find_peaks(inv_data)
    dip_time.append(float(list_time[dips]))
    dip_absrb.append(list_absrb[dips])

#Find the extreme boundaries of the collective peaks
#i.e. start of first peak and end of last peak
head_x=[]
head_y=[]
tail_x=[]
tail_y=[]

u=index[0]-5
while (slope[u]>5):
    u=u-1
head_x.append(float(time[u-4]))
head_y.append(absrb[u-4])

v=index[len(index)-1]
while (slope[v+5]<-5):
    v=v+1
tail_x.append(float(time[v+4]))
tail_y.append(absrb[v+4])

#Print the peak cordinates and the start/end times of the peak
print("The cordinates of peak 1 are", peaks_cordinate[0], "and it starts at time %.1f and ends at time %.1f" % (head_x[0],dip_time[0])) 
print("The cordinates of peak 2 are", peaks_cordinate[1], "and it starts at time %.1f and ends at time %.1f" % (dip_time[0],dip_time[1]))
print("The cordinates of peak 3 are", peaks_cordinate[2], "and it starts at time %.1f and ends at time %.1f" % (dip_time[1],dip_time[2]))
print("The cordinates of peak 4 are", peaks_cordinate[3], "and it starts at time %.1f and ends at time %.1f" % (dip_time[2],tail_x[0]))

#Label the boundaries of the peaks on the chromatogram
pyplot.plot(time,absrb)
pyplot.scatter(peaks_time,peaks_absrb,color='green')
pyplot.scatter(dip_time,dip_absrb,color='red',marker='*')
pyplot.scatter(head_x,head_y,color='red',marker='*')
pyplot.scatter(tail_x,tail_y,color='red',marker='*')

#Label the peaks on the chromatogram with time and maximum absorbance
for time,absrb in zip(peaks_time, peaks_absrb):
    pyplot.text(time,absrb,'(%.1f,%.1f)'%(time,absrb),ha='center',va='bottom')

#Label the axes
pyplot.title('CHROMATOGRAM',pad=20,color='magenta',fontsize=20)
pyplot.xlabel('TIME',color='purple',fontsize=14)
pyplot.ylabel('ABSORBANCE',color='purple',fontsize=14)

pyplot.show()

