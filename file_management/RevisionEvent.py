## Delivery Station Revision

class Revision:

    def __init__(self, ds_id, revise_time, new_design, revisor, comments = None) -> None:
        self.ds_id = ds_id 
        self.revise_time = revise_time
        self.new_design = new_design
        self.revisor=  revisor
        self.comment = comments
        self.revision_no = None
    

    def set_revision_no(self, no):
        self.revision_no = no