# Delivery Station CAD Files

import time

class CADDesign:

    def __init__(self, ds_id, drawing_file, designer, uploader, create_time = time.time()):
        self.ds_id = ds_id
        self.version_no = None
        self.drawing_file = drawing_file
        self.create_time = create_time
        self.designer = designer
        self.uploader = uploader
        self.no_shelving_units = 0
        self.no_conveyor_system = 0
    
    # set version no of the cad design
    def set_version_no(self, no):
        self.version_no = no

    def set_shelving_units(self, num):
        self.no_shelving_units = num
    
    def set_conveyor_units(self, num):
        self.no_conveyor_system = num
    

