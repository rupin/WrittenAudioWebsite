from django import template
import datetime
register = template.Library()


def secondstoTime(value):
	hours, remainder = divmod(value, 3600)
	minutes, seconds = divmod(remainder, 60)
	minutesText='minute'
	hoursText='hour'
	secondsText='second'
	retval=''
	if(hours>1):
		hoursText='hour'
	
	if(minutes>1):
		minutesText='minutes'
	if(seconds>1):
		secondsText='seconds'

	if(hours>0):
		retval=retval+ str(hours) + " "+ hoursText
	if(minutes>0):
		retval=retval+" "+str(minutes) + " "+ minutesText
	if(seconds>0):
		retval=retval +" "+ str(seconds) +" "+ secondsText
	return retval

	
	

register.filter('SecondsFormatter', secondstoTime)