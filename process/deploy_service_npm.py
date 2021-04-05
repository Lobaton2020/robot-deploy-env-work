from subprocess import Popen,PIPE,STDOUT,run,check_call
from os import listdir,chdir,path
from multiprocessing.dummy import Pool as ThreadPool
from time import sleep,strftime
import json
import ctypes, sys
def print_ok(json_data):
    print(json.dumps(json_data,indent=4))

def open_file(path):
    try:
        with open(path,"r") as file:
            return file.read().split("\n")
    except Exception as err:
        print(err)
        return False
def write_file(path,text):
    try:
        with open(path,"w+") as file:
            file.write(text)
            return True
    except Exception as err:
        print(err)
        return False

def select_correct_folders(folders_in,prefix,special_repository):
    folders = []
    for name in folders_in:
        if (name.startswith(prefix) and name not in special_repository):
            folders.append(name)
    return folders


def add_common_service(list_in,special_repository):
    list_repo = special_repository
    list_data = list_in
    list_data.append(list_repo+"/00.es_user")
    list_data.append(list_repo+"/01.es_entity")
    list_data.append(list_repo+"/03.ms_get_frequently_asked_questions"),
    list_data.append(list_repo+"/03.ms_get_terms_of_use"),
    return list_data


def make_path_service(directory_repos,dir_path,special_repository):
    list_dir_path_in = ""
    if special_repository in dir_path:
        list_dir_path_in = directory_repos+dir_path
    else:
        list_dir_path_in = map(lambda name : name if name.startswith('0') else  False,listdir(directory_repos+dir_path))
        list_dir_path_in = directory_repos +dir_path+"/" +getString(list_dir_path_in)
    return list_dir_path_in


def run_process_server_start(result):
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    try:
        dir_path,folder_logs = tuple(result.values())
        today =  strftime("%y%m%d")
        file_logs = "{}{}_{}.log".format(folder_logs,dir_path.split("/")[-1],today)
        print("Running service {} ...".format(dir_path.split("/")[-1]))
        cmd ="D: && cd {} && npm start".format(dir_path)
        process = Popen(args=cmd,stderr=STDOUT,stdout=PIPE,stdin=PIPE,shell=False)
        outs,errs = process.communicate()
        with open(file_logs,"w+") as file:
            if errs:
                print("Error in {}: {}".format(file_logs,str(errs)))
            file.write(outs.decode("ascii"))
            file.close()
    except Exception as err:
        print(err)
