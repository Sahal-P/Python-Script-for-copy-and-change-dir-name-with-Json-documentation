import os 
import json
import shutil
from subprocess import PIPE, run
import sys


GAME_DIR_PATTERN ="game"
GAME_CODE_EXTENSION =".go"
GAME_CODE_COMPILE = ["go","build"]

def find_all_game_paths(source):
    game_paths = []
    for root, dirs, files in os.walk(source):
        
        for directory in dirs:
           if GAME_DIR_PATTERN in directory.lower():
               path = os.path.join(source,directory)
               game_paths.append(path)
        
        break
    return game_paths

def get_name_from_paths(paths,to_strip):
    new_names =[]
    for path in paths :
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)
        
    return new_names


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        
def copy_and_overwrite(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(source,dest)
    
    
def make_json_metadata_file(path,game_dirs):
    data = {
        "gameNames": game_dirs,
        "numberOfGames":len(game_dirs)
        
    }
    
    with open(path,"w") as f:
        json.dump(data,f)
        

def compile_game_code(path):
    
    code_file_name = None
    
    for root, dirs, files in os.walk(path):
        for file in files:                              #       Another method
                                                        #    --------------------                         
            if file.endswith(GAME_CODE_EXTENSION):      #   if GAME_CODE_EXTENSION in file:                                                                                     
                code_file_name = file                   #      code_file_name = file
                break                                   #      break
        break
    if code_file_name is None:
        return
    
    command = GAME_CODE_COMPILE + [code_file_name]
    run_command(command, path)
    
    
def run_command(command,path):
    cwd = os.getcwd()
    os.chdir(path)
    
    result = run(command,stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print("code compiled >>>:",result)
    
    os.chdir(cwd)

def main(source,target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd , source) 
    target_path = os.path.join(cwd , target) 

    game_paths = find_all_game_paths(source_path)
    
    new_game_dir = get_name_from_paths(game_paths, "game" )
    print(new_game_dir)
    
    create_dir(target_path)
    
    for src, dest in zip(game_paths,new_game_dir):
        dest_path =  os.path.join(target_path, dest)
        copy_and_overwrite( src, dest_path)
        compile_game_code(dest_path)
    
    json_path = os.path.join(target_path,"metadta.json")
        
    make_json_metadata_file(json_path, new_game_dir)
        
    
  
if __name__ == "__main__":
    args = sys.argv
    if len(args) !=3:
        raise Exception("you must pass a source and target directory only--")
    
    source, target = args[1:] #dont want the file name - 1:
    
    main(source,target)