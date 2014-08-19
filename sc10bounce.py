#!/usr/bin/env python
# -*- coding: utf-8 -*-
print u"Content-type: text/html; charset=utf-8\n\n"

#mycomment=bounce input data/дребезг контактов

def lookup_prev_static(input_str):
    output_data=[0];
    input_data=[];
    output_str='';
    for i in input_str: input_data.append(int(i))
    #	print "\nfunct input :", input_data
    for i in xrange(1,len(input_data)):
	if input_data[i-1]==input_data[i]:
	    output=input_data[i]
	else:
	    output=output
	output_data.append(output)
    #output_data=input_data;
    #print "funct output: ", output_data
    for i in output_data: output_str+=str(i)
    #print input_str
    return output_str;

def lookup_prev_dynamic(____i,____i_prev,____j_prev):
    ____j=0
    if ____i==____i_prev: ____j=____i
    else: ____j=____j_prev
    return ____j;
#-------------main------------
input='111110000010000111111110111111000000001010101111101010011001100'
print 'input  :',input
print 'output :',lookup_prev_static(input)

j_str=''
i_prev=j_prev=0
for i in input:
    i=int(i)
    j=lookup_prev_dynamic(i,i_prev,j_prev)
    i_prev=i
    j_prev=j
    j_str+=str(j)
print 'outputd:',j_str
