#!/usr/bin/env python3

import sys
import package_checker

def help():
	print(f"Usage: {sys.argv[0]} <file.py>")

def main():
	if len(sys.argv) < 2:
		print("Expected file to parse")
		help()
		sys.exit(1)
	
	pyFileName = sys.argv[1]
	#print(f'argvs[1]: "{sys.argv[1]}"')
	parseAndInstall(pyFileName)


def parseAndInstall(pyFileName):
	hPyFile = open(pyFileName)
	arrImports = parseFile(hPyFile)
	hPyFile.close()
	
	print(arrImports)
	for sPackage in arrImports:
		pType = package_checker.resolvePackage(sPackage)
		print(f"{sPackage} => {pType}")

def parseFile(hFile):
	bSkipNext = False
	bInString = False
	saImports = []
	while True:
		sLine = hFile.readline()
		if len(sLine) == 0:
			break
		
		saNewImports, bInString, bSkipNext = parseLine(sLine, bInString, bSkipNext)
		for sImport in saNewImports:
			saImports.append(sImport)
	
	saImports = set(saImports)
	saImports = filter(lambda x: len(x) > 0, saImports)
	return list(saImports)

def parseLine(sLine, bInString = False, bSkipNext = False):
	iIndex = 0
	iLineLen = len(sLine)
	saImports = []

	while iIndex < iLineLen:
		if bSkipNext:
			bSkipNext = sLine.endswith('\\\n')
			break

		iIndex = skipSpaces(sLine, iIndex)
		
		# import directive
		if sLine.startswith('import', iIndex):
			iIndex = iIndex + 6
			while True:
				iIndex = skipSpaces(sLine, iIndex)
				
				iStartIndex = iIndex
				iIndex = skipNonSpaces(sLine, iIndex)
				
				saImports.append(sLine[iStartIndex:iIndex])

				iIndex = skipSpaces(sLine, iIndex)
				if sLine[iIndex] != ',':
					break
				iIndex = iIndex + 1
			if sLine[iIndex] == '\\':
				continue
		# from directive
		if sLine.startswith('from', iIndex):
			iIndex = iIndex + 4
			iIndex = skipSpaces(sLine, iIndex)

			iStartIndex = iIndex
			iIndex = skipNonSpaces(sLine, iIndex)
			
			saImports.append(sLine[iStartIndex:iIndex])

			iIndex = skipSpaces(sLine, iIndex)
			if sLine[iIndex] == '\\':
				bSkipNext = True
			break
		#iIndex = iIndex + 1
		break
	
	return saImports, bInString, bSkipNext

def skipSpaces(s, iIndex):
	if s[iIndex] == '\n':
		return iIndex
	while s[iIndex].isspace():
		iIndex = iIndex + 1
	return iIndex

def skipNonSpaces(s, iIndex):
	while not s[iIndex].isspace()\
		and s[iIndex] != ','\
		and s[iIndex] != '\\':
		iIndex = iIndex + 1
	return iIndex

if __name__ == '__main__':
	main()