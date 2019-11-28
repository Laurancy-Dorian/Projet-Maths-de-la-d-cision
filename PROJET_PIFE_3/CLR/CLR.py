import timeit
import sys
import csv
from collections import defaultdict

criteria = ["TB", "B", "AB", "P", "I", "AR"]

# ===== CSV ===== #

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





# ===== ENUMERATION ===== #

"""
	calculates the number of groups of 2 and 3 we can make with the number of students given in parameter
	return : a set of tuple, the first case is the number of groups of 2 students and the second is the number a group of 3
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

		# Get the number of groups of 2 students and groups of 3 
		nb23 = nbGrp23(nb)

		for possibility in (nb23) :

			if (possibility[0] > 0) :

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

			if (possibility[1] > 0) :

				firstElement = students.pop(0)

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

						students.insert(j, tmp_j)


					# Recompose the base collection
					students.insert(i, tmp_i)

				students.insert(0, firstElement)
			
		return (res)
			


# ===== GROUP SELECTION ===== #

"""
	Return true if the group is considered acceptable : each member of the group voted each other member at least the worst criteria defined by lvl 
	lvl : 0 = TB, 1 = B, 2 = AB ... 
"""			
def coupleIsAcceptable(couple, preferences, lvl) : 
	student1 = couple[0]
	student2 = couple[1]
	pref12 = preferences[student1][student2]
	pref21 = preferences[student2][student1]

	for st1 in couple : 
		for st2 in couple :
			if (st1 != st2) :
				if (preferences[st1][st2] not in criteria[0:lvl]) or (preferences[st2][st1] not in criteria[0:lvl]) :
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

	return res





# ===== MAIN ===== #
def main():

	filename = sys.argv[0]
	filename = filename[:-3]

	ext = ""
	for arg in sys.argv:
		if (arg.find("--ext=") != -1) :
			ext = arg[6:]
	

	# Max number of students
	nbstudents = 16

	# Get data from CSV
	preferences = loadDataFromCSV("../DONNEES/preferences" + ext + ".csv") 

	# List of the students
	students = list(preferences.keys())[0:nbstudents]

	# Launch the enumeration algorithm
	enum = enumeration(students)

	# Selects the best groups
	res = bestGroups(preferences, enum)

	exportcsv(filename + '.csv', res)

if __name__ == "__main__":
    main()
