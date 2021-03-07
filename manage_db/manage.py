from json import dumps, load
from util.configparser import load_config
class Manage:
    def __init__(self):
        config = dict(load_config())["CONFIGURATION"]
        self.path_db = config["PATH_DATABASE_JSON"]
        self.path_files_properties = ["PATH_DATABASE_JSON"]

    def openFile(self):
        try:
            with open(self.path_db,"r") as file:
                result, = tuple(load(file),)
                file.close()
                return result
        except Exception as err:
            print("## ERROR: {}".format(err))
            return False

    def saveFile(self,data):
        try:
            with open(self.path_db,"w") as file:
                file.write("[{}]".format(dumps(data),indent=4))
                file.close()
            return True
        except Exception as err:
            print("## ERROR: {}".format(err))
            return False

    def getByTable(self,tablename="properties"):
        tables = self.openFile()["tables"]
        for table in tables:
            if table["name"] == tablename:
                return table
        return False

    def addItemByTable(self,row,tablename="properties"):
        try:
            tables = self.openFile()
            for table in tables["tables"]:
                if table["name"] == tablename:
                    table["rows"].append(row)
            return self.saveFile(tables)
        except Exception as err:
            print("## ERROR: {}".format(err))
            return False


    def changeStatus(self,row_id,tablename="properties"):
        try:
            tables = self.openFile()
            for table in tables["tables"]:
                if table["name"] == tablename:
                    for row in table["rows"]:
                        if row["id"] == row_id:
                            if row["is_active"] in ['True','true']:
                                row["is_active"] = 'False'
                            else:
                                row["is_active"] = 'True'
            return self.saveFile(tables)
        except Exception as err:
            print("## ERROR: {}".format(err))
            return False

    def deleteRegister(self,row_id,tablename="properties"):
        try:
            tables = self.openFile()
            new_tables = []
            for table in tables["tables"]:
                if table["name"] == tablename:
                    for row in table["rows"]:
                        if row["id"] != row_id:
                            new_tables.append(row)
            for table in tables["tables"]:
                if table["name"] == tablename:
                    table["rows"] = new_tables
            return self.saveFile(tables)
        except Exception as err:
            print("## ERROR: {}".format(err))
            return False

    def registersActives(self,type_out="all",tablename="properties"):
        try:
            tables = self.openFile()
            new_tables = []
            for table in tables["tables"]:
                if table["name"] == tablename:
                    for row in table["rows"]:
                        if type_out == "all":
                            new_tables.append(row)
                            continue
                        if type_out:
                            if row["is_active"] in ['True','true']:
                                new_tables.append(row)
                        else:
                            if row["is_active"] in ['False','false']:
                                new_tables.append(row)
            return new_tables[::-1]
        except Exception as err:
            print("## ERROR: {}".format(err))
            return False