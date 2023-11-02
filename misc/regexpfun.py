import re

# will find ape

if re.search("ape", "The ape was at the apex"):
	print("There is an ape")

# period will match ape+ any char

allApes = re.findall("ape.", "The ape was at the apex")

for i in allApes:
	print(i)

# will find locations

theStr = "The ape was at the apex"

for i in re.finditer("ape.", theStr):
	locTuple = i.span()
	print(locTuple)
	print(theStr[locTuple[0]:locTuple[1]]

# matching a set of letters

animalString = "Cat rat mat pat"
allAnimals = re.findall("[cCrmfp]at", animalString)

for i in allAnimals: print(i)

# match a range

someAnimals = re.findall("[c-mC-m]at", animalString)
for i in someAnimals: print(i)

# exclusion w ^

someAnimals = re.findall("[^Cr]at", animalString)
for i in someAnimals: print(i)

# replacement

owlFood = "rat cat mat pat"
regex = re.compile("[cr]at")

owlFood = regex.sub("owl", owlFood)
print(owlFood)
