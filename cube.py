from numpy import ndarray
from numpy import linspace
class Cube:
    def __init__(self, x: float, y: float, z:float , side: float):
        self.vertex = [x, y, z]
        self.otherVertex = []
        self.side = side
        self.hasPoint = False
        for self.coord in self.vertex:
            self.otherVertex.append(self.coord + self.side)
    def printVertices(self):
        print(self.vertex)
        print(self.otherVertex)
    def IsPointInCube(self, x_ndarray: ndarray, y_ndarray: ndarray, z_ndarray: ndarray):
        for self.x, self.y, self.z in zip(x_ndarray, y_ndarray, z_ndarray):
            if(self.hasPoint == True):
               break
            if((self.vertex[0] <= self.x and self.x <= self.otherVertex[0]) and 
               (self.vertex[1] <= self.y and self.y <= self.otherVertex[1]) and 
               (self.vertex[2] <= self.z and self.z <= self.otherVertex[2])):
                self.hasPoint = True
        return self.hasPoint

if __name__ == "__main__":
    cube1 = Cube(1, 2, 3, 2)
    cube2 = Cube(1, 2, 1, 2)
    x = linspace(0, 10, 20)
    y = linspace(0, 10, 20)
    z = linspace(0, 10, 20)
    cube1Check = cube1.IsPointInCube(x, y, z)
    cube2Check = cube2.IsPointInCube(x, y, z)
    print(f"cube 1 has the point(s): {cube1Check}")
    print(f"cube 2 has the point(s): {cube2Check}")