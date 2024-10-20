from Object import *

class ObjectProvided(Object):
    def __init__(self, riddle, room, code):
        super().__init__(riddle, room, code)
    
    def setRiddle(self, riddle):
        super().setRiddle(riddle)