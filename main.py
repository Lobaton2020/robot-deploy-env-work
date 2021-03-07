from flask import Flask,render_template,make_response,redirect,request
from process.process_selenium import automatic_params
from process.deploy_server import deploy_server_dev
from util.configparser import load_config
from manage_db.manage import Manage
import time
from json import dumps
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


if __name__ == "__main__":
    app_config = dict(load_config())["APP"]
    app.run(
        host=app_config["HOST"],
        port=app_config["PORT"],
        debug=app_config["DEBUG"]
    )