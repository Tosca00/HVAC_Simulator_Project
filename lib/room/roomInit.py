from .roomGeometry import Room

def createRoom(height, width, length):
    room = Room()
    room.height = height
    room.width = width
    room.length = length
    return room

def CalculateVolume(room):
    return room.heigth * room.width * room.length