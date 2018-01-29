import math
from math import pow
def calculate_BMI():
	# dictionary for various categories
	category_dictionary = {
		'range(0.0,15.0)':'Very severely underweight',
		'range(15.0,16.0)':'Severely underweight',
		'range(16.0,18.5)':'Underweight',
		'range(18.5,25.0)':'Normal (healthy weight)',
		'range(25.0,30.0)':'Overweight',
		'range(30.0,35.0)':'Obese Class I (Moderately obese)',
		'range(35.0,40.0)':'Obese Class II (Severely obese)',
		'range(40.0,100.0)':'Obese Class III (Very severely obese)'
	}
	mass = float(input('Enter mass'))
	height = float(input("enter height"))
	flag = bool(input('SI units??'))

	if flag == True:
	# take height and mass as inputs IN SI units
		print('1')
		BMI_INDEX = str((mass/math.pow(height,2)))
		print(BMI_INDEX)
	if flag == False:
	# when mass and height in lbs,inches
		print('2')
		BMI_INDEX = str(((mass*703)/(math.pow(height,2))))

	# check conditions
	for i,j in category_dictionary.items():
		if BMI_INDEX in i:
			print('hello')
			print(j)
			return j

p=calculate_BMI()
print (p)







	