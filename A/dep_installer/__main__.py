# hack to import dep_installer from parent directory
# because you can't import . from here
# python is great and bla bla bla...
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import argparse
import dep_installer

my_parser = argparse.ArgumentParser(
    prog='dep_installer',
    description="Install missing modules for source file via pip",
    add_help=True
)

my_parser.add_argument(
    'path',
    type=str,
    help='Path to the *.py file'
)
my_parser.add_argument(
    '-v',
    '--verbose',
    dest="is_verbose",
    action='store_true',
    help="Verbose output"
)
my_parser.add_argument(
    '-n',
    '--dry-run',
    dest='is_dry',
    action='store_true',
    help="Do not run pip command on missing modules"
)

args = my_parser.parse_args()

hPyFile = open(args.path)
imported_modules = dep_installer.modules_of_file(hPyFile)
hPyFile.close()

for m in imported_modules:
    m_type = dep_installer.install_module(m, args.is_dry)
    print(f"{'[-]' if m_type == dep_installer.PackageType.UNKNOWN else '[+]'} {m}")
#	
#	print(arrImports)
#	for sPackage in arrImports:
#		pType = package_checker.resolvePackage(sPackage)
#		print(f"{sPackage} => {pType}")
