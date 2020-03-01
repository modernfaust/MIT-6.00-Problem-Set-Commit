#Problem Set 9
#Creating an inheritance hierarchy of geometric shapes as an exercise in OOP design

file = "shapes.txt"

from string import *

class Shape(object):
    def area(self):
        raise AttributeException("Subclasses should override this method.")

class Square(Shape):
    def __init__(self, h):
        """
        h: length of side of the square
        """
        self.side = float(h)
    def area(self):
        """
        Returns area of the square
        """
        return self.side**2
    def __str__(self):
        return 'Square with side ' + str(self.side)
    def __eq__(self, other):
        """
        Two squares are equal if they have the same dimension.
        other: object to check for equality
        """
        return type(other) == Square and self.side == other.side

class Circle(Shape):
    def __init__(self, radius):
        """
        radius: radius of the circle
        """
        self.radius = float(radius)
    def area(self):
        """
        Returns approximate area of the circle
        """
        return 3.14159*(self.radius**2)
    def __str__(self):
        return 'Circle with radius ' + str(self.radius)
    def __eq__(self, other):
        """
        Two circles are equal if they have the same radius.
        other: object to check for equality
        """
        return type(other) == Circle and self.radius == other.radius
#
# Problem 1: Create the Triangle class
#
#Implement the `Triangle` class, which also extends `Shape`.
class Triangle(Shape):
    def __init__(self, base,height):
        """
		b: length of the bottom of the triangle
        h: length of the height of the triangle
        """
        self.base = float(base)
        self.height = float(height)
    def area(self):
        """
        Returns area of the triangle
        """
        return (self.base * self.height)/2
    def __str__(self):
        return 'Triangle with base ' + str(self.base) + ' and height ' + str(self.height)
    def __eq__(self, other):
        """
        Two triangles are equal if they have the same base and height
        other: object to check for equality
        """
        return type(other) == Triangle and self.base == other.base and self.height == other.height
#
# Problem 2: Create the ShapeSet class
#
#Fill in the following code skeleton according to the
##    specifications.

# Add shape:

# Prompt: Which shape to add?
# Get input: triangle, square or circle
# Get input: add dimensions to shape. If shape dimensions == previous (using cmp), then abort
# create instance of class "shape"
# with shapeid

class ShapeSet:
    def __init__(self):
        """
        Initialize any needed variables
        """
        #self.load = str(load)
        #self.side = float(h)
        #self.base = float(base)
        #self.height = float(height)
        #self.radius = float(radius)		
        self.store = {}
        self.circlelist = []
        self.squarelist = []
        self.trianglelist = []
        self.shapeid = 1
        self.place = 1
    def addShape(self, sh):
        """
        Add shape sh to the set; no two shapes in the set may be
        identical
        sh: shape to be added
        """
        self.shapeid = self.place #to assign a shapeid to each shape
        
        for key in self.store:
            if sh.__eq__(self.store[key]):
                print("A", sh.__str__(),"exists already!")
                return 0

        if isinstance(sh,Triangle): #assign shapeid to triangle and store in dict
            self.store[self.shapeid] = sh
            self.trianglelist.append(sh.__str__())
            print(sh.__str__(),"stored!")
            self.next()
        if isinstance(sh,Circle): #assign shapeid to Circle and store in dict
            self.store[self.shapeid] = sh
            self.circlelist.append(sh.__str__())
            print(sh.__str__(),"stored!")
            self.next()
        if isinstance(sh,Square): #assign shapeid to triangle and store in dict
            self.store[self.shapeid] = sh
            self.squarelist.append(sh.__str__())
            print(sh.__str__(),"stored!")
            self.next()

    def __iter__(self):
        """
        Return an iterator that allows you to iterate over the set of
        shapes, one shape at a time
        """
        self.place = 0
        return self
    def next(self):
        x = self.place
        self.place +=1
        return x
    def __str__(self):
        """
        Return the string representation for a set, which consists of
        the string representation of each shape, categorized by type
        (circles, then squares, then triangles)
        """
        ## TO DO
        
        #for key in self.store:
        #    if isinstance(self.store[key],Circle):
        #        self.printlist.append(self.store[key].__str__())
        #    if isinstance(self.store[key],Square):
        #        self.printlist.append(self.store[key].__str__())
        #    if isinstance(self.store[key],Triangle):
        #        self.printlist.append(self.store[key].__str__())
        return print(self.circlelist,self.squarelist,self.trianglelist)
#
# Problem 3: Find the largest shapes in a ShapeSet
#
def findLargest(shapes):
    """
    Returns a tuple containing the elements of ShapeSet with the
       largest area.
    shapes: ShapeSet
    """
    ## TO DO #need to find out how to sort a list
    arealist = []
    sortedlist = []
    shape, area = 0,1
    largest = 0
    largestlist = []
    for key in shapes.store: #to create the arealist 
        arealist.append((shapes.store[key],shapes.store[key].area()))
    n = len(arealist)
    for k in range (n):
        for j in range (0,n-k-1):
            if arealist[j][area] > arealist[j+1][area]:
                 arealist[j] , arealist[j+1] = arealist[j+1],arealist[j]
    largest = arealist[-1]
    try:
        for i in range (0, n):
            if arealist[i][area] == largest[area]:
                largestlist.append(arealist[i])
        print ("The largest shapes are:", largestlist)
    except:
        print("The largest shape is:", largest)
    #for e in arealist: #to sort the arealist from largest to smallest
    #    if arealist[e][area] > arealist[e-1][area]:
            
    
#
# Problem 4: Read shapes from a file into a ShapeSet
#
def readShapesFromFile(filename):
    """
    Retrieves shape information from the given file.
    Creates and returns a ShapeSet with the shapes found.
    filename: string
    """
#h,base,height,radius,store,temp
    p2 = ShapeSet()
    inputFile = open(filename)
    for line in inputFile:
        sub_list = line.split(",")
        shape_name = sub_list[0]
        if shape_name == "triangle":
            p2.addShape(Triangle(sub_list[1],sub_list[2]))
        if shape_name == "circle":
            p2.addShape(Circle(sub_list[1]))
        if shape_name == "square":
            p2.addShape(Square(sub_list[1]))


h = 5
base = 3
height = 10
radius = 6
store = {}
temp = {}
#Shapes = readShapesfromfile("shapes.txt")
p1 = ShapeSet()
p1.addShape(Triangle(1.2,2.25))
p1.addShape(Triangle(1.2,2.25))
p1.addShape(Triangle(50,100))
p1.addShape(Circle(5))
p1.addShape(Circle(8))
p1.addShape(Square(50))
p1.__str__()
findLargest(p1)
readShapesFromFile(file)
