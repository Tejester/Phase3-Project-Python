# These are the nodes of the graph


class Room:
    def __init__(self,room_id,name,contents=[]):
        # self.surr = surr
        # self.desc = desc
        self.room_id = room_id
        self.name = name
        self.contents = contents