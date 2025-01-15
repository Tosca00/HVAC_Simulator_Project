from .roomGeometry import Room

def createRoom(height, width, length):
    room = Room()
    room.height = height
    room.width = width
    room.length = length
    return room

def CalculateVolume(room):
    return room.heigth * room.width * room.length


#per il momento la perdita di temperatura è costante
def loseTemp():
    import random
    return abs(random.gauss(0.005, 0.1))