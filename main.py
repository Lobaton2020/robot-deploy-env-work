from flask import Flask,render_template,make_response,redirect,request
from process.process_selenium import automatic_params
from process.deploy_server import deploy_server_dev
from process.deploy_service_npm import run_process_server_start
from util.configparser import load_config
from manage_db.manage import Manage
import time
from os import listdir
from json import dumps,load
from flask_cors import CORS

app = Flask(__name__,template_folder="templates",static_folder="static")

CORS(app)

@app.route('/')
def hello_world():
    manage = Manage()
    result = {
        "result" : None,
        "data" : manage.registersActives()
    }
    return render_template("auth/index.html",**result)

# ajax
@app.route("/insert_properties_zuul")
def insert_properties_zuul():
    try:
        automatic_params()
        return dumps({
            "status":200,
            "message":"Desplegando automatizacion de selenium e insecion de propiedades"
        })
    except Exception as err:
        return dumps({
            "status":500,
            "message":"Error al usar selenium",
            "error": err
        })

@app.route("/deploy_server_eureka")
def deploy_server_eureka():
    try:
        deploy_server_dev()
        return dumps({
            "status":200,
            "message":"Desplegando eureka y zuul"
        })
    except:
        return dumps({
            "status":500,
            "message":"Error al procesar los datos"
        })
#end

@app.route("/table/add",methods=["POST"])
def add_property():
    manage = Manage()
    manage.addItemByTable({
        "id":time.time(),
        "name": request.form["name"],
        "is_active":"True"
    })
    return make_response(redirect("/"))

@app.route("/table/edit/<float:id>")
def edit_status(id):
    manage = Manage()
    manage.changeStatus(row_id=id)
    return make_response(redirect("/"))


@app.route("/table/delete/<float:id>")
def delete_register(id):
    manage = Manage()
    manage.deleteRegister(row_id=id)
    return make_response(redirect("/"))

@app.route("/logs/services")
def log_services():
    data = []
    path_logs = "D:/soyyo/python-automatic/logs_system/"
    dirs = listdir(path_logs)
    for filename in list(dirs):
        try:
            with open(path_logs+filename,"r") as file:
                data.append({
                    "filename":filename,
                    "content":file.read()
                })
                file.close()
        except:
            print("Error")
    result = {
        "data":data
    }
    return render_template("auth/renderLogs.html",**result)

@app.route("/services")
def manager_services():
    path_services = "D:/production-apps/robot-deploy-env-work/static/data/data_services.json"
    result = {
        "data":load(open(path_services))
    }
    return render_template("auth/renderServices.html",**result)

@app.route("/services/run/")
def run_service():

    path_service = request.args.get("id")
    try:
        run_process_server_start({
        "path_service": path_service,
        "folder_logs": "D:/soyyo/python-automatic/logs_system/"
    },)
        return dumps({
            "status":200,
            "message":"Servicio {} deplegado correctamente".format(path_service)
        })
    except:
        return dumps({
            "status":500,
            "message":"Error al correr el servicio: {}".format(path_service)
        })

if __name__ == "__main__":
    app_config = dict(load_config())["APP"]
    app.run(
        host=app_config["HOST"],
        port=app_config["PORT"],
        debug=app_config["DEBUG"]
    )