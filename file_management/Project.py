# Delivery Station Project


class Project:

    def __init__(self, id,name = None, manager = None):
        self.project_id = id
        self.status = 1
        self.manager = manager
        self.name = name
        self.ds_list = set()
    
    def get_project_status(self):
        return self.status

    def get_project_id(self):
        return self.project_id

    def get_manager(self):
        return self.manager

    def get_ds_list(self):
        ds_id_list = []
        for ds in self.ds_list:
            ds_id_list.append(ds.id)
        return ds_id_list
    
    def update_project_status(self, new_status):
        self.status = new_status
        if self.status == 0:
            for ds in self.ds_list:
                ds.remove_project(self.project_id)
    
    def set_manager(self, m):
        self.manager = m
    
    def add_ds(self, ds):
        self.ds_list.add(ds)

