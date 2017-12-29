#! /usr/bin/python
import commands
import webbrowser

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

if int(x)>20 and int(x)<30:
	print "\n hello world"
elif int(x)<40:
	print commands.getoutput('date')
	print "terminal is opening....",commands.getoutput('gnome-terminal')
else: 
	print "you tube is opening...."
	webbrowser.open_new_tab('https://www.youtube.com')

	 
