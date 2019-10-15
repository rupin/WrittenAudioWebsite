from django import template
import datetime
register = template.Library()


def durationToParts(value, arg):
	if value is None or value==0:
		return 0

	hours, remainder = divmod(value, 3600)
	minutes, seconds = divmod(remainder, 60)
	
	
	if arg=='s':
		return seconds
	if arg=='m':
		return minutes
	if arg=='h':
		return hours

	return 0

def options(value, arg):
	if value is None or value==0:
		return 0

	hours, remainder = divmod(value, 3600)
	minutes, seconds = divmod(remainder, 60)
	option=''
	
	if arg=='s':
		for s in range (0,60):
			index=str(s)
			if(s==seconds):

				option=option+"<option value='"+index+"' selected='selected'>"+index+"</option>"
			else:
				option=option+"<option value='"+index+"'>"+index+"</option>"
		return option

	if arg=='m':
		for m in range (0,60):
			index=str(m)
			if(m==minutes):
				option=option+"<option value='"+index+"' selected='selected'>"+index+"</option>"
			else:
				option=option+"<option value='"+index+"'>"+index+"</option>"
		return option
	if arg=='h':
		for h in range (0,24):
			index=str(h)
			if(h==hours):
				option=option+"<option value='"+index+"' selected='selected'>"+index+"</option>"
			else:
				option=option+"<option value='"+index+"'>"+index+"</option>"
		return option
	# if arg=='m':
	# 	return minutes
	# if arg=='h':
	# 	return hours

	return 0
	

	
	

register.filter('DurationFilter', durationToParts)
register.filter('optionGenerator', options)