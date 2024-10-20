# Object class to track objects
from abc import ABC, abstractmethod

class Object:
    __riddle = None
    __room = None
    __code = None

    def __init__(self, riddle, room, code):
        self.__riddle = riddle
        self.__room = room
        self.__code = code

    # Getters and Setters
    def getRiddle(self):
        return self.__riddle
    
    @abstractmethod
    def setRiddle(self, riddle):
        self.__riddle = riddle

    def getRoom(self):
        return self.__room
    
    def setRoom(self, room):
        self.__room = room

    def getCode(self):
        return self.__code
    
    def setCode(self, code):
        self.__code = code

    def __str__(self):
        return f"('{self.__riddle}', '{self.__room}', '{self.__code})"