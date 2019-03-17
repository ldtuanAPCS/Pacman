class Food(object):
    def __init__(self, x, y):
        self.location = x, y

    def __repr__(self):
        st = "Food location: ", self.location[0], ", ", self.location[1] 
        return str(st)