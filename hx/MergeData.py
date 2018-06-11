#!/usr/bin/env python

mDict = {}
print('scan WithdrawSum')
with open('/tmp/WithdrawSum.csv') as file:
	iLine = 0
	for line in file:
		iLine += 1
		fields = line.split(',')
		if len(fields) != 5:
			print('%d: is not 5 fields')
			exit()
		mDict[fields[0]] = fields

print('scan Balance')
emptyWithdrawSum = ['','','','','']
with open('/Users/i070599/Documents/Balance.csv') as file:
	iLine = 0
	for line in file:
		iLine += 1
		fields = line.split(',')
		if len(fields) != 4:
			print('%d: is not 4 fields')
			exit()
		if fields[0] not in mDict:
			mDict[fields[0]].extend(fields[1:])
		else:

			mDict[fields[0]] = [fields[0]].extend(emptyWithdrawSum)
			print(fields)
			exit()

emptyFields = ['', '', '']

print('output to file')
with open('/User/i070599/Documents/Merged.csv', 'w') as file:
	for key, value in mDict.items():
		if len(value) == 5:
			value.extend(emptyFields)	
		file.write(','.join())

print('done')