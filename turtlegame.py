# simple animated game in which a turtle shoots lazers at ghosts

from turtle import *
import tkinter.messagebox
import tkinter
import random
import math
import datetime

screenMinX = -500
screenMinY = -500
screenMaxX = 500
screenMaxY = 500

# FlyingTurtle's projectile weapons to be used against the ghosts
class LaserBeam(RawTurtle):
    def __init__(self,canvas,x,y,direction,dx,dy):
        super().__init__(canvas)
        self.penup()
        self.goto(x,y)
        self.setheading(direction)
        self.color("Green")
        self.lifespan = 200
        self.__dx = math.cos(math.radians(direction))*2 + dx
        self.__dy = math.sin(math.radians(direction))*2 + dy
        self.shape("laser")

    # returns number of moves left before the laser beam is taken out of play
    def getLifespan(self):
        return self.lifespan

    # returns horizontal change in position per increment of movement
    def getdx(self):
        return self.__dx

    # returns vertical change in position per increment of movement
    def getdy(self):
        return self.__dy

    # returns approximate radius of the lazer beam, used to determine area of effect
    def getRadius(self):
        return 4

    # moves the laser beam from its current position to a new position
    def move(self):
        screen = self.getscreen()
        x = self.xcor()
        y = self.ycor()

        x = (self.__dx + x - screenMinX) % (screenMaxX - screenMinX) + screenMinX
        y = (self.__dy + y - screenMinY) % (screenMaxY - screenMinY) + screenMinY

        self.goto(x,y)
        self.lifespan -= 1

# the antagonists of our story, the drifting ghosts whose touch is deadly
class Ghost(RawTurtle):
    def __init__(self,canvasobj,dx,dy,x,y,size):
        RawTurtle.__init__(self,canvasobj)
        self.penup()
        self.goto(x,y)
        self.__dx = dx
        self.__dy = dy
        self.__size = size
        if self.__size==3:
            self.shape("blueghost.gif")
        elif self.__size==2:
            self.shape("pinkghost.gif")

    # returns horizontal change in position per increment of movement
    def getdx(self):
        return self.__dx

    # returns vertical change in position per increment of movement
    def getdy(self):
        return self.__dy

    # alters the horizontal change in position per increment of movement
    # by setting it equal to the argument newdx
    def setdx(self,newdx):
        self.__dx = newdx

    # alters the vertical change in position per increment of movement
    # by setting it equal to the argument newdy
    def setdy(self,newdy):
        self.__dy = newdy

    #Moves the ghost from its current position to a new position
    def move(self):
        screen = self.getscreen()
        x = self.xcor()
        y = self.ycor()

        x = (self.__dx + x - screenMinX) % (screenMaxX - screenMinX) + screenMinX
        y = (self.__dy + y - screenMinY) % (screenMaxY - screenMinY) + screenMinY

        self.goto(x,y)

    #returns the apprximate "radius" of the Ghost object
    def getRadius(self):
        return self.__size * 10 - 5

# the hero of our story, guided by the player in a quest to vanquish the ghosts
class FlyingTurtle(RawTurtle):
    def __init__(self,canvasobj,dx,dy,x,y, size):
        RawTurtle.__init__(self,canvasobj)
        self.penup()
        self.color("purple")
        self.goto(x,y)
        self.__dx = dx
        self.__dy = dy
        self.__size = size
        self.shape("turtle")

    # returns horizontal change in position per increment of movement
    def getdx(self):
        return self.__dx

    # returns vertical change in position per increment of movement
    def getdy(self):
        return self.__dy

    # alters the horizontal change in position per increment of movement
    # by setting it equal to the argument newdx
    def setdx(self,newdx):
        self.__dx = newdx

    # alters the horizontal change in position per increment of movement
    # by setting it equal to the argument newdx
    def setdy(self,newdy):
        self.__dy = newdy

    # moves the flyingturtle from its current position to a new position
    def move(self):
        screen = self.getscreen()
        x = self.xcor()
        y = self.ycor()

        x = (self.__dx + x - screenMinX) % (screenMaxX - screenMinX) + screenMinX
        y = (self.__dy + y - screenMinY) % (screenMaxY - screenMinY) + screenMinY

        self.goto(x,y)

    # jet pack propulsion that increases the speed of the flying turtle aka
    # increases the distance covered by each increment of movement
    def turboBoost(self):
        angle = self.heading()
        x = math.cos(math.radians(angle))
        y = math.sin(math.radians(angle))
        self.__dx = self.__dx + x
        self.__dy = self.__dy + y

    # immediately halts flyingturtle
    def stopTurtle(self):
        angle = self.heading()
        self.__dx = 0
        self.__dy = 0

    # returns approximate radius of the flyingturtle object
    def getRadius(self):
        return 2

# returns true if a collision has occured between the two objects taken as arguments
def intersect(obj1,obj2):
    distance = math.sqrt((obj1.xcor() - obj2.xcor())**2 + (obj1.ycor() - obj2.ycor())**2)
    radii_sum = obj1.getRadius() + obj2.getRadius()
    if distance <= radii_sum:
        return True
    else:
        return False



def main():

    # start by creating a RawTurtle object for the window.
    firstwindow = tkinter.Tk()
    firstwindow.title("Turtle Saves the World!")
    canvas = ScrolledCanvas(firstwindow,600,600,600,600)
    canvas.pack(side = tkinter.LEFT)
    t = RawTurtle(canvas)

    screen = t.getscreen()
    screen.setworldcoordinates(screenMinX,screenMinY,screenMaxX,screenMaxY)
    screen.register_shape("blueghost.gif")
    screen.register_shape("pinkghost.gif")
    screen.register_shape("laser",((-2,-4),(-2,4),(2,4),(2,-4)))

    # scoreboard
    frame = tkinter.Frame(firstwindow)
    frame.pack(side = tkinter.RIGHT,fill=tkinter.BOTH)
    scoreVal = tkinter.StringVar()
    scoreVal.set("0")
    scoreTitle = tkinter.Label(frame,text="Score")
    scoreTitle.pack()
    scoreFrame = tkinter.Frame(frame,height=2,bd=1,relief=tkinter.SUNKEN)
    scoreFrame.pack()
    score = tkinter.Label(scoreFrame,height=2,width=20,textvariable=scoreVal,fg="yellow",bg="black")
    score.pack()

    # tally of lives remaining
    livesTitle = tkinter.Label(frame,text="Extra Lives Remaining")
    livesTitle.pack()
    livesFrame = tkinter.Frame(frame,height=30,width=60,relief=tkinter.SUNKEN)
    livesFrame.pack()
    livesCanvas = ScrolledCanvas(livesFrame,150,40,150,40)
    livesCanvas.pack()
    livesTurtle = RawTurtle(livesCanvas)
    livesTurtle.ht()
    livesScreen = livesTurtle.getscreen()
    life1 = FlyingTurtle(livesCanvas,0,0,-35,0,0)
    life2 = FlyingTurtle(livesCanvas,0,0,0,0,0)
    life3 = FlyingTurtle(livesCanvas,0,0,35,0,0)
    lives = [life1, life2, life3]
    t.ht()

    screen.tracer(10)

    # Tiny Turtle!
    flyingturtle = FlyingTurtle(canvas,0,0,(screenMaxX-screenMinX)/2+screenMinX,(screenMaxY-screenMinY)/2 + screenMinY,3)

    # a list to keep track of all the lasers
    lasers = []

    # a list to keep track of all the dead lasers
    deadLasers = []

    # a list to keep track of all the ghosts
    ghosts = []

    # a list to keep track of all the dead ghosts
    deadGhosts = []

    # create some ghosts and randomly place them around the screen
    for numofghosts in range(6):
        dx = random.random()*6  - 4
        dy = random.random()*6  - 4
        x = random.random() * (screenMaxX - screenMinX) + screenMinX
        y = random.random() * (screenMaxY - screenMinY) + screenMinY

        ghost = Ghost(canvas,dx,dy,x,y,3)

        ghosts.append(ghost)

    def play():
        #start counting time for the play function
        ##LEAVE THIS AT BEGINNING OF play()
        start = datetime.datetime.now()

        # check if all ghosts have been slain. If yes, game won
        if ghosts == []:
            tkinter.messagebox.showinfo("YOU WIN!!!", "You saved the world!")
            return

        # move the turtle
        flyingturtle.move()

        # move the lasers
        for laser in lasers:
            laser.move()
            if laser.lifespan == 0:
                lasers.remove(laser)
                deadLasers.append(laser)
                laser.goto(-screenMinX*2,-screenMinY*2)
                laser.ht()

        # move the ghosts
        for each_ghost in ghosts:
            each_ghost.move()

        # check for collisions
        for ghost in ghosts:
            for laser in lasers:
                if intersect(ghost,laser): # if ghost is shot by a laser beam
                    ghosts.remove(ghost)
                    deadGhosts.append(ghost)
                    ghost.goto(-screenMinX*2,-screenMinY*2)
                    ghost.ht()

                    lasers.remove(laser)
                    deadLasers.append(laser)
                    laser.goto(-screenMinX*2,-screenMinY*2)
                    laser.ht()

                    scoreInt = int(scoreVal.get()) + 20
                    scoreVal.set(str(scoreInt))

            if intersect(ghost,flyingturtle): # if flyingturtle is hit by a ghost
                lostlife = lives.pop()
                lostlife.ht()

                ghosts.remove(ghost)
                deadGhosts.append(ghost)
                ghost.goto(-screenMinX*2,-screenMinY*2)
                ghost.ht()

                # check if flying turtle out of lives. If yes, game lost
                if lives == []:
                    tkinter.messagebox.showinfo("You lost...","Apologies, the world is doomed...")
                    return
                else:
                    tkinter.messagebox.showwarning("Careful!","You've lost a life!")


        #stop counting time for the play function
        ##LEAVE THIS AT END OF ALL CODE IN play()
        end = datetime.datetime.now()
        duration = end - start

        millis = duration.microseconds / 1000.0

        # set the timer to go off again
        screen.ontimer(play,int(10-millis))


    # set the timer to go off the first time in 5 milliseconds
    screen.ontimer(play, 5)

    # turn turtle 7 degrees to the left
    def turnLeft():
        flyingturtle.setheading(flyingturtle.heading()+7)

    # turn turtle 7 detrees to the Right
    def turnRight():
        flyingturtle.setheading(flyingturtle.heading()-7)

    # turboBoost turtle
    def forward():
        flyingturtle.turboBoost()

    # stop Turtle
    def stop():
        flyingturtle.stopTurtle()

    # flyingturtle unleashes her laser beam projectiles
    def fireLaser():
        x = flyingturtle.xcor()
        y = flyingturtle.ycor()
        direction = flyingturtle.heading()
        dx = flyingturtle.getdx()
        dy = flyingturtle.getdy()
        laser = LaserBeam(canvas,x,y,direction,dx,dy)
        lasers.append(laser)


    # call functions above when pressing relevant keys
    screen.onkeypress(turnLeft,"Left")
    screen.onkeypress(turnRight,"Right")
    screen.onkeypress(forward,"Up")
    screen.onkeypress(stop,"Down")
    screen.onkeypress(fireLaser,"")

    screen.listen()
    tkinter.mainloop()

if __name__ == "__main__":
    main()
