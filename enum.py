import timeit


def makeCollection(number):
	col = []
	for i in range (number):
		col.append(i+1)

	return col


"""
	Return the enumeration of the collection given in parameter
	pre : students must have a even number of elements
"""
def enum(students):
	# Base Case : The collections only contains 2 elements
	if (len(students) == 2):
		return [[(students[0], students[1])]]
	else:
		res = []

		firstElement = students.pop(0)

		for i in range (0, len(students)):
			tmp_i = students.pop(i)

			lowerEnum = enum(students)

			newTuple = (firstElement, tmp_i)
			for line in (lowerEnum):
				line.insert(0, newTuple)
				res.append(line)

			students.insert(i, tmp_i)	

		students.insert(0, firstElement)
			
		return (res)
			



def main():

	# Creates the collection of students
	nb = int(input("Enter the number of students (must be even) : "))
	students = makeCollection(nb)
	print ("Students :  " + str(students))

	# Will mesure the computation time
	timestart = timeit.default_timer()

	# Launch the enumeration algorithm
	res = enum(students)

	timestop = timeit.default_timer()

	# Print the result if it isn't too big
	if (nb <= 10) : 
		for line in (res) :
			print (line)

	# Additional stats		
	print ("Number of possibilities : " + str(len(res)))
	print('Time: ', str(round(timestop - timestart, 4)) + " seconds")  

main()