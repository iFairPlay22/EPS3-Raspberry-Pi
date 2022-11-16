import RPi.GPIO as GPIO
import time

class DistanceDetector:
    
    def __init__(self):
        
        # TODO: Change the GPIOs
        self.__detectors = {
            "top":    DistanceSensor(GPIO_Trigger=18, GPIO_Echo=24),
            "bottom": DistanceSensor(GPIO_Trigger=18, GPIO_Echo=24),
            "front":  DistanceSensor(GPIO_Trigger=18, GPIO_Echo=24),
            "back":   DistanceSensor(GPIO_Trigger=18, GPIO_Echo=24),
            "right":  DistanceSensor(GPIO_Trigger=18, GPIO_Echo=24),
            "left":   DistanceSensor(GPIO_Trigger=18, GPIO_Echo=24)
        }
        
    def get(self):     
        return { direction: detector.get_distance() for direction, detector in self.__detectors }
            
    def __del__(self):
        GPIO.cleanup()

class DistanceSensor:
    
    def __init__(self, GPIO_Trigger: int, GPIO_Echo: int):
        
        # set GPIO Pins
        self.__GPIO_TRIGGER = GPIO_Trigger
        self.__GPIO_ECHO    = GPIO_Echo
        
        # Time to wait before changing trigger (0.01 ms)
        self.__DETECTION_TIME = 0.01
        
        # sonic speed (34300 cm/s)
        self.__SONIC_SPEED = 34300
        
        # Init ports
        self.__init_GPIOs()
     
    def __init_GPIOs(self): 
        
        # GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
    
        # Set GPIO direction (IN / OUT)
        GPIO.setup(self.__GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.__GPIO_ECHO,    GPIO.IN)
        
        # Desactivate detection
        GPIO.output(self.__GPIO_TRIGGER, False)
            
    def get_distance(self):
        
        # Activate detection
        GPIO.output(self.__GPIO_TRIGGER, True)
    
        # Wait
        time.sleep(self.__DETECTION_TIME * 0.001)
        
        # Desactivate detection
        GPIO.output(self.__GPIO_TRIGGER, False)
    
        start_time = time.time()
        stop_time  = time.time()
    
        # save time of departure
        while GPIO.input(self.__GPIO_ECHO) == 0:
            start_time = time.time()
    
        # save time of arrival
        while GPIO.input(self.__GPIO_ECHO) == 1:
            stop_time = time.time()
    
        # time difference between departure and arrival
        time_elapsed = stop_time - start_time
        
        # distance detected 
        distance = (time_elapsed * self.__SONIC_SPEED) / 2
        
        return distance
        
if __name__ == '__main__':
    
    obstacle_detector = DistanceDetector()
    
    while True:
        distances = obstacle_detector.get()        
        print("Distances in cm: " + str(distances))
        time.sleep(1)