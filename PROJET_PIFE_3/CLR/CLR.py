import timeit
import sys
import csv
from collections import defaultdict

criteria = ["TB", "B", "AB", "P", "I", "AR"]

def makeCollection(number):
	col = []
	for i in range (number):
		col.append(i+1)

	return col


"""
	Load the data from CSV
	return: a dict whose keys are the students id
			ex : result["John"]["Marie"] = AB
					==> This means John rated Marie 'AB'
"""
def loadDataFromCSV(path):
	results = defaultdict(dict)

	with open(path) as csvfile:
		reader = csv.reader(csvfile)
		students = next(reader)
		for row in reader:
			student = row[0]
			i = 1
			for column in row[1:] :

				results [student][students[i]] = column

				i+=1
				
	return results


"""
	Return the enumeration of the collection given in parameter
	pre : students must have a even number of elements
"""
def enumeration(students):
	# Base Case : The collections only contains 2 elements
	if (len(students) == 2):
		return [[(students[0], students[1])]]
	else:
		res = [] # Collection containing all the lines

		# we remove the first element
		firstElement = students.pop(0)

		for i in range (0, len(students)):

			tmp_i = students.pop(i)
			
			lowerEnum = enumeration(students) # Call enum with the smaller collection of students (minus 2)

			newTuple = (firstElement, tmp_i) # Make a new group composed of the first element of the collection and the i^st element

			# Add the new tuple in each line of the lower enum
			for line in (lowerEnum):
				line.insert(0, newTuple)
				res.append(line)


			# Recompose the base collection
			students.insert(i, tmp_i)	

		students.insert(0, firstElement)
			
		return (res)
			
			
def coupleIsAcceptable(couple, preferences, lvl) : 
	student1 = couple[0]
	student2 = couple[1]
	pref12 = preferences[student1][student2]
	pref21 = preferences[student2][student1]
	return (pref12 in criteria[0:lvl]) and (pref21 in criteria[0:lvl])

"""
	Return a python list containing the best groups
"""
def bestGroups(preferences, enumeration) :
	res = []
	level=1
	while (len(res) == 0 and level < len(criteria)) :
		for line in enumeration :
			lineAccepted = True

			for couple in line :
				if (not(coupleIsAcceptable(couple, preferences, level))) :
					lineAccepted = False
			if (lineAccepted) :
				res.append(line)
		level += 1

	#print (criteria[0:level])
	return res

def main():


	"""
		try:
			sys.argv[1]
		except IndexError:
			nb = 12
		else:
			nb = int(sys.argv[1])
	"""

	# Max number of students
	nbstudents = 16

	# Get data from CSV
	preferences = loadDataFromCSV("../DONNEES/preferencesIG4MD.csv") 
	
	# List of the students
	students = list(preferences.keys())[0:nbstudents]
	
	
	''' 
	# Creates the collection of students
	#nb = int(input("Enter the number of students (must be even) : "))
	students = makeCollection(nb)
	print ("Students :  " + str(students))
	'''

	# Will mesure the computation time
	timestart = timeit.default_timer()

	# Launch the enumeration algorithm
	enum = enumeration(students)

	timestop = timeit.default_timer()

	"""
	# Print the result if it isn't too big
	if (nb <= 10) : 
		for line in (res) :
			print (line)
	"""

	# Additional stats		
	#print ("Number of possibilities : " + str(len(enum)))
	#print('Time: ', str(round(timestop - timestart, 4)) + " seconds")  


	# Selects the best groups
	res = bestGroups(preferences, enum)

	#print (len(res))
	#print (len(enum))
	with open('CLR.csv', 'w') as myfile:
		wr = csv.writer(myfile)
		wr.writerow(res)

if __name__ == "__main__":
    main()
