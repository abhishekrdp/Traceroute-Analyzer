#! /user/bin/python
#Filename Project4
import re
import sys

if len(sys.argv)!=2:
  sys.exit("Input the file name!")

f = file(sys.argv[1],'r')
	
data = f.readlines()

local_avg = list()

l_temp = list()
k = list()


for line in range(0,len(data)):
	if data[line].split()[0] != 'traceroute':	
		match = re.findall("\d+.\d+ ms",data[line])
		#print match	
		l_temp = list()
		
		if len(match) !=0:
			if re.search("\* \* \*",data[line - 1])!=None:
				local_avg.append(float(-1.0))
			else:			
				for m in match:		 
					l_temp.append(float(m.split()[0])) 
			
			if(len(l_temp) > 0):			
				curr_avg = sum(l_temp)/len(l_temp)
				local_avg.append(curr_avg)
	else:	
		for each in range(0,len(local_avg)):
			if each == 0:
				k.append(float(local_avg[each] - 0))
			elif each == len(local_avg):
				if (float(local_avg[each] - local_avg[each - 1])) > 0 and local_avg[each - 1 ]!= -1.0:
					k.append(float(local_avg[len(local_avg)] - local_avg[len(local_avg) - 1 ]))		
			else:
				if (float(local_avg[each] - local_avg[each - 1])) > 0 and local_avg[each - 1]!= -1.0:
					k.append(float(local_avg[each] - local_avg[each - 1]))
				
		
		local_avg = list()	
						
if len(k) > 0:
	value3 = sum(k)/len(k)

f.close()
g = open('avg','w')

#***********************************************************************************
#***********************Searching average hops and average delay here***************

f = file(sys.argv[1],'r')

global_hops = list()
delay_arr = list()
link_delay = 0.0

#for all the lines before line with traceroute--------------------------------->
data = f.readlines()
for line in range(0,len(data)):
	if data[line].split()[0]=='traceroute' and line!= 0:
		
		if re.search("\* \* \*",data[line - 1]) == None:
			#print data[line - 1]
			global_hops.append(float(data[line - 1].split()[0]))		
			mat = re.findall("\d+.\d+ ms",data[line - 1])					
			if len(mat) != 0:
				for m in mat:
					l_temp.append(float(m.split()[0])) 					
			if len(l_temp)!=0:
				link_delay = float(sum(l_temp)/len(l_temp))
			delay_arr.append(link_delay)
			l_temp =list()

#for last line<---------------------------------------------------------------->					
if re.search("\* \* \*",data[len(data)-1])==None:
	l_temp =list()				
	global_hops.append(float(data[len(data)-1].split()[0]))
	mat = re.findall("\d+.\d+ ms",data[len(data) - 1])
	if len(mat) != 0:
		for m in mat:
			l_temp.append(float(m.split()[0])) 
	if len(l_temp)!=0:	
		link_delay = float(sum(l_temp)/len(l_temp))
	delay_arr.append(link_delay)

#g = open('avg','w')
h = open('histo','w')

value1 = str('Avg number of hops '+ str(sum(global_hops)/len(global_hops)))
value2 = str('Avg del: '+str(sum(delay_arr)/len(delay_arr)))
value4 = str('Avg link delay: '+str(value3))
g.write(value1 + "\n" + value2 + "\n" + value4 + "\n")

hops_count = {}
for x in global_hops:
	hops_count[x] = global_hops.count(x)
max_hops = int( max( global_hops ) ) + 1
for x in range( 1, max_hops ):
	h.write(str( x ) + " " + str( hops_count.get( x, 0 ) ) + "\n")


g.close()
f.close()
h.close()

