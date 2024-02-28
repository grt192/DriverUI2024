import cv2
import requests

visionURL = "http://10.1.92.19:1186/stream.mjpg"
visionTestURL = "http://10.1.92.19:1186"
camURl = "http://10.1.92.2:1181/stream.mjpg"
camTestURL = "http://10.1.92.2:1181"


def checkVision(self):
    try:
        response = requests.get(self.visionTestURL, timeout=1)
        if response.status_code != 200:
            print("Vision not accessable! Status Code: " + str(response.status_code))
            return False
        response.close()
    except Exception as e:
        print("Check Vision exception in the")
        print(e)
    return True

def checkDriver(self):
    try:
        response = requests.get(self.camTestURL, timeout=1)
        if response.status_code != 200:
            print("Driver cam not accessable! Status Code: " + str(response.status_code))
            return False
        response.close()
    except Exception as e:
        print("Check Driver exception in the following line:")
        print(e)
    return True

 def reconnect(self):
        try:
            if not self.checkNetwork():
                return
        except Exception as e:
            print(e)
            return
        if self.checkDriver():
            self.setDriverCap()
            self.timer.start(1)
        if self.checkVision():
            self.setVisionCap()
            self.vtimer.start(1)
        else:
           print("Network Issue!")