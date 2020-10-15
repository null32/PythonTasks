__all__ = ['modules_of_file', 'install_module', 'PackageType']

from dep_installer import module_installer
from dep_installer import source_parser
from dep_installer.module_installer import PackageType 

def modules_of_file(file_handle):
    return source_parser.parseFile(file_handle)

def install_module(module_name, is_dry=False):
    return module_installer.resolve_package(module_name, is_dry)