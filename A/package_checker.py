#!/usr/bin/env python3

from enum import Enum
import sys
import subprocess
import os

class PackageType(Enum):
    UNKNOWN = 0
    SYSTEM = 1
    LOCAL = 2
    PIP = 3

def resolvePackage(sPackageName):
    if check_system(sPackageName):
        return PackageType.SYSTEM
    if check_local(sPackageName):
        return PackageType.LOCAL
    if tryPipInstall(sPackageName):
        return PackageType.PIP
    return PackageType.UNKNOWN

saSystemPackages = sys.builtin_module_names
def check_system(sPackageName):
    return sPackageName in saSystemPackages

'''
def check_pip(sPackageName):
    pipPackages = getLocalPip()
    return sPackageName in pipPackages

saPipPackages = None
def getLocalPip():
    global saPipPackages
    if saPipPackages != None:
        return saPipPackages
    saPipPackages = []
    
    try:
        hRunInfo = subprocess.run(['pip', 'freeze'], capture_output=True)
    except:
        print("Failed to run pip")
        raise

    sOut = hRunInfo.stdout.decode()
    for sLine in sOut.split('\n'):
        if len(sLine) == 0:
            continue
        sName, sVer = sLine.split('==')
        saPipPackages.append(sName)
'''

def tryPipInstall(sPackageName):
    try:
        hRunInfo = subprocess.run(['pip3', 'install', sPackageName], capture_output=True)
    except:
        print("Failed to run pip")
        raise

    return hRunInfo.returncode == 0

# check sys.path for libs
def check_local(sPackageName):
    localPackages = getPathPackages()
    return sPackageName in localPackages

saPathPackages = None
def getPathPackages():
    global saPathPackages
    if saPathPackages != None:
        return saPathPackages
    saPathPackages = []

    for sSearchPath in sys.path:
        saPathPackages.extend(getFolderModules(sSearchPath))
    
    return saPathPackages

def getFolderModules(sFolderPath, prefix=None):
    if not os.path.exists(sFolderPath):
        return []

    saRes = []
    saFiles = os.listdir(sFolderPath)
    for sFileName in saFiles:
        sFullName = os.path.join(sFolderPath, sFileName)

        if os.path.isfile(sFullName) and sFullName.endswith(".py"):
            saRes.append(moduleName(sFileName, prefix))

        if os.path.isdir(sFullName):
            if '__init__.py' in os.listdir(sFullName):
                saRes.append(moduleName(sFileName, prefix))
            
            saRes.extend(getFolderModules(sFullName, sFileName))
        
        # TODO add symlinks processing
    return saRes

def moduleName(sFileName, sPrefix):
    moduleName = sFileName if sPrefix == None else f"{sPrefix}.{sFileName}"
    if moduleName.endswith('.py'):
        moduleName = moduleName[:-3]
    return moduleName