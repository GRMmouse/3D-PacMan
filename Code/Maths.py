from math import sin,cos,acos,pi
    
#almostEqual from course notes
#http://www.cs.cmu.edu/~112/notes/notes-data-and-exprs.html#AlmostEqual
def almostEqual(a,b):
    return abs(a-b)<10**(-10)

def radToDeg(rad):
    "convert radian to degree"
    return rad/pi*180

def degToRad(deg):
    "convert degree to radian"
    return float(deg)/180*pi

#the Matrix class
class Matrix(object):

    def __init__(self,board):
        "Construct a Matrix using a 2D list"
        self.board=board
        self.rows=len(board)
        self.cols=len(board[0])

    def __eq__(self,other):
        if not isinstance(other,type(self)): return False
        if self.rows!=other.rows or self.cols!=other.cols: return False
        return self.board==other.board

    def __ne__(self,other):
        return not self==other

    def __str__(self):
        "String Representation"
        result="M:"
        for row in self.board[:-1]:#the last row has no comma but a ]
            result+= str(row)+"\n  "
        result+=str(self.board[-1])
        return result
    
    def __add__(self,other):
        "Matrix Addition"
        if not isinstance(other,type(self)):
            tex="Failed Matrix Addition: check type"
            raise Exception(tex)
        if self.rows!=other.rows or self.cols!=other.cols:
            tex="Failed Matrix Addition: check dimensions"
            raise Exception(tex)
        else:
            newBoard=[]
            for row in xrange(self.rows):
                newRow=[]
                for col in xrange(self.cols):
                    newElem=self.board[row][col]+other.board[row][col]
                    newRow+=[newElem]
                newBoard+=[newRow]
            return Matrix(newBoard)

    def __radd__(self,other):
        return self+other
    
    def __sub__(self,other):
        "Matrix Subtraction"
        if not isinstance(other,type(self)):
            tex="Failed Matrix Subtraction: Check type"
            raise Exception(tex)
        if self.rows!=other.rows or self.cols!=other.cols:
            tex="Failed Matrix Subtraction: Check dimensions"
            raise Exception(tex)
        else:
            newBoard=[]
            for row in xrange(self.rows):
                newRow=[]
                for col in xrange(self.cols):
                    newElem=self.board[row][col]-other.board[row][col]
                    newRow+=[newElem]
                newBoard+=[newRow]
            return Matrix(newBoard)

    @staticmethod
    def scalMul(self,other):
        newBoard=[]
        for row in xrange(self.rows):
            newRow=[]
            for col in xrange(self.cols):
                newElem=self.board[row][col]*other
                newRow+=[newElem]
            newBoard+=[newRow]
        return Matrix(newBoard)

    @staticmethod
    def matrMul(self,other):
        newBoard=[]
        for selfRow in xrange(self.rows):
            newRow=[]
            for othCol in xrange(other.cols):
                newElem=0
                #self.cols==other.rows
                for i in xrange(self.cols):
                        newElem+=(self.board[selfRow][i]*
                                  other.board[i][othCol])
                newRow+=[newElem]
            newBoard+=[newRow]
        return Matrix(newBoard)
        
    def __mul__(self,other):
        "Scalar and Matrix Multipication"
        if type(other)==int or type(other)==float:#Scalar
            return Matrix.scalMul(self,other)
        elif isinstance(other,type(self)):
            if self.cols!=other.rows:
                tex="Failed Matrix Multiplication: Check dimensions"
                raise Exception(tex)
            else:#Matrix
                return Matrix.matrMul(self,other)

    def __rmul__(self,other):
        return self*other #not communitive, designed for scalMul

    def transpose(self):
        "Return a new Matrix with rows and cols swapped"
        newBoard=[]
        for col in xrange(self.cols):
            newRow=[]
            for row in xrange(self.rows):
                newRow+=[self.board[row][col]]
            newBoard+=[newRow]
        return Matrix(newBoard)

    def vector(self):
        if self.cols!=1:
            raise Exception("Failed Conversion: cols must be one")
        vList=self.transpose().board[0]
        return Vector(vList)

#the Vector class            
class Vector(object):

    def __init__(self,vList):
        "Construct a vector using a 1d list"
        self.vList=vList

    def __str__(self):
        return "Vector"+str(self.vList)

    def __eq__(self,other):
        if not isinstance(other,type(self)): return False
        return self.vList==other.vList

    def __ne__(self,other):
        return not self==other
    
    def __add__(self,other):
        "Vector Addition"
        if isinstance(other,Point):
            return other+self
        elif isinstance(other,type(self)):
            newVList=[]
            for i in xrange(len(self.vList)):
                newElem=self.vList[i]+other.vList[i]
                newVList+=[newElem]
            return Vector(newVList)
        else:
            raise Exception("""Failed Vector Addition:
                            Not Implemented Operation""")
                
    def __sub__(self,other):
        "Vector Subtraction"
        if not isinstance(other,type(self)):
            raise Exception("Failed Vector Subtraction: Check type")
        else:
            newVList=[]
            for i in xrange(len(self.vList)):
                newElem=self.vList[i]-other.vList[i]
                newVList+=[newElem]
            return Vector(newVList)

    def __radd__(self,other):
        return self+other

    def __mul__(self,other):
        "Scalar Multiplication and Dot Product"
        if type(other)==int or type(other)==float:
            newList=[]
            for elem in self.vList:
                newElem=elem*other
                newList+=[newElem]
            return Vector(newList)
        elif isinstance(other,type(self)):
            result=0
            for i in xrange(len(self.vList)): #checked in init dimension is 3
                newElem=self.vList[i]*other.vList[i]
                result+=newElem
            return result #return a numeric value
        else:
            raise Exception("Failed Vector Multiplication: Check type")

    def __rmul__(self,other):
        return self*other

    def __div__(self,other):
        "Scalar Division"
        if type(other)!=int and type(other)!=float:
            raise Exception("Failed Vector Division: Check type")
        elif other==0:
            raise Exception("Failed Vector Division: Division by Zero")
        else:
            factor=1.0/other
            return factor*self
    
    @staticmethod        
    def cross(self,other):
        "Return cross product of vectors"
        #axb=[0,-a2,a1]   [b0]   [c0]
        #    [a2,0,-a0] * [b1] = [c1]
        #    [-a1,a0,0]   [b2]   [c2]
        a=self.vList
        boardA=[[  0  ,-a[2],a[1] ],
                [a[2] ,  0  ,-a[0]],
                [-a[1],a[0] ,  0  ]]
        product=Matrix(boardA)*other.matrix()
        return product.vector()
 
    def absolute(self):
        "Return the absolute length of vector"
        result=0
        for elem in self.vList:
            result+=elem**2
        return result**0.5

    def getAngle(self,other):
        "return the angle between two vectors"
        return acos(self*other/(self.absolute()*other.absolute()))
    
    def matrix(self):
        "return a Matrix corresponding to the vector"
        return Matrix([self.vList]).transpose()

    def three(self):
        if len(self.vList)!=2:
            raise Exception("Vector Conversion Failed: Check Dimension")
        else:
            newList=self.vList+[0]
            return Vector(newList)

#the Point class
class Point(object):

    def __init__(self,*args):
        "Takes the coordinates to create a point in space"
        self.pList=list(args)
        self.dimension=len(self.pList)
        if self.dimension!=2 and self.dimension!=3:
            raise Exception("Failed Point Construction: Check Dimension")

    def __eq__(self,other):
        if not isinstance(other,type(self)): return False
        return self.pList==other.pList

    def __ne__(self,other):
        return not self==other

    def __str__(self):
        x,y=self.pList[0],self.pList[1]
        if self.dimension==2:
            return "Point(%f,%f)"%(x,y)
        elif self.dimension==3:
            z=self.pList[2]
            return "Point(%f,%f,%f)"%(x,y,z)
        else:
            raise Exception("Failed String Conversion: Check Dimension")

    def __add__(self,other):
        "Takes a vector and add it to the Point"
        if not isinstance(other,Vector):
            raise Exception("Failed Point Addition: Check type")
        elif self.dimension!=len(other.vList):
            raise Exception("Failed Point Addition: Check Dimension")
        else:
            newList=[]
            for i in xrange(self.dimension):
                newList+=[self.pList[i]+other.vList[i]]
            newTuple=tuple(newList)
            return Point(*newTuple)
            
    def __radd__(self,other):
        return self+other                            

    def __sub__(self,other):
        """"Takes a vector,return the point the opposite vector points at.
Takes two points, return a vector pointing from other to self"""
        if isinstance(other,Vector): 
            newList=[]
            for i in xrange(self.dimension):
                newList+=[self.pList[i]-other.vList[i]]
            newTuple=tuple(newList)
            return Point(*newTuple)
        elif isinstance(other,type(self)):
            newList=[]
            for i in xrange(self.dimension):
                newList+=[self.pList[i]-other.pList[i]]
            return Vector(newList)
        else:
            raise Exception(""""Failed Point Subtraction:
                             Not Implemented Operation""")

    @staticmethod
    def absolute(self,other):
        "return the absolute distance between two points"
        if not isinstance(other,type(self)):
            raise Exception("Get Distance Failed: Check type")
        else:
           return (self-other).absolute()

    def three(self):
        "takes a 2D point, return a 3D point"
        if len(self.pList)!=2:
            raise Exception("Point Conversion Failed: Check Dimension")
        else:
            return Point(self.pList[0],self.pList[1],0)

    def two(self):
        "takes a legal 3D point, return a 2D point"
        if len(self.pList)!=3:
            raise Exception("Point Conversion Failed: Check Dimension")
        else:
            newList=self.pList[:-1]
            return Point(newList[0],newList[1])
        
##############
#Matrix Tests#
##############
        
def testMatrixEquation(a,b,c):
    print "Testing Matrix Equation and Inequation...",
    assert(a==Matrix([[1,2,3],[4,5,6]])==a)
    assert(a!=b)
    assert (a!=c)
    assert (a!=3)
    print "Passed!"

def testMatrixAdd(a,b,c):
    print "Tesing Matrix Addition...",
    assert(a+c==Matrix([[2,2,3],[5,5,6]]))
    try:
        print a+b
        print "Addition Test Failed: Wrong Size added" #this should not run
    except: pass
    assert (c+a==a+c)
    print "Passed!"

def testMatrixSub(a,b,c):
    print "Testing Matrix Subtraction...",
    assert (a-c== Matrix([[0,2,3],[3,5,6]]))
    try:
        print a-b
        print "Subtraction Test Failed: Wrong Size subtracted"
    except: pass
    assert (c-a== Matrix([[0,-2,-3],[-3,-5,-6]]))
    print "Passed!"

def testMatrixMul(a,b,c):
    print "Testing Matrix Multiplication...",
    assert (2*a==a*2==Matrix([[2,4,6],[8,10,12]]))
    assert (a*b==Matrix([[6,0],[15,0]]))
    assert (b*a==Matrix([[1,2,3],[1,2,3],[1,2,3]]))
    try:
        print a*c
        print "Multiplication Test Failed: Wrong Size multiplied"
    except: pass
    print "Passed!"

def testMatrixTranspose(a,b,c):
    print "Testing Matrix Transposition...",
    assert (a.transpose()==Matrix([[1,4],[2,5],[3,6]]))
    assert (b.transpose()==Matrix([[1,1,1],[0,0,0]]))
    assert (c.transpose().transpose()==c)
    print "Passed!"

def testMatrixVector(a):
    print  "Testing Matrix Vector...",
    d=Matrix([[1],[2],[3]])
    assert (d.vector()==Vector([1,2,3]))
    try:
        print a.vector()
        print "Vector Test Failed: Wrong Size converted"
    except: pass
    print "Passed!"

def testMatrix():
    print "Testing Matrix Class..."
    a=Matrix([[1,2,3],
              [4,5,6]])
    b=Matrix([[1,0],
              [1,0],
              [1,0]])
    c=Matrix([[1,0,0],
              [1,0,0]])
    assert (a.rows==2)
    assert (a.cols==3)
    assert (a.board==[[1,2,3],[4,5,6]])
    testMatrixEquation(a,b,c)
    testMatrixAdd(a,b,c)
    testMatrixSub(a,b,c)
    testMatrixMul(a,b,c)
    testMatrixTranspose(a,b,c)
    testMatrixVector(a)
    print "All Matrix Tests Passed!\n"

##############
#Vector Tests#
##############

def testVectorEquation(a,b):
    print "Testing Vector Equation and Inequation...",
    assert(a==Vector([1,2,3])==a)
    assert (a!=b)
    assert (a!=42)
    print "Passed!"

def testVectorAdd(a,b):
    print "Testing Vector Addition...",
    assert (a+b==b+a==Vector([2,3,4]))
    try:
        print a+42
        print "Vector Addition Test Failed: Wrong Type Added"
    except:pass
    print "Passed!"

def testVectorSub(a,b):
    print "Testing Vector Subtraction...",
    assert (a-b==Vector([0,1,2]))
    assert (b-a==Vector([0,-1,-2]))
    try:
        print a-42
        print "Vector Subtraction Test Failed: Wrong Type Subtracted"
    except:pass
    print "Passed!"

def testVectorMul(a,b):
    print "Testing Vector Multiplication...",
    assert (2*a==Vector([2,4,6]))
    assert (a*b==b*a==6)
    assert (Vector.cross(a,b)==Vector([-1, 2, -1]))    
    assert (Vector.cross(b,a)==Vector([1,-2,1]))
    print "Passed!"

def testVectorDiv(a,b):
    print "Testing Vector Division...",
    assert (a/2==a*(1/2)==Vector([0.5,1,1.5]))
    try:
        print a/0
        print "Vector Division Test Failed: Division by Zero"
    except: pass
    try:
        print a/b
        print "Vector Division Test Failed: Wrong Type divided"
    except: pass
    print "Passed!"

def testVectorAbsolute(a,b,c):
    print "Testing Vector Absolute...",
    assert almostEqual(a.absolute(), 14**0.5)
    assert almostEqual(b.absolute(), 3**0.5)
    assert almostEqual(c.absolute(),13)
    print "Passed!"

def testVectorMatrix(a,b):
    print "Testing Vector Matrix Conversion...",
    assert (a.matrix()== Matrix([[1],[2],[3]]))
    assert (b.matrix()== Matrix([[1],[1],[1]]))
    print "Passed!"

def testVector():
    print "Testing Vector CLass..."
    a=Vector([1,2,3])
    b=Vector([1,1,1])
    c=Vector([3,4,12])
    assert (a.vList==[1,2,3])
    testVectorEquation(a,b)
    testVectorAdd(a,b)
    testVectorSub(a,b)
    testVectorMul(a,b)
    testVectorAbsolute(a,b,c)
    testVectorMatrix(a,b)
    print "All Vector Tests Passed!\n"

#############
#Point Tests#
#############

def testPointEquation(a,b):
    print "Testing Point Equation and Inequation...",
    assert(b==Point(1,2,3)==b)
    assert (a!=b)
    assert (a!=42)
    print "Passed!"

def testPointAdd(a,b,v):
    print "Testing Point Addition...",
    assert (a+v==v+a==Point(2,3,4))#point+vector=point
    try:
        print a+b
        print "Point Addition Test Failed: Wrong Type Added"
    except:pass
    print "Passed!"

def testPointSub(a,b,v):
    print "Testing Point Subtraction...",
    assert (b-a==Vector([1,2,3]))#pointB-pointA=Vector AB
    assert (a-v==Point(-2,-3,-4))#point-vector=Point
    assert (a-b+b==a)
    try:
        print a-42
        print "Point Subtraction Test Failed: Wrong Type Subtracted"
    except:pass
    print "Passed!"

def testPointAbsolute(a,b,c):
    print "Testing Point Absolute...",
    assert almostEqual(Point.absolute(a,b),14**0.5)
    assert almostEqual(Point.absolute(a,c),13)
    print "Passed!"

def testPoint():
    print "Testing Point Class..."
    a=Point(0,0,0)
    b=Point(1,2,3)
    c=Point(3,4,12)
    v=Vector([2,3,4])
    testPointEquation(a,b)
    testPointAdd(a,b,v)
    testPointSub(a,b,v)
    testPointAbsolute(a,b,c)
    print "All Point Tests passed!\n"
    
def testAll():
    testMatrix()
    testVector()
    testPoint()

testAll()
