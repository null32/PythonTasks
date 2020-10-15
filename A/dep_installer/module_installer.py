from enum import Enum
import sys
import subprocess
import os

class PackageType(Enum):
    UNKNOWN = 0
    SYSTEM = 1
    LOCAL = 2
    PIP = 3

def resolve_package(package_name, is_dry=False):
    if check_system(package_name):
        return PackageType.SYSTEM
    if check_local(package_name):
        return PackageType.LOCAL
    if not is_dry:
        if try_pip_install(package_name):
            return PackageType.PIP
    else:
        if check_pip_search(package_name):
            print(f"pip3 install {package_name}")
            return PackageType.PIP
    return PackageType.UNKNOWN

def check_system(package_name):
    return package_name in sys.builtin_module_names

def check_pip_search(package_name):
    try:
        run_info = subprocess.run(['pip3', 'search', package_name], capture_output=True)
    except:
        print("Failed to run pip")
        raise

    is_found = False
    for out_line in run_info.stdout.decode().split('\n'):
        if out_line.startswith(package_name + ' '):
            is_found = True

    return is_found

def try_pip_install(package_name):
    try:
        run_info = subprocess.run(['pip3', 'install', package_name], capture_output=True)
    except:
        print("Failed to run pip")
        raise

    return run_info.returncode == 0

# check sys.path for libs
def check_local(package_name):
    localPackages = get_path_packages()
    return package_name in localPackages

packages_in_path = None
def get_path_packages():
    global packages_in_path
    if packages_in_path != None:
        return packages_in_path
    packages_in_path = []

    for search_path in sys.path:
        packages_in_path.extend(get_folder_modules(search_path))
    
    return packages_in_path

def get_folder_modules(folder_path, prefix=None):
    if not os.path.exists(folder_path):
        return []

    res = []
    for file_name in os.listdir(folder_path):
        full_name = os.path.join(folder_path, file_name)

        if os.path.isfile(full_name) and full_name.endswith(".py"):
            res.append(module_name(file_name, prefix))

        if os.path.isdir(full_name):
            if '__init__.py' in os.listdir(full_name):
                res.append(module_name(file_name, prefix))
            
            res.extend(get_folder_modules(full_name, file_name))
        
        # TODO add symlinks processing
    return res

def module_name(file_name, prefix):
    module_name = file_name if prefix == None else f"{prefix}.{file_name}"
    if module_name.endswith('.py'):
        module_name = module_name[:-3]
    return module_name