
import configparser as cfp

def load_config(filename="config.cfg"):
    config = cfp.ConfigParser()
    config.read(filename)
    return config
