import numpy as np

class Sparse():
    def __init__(self):
        # index              0  1  2  3  4  5  6   7  8  9  10     
        self.aa =  np.array([1, 5, 6, 7, 8, 2, 9, 10, 3, 11, 4])
        self.pne = np.array([2, 3, 4, 0, 6, 7, 0,  9, 0, 11, 0])
        self.ci =  np.array([1, 2, 3, 4, 1, 2, 4,  1, 3,  1, 4])
        self.rsi = np.array([1, 5, 8, 10])
        self.n = 4

    def setvectors(self, A):
        self.aa = []
        pass

    def getter(self, i, j):
        si = self.rsi[i-1] -1
        while True:
            if self.ci[si] == j:
                return self.aa[si]
            if self.pne[si] == 0:
                break
            si = self.pne[si] - 1
        return 0
    
    def getrow(self,i):
        row = np.array([])
        for x in range(self.n):
            row = np.append(row,self.getter(i,x+1))  
        return row
    
    def setter(self, i , j , val):
        si = self.rsi[i-1] -1
        while True:
            if self.ci[si] == j:
                # update the value and return
                self.aa[si] = val
                return
            if self.ci[ self.pne[si] - 1] > j or (self.pne[si] )  == 0  :
                # append the value
                self.aa = np.append(self.aa, val)
                self.pne = np.append(self.pne, self.pne[si])
                self.ci = np.append(self.ci, j)
                self.pne[si] = len(self.aa)
                return
            if self.pne[si] == 0:

                break
            si = self.pne[si] -1

    def setrow(self,i,row):
        for c in range(0, self.n ):
            self.setter(i, c+1, row[c] )
    
    def gaussEleimation(self):
        # Assuming A is a square matrix
        m = self.n
        for i in range(1,m):
            for j in range(i+1,m+1):
                #b[j] = b[j] - A[j,i] * b[i] / A[i,i]
                self.setrow(j, self.getrow(j) - self.getter(j,i) * self.getrow(i) / self.getter(i,i) )
        #Back substitution, let the solution be x = b
        # x = np.ones(3)
        # for i in reversed(range(m)):
        #     sum = 0
        #     for j in range(i+1,m):
        #     sum += A[i,j] * x[j]
        #     x[i] = (b[i] - sum )/A[i,i]
        # return x
    
            
    
    def pMatrix(self):
        for i in range(self.n):
            for j in range(self.n):
                print(self.getter(i+1, j+1), end=" ")
            print("\n")
    
sp = Sparse()
sp.setrow(4, [1,2,3,4789798])
sp.pMatrix()