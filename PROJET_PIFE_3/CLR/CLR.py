import timeit
import sys
import csv
from collections import defaultdict

criteria = ["TB", "B", "AB", "P", "I", "AR"]

"""
	Exports the array in csv in format :
		a b;c d;e f;
		a c;b d;e f:
		etc.

"""
def exportcsv(path, tab) :
	with open(path, 'w', newline='') as myfile:
		wr = csv.writer(myfile)

		for line in tab :
			tmptab = []
			for grp in line : 
				strcsv = ""
				espace = ""
				for eleve in grp :
					strcsv = strcsv + espace + str(eleve)
					espace = " "
				tmptab.append(strcsv)
			wr.writerow(tmptab)
		

	

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
	elif (len(students) == 3):
		return [[(students[0], students[1], students[2])]]
	else:
		res = [] # Collection containing all the lines

		nb = len (students)

		# we remove the first element

		if (nb % 2 == 0) :

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
		else :

			for i in range (0, len(students)):
				tmp_i = students.pop(i)

				for j in range (i, len(students)):
					tmp_j = students.pop(j)

					for k in range (j, len(students)) :
						tmp_k = students.pop(k)
						lowerEnum = enumeration(students) # Call enum with the smaller collection of students (minus 2)

						newTuple = (tmp_i, tmp_j, tmp_k) # Make a new group composed of the first element of the collection and the i^st element

						# Add the new tuple in each line of the lower enum
						for line in (lowerEnum):
							line.insert(0, newTuple)
							res.append(line)

						# Recompose the base collection
						students.insert(k, tmp_k)

					# Recompose the base collection
					students.insert(j, tmp_j)	

				# Recompose the base collection
				students.insert(i, tmp_i)	
			
		return (res)
			
			
def coupleIsAcceptable(couple, preferences, lvl) : 
	student1 = couple[0]
	student2 = couple[1]
	pref12 = preferences[student1][student2]
	pref21 = preferences[student2][student1]

	for st1 in couple : 
		for st2 in couple :
			if (st1 != st2) :
				if (preferences[st1][st2] not in criteria[0:lvl]) or (preferences[st2][st1] not in criteria[0:lvl]) :
					print (lvl)
					return False


	return True

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
					break
			if (lineAccepted) :
				res.append(line)
		level += 1

	#print (criteria[0:level])
	return res

def main():

	filename = sys.argv[0]
	filename = filename[:-3]

	ext = ""
	for arg in sys.argv:
		if (arg.find("--ext=") != -1) :
			ext = arg[6:]
	

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
	preferences = loadDataFromCSV("../DONNEES/preferences" + ext + ".csv") 
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

	
	# Print the result if it isn't too big

	"""
	for line in (enum) :
		print (line)
	print (len(enum))
	"""
	
	
	# Additional stats		
	#print ("Number of possibilities : " + str(len(enum)))
	#print('Time: ', str(round(timestop - timestart, 4)) + " seconds")  


	# Selects the best groups
	res = bestGroups(preferences, enum)

	exportcsv(filename + '.csv', res)

if __name__ == "__main__":
    main()
