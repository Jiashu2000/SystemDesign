# Delivery Station System

import DeliveryStation
import Project
from IPython.display import display, Image
import datetime
import pandas as pd

class DSSystem:

    def __init__(self) -> None:
        self.no_of_stations = 0
        self.ds_id= {}
        self.ds_by_region = {}
        self.no_of_projects = 0
        self.project_list = {}

    def get_no_stations(self):
        return self.no_of_stations
    
    def get_ds(self, id):
        return self.ds_id[id]
    
    def create_new_ds(self):
        addr = input("Please enter the address of the delivery station: ")
        new_ds_id = self.no_of_stations + 1
        new_ds = DeliveryStation.DeliveryStation(new_ds_id, address = addr)
        self.ds_id[new_ds_id] = new_ds
        self.no_of_stations += 1
        print("------- ------ ------- ------ ------- ------ ------- ------")
        print("A new delivery station has been created in the system.")
        print("The id of the new delivery station is: ", new_ds.id)
        print('The delivery station is located at: ', new_ds.get_address())
        return new_ds
    
    def create_ds_list(self):
        new_ds_id = self.no_of_stations + 1
        new_ds = DeliveryStation.DeliveryStation(new_ds_id)
        self.ds_id[new_ds_id] = new_ds
        self.no_of_stations += 1
        return new_ds

    def set_ds_cat(self, ds_id, cat):
        ds = self.ds_id[ds_id]
        new_design = ds.upload_new_design(cat, "emp1", "emp2")

    
    def update_ds_address_info(self):
        ds_id = int(input("Please enter the id of the delivery station that you want to update information for: "))
        old_address = self.get_ds(ds_id).get_address()
        new_address = input("Please enter the new address of the delivery station: ")
        self.get_ds(ds_id).set_address(new_address)
        print("------- ------ ------- ------ ------- ------ ------- ------")
        print("The old address of the ds station is: ", old_address)
        print("The new address of the ds station is: ", new_address)
        print("The address of delivery station", ds_id, "has been changed.")

    def get_ds_latest_design(self):
        ds_id = int(input("Please enter the id of the delivery station: "))
        ds = self.get_ds(ds_id)
        latest_design = ds.get_latest_design()
        if not latest_design:
            print("------- ------ ------- ------ ------- ------ ------- ------")
            print("No design file has been uploaded for the DS")
            return 

        print("------- ------ ------- ------ ------- ------ ------- ------")
        print("The latest design version of the DS is: ", latest_design.version_no)
        print("The latest design of the DS: ")
        im = Image(latest_design.drawing_file, width = 500, height = 500)
        display(im)

    def update_ds_latest_design(self):
        ds_id = int(input("Please enter the id of the delivery station: "))
        ds = self.get_ds(ds_id)
        new_design_input = input("Please upload the new design: ")
        designer = input("Please enter the name of the designer: ")
        uploader = input("Please enter the name of the uploader: ")
        new_design = ds.upload_new_design(new_design_input, designer, uploader)
        new_design_version_no = new_design.version_no

        print("------- ------ ------- ------ ------- ------ ------- ------")
        print("The latest design of the DS had been uploaded. ")
        print("The designer is: ", new_design.designer)
        print("The uploader is: ", new_design.uploader)
        print("The design was uploaded at: ", datetime.datetime.fromtimestamp(new_design.create_time).strftime('%Y-%m-%d %H:%M:%S'))
        print("The version no of the latest design is: ", new_design_version_no)
        print("The latest design of the DS is:" )
        im = Image(new_design.drawing_file, width = 500, height = 500)
        display(im)

    def get_ds_all_past_design(self):
        ds_id = int(input("Please enter the id of the delivery station: "))
        ds = self.get_ds(ds_id)
        past_design = ds.get_past_design()
        print("------- ------ ------- ------ ------- ------ ------- ------")
        print("Past Designs for DS ", ds_id, ": ")
        print("Design Version No\t\t Design Doc\t\t\t\t\t\t  Upload Time")
        for v_no in past_design.keys():
            d = past_design[v_no]
            print(v_no, '\t\t', d.drawing_file, '\t\t', datetime.datetime.fromtimestamp(d.create_time).strftime('%Y-%m-%d %H:%M:%S'))

    def get_ds_specific_past_design(self):
        ds_id = int(input("Please enter the id of the delivery station: "))
        ds = self.get_ds(ds_id)
        v_no = int(input("Please enter the design version no: "))
        past_design = ds.get_past_design()[v_no]
        print("------- ------ ------- ------ ------- ------ ------- ------")
        print("Design Version" + str(v_no) + "for DS ", str(ds_id), ": ")

        print("The designer is: ", past_design.designer)
        print("The uploader is: ", past_design.uploader)
        print("The design was uploaded at: ", datetime.datetime.fromtimestamp(past_design.create_time).strftime('%Y-%m-%d %H:%M:%S'))
        print("The design of the DS is:" )
        im = Image(past_design.drawing_file, width = 500, height = 500)
        display(im)

    def create_project(self):
        new_project_id = self.no_of_projects + 1
        name = input("Please enter the name of the project: ")
        ds_list_input = input("Please enter delivery station ids included in this project: ").strip()
        new_project = Project.Project(new_project_id, name)
        for i in ds_list_input.split(" "):
            ds_id = int(i)
            ds = self.ds_id[ds_id]
            new_project.add_ds(ds)
            ds.add_new_project(new_project)
        self.project_list[new_project_id] = new_project
        self.no_of_projects += 1
        print("------- ------ ------- ------ ------- ------ ------- ------")
        print("The new project, ", name, "has been created in the system.")
        print("The project id is ", new_project_id)
        print("DS included in the projects are:", new_project.get_ds_list())

    # get all active projects
    def get_active_project_list(self):
        active_list = []
        for project in self.project_list.values():
            if project.get_project_status() == 1:
                active_list.append(project)
        print("------- ------ ------- ------ ------- ------ ------- ------")
        print("Current Active Projects:")
        print("Project ID\t\t   Project Name")
        for p in active_list:
            print(p.project_id,'\t\t\t\t', p.name)

    # get active projects of a specific ds
    def get_ds_active_project_list(self):
        ds_id = int(input("Please enter the id of the delivery station: "))
        ds = self.ds_id[ds_id]
        active_list = ds.get_active_project_list()
        print("------- ------ ------- ------ ------- ------ ------- ------")
        print("Current Active Projects of DS ", ds_id, ":")
        print("Project ID\t\t   Project Name")
        for p in active_list:
            print(p.project_id,'\t\t\t\t', p.name)

    # update the project status
    def update_project_status(self):
        project_id = int(input("Please enter the id of the project: "))
        new_status_input = input("Please enter the new status of the project: ")
        if new_status_input == 'cancelled':
            new_status = 0
        project = self.project_list[project_id]
        project.update_project_status(new_status)
        print("------- ------ ------- ------ ------- ------ ------- ------")
        print("Project ", project_id, "status changed")
    

    def get_ds_key_metrics(self):
        ds_id = int(input("Please enter the id of the delivery station: "))
        ds = self.ds_id[ds_id]
        key_metrics = ds.get_key_metrics()
        print("------- ------ ------- ------ ------- ------ ------- ------")
        print("Key Metrics of DS ", ds_id, ":")
        for k, v in key_metrics.items():
            print(k, ": ", v)       


    def update_ds_key_metrics_from_csv(self, csv_file):
        metric_df = pd.read_csv(csv_file)
        metric_df.apply(lambda row: self.update_metric_helper(row), axis = 1)
        print("------- ------ ------- ------ ------- ------ ------- ------")
        print("Key metrics have been updated")
    
    def update_metric_helper(self, row): 
        ds_id = row["ds_id"]
        shelving_unit = row["no_shelving_units"]
        conveyor_unit = row['no_conveyor_system']
        ds = self.get_ds(ds_id)
        cad = ds.get_latest_design()
        cad.set_shelving_units(shelving_unit)
        cad.set_conveyor_units(conveyor_unit)
    
    


