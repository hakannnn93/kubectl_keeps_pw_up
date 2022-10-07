from concurrent.futures import thread
import json
from ntpath import join
import os
import socket
from threading import Thread
import threading
from time import sleep
import signal
import sys

class KeepOpenPw:

    def __init__(self) -> None:
        self.f = open("pw_config.json")
        self.jsonObjectArray = json.load(self.f)
        self.commandForPw = "kubectl port-forward "
        self.flagForNameSpace = "-n "
        self.connectionArray = dict()
        self.url = "127.0.0.1"
    
    def run_pw_for_json(self):
        for jsonObject in self.jsonObjectArray:            
            self.open_pw_for_object(jsonObject)
        
    def open_pw_for_object(self,jsonObject):
            if (jsonObject["do_pw"] == True):
                print(jsonObject["configName"])
                scmd = self.make_pw_command(jsonObject)
                self.run_cmd_thread(scmd)
                sleep(1)
                self.connectionArray[self.url+str(jsonObject["pw_to_port"])] = True        
    
    def make_pw_command(self,jsonObject):
            scmd = self.commandForPw \
                    + jsonObject["name"] + " "\
                    + str(jsonObject["pw_to_port"]) + ":" + str(jsonObject["cloud_port"]) + " " \
                    + self.flagForNameSpace + jsonObject["namespace"]
            return scmd

    def run_cmd_thread(self,scmd):
        thread = Thread(target=self.start_pw, args=(scmd,))
        thread.start()

    def start_pw(self,scmd):
        while(1):
            try:
                ret = os.system(scmd)
                print("Im done!! + "  + str(ret))
                if(ret != 0):
                    break
            except KeyboardInterrupt:
                print("xxx KeyboardInterrupt ")
                sys.exit(0)

def main():
    a = KeepOpenPw()
    a.run_pw_for_json()

if __name__ == "__main__":
    main()