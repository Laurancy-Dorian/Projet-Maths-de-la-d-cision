#############################################
#                                           #
#    CLR GROUP - Decision maths project     #
#                                           #
#############################################


import sys
import csv
from collections import defaultdict

criteria = ["TB", "B", "AB", "P", "I", "AR"]



### ===== CSV IMPORT AND EXPORT ===== ###

"""
	Exports the array in csv in format :
		a b;c d;e f;
		a c;b d;e f:
		etc.
	param : path 	The path of the file
			tab 	The array data to export

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
		


"""
	Load the data from CSV
	param : path 	The path of the file
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





### ===== ENUMERATION ===== ###

"""
	calculates the number of groups of 2 and 3 we can make with the number of students given in parameter
	param : n 	The number of students
	return : 	a set of tuple, the first case is the number of groups of 2 students and the second is the number a group of 3
					ex : { (1, 3), (4, 1) } === 1 group of 2 and 3 groups of 3 OR 4 groups of 2 and 1 group of 3
"""
def nbGrp23 (n) :
	if n < 2 :
		return None
	elif n == 2 :
		return [(1,0)]
	elif n == 3:
		return [(0,1)]
	else :
		rec2 = nbGrp23 (n-2)
		rec3 = nbGrp23 (n-3)

		res = set()
		if (rec2 != None) :
			for line in rec2 :
				res.add((line[0]+1,line[1]))
		if (rec3 != None) :
			for line in rec3 :
				res.add((line[0],line[1]+1))

		return res


"""
	Return the enumeration of 2 and 3 students of the collection given in parameter
	param : students  	the list of the names of the students
"""
def enumeration(students):
	# basic case : The collection only contains 2 or 3 elements
	if (len(students) == 2):
		return [[(students[0], students[1])]]
	elif (len(students) == 3):
		return [[(students[0], students[1], students[2])]]
	else:
		res = [] # Collection containing all the lines

		nb = len (students)

		# Get the number of groups of 2 students and groups of 3 
		nb23 = nbGrp23(nb)

		# For each possibility of groups, we make groups
		for possibility in (nb23) :
			if (possibility[0] > 0) : 	# If it is possible to make one more group of 2 students
				
				firstElement = students.pop(0) # Get the first element of the list

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

			if (possibility[1] > 0) :

				firstElement = students.pop(0) # Get the first element of the list

				for i in range (0, len(students)):
					tmp_i = students.pop(i)
					for j in range (i, len(students)) :
						tmp_j = students.pop(j)
						lowerEnum = enumeration(students) # Call enum with the smaller collection of students (minus 2)
						newTuple = (firstElement,tmp_i, tmp_j) # Make a new group composed of the first element of the collection and the i^st element

						# Add the new tuple in each line of the lower enum
						for line in (lowerEnum):
							line.insert(0, newTuple)
							res.append(line)

						# Recompose the base collection
						students.insert(j, tmp_j)


					# Recompose the base collection
					students.insert(i, tmp_i)

				students.insert(0, firstElement)
			
		return (res)



### ===== GROUP SELECTION ===== ###


"""
	Return true if the group is considered acceptable : each member of the group voted each other member at least the worst criteria defined by lvl 
	 
	param : group 			a tuple containing the name of the members of the group
			preferences 	the preference matrix
			lvl 			A list containing the numbers representing the lvl we currently seek 1 = TB, 2 = B, 3 = AB ...
							each cell of this list is the rate from a student from another (the order of the number in the list is not important)
								ex : The lvl [1, 3] means that a student rated the other TB and one student rated the other AB. Note that [1, 3] and [3, 1] will produce the same result
"""			
def groupAcceptable(group, preferences, lvl) : 

	# Truncate the table if it is too big, its size should be : n(n-1), with n = the number of students in the group
	levels = lvl[0:len(group) * (len(group) - 1)]

	for st1 in group : 
		for st2 in group :
			if (st1 != st2) :

				l = 0
				ok = False
				while l < len(levels) and ok is False:

					# If the first student rated one the second student by one of the levels, then we remove this level from the array (so that it will not be used for another student)
					if (preferences[st1][st2] in criteria[0:levels[l]]):
						levels.pop(l)
						ok = True

					l += 1

	# If all the levels have been removed, it means that the group is acceptable according to the lvl array
	return len(levels) == 0

	

"""
	Return a python list containing the best groups
	param : preferences 	The preference matrix
			enumeration 	The result of the enumeration of students

"""
def bestGroups(preferences, enumeration) :
	res = []

	# Each cell of this array will increase by one each time we make a loop
	level= [1,1,1,1,1,1]
	indexlvl = 5 	# The index of the first cell to increase


	while (len(res) == 0 and level[0] < len(criteria)) :
		
		for line in enumeration :
			lineAccepted = True

			# Look if the groups are acceptable : if at least one group is NOT acceptable, then the whole line is rejected
			for group in line :
				if (not(groupAcceptable(group, preferences, level))) :
					lineAccepted = False
					break

			# if all groups in this line are acceptable, we add the line to the results
			if (lineAccepted) :
				res.append(line)

		# We change the level to the next one
		level[indexlvl] += 1 
		indexlvl -= 1
		if (indexlvl < 0) :
			indexlvl = 5

	return res





### ===== MAIN ===== ###
def main():

	# Get the name of the script for naming the .csv file with the same name
	filename = sys.argv[0]
	filename = filename[:-3]

	# Get the extension of the source .csv file
	ext = ""
	for arg in sys.argv:
		if (arg.find("--ext=") != -1) :
			ext = arg[6:]
	
	# Max number of students : The script will crash beyond
	nbstudents = 16

	# Get data from source CSV
	preferences = loadDataFromCSV("../DONNEES/preferences" + ext + ".csv") 

	# List of the students
	students = list(preferences.keys())[0:nbstudents]

	# Launch the enumeration algorithm
	enum = enumeration(students)

	# Selects the best groups
	res = bestGroups(preferences, enum)

	# Exports the result in a csv file
	exportcsv(filename + '.csv', res)


if __name__ == "__main__":
    main()
