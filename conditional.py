#! /usr/bin/python

#print normal message

print "hello there"

print "this is an example of python"

'''
print "it is an example of comment"

'''

#taking input from user
#raw_input always gives the output in strings type format

a = raw_input("plz enter your name: ")

print "welcome here," + a

print "the type of data entered is",type(a)

print "\n \n -------------------------------------------- \n \n "

x= raw_input("type any number here:")

if int(x)>20:
	print "\n hello world"
else: 
	print "\n hello all"
	 
