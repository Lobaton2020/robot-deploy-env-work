from subprocess import Popen,PIPE,STDOUT
from multiprocessing.dummy import Pool as ThreadPool
from json import dumps
from datetime import datetime
from util.configparser import load_config
from manage_db.manage import Manage
from os.path import exists,basename
from os import mkdir

def run_process_server(config_data):
    try:
        config = dict(load_config())["CONFIGURATION"]
        folder_logs = config["FOLDER_LOGS"]
        filename,cmd = tuple(config_data.values())
        filename_log,filename_file = tuple(filename.split("|"))
        date = datetime.now().strftime("%Y%m%d")
        print("Running: {}".format(filename_log))
        process = Popen(args=cmd,stderr=STDOUT,stdout=PIPE,stdin=PIPE,shell=False)
        outs,errs = process.communicate()
        if not exists(folder_logs):
            mkdir(folder_logs)
        filename_file = basename(filename_file.format(date))
        with open("{}/{}".format(folder_logs,filename_file,date),"w+") as file:
            if errs:
                print("Error in {}: {}".format(filename_file,str(errs)))
            file.write(str(outs.decode("ascii")))
            file.close()
        print("Finish: {}".format(filename_log))
    except Exception as err:
        print("Error: {}".format(err))

def run(list_proccess,length ):
    pool = ThreadPool(length)
    pool.map(run_process_server,list_proccess)
    pool.close()

def deploy_server_dev():
    def makeDict(dict,path):
        return {
            "filename":dict["name"],
            "cmd":dict["cmd"].format(path)
        }
    config = dict(load_config())["CONFIGURATION"]
    manage = Manage()
    list_proccess = manage.registersActives(type_out=True,tablename="commands")
    list_proccess = [makeDict(item,config["PATH_CORECONFIG_DEV"]) for item in list_proccess]
    run(list_proccess,len(list_proccess))

