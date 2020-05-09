import os
import sys

path_left = sys.argv[1]
path_right = sys.argv[2]


def list_path(path):
    dirs = []
    files = []
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                files.append((entry.name,entry.stat().st_size))
            elif entry.is_dir():
                dirs.append(entry.name)
            else:
                RuntimeError("neither dir nor file: {} in {}".format(entry, path))
    return (dirs,files)

def search_missing(base, comp):
    missing = []
    common = []
    for data in base:
        if data in comp:
            common.append(data)
        else:
            missing.append(data)
            
    return sorted(missing), sorted(common)

def combine_and_add_path(missing_dirs, missing_files, path):
    missing = []
    
    for elem in missing_dirs:
        elem_tmp = os.path.join(path,elem)
        missing.append(elem_tmp)
        
    for elem,_ in missing_files:
        elem_tmp = os.path.join(path,elem)
        missing.append(elem_tmp)        

    return missing


def compare_and_print(path_left, path_right):
    (dirs_left, files_left) = list_path(path_left)
    (dirs_right, files_right) = list_path(path_right)
    
            
    missing_files_right, common_1 = search_missing(files_left, files_right)
    missing_files_left, common_2 = search_missing(files_right, files_left)
    assert(common_1 == common_2)

    missing_dirs_right, common_1  = search_missing(dirs_left, dirs_right)
    missing_dirs_left, common_2 = search_missing(dirs_right, dirs_left)
    assert(common_1 == common_2)
    common = common_1
    
    
    
    #print("current path left:", path_left)
    #print("current path right:", path_right)
    #print("missing_files_left:", missing_files_left)
    #print("missing_dirs_left:", missing_dirs_left)
    #print("missing_files_right:", missing_files_right)
    #print("missing_dirs_right:", missing_dirs_right)
    
    missing_left = combine_and_add_path(missing_dirs_left, missing_files_left, path_left)
    missing_right = combine_and_add_path(missing_dirs_right, missing_files_right, path_right)
    
    return common, missing_left, missing_right

def search_dirs(path_left, path_right):
    common, missing_left, missing_right = compare_and_print(path_left, path_right)
    for elem in common:
        pl = os.path.join(path_left, elem)
        pr = os.path.join(path_right, elem)
        missing_left_tmp, missing_right_tmp = search_dirs(pr, pl)
        missing_left.extend(missing_left_tmp)
        missing_right.extend(missing_right_tmp)
    return missing_left, missing_right 
                
missing_left, missing_right  = search_dirs(path_left, path_right)

print("================missing left:================")
for elem in missing_left:
    print(elem)
print("================missing right:================")
for elem in missing_right:
    print(elem)
    
    
    
    
                
