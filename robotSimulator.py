# Problem Set 11
# Random walk simulation of a fleet of cleaning robots with visual plots
#


import math
import random
import ps11_visualize
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).

        x: a real number indicating the x-coordinate
        y: a real number indicating the y-coordinate
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: integer representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)


# === Problems 1 and 2

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.x = random.randint(1,(self.width))
        self.y = random.randint(1,(self.height))
        self.clean = False
        self.room_grid = {}

        #first thing I did: created a cartesian grid and tagged all fields as unclean. When cleaning a tile, would tag as clean. Pre-fill before tagging as clean.
        #second try, upon looking at solutions: create an empty container, fill it with tiles that have been cleaned. 
        #final: create a grid and have each position flagged unclean (False).

        try:
            for m in range(width):
                for n in range (height):
                    self.room_grid[(m,n)] = self.clean
        except:
            print("Width and Height must be integers greater than 0.")

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """

        current_position=(int(pos.getX()),int(pos.getY()))
        self.room_grid[current_position] = True

        #first try: set position in pre-filled container as True to indicate cleanliness. 
        #second try, upon solutions: fill empty container with positions, mark as clean. 
        #final: set position in pre_filled container to True for clean.

        #mark the current grid on pos(x,y) as clean (True)
        
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """

        #tile = (int(m),int(n))
        #if tile in self.room_grid:
        #    return True
        #return False

        #first try: returned T or F depending on cleanliness of tile in grid
        #second try, upon solutions: check if tile in container. Return T if yes. This works because ps11_visualize.RobotVisualization.update() references this function,
        #before the container has stored any elements, thus raising an error. 
        #final: use "try" to locate clean tile. If (m,n) are out of scope of container, return False.

        try:
            if self.room_grid[(m,n)] == True:
                return self.room_grid[(m,n)]
        except:
            return False

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width*self.height
    
    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """

        is_cleaned=list(self.room_grid.values())
        return is_cleaned.count(True)
        #return len(self.room_grid)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        # TODO: Your code goes here
        self.x = random.randint(1,(self.width))
        self.y = random.randint(1,(self.height))
        return Position(self.x,self.y)
          
    def isPositionInRoom(self, pos):
        """
        Return True if POS is inside the room.

        pos: a Position object.
        returns: True if POS is in the room, False otherwise.
        """
        pos.getX()
        pos.getY()

        if pos.getX() <= self.width and pos.getX() >= 0:
            if pos.getY() <= self.height and pos.getY() >= 0:
                return True
        return False

    
class BaseRobot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in
    the room.  The robot also has a fixed speed.

    Subclasses of BaseRobot should provide movement strategies by
    implementing updatePositionAndClean(), which simulates a single
    time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified
        room. The robot initially has a random direction d and a
        random position p in the room.

        The direction d is an integer satisfying 0 <= d < 360; it
        specifies an angle in degrees.

        p is a Position object giving the robot's position.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.d = random.randint(0,360)
        self.p = self.room.getRandomPosition()
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        
        return self.p
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.d
        
    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.p = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.d = direction

class Robot(BaseRobot):
    """
    A Robot is a BaseRobot with the standard movement strategy.

    At each time-step, a Robot attempts to move in its current
    direction; when it hits a wall, it chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
    
        current_pos = self.getRobotPosition()
        new_pos = current_pos.getNewPosition(self.getRobotDirection(),self.speed)
        if self.room.isPositionInRoom(new_pos) == True:
            self.setRobotPosition(new_pos)
            self.room.cleanTileAtPosition(self.getRobotPosition())
        else:
            self.setRobotDirection(random.randint(0,360))

        #self.updatePositionAndClean()

        #self.setRobotPosition(self.room.getRandomPosition()) #don't know if this is necessary

        #what this will do is pick a new position based on d and speed. Check if position is valid and unclean -- then execute.
        #should the new position not be in the room or is unclean, set a random direction. 

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize):
    """
    Runs NUM_TRIALS trials of the simulation and returns a list of
    lists, one per trial. The list for a trial has an element for each
    timestep of that trial, the value of which is the percentage of
    the room that is clean after that timestep. Each trial stops when
    MIN_COVERAGE of the room is clean.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE,
    each with speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    Visualization is turned on when boolean VISUALIZE is set to True.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    visualize: a boolean (True to turn on visualization)
    """
    list_of_lists = []
    trial_list = []
    
    #initiate the trials
    for trials in range(num_trials):
        trial_list = []
        robot_list = []
        if visualize:
            anim = ps11_visualize.RobotVisualization(num_robots, width, height,0.2)
        covered = 0.
        calls = 0
        #initialize room for testing, for each trial
        test_room = RectangularRoom(width,height) 

        #create list of robots for each trial
        for robots in range(num_robots):
            robot_list.append(robot_type(test_room,speed))

        #execute trial, end when coverage exceeds minimum coverage
        while covered < min_coverage:
            if visualize:
                anim.update(test_room, robot_list) 
            for robot in robot_list:
                robot.updatePositionAndClean()
            total = test_room.getNumTiles()
            cleaned = test_room.getNumCleanedTiles()
            covered = (cleaned/total)
            trial_list.append(covered)
            calls+=1
        if visualize:
            anim.done()
        list_of_lists.append(trial_list)
        print("Trial",trials+1,"took",calls,"time steps.")
    return list_of_lists
        
# === Provided function
def computeMeans(list_of_lists):
    """
    Returns a list as long as the longest list in LIST_OF_LISTS, where
    the value at index i is the average of the values at index i in
    all of LIST_OF_LISTS' lists.

    Lists shorter than the longest list are padded with their final
    value to be the same length.
    """
    # Find length of longest list
    longest = 0
    for lst in list_of_lists:
        if len(lst) > longest:
           longest = len(lst)
    # Get totals
    tots = [0]*(longest)
    for lst in list_of_lists:
        for i in range(longest):
            if i < len(lst):
                tots[i] += lst[i]
            else:
                tots[i] += lst[-1]
    # Convert tots to an array to make averaging across each index easier
    tots = pylab.array(tots)
    # Compute means
    means = tots/float(len(list_of_lists))
    return means

# === Problem 4
def average_length(list_of_lists):
    """
    Computes the average length of the lists within list_of_lists.
    """
    total=0
    for lists in list_of_lists:
        total+=len(lists)
    return float(total/len(list_of_lists))

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on room size.
    """
    x_axis = []
    y_axis = []
    X,Y = 0,1
    room_sizes = [(5,5),(10,10),(15,15),(20,20),(25,25)]
    num_robots = 1
    num_trials = len(room_sizes)
    for size in room_sizes:
        list_of_lists = []
        list_of_lists=runSimulation(num_robots, 1.0, size[X], size[Y], 0.75, num_trials, Robot, False)
        y_axis.append(average_length(list_of_lists))
        x_axis.append(size[X]*size[Y])
    print(x_axis)
    plt.plot(x_axis,y_axis,'-g')
    plt.axis([0,max(x_axis)+(max(x_axis)/4),0,max(y_axis)+(max(y_axis)/4)])
    plt.xlabel("Room Area")
    plt.ylabel("Average Number of Timesteps")
    plt.title("Average cleaning time for 1 robot and various room sizes")
    plt.show()
def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    x_axis = []
    y_axis = []
    X,Y = 0,1
    room_sizes = (25,25)
    num_robots = [1,2,3,4,5,6,7,8,9,10]
    num_trials = 10
    for num in num_robots:
        list_of_lists = []
        list_of_lists=runSimulation(num, 1.0, room_sizes[X], room_sizes[Y], 0.75, num_trials, Robot, False)
        y_axis.append(average_length(list_of_lists))
        x_axis = num_robots
    print(y_axis)
    plt.plot(x_axis,y_axis,'-g')
    plt.axis([0,(max(x_axis)+(max(x_axis)/4)),0,max(y_axis)+(max(y_axis)/4)])
    plt.xlabel("Number of Robots")
    plt.ylabel("Average Number of Timesteps")
    plt.title("Average cleaning time for various robot quantities")
    plt.show()
def showPlot3():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    x_axis = []
    y_axis = []
    X,Y = 0,1
    room_sizes = [(20,20),(25,16),(40,10),(50,8),(80,5),(100,4)]
    num_robots = 2
    num_trials = 5
    for shape in room_sizes:
        list_of_lists = []
        list_of_lists=runSimulation(num_robots, 1.0, shape[X], shape[Y], 0.8, num_trials, Robot, False)
        y_axis.append(average_length(list_of_lists))
        x_axis.append(shape)
    print(y_axis)
    plt.scatter(x_axis,y_axis)
    plt.axis([0,(len(x_axis)+len(x_axis)/4),0,max(y_axis)+(max(y_axis)/4)])
    plt.xlabel("Shape of Room")
    plt.ylabel("Average Number of Timesteps")
    plt.title("Average cleaning time for various room shapes")
    plt.show()
def showPlot4():
    """
    Produces a plot showing cleaning time vs. percentage cleaned, for
    each of 1-5 robots.
    """
    x_axis = []
    y_axis = []
    y_axis_dict = {}
    X,Y = 0,1
    room_sizes = (25,25)
    num_robots = [1,2,3,4,5]
    num_trials = 10
    min_coverage = [0.16,0.32,0.48,0.64,0.8]
    for robot_number in num_robots:
        list_of_lists = []
        x_axis = []
        y_axis = []
        for min in min_coverage:
            list_of_lists=runSimulation(robot_number, 1.0, room_sizes[X], room_sizes[Y], min, num_trials, Robot, False)
            y_axis.append(average_length(list_of_lists))
        y_axis_dict[robot_number] = y_axis
    x_axis = min_coverage
        #for each %coverage, store list_of_lists in y_axis.
        #store %coverage in x axis.
    print(y_axis_dict)
    min_coverage = float(0.8/len(num_robots))

    plt.plot(x_axis,y_axis_dict[1],'-g',label = '1 Robot')
    plt.plot(x_axis,y_axis_dict[2],'-b',label = '2 Robots')
    plt.plot(x_axis,y_axis_dict[3],'-r',label = '3 Robots')
    plt.plot(x_axis,y_axis_dict[4],'-y',label = '4 Robots')
    plt.plot(x_axis,y_axis_dict[5],'-o',label = '5 Robots')
    #plt.legend({'1 Robot','2 Robots','3 Robots','4 Robots','5 Robots'},'Location','southwest')
    plt.axis([0,(max(x_axis)+(max(x_axis)/4)),0,max(y_axis_dict[1])+max(y_axis_dict[1])/4])
    plt.legend(loc='upper left')
    plt.xlabel("Percentage Cleaned")
    plt.ylabel("Average Timesteps")
    plt.title("Average cleaning time vs percentage cleaned for 1-5 robots")
    plt.show()

# === Problem 5

class RandomWalkRobot(BaseRobot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement
    strategy: it chooses a new direction at random after each
    time-step.
    """

    def updatePositionAndClean(self):
        
        current_pos = self.getRobotPosition()
        new_pos = current_pos.getNewPosition(self.getRobotDirection(),self.speed)
        if self.room.isPositionInRoom(new_pos) == True:
            self.setRobotPosition(new_pos)
            self.room.cleanTileAtPosition(self.getRobotPosition())
        self.setRobotDirection(random.randint(0,360))

# === Problem 6

def showPlot5():
    """
    Produces a plot comparing the two robot strategies.
    """
    x_axis = []
    y_axis = []
    robot_t_list = []
    random_t_list = []
    X,Y = 0,1
    room_sizes = [(5,5),(10,10),(15,15),(20,20),(25,25)]
    num_robots = 1
    num_trials = len(room_sizes)
    for size in room_sizes:
        list_of_lists = []
        list_of_lists=runSimulation(num_robots, 1.0, size[X], size[Y], 0.75, num_trials, Robot, False)
        robot_t_list.append(average_length(list_of_lists))
        list_of_lists=runSimulation(num_robots, 1.0, size[X], size[Y], 0.75, num_trials, RandomWalkRobot, False)
        random_t_list.append(average_length(list_of_lists))
        x_axis.append(size[X]*size[Y])

    plt.plot(x_axis,robot_t_list,'-g',label = 'Generic Robot')
    plt.plot(x_axis,random_t_list,'-b',label = 'Random Walk Robot')
    plt.axis([0,max(x_axis)+(max(x_axis)/4),0,max(random_t_list)+(max(random_t_list)/4)])
    plt.legend(loc='upper left')
    plt.xlabel("Room Area")
    plt.ylabel("Average Number of Timesteps")
    plt.title("Average cleaning time for 2 types of robots and various room sizes")
    plt.show()
#robot = BaseRobot(room,8)

#avg = runSimulation(10, 1.0, 15, 20, 0.8, 30, RandomWalkRobot, True) 
showPlot5()