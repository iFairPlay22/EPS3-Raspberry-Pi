import time


class DroneHealth():

    def __init__(self):
        self.launch_mission = False
        self.altitude = 100
        self.battery = 100
        self.start_timer = 0

    def launch(self):

        self.launch_mission = True
        self.start_timer = time.time()

    def increment_altitude(self):

        self.altitude += 1
        return self.altitude

    def decrement_battery(self):

        self.battery -= 1
        return self.battery

    def getStatus(self):
        # return 1 if mission successed, 2 if drone is charging and 3 if drone is flying
        if self.launch_mission:
            if time.time() - self.start_timer > 20:
                self.launch_mission = False
                return '1'
            elif time.time() - self.start_timer > 10:
                return '2'
            else:
                return '3'
        return '1'
