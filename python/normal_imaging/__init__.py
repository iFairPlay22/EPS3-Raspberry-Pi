import os
import subprocess
from datetime import datetime
from PIL import Image

class NormalCamera():

    def __init__(self, tmp_folder) -> None:
        self.tmp_folder = tmp_folder
        
    def get(self):
        
        # File path
        date_time_string = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')
        full_path = os.path.join(self.tmp_folder, date_time_string + ".jpeg")
         
        # Save image
        os.system(f"libcamera-jpeg -o ${full_path}")
        exit()
        
        output = subprocess.check_output("ls", shell=True)
        print(output)
        exit()

        # Get image array
        image = Image.open(full_path).convert('L')
        image_array = [ [ image.getpixel((r,c)) for c in range(image.size[1]) ] for r in range(image.size[0]) ]

        # Delete image
        if os.path.exists(full_path):
            os.remove(full_path)
        
        return image_array