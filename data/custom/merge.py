import sys

f1 = open(sys.argv[1],"r")
f2 = open(sys.argv[2], "r")
of = open("temp.txt", "w")
line1 = f1.readline().strip('\n')
line2 = f2.readline().strip('\n')

while (line1 or line2):

	if not(line2):
		of.write(line1 + '\n')
		line1 = f1.readline().strip('\n')

	elif not(line1):
		of.write(line2 + '\n')
		line2 = f2.readline().strip('\n')

	else:
		if line1 == line2:
			of.write(line2 + '\n')
			line1 = f1.readline().strip('\n')
			line2 = f2.readline().strip('\n')

		elif line1 < line2:
			of.write(line1 + '\n')
			line1 = f1.readline().strip('\n')

		else:
			of.write(line2 + '\n')
			line2 = f2.readline().strip('\n')

f1.close()
f2.close()
of.close()
