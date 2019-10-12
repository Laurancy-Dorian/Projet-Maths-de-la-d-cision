
"""
	Return the enumeration of the collection given in parameter
"""
def enum(students):

	# Base Case : The collections only contains 2 elements
	if (len(students) == 2):
		return [[(students[0], students[1])]]
	else:
		res = []
		for i in range (len(students)-1):
			for j in range (i+1, len(students)-1):
					tmp = students.copy()

					tmp.pop(j)
					tmp.pop(i)

					en = enum(tmp)

					adding = (students[i], students[j])
					for ligne in (en):
						ligne.append(adding)
						res.append(ligne)


		return (res)
			



def main():
	ensemble = [1, 2, 3, 4, 5, 6]
	res = enum(ensemble)
	print ("Nombre de possibilités : " + str(len(res)))
	for ligne in (res) :
		print (ligne)


main()