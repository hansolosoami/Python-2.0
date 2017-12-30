#!/usr/bin/python
import commands
import os

choice="""
press 1  to OPEN CALC  :
press 2  to OPEN Text Editor  :
press 3  to Create Directory :
press 4  to Reboot Your Machine :
press 5  to  CHECK CURRENT RAM USED out of Total in MB :
"""
print choice

ch=raw_input("enter any number")

if int(ch)==1:
	print commands.getoutput('gcalccmd')
elif int(ch)==2:
	print commands.getoutput('gedit')
elif int(ch)==3:
	os.mkdir('mydir')
	print "directory is created!!!!"
elif int(ch)==4:
	print commands.getoutput('reboot')
elif int(ch)==5:
	print commands.getoutput('cat /proc/meminfo')  
else:
	print "wrong choice"


