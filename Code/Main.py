from Maths import *
from Tkinter import *
import random,os,winsound

################################################################################
# The Smiley Class #############################################################
################################################################################
class Smiley(object):
    "Nice Smiley Faces"

    def __init__(self,x,y,r=20):
        self.x=x
        self.y=y
        self.start=30
        self.extent=300
        self.r=r
        self.color="yellow"

    def draw(self,canvas):
        x=self.x
        y=self.y
        r=self.r
        canvas.create_arc(x-r,y-r,x+r,y+r,start=self.start,
                          extent=self.extent,fill=self.color)
         
################################################################################
# The Color Class ##############################################################
################################################################################

class Color(object):
    "The Class of Colors, for gradual changing colors"
    
    def __init__(self,r,g,b):
        "color init"
        self.r,self.g,self.b=r,g,b

    def __eq__(self,other):
        "the same colors"
        if not isinstance(other,Color): return False
        return self.r==other.r and self.g==other.g and self.b==other.b

    def __nq__(self,other):
        "not the same colors"
        return not self==other

    def __str__(self):
        "return the name of the color"
        r= int(self.r) % 256
        g= int(self.g) % 256
        b= int(self.b) % 256
        return "#%02x%02x%02x" % (r,g,b)
        
    def __add__(self,other):
        "adding colors"
        r=self.r+other.r
        g=self.g+other.g
        b=self.b+other.b
        return Color(r,g,b)

    def __sub__(self,other):
        "finding the difference"
        r=self.r-other.r
        g=self.g-other.g
        b=self.b-other.b
        return Color(r,g,b)

    def __mul__(self,other):
        "multiplying the color vals"
        if type(other)!=int and type(other)!=float:
            raise Exception("Not Implemented")
        r=self.r*other
        g=self.g*other
        b=self.b*other
        return Color(r,g,b)

    def __rmul__(self,other):
        return self*other
    
    def __div__(self,other):
        "dividing the color vals"
        if type(other)!=int: raise Exception("Not Implemented")
        if other==0: raise Exception ("Division by Zero")
        other=float(other)
        r=self.r/other
        g=self.g/other
        b=self.b/other
        return Color(r,g,b)

    def negative(self):
        "return the negative color"
        r=255-self.r
        g=255-self.g
        b=255-self.b
        return Color(r,g,b)

    @staticmethod
    def randomRGB():
        "generate a random RGB color"
        r=random.randint(0,255)
        g=random.randint(0,255)
        b=random.randint(0,255)
        return Color(r,g,b)
    
################################################################################
# The Wall Class ###############################################################
################################################################################

class Wall(object):
    def __init__(self,botLef,botRig,color,height=100):
        """Takes the bottom left and bottom right point and the height
        Build a wall"""
        self.bL=botLef
        self.bR=botRig
        self.h=height
        self.tL=botLef+Vector([0,0,height])
        self.tR=botRig+Vector([0,0,height])
        self.color=color

    def draw(self,canvas,width,height,pacMan):
        pointList=[]
        cx,cy=width/2,height/2
        for point in [self.bL,self.tL,self.tR,self.bR]:
            dx,dy=pacMan.projection(point)
            pointList+=[cx+dx,cy-dy] #up is down
        canvas.create_polygon(pointList,fill=str(self.color),
                              outline="black",width=2)
    
################################################################################
# The PacMan Class #############################################################
################################################################################

class PacMan(object):
    def __init__(self,game):
        self.curRow,self.curCol=23,12 #game specified
        self.game=game
        self.v=20
        self.dir=pi/2
        self.pos=self.boardToPos(self.curRow,self.curCol)+Vector([0,0,75])
        self.color="yellow"
        self.points=0
        self.life=3

    def partialInit(self):
        "init except life and points"
        self.curRow,self.curCol=23,12 #game specified
        self.dir=pi/2
        self.pos=self.boardToPos(self.curRow,self.curCol)+Vector([0,0,75])
        for ghost in self.game.ghostList:
            ghost.__init__()
        if self.life>0:
            self.game.respawnTimer=3999
        elif self.life==0:
            self.game.state="finish"

    def boardToPos(self,row,col):
        "takes a row and a col and returns a Point(x,y)"
        game=self.game
        x=col*game.size+game.size/2
        y=-row*game.size-game.size/2
        return Point(x,y,0)

    def posToBoard(self,point):
        "takes a point and returns a tuple (row,col)"
        game=self.game
        x,y=point.pList[0],point.pList[1]
        row=int(-y/game.size)
        col=int(x/game.size)
        return (row,col)
        
    def move(self,angle):
        "make a move, undo the move if not legal"
        newDir=Vector([cos(self.dir+angle),+sin(self.dir+angle),0])
        newPos=self.pos+newDir*self.v
        (curRow,curCol)=self.posToBoard(newPos)
        if self.isLegal(curRow,curCol):
            self.pos=newPos
            self.curRow,self.curCol=curRow,curCol
        self.update(self.game)   

    def isLegal(self,row,col):
        "check if a cell is legal"
        game=self.game
        if row<0 or col<0 or row>=game.rows or col>=game.cols:
            return False
        if game.board[row][col]==1:
            return False
        else:
            return True

    #check if there are any points left
    def pointsLeft(self):
        "check if there are any points left"
        left=False
        for row in xrange(self.game.rows):
            for col in xrange(self.game.cols):
                if self.game.board[row][col]==2 or self.game.board[row][col]==3:
                    left=True
        return left

    def ghostOnPacMan(self):
        "check if ghost is on PacMan"
        for ghost in self.game.ghostList:
            if (ghost.curRow==self.curRow and
                ghost.curCol==self.curCol):
                return True
        return False
        
    #check if the game is finished
    def isFinished(self):
        "check if the game is finished"
        finish=self.ghostOnPacMan() or not self.pointsLeft()
        if finish==True and self.life>0:
            self.life-=1
            self.partialInit()

    #A,D for rotation
    def rotate(self,angle):
        "rotate the view"
        self.dir+=angle

    def update(self,game):
        "deal with board events"
        cell=game.board[self.curRow][self.curCol]
        if cell==2:
            self.points+=10#pellets
            game.board[self.curRow][self.curCol]=0
        elif cell==3:
            self.points+=50#energizer
            game.board[self.curRow][self.curCol]=0
        self.isFinished()

    def projection(self,point):
        """takes a pacMan and a 3D point,
return its 2D projection relative to the center of pacMan"""
        #vA and vB are vectors, diagram listed in word document
        k=300
        eyeDir=Vector([cos(self.dir),+sin(self.dir),0])
        source=self.pos
        vX=point-source
        sA=vX*eyeDir
        if sA<=0: sA=1.5
        screenPoint=source+vX*(1/sA)
        centerOfScreen=self.pos+eyeDir
        vpacMan=screenPoint-centerOfScreen
        x=vpacMan*k*Vector([+sin(self.dir),-cos(self.dir),0])
        y=vpacMan*k*Vector([0,0,1])
        return x,y

################################################################################
### The Ghost Classes###########################################################
################################################################################
class Ghost(object):
    """\
Rule #1: The ghost never stops!!!
Rule #2: The ghost never turns back
Rule #3: If the next move brings the ghost closer to its target, It makes
         that move"""

    def move(self,game):
        self.curRow+=self.dRow
        self.curCol+=self.dCol
        if not self.isLegal(game,self.curRow,self.curCol):
            self.curRow-=self.dRow
            self.curCol-=self.dCol
            self.moving=False


    def isLegal(self,game,row,col):
        if row<0 or col<0 or row>=game.rows or col>=game.cols:
            return False
        if game.board[row][col]==1:
            return False
        else:
            return True

    #A,D for rotation
    def changeDir(self,game,angle):
        oldDRow,oldDCol=self.dRow,self.dCol
        rotationMatrix=Matrix([[+int(+cos(angle)),-int(sin(angle))],
                               [+int(+sin(angle)),+int(cos(angle))]])
        newDirMatrix=rotationMatrix*Matrix([[oldDRow],[oldDCol]])
        self.dRow=newDirMatrix.vector().vList[0]
        self.dCol=newDirMatrix.vector().vList[1]
        if not self.isLegal(game,self.curRow+self.dRow,self.curCol+self.dCol):
            self.dRow=oldDRow
            self.dCol=oldDCol
            self.moving=False
        self.moving=True

    @staticmethod
    def getDistance(row,col,targetRow,targetCol):
        return (((row-targetRow)**2+
                 (col-targetCol)**2))**0.5
        
    def isNearTarget(self,dRow,dCol,targetRow,targetCol):
        old=Ghost.getDistance(self.curRow,self.curCol,targetRow,targetCol)
        new=Ghost.getDistance(self.curRow+dRow,self.curCol+dCol,
                                  targetRow,targetCol)
        return new<old

    #change dir when the move makes the ghost closer to pacMan
    def followTarget(self,game,targetRow,targetCol):
        if self.moving: #gets nearer to pacMan
            for angle in [0,pi/2,-pi/2]: 
                oldDRow,oldDCol=self.dRow,self.dCol
                rotationMatrix=Matrix([[+int(+cos(angle)),-int(sin(angle))],
                                       [+int(+sin(angle)),+int(cos(angle))]])
                newDirMatrix=rotationMatrix*Matrix([[oldDRow],[oldDCol]])
                dRow=newDirMatrix.vector().vList[0]
                dCol=newDirMatrix.vector().vList[1]
                if self.isNearTarget(dRow,dCol,targetRow,targetCol):
                    self.changeDir(game,angle)
                    return #return as soon as a move is made
                
        else: #find a way to move, regardless
            while True:                 
                angle=random.choice([pi/2,-pi/2]) 
                oldDRow,oldDCol=self.dRow,self.dCol
                rotationMatrix=Matrix([[+int(+cos(angle)),-int(sin(angle))],
                                       [+int(+sin(angle)),+int(cos(angle))]])
                newDirMatrix=rotationMatrix*Matrix([[oldDRow],[oldDCol]])
                dRow=newDirMatrix.vector().vList[0]
                dCol=newDirMatrix.vector().vList[1]
                if self.isLegal(game,self.curRow+dRow,self.curCol+dCol):
                    self.changeDir(game,angle)
                    return #return as soon as possible

class Blinky(Ghost):
    "Blinky targets the current location of pacMan"

    def __init__(self,curRow=10,curCol=13):
        self.curRow,self.curCol=curRow,curCol
        self.dRow,self.dCol=0,1
        self.color="red"
        self.moving=True

    def update(self,game):
        #super(type(self),self).update(game)
        pacManRow,pacManCol=game.pacMan.curRow,game.pacMan.curCol
        self.followTarget(game,pacManRow,pacManCol)
        self.move(game)

class Pinky(Ghost):
    "Pinky targets 4 cells into the direction pacMan is moving"

    def __init__(self,curRow=13,curCol=11):
        self.curRow,self.curCol=curRow,curCol
        self.dRow,self.dCol=0,1
        self.color="pink"
        self.moving=True

    def update(self,game):
        #super(type(self),self).update(game)
        pacMan=game.pacMan
        v=pacMan.v*Vector([cos(pacMan.dir),sin(pacMan.dir),0])
        targetPos=pacMan.pos+2*v
        targetRow,targetCol=pacMan.posToBoard(targetPos)
        self.followTarget(game,targetRow,targetCol)
        self.move(game)

class Inky(Ghost):
    "Inky targets 4 cells in the opposite direction pacMan is moving"

    def __init__(self,curRow=13,curCol=13):
        self.curRow,self.curCol=curRow,curCol
        self.dRow,self.dCol=0,1
        self.color="cyan"
        self.moving=True

    def update(self,game):
        pacMan=game.pacMan
        pacMan=game.pacMan
        v=pacMan.v*Vector([cos(pacMan.dir),sin(pacMan.dir),0])
        targetPos=pacMan.pos-2*v
        targetRow,targetCol=pacMan.posToBoard(targetPos)
        self.followTarget(game,targetRow,targetCol)
        self.move(game)
        
class Clyde(Ghost):
    "Clyde randomly targets either pacMan or its home corner (1,1)"
    
    def __init__(self,curRow=13,curCol=15):
        self.curRow,self.curCol=curRow,curCol
        self.dRow,self.dCol=0,1
        self.color="orange"
        self.moving=True

    def update(self,game):
        pacMan=game.pacMan
        pacManRow,pacManCol=pacMan.curRow,pacMan.curCol
        targetRow=random.choice([pacManRow,1]) #home corner
        targetCol=random.choice([pacManCol,1])
        self.followTarget(game,targetRow,targetCol)
        self.move(game)

################################################################################
# The Bridge Class #############################################################
################################################################################

class Bridge(object):
    "The class linking 2D with 3D"
    def __init__(self,game):
        self.game=game
        self.board=game.board
        self.walls=[]
        self.wallSize=self.game.size
        self.viewRange=5
        
    def update(self):
        "add walls to self.walls"
        self.generateBoard(self.game)
        walls=self.generateWalls()
        newList=[]
        for wall in sorted(walls,self.compareWalls):
            if self.isLegalWall(wall):
                newList+=[wall]
        self.game.walls=newList

    def compareWalls(self,alph,beta):
        "cmp for sorting, compare two walls according to their distance"
        pos=self.game.pacMan.pos
        cToSelf=((alph.bL-pos)+(alph.bR-pos))/2
        cToOth=((beta.bL-pos)+(beta.bR-pos))/2
        return int(-cToSelf.absolute()+cToOth.absolute())

    def isLegalWall(self,wall):
        "decide whether a wall should be drawn"
        pos=self.game.pacMan.pos
        eyeDir=Vector([cos(self.game.pacMan.dir),sin(self.game.pacMan.dir),0])
        cToWall=(wall.bL-pos)/2+(wall.bR-pos)/2
        eyeToBL=wall.bL-pos
        eyeToBR=wall.bR-pos
        if cToWall.absolute()<10:
            return False
        if eyeDir*(wall.bL-pos)<=0 and eyeDir*(wall.bR-pos)<=0:
            return False
        return True    

    def generateBoard(self,game):
        "generate a board according to the environment"
        curRow,curCol=game.pacMan.curRow,game.pacMan.curCol
        left=right=curCol
        up=down=curRow
        vRange=self.viewRange
        while game.board[curRow][left]!=1 and left-curCol>=-vRange:
            left-=1
        while game.board[curRow][right]!=1 and right-curCol<=vRange:
            right+=1
        while game.board[up][curCol]!=1 and up-curRow>=-vRange:
            up-=1
        while game.board[down][curCol]!=1 and down-curRow<=vRange:
            down+=1
        newBoard=[]
        for row in xrange(max(0,up),min(game.rows,down+1)):
            newRow=[]
            for col in xrange(max(0,left),min(game.cols,right+1)):
                newRow.append(game.board[row][col])
            newBoard.append(newRow)
        self.left,self.right=left,right
        self.up,self.down=up,down
        self.board=newBoard
       
    def generateWalls(self):
        "loop through the cells to generate Walls and Dots"
        result=[]
        for row in xrange(len(self.board)):
            for col in xrange(len(self.board[0])):
                if self.board[row][col]==1:
                    result+=self.buildWall(row,col)
                elif self.board[row][col]==2:
                    result+=self.buildDot(row,col)
                elif self.board[row][col]==3:
                    result+=self.buildBigDot(row,col)
        result+=self.findGhost()
        return result

    def buildWall(self,row,col):
        "Construct the walls according to their relative position"
        color=self.getWallColor(row,col)
        result=[]
        half=self.wallSize/2
        curRow=self.game.pacMan.curRow-self.up
        curCol=self.game.pacMan.curCol-self.left
        y=-(row+self.up)*self.wallSize-half #up is down
        x=+(col+self.left)*self.wallSize+half
        # [left-front,front,right-front]
        # [left      ,user ,right      ]
        # [left-back ,back ,right-back ]
        if row<curRow and col<curCol:
            result+=[Wall(Point(x+half,y-half,0),Point(x+half,y+half,0),color)]
            result+=[Wall(Point(x+half,y-half,0),Point(x-half,y-half,0),color)]
        elif row<curRow and col==curCol:
            result+=[Wall(Point(x-half,y-half,0),Point(x+half,y-half,0),color)]
        elif row<curRow and col>curCol:
            result+=[Wall(Point(x-half,y-half,0),Point(x-half,y+half,0),color)]
            result+=[Wall(Point(x-half,y-half,0),Point(x+half,y-half,0),color)]
        elif row==curRow and col<curCol:
            result+=[Wall(Point(x+half,y+half,0),Point(x+half,y-half,0),color)]
        elif row==curRow and col>curCol:
            result+=[Wall(Point(x-half,y-half,0),Point(x-half,y+half,0),color)]
        elif row>curRow and col<curCol:
            result+=[Wall(Point(x+half,y+half,0),Point(x-half,y+half,0),color)]
            result+=[Wall(Point(x+half,y+half,0),Point(x+half,y-half,0),color)]
        elif row>curRow and col==curCol:
            result+=[Wall(Point(x-half,y+half,0),Point(x+half,y+half,0),color)]
        elif row>curRow and col>curCol:
            result+=[Wall(Point(x-half,y+half,0),Point(x+half,y+half,0),color)]
            result+=[Wall(Point(x-half,y+half,0),Point(x-half,y-half,0),color)]   
        return result        

    def buildDot(self,row,col):
        "Construct dots according to their relative position"
        color="yellow"
        result=[]
        half=self.game.size/2
        y=-(row+self.up)*self.wallSize-half #up is down
        x=+(col+self.left)*self.wallSize+half
        halfW=halfH=10
        #This forms a 3D cross
        result+=[Wall(Point(x-halfW,y,50-halfH),
                      Point(x+halfW,y,50-halfH),color,2*halfH)]
        result+=[Wall(Point(x,y-halfW,50-halfH),
                      Point(x,y+halfW,50-halfH),color,2*halfH)]
        return result

    def buildBigDot(self,row,col):
        "Construct Big dots according to their relative position"
        color="yellow"
        result=[]
        half=self.game.size/2
        y=-(row+self.up)*self.wallSize-half #up is down
        x=+(col+self.left)*self.wallSize+half
        halfW=halfH=40
        #This forms a 3D cross
        result+=[Wall(Point(x-halfW,y,50-halfH),
                      Point(x+halfW,y,50-halfH),color,2*halfH)]
        result+=[Wall(Point(x,y-halfW,50-halfH),
                      Point(x,y+halfW,50-halfH),color,2*halfH)]
        return result

    def findGhost(self):
        "Construct the ghost"
        result=[]
        for ghost in self.game.ghostList:
            gRow,gCol=ghost.curRow,ghost.curCol
            if (self.up<=gRow<=self.down and
                self.left<=gCol<self.right):
                result+=self.buildGhost(ghost,gRow-self.up,gCol-self.left)
        return result
    
    def buildGhost(self,ghost,row,col):
        "Construct toe ghost according to their relative position"
        color=ghost.color
        result=[]
        half=self.game.size/2
        y=-(row+self.up)*self.wallSize-half #up is down
        x=+(col+self.left)*self.wallSize+half
        halfW=halfH=50
        #This forms a 3D cross
        result+=[Wall(Point(x-halfW,y,50-halfH),
                      Point(x+halfW,y,50-halfH),color,2*halfH)]
        result+=[Wall(Point(x,y-halfW,50-halfH),
                      Point(x,y+halfW,50-halfH),color,2*halfH)]
        return result
            
    def getWallColor(self,row,col):
        "determine the color of the walls based on the ghost's position"
        actualRow,actualCol=row+self.up,col+self.left
        if self.withinRange(actualRow,actualCol):
            return str(Color(123,0,0))#maroon
        else:
            return str(Color(34,139,34))#green

    def withinRange(self,row,col):
        "Check if a ghost is within range"
        gRange=2
        for ghost in self.game.ghostList:
            distance=(row-ghost.curRow)**2+(col-ghost.curCol)**2
            distance=distance**0.5
            if distance<=gRange: return True
        return False

################################################################################
# The Button Class #############################################################
################################################################################

class Button(object):
    "Button Class"

    def __init__(self,topLeft,bottomRight,text):
        self.x1,self.y1=topLeft[0],topLeft[1]
        self.x2,self.y2=bottomRight[0],bottomRight[1]
        self.text=text
        self.state="rest" #
        self.colors={"rest":"purple","hover":"yellow","down":"pink"}
        self.textColor="green"

    def draw(self,canvas):
        canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2,width=5,
                                fill=self.colors[self.state],outline="black")
        cx,cy=(self.x1+self.x2)/2,(self.y1+self.y2)/2
        canvas.create_text(cx,cy,fill=self.textColor,text=self.text,
                           font="Arial 30 bold")
        
    def update(self,event,eventType):
        x,y=event.x,event.y
        if self.inRange(x,y):
            if eventType=="Motion":
                self.state="hover"
                return False
            elif eventType=="Press":
                self.state="down"
                return True
        else:
            self.state="rest"
            return False

    def inRange(self,x,y):
        if self.x1<=x<=self.x2 and self.y1<=y<=self.y2: return True
        else: return False

################################################################################
# The MiniMap Class ############################################################
################################################################################
class MiniMap(object):
    "The MiniMap displaying the original 2D board"

    def __init__(self,game):
        self.game=game
        self.pacMan=game.pacMan
        self.rows,self.cols=game.rows,game.cols
        self.range=4
        self.size,self.margin=20,5
        self.curRow,self.curCol=self.pacMan.curRow,self.pacMan.curCol
        self.board=self.generateBoard()
        self.ghostList=game.ghostList
        
    def generateBoard(self):
        result=[]
        board=self.game.board
        for row in xrange(self.curRow-self.range,self.curRow+self.range+1):
            newRow=[]
            for col in xrange(self.curCol-self.range,self.curCol+self.range+1):
                if row<0 or row>=self.rows or col<0 or col>=self.cols:
                    newRow+=[0]
                else:
                    newRow+=[board[row][col]]
            result+=[newRow]
        return result

    def update(self):
        if self.curRow!=self.pacMan.curRow or self.curCol!=self.pacMan.curCol:
            self.curRow,self.curCol=self.pacMan.curRow,self.pacMan.curCol
            self.board=self.generateBoard()
            
    def draw(self,canvas,left,top):
        size=self.size
        for row in xrange(len(self.board)):
            for col in xrange(len(self.board[0])):
                x=left+col*size
                y=top+row*size
                cell=self.board[row][col]
                self.drawCell(canvas,x,y,cell)
        for ghost in self.ghostList:
            if self.onBoard(ghost): self.drawGhost(canvas,ghost,left,top)
        smiley=Smiley(left+self.size*(self.range+0.5),
                      top+self.size*(self.range+0.5),size*0.5)
        smiley.draw(canvas)

    def onBoard(self,ghost):
        return (abs(ghost.curRow-self.pacMan.curRow)<=self.range and
                abs(ghost.curCol-self.pacMan.curCol)<=self.range)

    def drawGhost(self,canvas,ghost,left,top):
        x=left+((ghost.curCol-self.pacMan.curCol)+self.range)*self.size
        y=top+((ghost.curRow-self.pacMan.curRow)+self.range)*self.size
        d=self.size
        color=ghost.color
        canvas.create_oval(x,y,x+d,y+d,fill=color)
    
    def drawCell(self,canvas,x,y,cell):
        size,margin=self.size,self.margin
        cx,cy=x+size/2,y+size/2
        r,R=4,8
        canvas.create_rectangle(x,y,x+size,y+size,fill="black")
        if cell==1:
            canvas.create_rectangle(x+margin,y+margin,
                                    x+size-margin,y+size-margin,
                                    fill="dark blue")
        elif cell==2:
            canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill="yellow")
        elif cell==3:
            canvas.create_oval(cx-R,cy-R,cx+r,cy+r,fill="yellow")

################################################################################
# The Game Class ###############################################################
################################################################################

class Game(object):
    "The Main Animation Class"
    
    def __init__(self,width=1000,height=1000):
        self.width=width
        self.height=height
        self.size=200
        self.margin=5
        self.cmd=cmd = """start "C:\\ProgramFiles(x86)\\Windows Media \
Player\\wmplayer.exe" song.mp3"""

###########
## Model ##
###########

    def initTimer(self):
        self.ghostTimer=0
        self.timerDelay=100
        self.period=900 #the ghost moves every 900 milisecond
        self.respawnTimer=3999
        self.tutorialTimer=0
        self.tutorialPeriod=1500
        self.dayTimer=0
        self.dayPeriod=60 #seconds
                
    def initBoard(self): # This is the traditional pacMan board
        self.board=[\
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
            [1,3,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,3,1],
            [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
            [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
            [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
            [1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1],
            [0,0,0,0,0,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,0,0,0,0,0],
            [0,0,0,0,0,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,0,0,0,0,0],
            [0,0,0,0,0,1,2,1,1,0,1,1,1,0,0,1,1,1,0,1,1,2,1,0,0,0,0,0],
            [1,1,1,1,1,1,2,1,1,0,1,1,1,0,0,1,1,1,0,1,1,2,1,1,1,1,1,1],
            [0,0,0,0,0,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,0,0,0,0,0],
            [1,1,1,1,1,1,1,2,1,0,1,0,0,0,0,0,0,1,0,1,2,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,1,2,1,0,1,1,1,0,0,1,1,1,0,1,2,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,2,1,0,1,1,1,1,1,1,1,1,0,1,2,1,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,2,1,0,1,1,1,1,1,1,1,1,0,1,2,1,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
            [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
            [1,3,2,2,1,1,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,1,1,2,2,3,1],
            [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
            [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
            [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
            [1,2,1,1,1,2,2,2,2,2,1,1,2,1,1,2,1,1,2,2,2,2,2,1,1,1,2,1],
            [1,2,2,2,2,2,1,1,1,2,2,2,2,2,2,2,2,2,2,1,1,1,2,2,2,2,2,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
        self.rows=len(self.board)
        self.cols=len(self.board[0])

    def initActors(self):
        self.pacMan=PacMan(self)
        self.blinky=Blinky()
        self.pinky=Pinky()
        self.inky=Inky()
        self.clyde=Clyde()
        self.ghostList=[self.blinky,self.pinky,self.inky,self.clyde]

    def initProjection(self):
        self.bridge=Bridge(self)
        self.walls=[]
    
    def initEvents(self):
        self.keyEvents=[]
        self.preX=self.preY=None
        self.buttonDict=dict()
        self.helpButtons=dict()
        self.miniMap=MiniMap(self)
        self.helpCounter=0
       
    def initButtons(self):
        screenWidth=1600
        screenHeight=1000
        space=400
        marginY=200
        margin=100
        width,height=200,100
        x,y=screenWidth/2-space-width,marginY
        self.buttonDict["play"]=Button((x,y),(x+width,y+height),"PLAY")
        x=screenWidth/2+space
        self.buttonDict["help"]=Button((x,y),(x+width,y+height),"HELP")
        x,y=screenWidth/2-space-width,marginY*2+space/3
        self.buttonDict["credits"]=Button((x,y),(x+width,y+height),"CREDITS")
        x=screenWidth/2+space
        self.buttonDict["quit"]=Button((x,y),(x+width,y+height),"QUIT")
        left,top=screenWidth-margin-width,screenHeight-marginY-height
        right,bottom=screenWidth-margin,screenHeight-marginY
        self.helpButtons["play"]=Button((left,top),(right,bottom),"RESUME")
        self.helpButtons["menu"]=Button((left,top-height-margin),
                                        (right,bottom-height-margin),"MENU")
                                        
    def initAnimation(self):
        self.state="flash"#flash,menu,play,help,credit,finish
        self.initTimer()
        self.initBoard()
        self.initActors()
        self.initProjection()
        self.initEvents()
        self.initButtons()

##########
## View ##
##########
    def drawTimer(self,canvas):
        milisecondInSecond=1000
        text="%d"%(self.respawnTimer/milisecondInSecond)
        cx,cy=self.width/2,self.height/2
        startColor=Color(0,255,0)
        endColor=Color(255,0,0)
        maxTime=3999
        color=(endColor-startColor)/maxTime*self.respawnTimer
        canvas.create_text(cx,cy,text=text,fill=str(color),font="Arial 100 bold")

    def drawLife(self,canvas):
        r=15
        x=y=self.margin+2*r
        for i in xrange(self.pacMan.life):
            face=Smiley(x,y)
            x+=3*r
            face.draw(canvas)
    
    def drawScore(self,canvas):
        r=15
        x=self.margin
        y=self.margin+3*r
        total=int(round(2660/1.5))
        current=self.pacMan.points
        endColor=Color(255,0,0) #red
        startColor=Color(255,255,0) #yellow
        color=(endColor-startColor)/total*current+startColor
        text="Points: %04d"%current
        canvas.create_text(x,y,anchor=NW,text=text,
                           fill=color,font="Arial 30 bold")

    def drawMiniMap(self,canvas):
        miniMap=self.miniMap
        size,mapRange=self.miniMap.size,self.miniMap.range
        width=size*(2*mapRange+1)
        margin=10
        miniMap.draw(canvas,self.width-width-margin,margin)

    def drawWelcome(self,canvas):
        cx,cy=self.width/2,self.height/4
        text="Welcome to the 3D Pac Man tutorial!"
        canvas.create_text(cx,cy,text=text,fill="red",font="Arial 55 bold")
    
    def drawLifeTutorial(self,canvas):
        d=30
        x1=y1=self.margin
        x2,y2=x1+5*d,y1+2*d
        canvas.create_oval(x1,y1,x2,y2,fill=None,outline="red",width=5)
        text="This is your Life Counter! You have 3 lives in total."
        canvas.create_text(x2,y2,anchor=SW,text=text,fill="red",
                           font="Arial 30 bold")

    def drawScoreTutorial(self,canvas):
        d=30
        x1,y1=self.margin,self.margin+d
        x2,y2=x1+8*d,y1+2*d
        canvas.create_oval(x1,y1,x2,y2,fill=None,outline="red",width=5)
        text="""This is your Score Counter!
Small pellets are worth 10 points
Big pellets are worth 50 points."""
        canvas.create_text(x2,y2,anchor=NW,text=text,fill="red",
                           font="Arial 30 bold")

    def drawMiniMapTutorial(self,canvas):
        size,mapRange=self.miniMap.size,self.miniMap.range
        height=width=size*(2*mapRange+1)
        margin=10
        x,y=self.width-width-margin,margin
        canvas.create_oval(x,y,x+width,y+height,fill=None,outline="red",width=5)
        text="""This is your Mini-map!
Pellets and ghosts will appear on the map!"""
        canvas.create_text(x,y,anchor=NE,text=text,fill="red",
                           font="Arial 30 bold")

    def drawScreenTutorial(self,canvas):
        canvas.create_oval(0,0,self.width,self.height,width=5,
                           fill=None,outline="red")
        cx,cy=self.width/2,self.height/4
        text="This is the 3D region!"
        canvas.create_text(cx,cy,text=text,fill="red",
                           font="Arial 55 bold")
        
    def drawInterfaceTutorial(self,canvas):
        if self.helpCounter==0:
            self.drawWelcome(canvas)
        elif self.helpCounter==1:
            self.drawLifeTutorial(canvas)
        elif self.helpCounter==2:
            self.drawScoreTutorial(canvas)
        elif self.helpCounter==3:
            self.drawMiniMapTutorial(canvas)
        elif self.helpCounter==4:
            self.drawScreenTutorial(canvas)  

    def drawLeftTutorial(self,canvas):
        margin=400
        x,y=margin,self.height/2
        cx,cy=self.width/2,self.height/2
        size=100
        text="Press A to move Left!"
        button=Button((x-size/2,y-size/2),(x+size/2,y+size/2),"A")
        button.draw(canvas)
        canvas.create_text(cx,cy,text=text,
                           fill="red",font="Arial 40 bold")
        

    def drawRightTutorial(self,canvas):
        margin=400
        x,y=self.width-margin,self.height/2
        cx,cy=self.width/2,self.height/2
        size=100
        text="Press D to move Right!"
        button=Button((x-size/2,y-size/2),(x+size/2,y+size/2),"D")
        button.draw(canvas)
        canvas.create_text(cx,cy,text=text,
                           fill="red",font="Arial 40 bold")

    def drawForwardTutorial(self,canvas):
        margin=200
        x,y=self.width/2,margin
        cx,cy=self.width/2,self.height/2
        size=100
        text="Press W to move Forward!"
        button=Button((x-size/2,y-size/2),(x+size/2,y+size/2),"W")
        button.draw(canvas)
        canvas.create_text(cx,cy,text=text,
                           fill="red",font="Arial 40 bold")

    def drawBackwardTutorial(self,canvas):
        margin=200
        x,y=self.width/2,self.height-margin
        cx,cy=self.width/2,self.height/2
        size=100
        text="Press S to move Backward!"
        button=Button((x-size/2,y-size/2),(x+size/2,y+size/2),"S")
        button.draw(canvas)
        canvas.create_text(cx,cy,text=text,
                           fill="red",font="Arial 40 bold")
        
    def drawMoveTutorial(self,canvas): #a,d,w,s
        if self.helpCounter==5: #a
            self.drawLeftTutorial(self.canvas)
        elif self.helpCounter==6: #d
            self.drawRightTutorial(self.canvas)
        elif self.helpCounter==7: #w
            self.drawForwardTutorial(self.canvas)
        elif self.helpCounter==8: #s
            self.drawBackwardTutorial(self.canvas)

    def drawRotateQTutorial(self,canvas):
        margin=300
        x,y=margin,margin
        size=100
        cx,cy=self.width/2,self.height/2
        text="Press Q to rotate Left!"
        canvas.create_text(cx,cy,text=text,
                           fill="red",font="Arial 40 bold")
        button=Button((x-size/2,y-size/2),(x+size/2,y+size/2),"Q")
        button.draw(canvas)

    def drawRotateETutorial(self,canvas):
        margin=300
        x,y=self.width-margin,margin
        size=100
        cx,cy=self.width/2,self.height/2
        text="Press E to rotate Right!"
        canvas.create_text(cx,cy,text=text,
                           fill="red",font="Arial 40 bold")
        button=Button((x-size/2,y-size/2),(x+size/2,y+size/2),"E")
        button.draw(canvas)

    def drawMouseRotateTutorial(self,canvas):
        cx,cy=self.cx,self.cy
        r=20
        text="Move Mouse to Rotate!"
        canvas.create_oval(cx-r,cy-r,cx+r,cy+r,width=10,
                           fill=None,outline="red")
        canvas.create_text(self.width/2,self.height/3,text=text,
                           fill="red",font="Arial 40 bold")
    
    def drawRotateTutorial(self,canvas): #q,e,mouse left,mouse right
        if self.helpCounter==9: #q
            self.drawRotateQTutorial(self.canvas)
        elif self.helpCounter==10: #e
            self.drawRotateETutorial(self.canvas)
        elif self.helpCounter==11: #mouse left
            self.drawMouseRotateTutorial(self.canvas)
        elif self.helpCounter==12: #mouse right
            self.drawMouseRotateTutorial(self.canvas)

    def drawGhostTutorial(self,canvas):
        cx,cy=self.width/2,self.height/4
        text="""This is a ghost.
Walls around ghosts will turn red.
You will respawn 3 seconds after a ghost catches you"""
        tHeight=40
        for line in text.splitlines():
            canvas.create_text(cx,cy,text=line,
                               fill="yellow",font="Arial 30 bold")
            cy+=tHeight

    def drawGoodLuck(self,canvas):
        textHeight=100
        cx,cy=self.width/2,self.height/3-textHeight/2
        text="""Press P to Pause
Good Luck
Have Fun!"""
        for line in text.splitlines():
            canvas.create_text(cx,cy,text=line,
                               fill="yellow",font="Arial 60 italic")
            cy+=textHeight        
        
    def drawTutorial(self,canvas):
        if 0<=self.helpCounter<=4: self.drawInterfaceTutorial(canvas)
        elif 5<=self.helpCounter<=8: self.drawMoveTutorial(canvas)
        elif 9<=self.helpCounter<=12: self.drawRotateTutorial(canvas)
        elif self.helpCounter==13: self.drawGhostTutorial(canvas)
        elif self.helpCounter==14: self.drawGoodLuck(canvas)

    def drawHelp(self,canvas):
        cy=self.height/2
        shadeW=10
        canvas.create_rectangle(0,0,self.width,cy,fill="sky blue")
        canvas.create_rectangle(0,cy,self.width,self.height,
                                fill=str(Color(184,134,11)))#brown
        for wall in self.walls:
            wall.draw(canvas,self.width,self.height,self.pacMan)
        self.drawLife(canvas)
        self.drawScore(canvas)
        self.drawMiniMap(canvas)
        self.drawTutorial(canvas)

    def drawSky(self,canvas):
        start=Color(135,206,235)
        mid=Color(0,0,0)
        quaterPeriod=self.dayPeriod/4
        current=(int(self.dayTimer)%self.dayPeriod+
                 (self.dayTimer-int(self.dayTimer)))
                  #a float between 0 and dayPeriod
        if 0<=current<quaterPeriod:
            skyColor=start
        elif quaterPeriod<=current<quaterPeriod*2:
            skyColor=(mid-start)*(current-quaterPeriod)/quaterPeriod+start
        elif quaterPeriod*2<=current<quaterPeriod*3:
            skyColor=mid
        else:
            skyColor=(start-mid)*(current-3*quaterPeriod)/quaterPeriod+mid
        canvas.create_rectangle(0,0,self.width,self.height/2,fill=skyColor)
        
    def drawPlay(self,canvas):
        cy=self.height/2
        shadeW=10
        self.drawSky(canvas)
        canvas.create_rectangle(0,cy,self.width,self.height,
                                fill=str(Color(184,134,11)))#brown
        for wall in self.walls:
            wall.draw(canvas,self.width,self.height,self.pacMan)
        if self.respawnTimer>0:
            self.drawTimer(self.canvas)
        self.drawLife(canvas)
        self.drawScore(canvas)
        self.drawMiniMap(canvas)

    def drawPause(self,canvas):
        self.drawPlay(canvas)
        for key in self.helpButtons:
            button=self.helpButtons[key]
            button.draw(canvas)
        
    def drawFlash(self,canvas):
        canvas.create_rectangle(0,0,self.width,self.height,fill="blue")
        cx,cy=self.width/2,self.height/2
        textHeight=100
        name="dkosbie.gif"
        text="The 3D Pac Man"
        hint="Mouse Click to Continue"
        self.image=PhotoImage(file=name)
        canvas.create_image((cx,cy),image=self.image)
        canvas.create_text(cx,textHeight,text=text,
                           fill="yellow",font="Arial 50 bold")
        canvas.create_text(cx,self.height-textHeight,text=hint,
                           fill="yellow",font="Arial 30 italic")

    def drawFinish(self,canvas):
        hint1="Excessive Gaming is so not-112"
        hint2="R for Restart, R for R!!!"
        cx,cy=self.width/2,self.height/2
        textHeight=100
        cy=self.height/2
        shadeW=10
        canvas.create_rectangle(0,0,self.width,cy,fill="sky blue")
        canvas.create_rectangle(0,cy,self.width,self.height,
                                fill=str(Color(184,134,11)))#brown
        for wall in self.walls:
            wall.draw(canvas,self.width,self.height,self.pacMan)
        self.drawLife(canvas)
        self.drawScore(canvas)
        self.drawMiniMap(canvas)
        canvas.create_image((cx,cy),image=self.image)
        canvas.create_text(cx,textHeight,text=hint1,
                           fill="red",font="Arial 30 italic")
        canvas.create_text(cx,self.height-textHeight,text=hint2,
                           fill="red",font="Arial 30 italic")

    def drawMenu(self,canvas):
        textHeight=100
        title="Menu"
        canvas.create_rectangle(0,0,self.width,self.height,fill="blue")
        cx,cy=self.width/2,self.height/2
        canvas.create_image((cx,cy),image=self.image)
        canvas.create_text(cx,textHeight,text=title,
                           font="Arial 50 bold",fill="yellow")
        for key in self.buttonDict:
            button=self.buttonDict[key]
            button.draw(canvas)

    def drawCredits(self,canvas):
        textHeight=80
        title="Credits"
        text="""This game would never be possible
without the most generous helps and suppports from:
Leon Zhang, for his help in 3D Projection
Rebekah Zhao, for her support in Image Processing
Emma Zhong, for her suggestion on User Interface Design
and the rest of the 15-112 staff
who invested their precious time helping!

Click Anywhere to Return to Menu"""
        canvas.create_rectangle(0,0,self.width,self.height,fill="dark blue")
        cx,cy=self.width/2,self.height/2
        canvas.create_text(cx,textHeight,text=title,
                           font="Arial 50 bold",fill="yellow")
        startColor=Color(255,20,147) #pink
        endColor=Color(0,255,127) #forest green
        y=textHeight*2
        listOfLines=text.splitlines()
        n=len(listOfLines)
        for i in xrange(n):
            line=listOfLines[i]
            color=(endColor-startColor)/n*i+startColor
            canvas.create_text(cx,y,text=line,font="Arial 40 italic",fill=color)
            y+=textHeight           
        
    def redrawAll(self):
        self.canvas.delete(ALL)
        if self.state=="flash":
            self.drawFlash(self.canvas)
        elif self.state=="menu":
            self.drawMenu(self.canvas)
        elif self.state=="help":
            self.drawHelp(self.canvas)
        elif self.state=="play":
            self.drawPlay(self.canvas)
        elif self.state=="pause":
            self.drawPause(self.canvas)
        elif self.state=="credits":
            self.drawCredits(self.canvas)
        elif self.state=="finish":
            self.drawFinish(self.canvas)
        
#############
## Control ##
#############
    def rise(self,height):
        if self.pacMan.pos.pList[2]+height>=25:
            self.pacMan.pos+=Vector([0,0,height])
            
    def sizeChange(self,event):
        self.width=event.width
        self.height=event.height
        self.redrawAll()

    def onMouseMotion(self,event):
        if self.state=="menu":
            for key in self.buttonDict:
                button=self.buttonDict[key]
                button.update(event,"Motion")
        elif self.state=="play" and self.respawnTimer<=0:
            if event.x==self.width/2 and event.y==self.height/2:
                self.preX=event.x
            if self.preX==None:
                self.preX=event.x
            elif self.preX-event.x>5:
                self.pacMan.rotate(pi/72)
                self.preX=event.x
            elif event.x-self.preX>5:
                self.pacMan.rotate(-pi/72)
                self.preX=event.x
        elif self.state=="pause":
             for key in self.helpButtons:
                button=self.helpButtons[key]
                button.update(event,"Motion")
        elif self.state=="help" and 11<=self.helpCounter<=12:
            self.cx,self.cy=event.x,event.y
        self.redrawAll()

    def onLeftMousePressed(self,event):
        if self.state=="flash":
            self.state="menu"
        elif self.state=="menu":
            for key in self.buttonDict:
                flag=self.buttonDict[key].update(event,"Press")
                if flag==True:
                    if key=="play":
                        self.initAnimation()
                        self.root.config(cursor="none")
                    elif key=="quit": quit()
                    elif key=="help": self.helpCounter=0
                    self.state=key
        elif self.state=="pause":
            for key in self.helpButtons:
                flag=self.helpButtons[key].update(event,"Press")
                if flag==True:
                    if key=="play":
                        self.respawnTimer=3999
                        self.root.config(cursor="none")
                    self.state=key
        elif self.state=="credits":
            self.state="menu"
        self.redrawAll()
        
    def onRightMousePressed(self,event):
        if self.state=="play":
            self.rise(-25)
            self.pacMan.v/=4
            for ghost in self.ghostList:
                ghost.changeDir(self,pi)
            self.redrawAll()

    def onRightMouseReleased(self,event):
        if self.state=="play":
            self.rise(+25)
            self.pacMan.v*=4
            self.redrawAll()

    #from course notes
    #http://www.kosbie.net/cmu/fall-11/15-112/handouts
    #/misc-demos/src/keyEventsDemo.py
    def onKeyPressedWrapper(self,event):
        self.root.event_generate('<Motion>', warp=True,
                         x=self.width/2, y=self.height/2)
        if event.char not in self.keyEvents:
            self.keyEvents.append(event.char)

    def onKeyPressedMove(self,char):
        if char=="a":
            self.pacMan.move(+pi/2)
        elif char=="s":
            self.pacMan.move(pi)
        elif char=="d":
            self.pacMan.move(-pi/2)
        elif char=="w":
            self.pacMan.move(0)
        elif char=="q":
            self.pacMan.rotate(pi/36)
        elif char=="e":
            self.pacMan.rotate(-pi/36)
        elif char=="p":
            self.state="pause"
        elif char=="f": self.state="finish"#This is a cheat code
        self.redrawAll()
    
    def onKeyPressed(self,char):
        if self.state=="play" and self.pacMan.life>0 and self.respawnTimer<=0:
            self.onKeyPressedMove(char)
        if char=="r":
            self.initAnimation()
            self.state="menu"
        
    def onKeyReleased(self,event):
        if event.char in self.keyEvents:
            self.keyEvents.remove(event.char)

    def playTimerFired(self):
        milisecondInSecond=1000
        self.ghostTimer+=self.timerDelay
        self.dayTimer+=self.timerDelay/float(milisecondInSecond)
        if self.ghostTimer>=self.period and self.respawnTimer<=0:
            for ghost in self.ghostList:
                ghost.update(self)
            self.ghostTimer=0
        if self.respawnTimer>0:
            self.respawnTimer-=self.timerDelay
        self.bridge.update()
        self.pacMan.update(self)
        self.miniMap.update()

    def moveTutorial(self):
        trial=2
        if self.helpCounter==5: #move tutorial "a"
            for i in xrange(trial):
                self.pacMan.move(+pi/2)
                self.redrawAll()
        elif self.helpCounter==6: #move tutorial "d"
            for i in xrange(trial):
                self.pacMan.move(-pi/2)
                self.redrawAll()
        elif self.helpCounter==7: #move tutorial "w"
            for i in xrange(trial):
                self.pacMan.move(0)
                self.redrawAll()
        elif self.helpCounter==8: #move tutorial "s"
            for i in xrange(trial):
                self.pacMan.move(pi)
                self.redrawAll()

    def rotateTutorial(self):
        if self.helpCounter==9: #rotate tutorial "q"
            self.pacMan.rotate(pi/36)
            self.redrawAll()
        elif self.helpCounter==10: #rotate tutorial "e"
            self.pacMan.rotate(-pi/36)
            self.redrawAll()
        elif self.helpCounter==11: #rotate tutorial "mouse left"
            self.pacMan.rotate(+pi/72)
            self.root.event_generate('<Motion>', warp=True,
                         x=self.width/2-self.tutorialTimer/10,
                                     y=self.height/2)
            self.redrawAll()
        elif self.helpCounter==12: #rotate tutorial "mouse right"
            self.pacMan.rotate(-pi/72)
            self.root.event_generate('<Motion>', warp=True,
                         x=self.width/2+self.tutorialTimer/10, y=self.height/2)
            self.redrawAll()
            
    def helpHandler(self):
        if self.tutorialTimer<self.tutorialPeriod:
            self.tutorialTimer+=self.timerDelay
        else:
            self.tutorialTimer=0
            if self.helpCounter<=13:
                self.helpCounter+=1
            else:
                self.initAnimation()
                self.state="menu"
                return
        if 5<=self.helpCounter<=8: self.moveTutorial()
        elif 9<=self.helpCounter<=12: self.rotateTutorial()
        elif self.helpCounter==13:
            self.blinky.curRow,self.blinky.curCol=21,12
            self.bridge.update()
            self.pacMan.update(self)
            self.miniMap.update()
            self.redrawAll()
        
    def helpTimerFired(self):
        self.helpHandler()
        self.bridge.update()
        self.pacMan.update(self)
        self.miniMap.update()

    def onTimerFired(self):
        if self.timerDelay==None:
            return
        for char in self.keyEvents:
            self.onKeyPressed(char)
        if self.state=="menu":
            self.root.config(cursor="arrow")
        if self.state=="play":
            self.playTimerFired()
        if self.state=="help":
            self.helpTimerFired()
        if self.state=="pause":
            self.root.config(cursor="arrow")
        self.redrawAll()
        self.canvas.after(self.timerDelay,self.onTimerFired)

    def run(self):
        self.root=Tk()
        self.canvas=Canvas(self.root,width=self.width,height=self.height)
        self.canvas.pack(fill=BOTH,expand=YES)
        #os.system(self.cmd)
        #winsound.PlaySound("song.mp2",winsound.SND_FILENAME)
        self.root.bind("<Motion>", self.onMouseMotion)
        self.root.bind("<Configure>", self.sizeChange)
        self.root.bind("<KeyPress>",self.onKeyPressedWrapper)
        self.root.bind("<KeyRelease>",self.onKeyReleased)
        self.root.bind("<Button-1>",self.onLeftMousePressed)
        self.root.bind("<Button-3>", self.onRightMousePressed)
        self.root.bind("<B3-ButtonRelease>", self.onRightMouseReleased)
        self.root.attributes("-fullscreen", True)
        self.initAnimation()
        self.onTimerFired()
        self.root.mainloop()
        print "Done"

def main():
    game=Game()
    game.run()

main()
