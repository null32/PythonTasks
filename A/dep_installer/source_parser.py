import sys

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