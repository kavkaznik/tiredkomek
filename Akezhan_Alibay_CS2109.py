class MatrixError(Exception):
    def __init__(self, matrix1, matrix2):
        self.matrix1 = matrix1
        self.matrix2 = matrix2


class Matrix:
    def __init__(self, mtrx):  # initialization or constructor
        self.mtrx = mtrx

    def zero(self, r, c):
        a = []
        b = []
        for x in range(c):
            a.append(0)
        for x in range(r):
            b.append(a)
        return b

    def size(self):  # size
        return len(self.mtrx), len(self.mtrx[0])

    def __str__(self):  # string method
        a = ''
        for x in range(len(self.mtrx)):
            for j in range(len(self.mtrx[0])):
                a = a + str(self.mtrx[x][j]) + '\t'
            a = a + '\n'
        return a

    def __add__(self, other):  # adding
        if len(self.mtrx[0]) != len(other.mtrx[0]) or len(self.mtrx) != len(self.mtrx):
            raise MatrixError(self, other)
        for j in range(len(self.mtrx[0])):
            for x in range(len(self.mtrx)):
                self.mtrx[x][j] = self.mtrx[x][j] + other.mtrx[x][j]
        return self

    def __mul__(self, other):  # multiplication
        if isinstance(other, int) or isinstance(other, float):
            for j in range(len(self.mtrx[0])):
                for x in range(len(self.mtrx)):
                    self.mtrx[x][j] = self.mtrx[x][j] * other
        elif isinstance(other, Matrix):
            if len(self.mtrx[0]) != len(self.mtrx):
                raise MatrixError(self, other)
            result = Matrix(self.zero(len(self.mtrx), len(other.mtrx[0])))
            mt=[]
            tm=[]
            for x in range(len(result.mtrx)):
                for j in range(len(result.mtrx[0])):
                    a = 0
                    for k in range(len(self.mtrx)):
                        a = a + self.mtrx[x][k] * other.mtrx[k][j]
                    mt.append(a)
                tm.append(mt)
                mt=[]
            asa=Matrix(tm)
            return asa
        return self

    __rmul__ = __mul__  # reverse multiplication

    def transposed(self):
        result = Matrix(self.zero(len(self.mtrx[0]), len(self.mtrx)))
        for x in range(len(result.mtrx)):
            for j in range(len(result.mtrx[0])):
                result.mtrx[x][j] = self.mtrx[j][x]
        return result

    def transpose(self):
        result = Matrix(self.zero(len(self.mtrx[0]), len(self.mtrx)))
        for x in range(len(result.mtrx)):
            for j in range(len(result.mtrx[0])):
                result.mtrx[x][j] = self.mtrx[j][x]
        self.mtrx = result.mtrx

class SquareMatrix(Matrix):
    def __pow__(self,n):
        if n==0:
            a=[]
            b=[]
            for x in range(len(self.mtrx)):
                for j in range(len(self.mtrx[0])):
                    if x!=j:
                        a.append(0)
                    elif x==j:
                        a.append(1)
                b.append(a)
                a=[]

            kk=Matrix(b)
            return kk
        elif n==1:
            return self
        elif n>1:
            k=self
            for x in range(1,n):
                self=self*k
            return self


matrix0 = Matrix([[0, 1], [1, 0]])
matrix1 = Matrix([[2, 1, 2], [3, 3, -4], [4, 5, 4]])  # matrix number 1
matrix2 = Matrix([[4, 5, 2], [6, 6, 1], [8, 9, 8]])  # matrix number 2
matrix4 = Matrix([[10, 10], [0, 0], [1, 1]])
print('Str method')
print(matrix1)
print('-' * 10)
print('Matrix size')
print(matrix1.size())
print('-' * 10)
print('Adding two matrix')
print(matrix2 + matrix1)
print('-' * 10)
print('Scalar multiplication')
print(3 * matrix1)
print('-' * 10)
print('MatrixError class')
try:
    matrix3 = matrix2 + matrix0
    print('WA\n' + str(matrix3))
except MatrixError as e:
    print("can't add:\n")
    print(e.matrix1)
    print('by\n')
    print(e.matrix2)
print('-' * 10)
print('transposed')
print(matrix4)
print(matrix4.transposed())
print(matrix4)
print('-' * 10)
print('transpose')
print(matrix4)
matrix4.transpose()
print(matrix4)
print('-' * 10)
print('matrix1')
print(matrix1)
print('matrix2')
print(matrix2)
print('multiplication')
print(matrix1 * matrix2)
print('-' * 10)

m1 = Matrix([[3,2],[-10,0],[14,5]])
m2 = Matrix([[5,2,10],[-0.5,-0.25,18],[-22,-2.5,-0.125]])
print(m2 * m1)
print('-' * 10)
try:
    m=m1 * m2
except MatrixError as e:
    print("error: ")
    print(e.matrix1)
    print("by: ")
    print(e.matrix2)
mid=Matrix([[1,0,0],[0,1,0],[0,0,1]])
print('multiplications')
print(5*m2)
m2 = Matrix([[5,2,10],[-0.5,-0.25,18],[-22,-2.5,-0.125]])
print(m2* (120*mid*m1))
print('matrix')
pow_m=SquareMatrix([[1,2],[0,3]])
print(pow_m)
print(isinstance(pow_m,SquareMatrix))
print('0 power')
print(pow_m**0)
print('1 power')
print(pow_m**1)
print('2 power')
print(pow_m**2)