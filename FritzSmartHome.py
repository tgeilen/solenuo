from FHAHandler import FHAHandler
from DBHandler import DBHandler
from webSolarHandler import  WebSolarHandler
import time


class FritzSmartHome:    

    def __init__(self):
        
        self.db = DBHandler()
        
        username, password = self.db.getAccount("FritzBox")
        self.fhh = FHAHandler(username, password)
        username, password = self.db.getAccount("webSolar")
        self.pv = WebSolarHandler(username, password) 

       
        self.db.updateSavedDevices(self.fhh.getFHA().get_switch_list())

    

        
    
    def trackPVData(self):
        
        output = self.pv.getCurrentPowerOutput()
        usage = self.pv.getCurrentPowerUsage()
        gridPower = self.pv.getCurrentGridInput()
        self.db.addPvData(output,usage,gridPower)

    def getPVStats(self):

        output = self.pv.getCurrentPowerOutput()
        usage = self.pv.getCurrentPowerUsage()
        gridInput = self.pv.getCurrentGridInput()
        self.db.addPvData(output, usage, gridInput)

        return (output, usage, gridInput)

    
    def getSwitchList(self):
         
        return self.fhh.getDevices()

    def getSwitchesInfo(self):
         
        dict = {}
        for device in self.fhh.getDevices():
            dict[device] = self.fhh.getFHA().get_state(device)

        return dict

    def getDashboardInfo(self):
         
        dict = {}
        for device in self.fhh.getDevices():
            deviceDict = {}
            data = self.fhh.getFHA().get_state(device)
            try:
            
                deviceDict["name"]= data["name"]
                deviceDict["powerState"] = data["state"]
                deviceDict["powerOutput"] = data["power"]
                deviceDict["threshold"] = self.db.getThreshold(device)
                deviceDict["automationState"] = self.db.getAutomationState(device)
                dict[device] = deviceDict
            except:
                ##his is only the case if a device is currently not connected to the FirtzBox
                continue
    

        return dict
       
        


    def checkSwitches(self):
        

        output, usage, grid = self.getPVStats()
        delta = output - usage
        

        devices = self.db.getSavedDeviceInformation()  
        for info in devices:
            key = info[0]
            threshold = info[2]

            powerState = self.fhh.getState(key)
            self.db.updatePowerState(key, powerState)

            automationState = info[4]==1
            if(automationState):
                if(delta>0):
                    if(delta>threshold and not powerState):
                        self.fhh.changeState(key, "on")
                        self.db.trackStateChange(key, "on")
                        print(info[1] + " turned on")
                        break
                else:
                    if(threshold>delta and powerState):
                        self.fhh.changeState(key, "off")
                        self.db.trackStateChange(key, "off")
                        print(info[1] + " turned off")
                        break

    def automate(self):
        while(True):
            try:
                updateTime = 5
                if(self.db.getAutomation()==1):
                    updateTime = self.db.getUpdateTime()
                    self.checkSwitches()
                time.sleep(updateTime)
                
            except Exception as e:
                print("something failed, when checking the switches")
                print (e)
                print("trying to restart")
                self.pv.close()
                break
        

if __name__ == "__main__":
    while(True):
        fsh = FritzSmartHome()
        print("Setup complete")
        fsh.automate()


