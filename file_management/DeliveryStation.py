# Digital Twins Delivery Station

import CADDesign
import time
import RevisionEvent
import Project

class DeliveryStation:

    def __init__(self, id, latitude = None, longitude = None, address = None, city = None, state = None):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.city = city
        self.state = state
        self.cad_file_log = {}
        self.latest_cad = None
        self.latest_cad_version_no = 0
        self.revision_logs = {}
        self.last_revision_no = 0
        self.project_list = {}

    # get id of the delivery station
    def get_id(self):
        return self.id
    
    # get address of the delivery station
    def get_address(self):
        return self.address

    # get address of the delivery station
    def set_address(self, addr):
        self.address = addr

    # set location of the delivery station
    def set_location(self, long, lat):
        self.longitude = long
        self.latitude = lat
    
    # get the latest design of the delivery station
    def get_latest_design(self):
        if not self.latest_cad:
            return None
        return self.latest_cad
    
    # get historical design of the delivery station.
    # if no version number id is provided, return all historical design.
    def get_past_design(self, version_no = None):
        if version_no:
            return self.cad_file_log[version_no]
        return self.cad_file_log
    
    # upload a new cad design file
    def upload_new_design(self, new_design, designer, uploader, create_time = None, comments = None):
        # create a cad design instance
        if not create_time:
            create_time = time.time()
        new_cad = CADDesign.CADDesign(self.id, new_design, designer, uploader, create_time)

        # update cad version no
        new_cad_version_no = self.latest_cad_version_no + 1
        new_cad.set_version_no(new_cad_version_no)

        # create revision instance
        revision_time = time.time()
        revision = RevisionEvent.Revision(self.id, revision_time, new_design, uploader, comments)
        
        # update revision version no
        revision_no = self.last_revision_no + 1
        revision.set_revision_no(revision_no)
        
        self.update_design(new_cad, new_cad_version_no, revision, revision_no)
        return new_cad

    # update design
    def update_design(self, new_cad, new_cad_version_no, revision, revision_no):
        self.latest_cad = new_cad
        self.latest_cad_version_no = new_cad_version_no
        self.cad_file_log[new_cad_version_no] = new_cad

        self.last_revision_no = revision_no
        self.revision_logs[revision_no] = revision
    
    # get certain projects
    def get_project(self, project_no):
        return self.project_list[project_no]
    
    # get all projects
    def get_project_list(self):
        return self.project_list.keys()

    # get all active projects
    def get_active_project_list(self):
        active_list = []
        for project in self.project_list.values():
            if project.get_project_status() == 1:
                active_list.append(project)
        return active_list

    # add new projects to the delivery station
    def add_new_project(self, project: Project.Project):
        self.project_list[project.get_project_id()] = project

    # remove projects
    def remove_project(self, project_id):
        del self.project_list[project_id]

    # get key metrics
    def get_key_metrics(self):
        key_metrics = {}
        key_metrics["no_shelving_units"] = self.latest_cad.no_shelving_units
        key_metrics['no_conveyor_system'] = self.latest_cad.no_conveyor_system
        return key_metrics




