import numpy as np
import xlrd


xls_file= xlrd.open_workbook('test1.xls')#get file ...... xls_file is the object created first ..... xlrd.open_workbook is command defined in xlrd package
sheet=xls_file.sheet_by_name('Sheet1')#get in file .... xls_file is now inside memory ... define a sheet object ...operate on file created with function sheet by nanme........sheet 1 is the naem of the sheet in the file
sheet=xls_file.sheet_by_index(0) #open sheet by index.....

column_number=sheet.ncols
row_number=sheet.nrows

def counter(): # begin counting from zero
    count=np.array([])
    ap=-1
    for i in range (row_number):
        for j in range(column_number):
            ap+=1
            count=np.append(count,ap)
    return count

def value(i,j): # calculate the value from sheet
    x=sheet.cell(i,j).value #read cell value....sheet is the object
    return x

def set_element_vec(): #set element value in element vector
    x=np.array([])
    for i in range(row_number):
        for j in range(column_number):
            if sheet.cell(i,j).value != 0:
                x=np.append(x,sheet.cell(i,j).value)
            else:
                pass
    return x

element_vector=set_element_vec()

def pos_index_next_element(): # set index of next element in element vector in PNE array
    k=np.array([])#PNE
    x=np.array([])#EV
    count = 1
    for i in range( row_number):
        for j in range( column_number):
            if value(i,j) != 0: 
                if j!=row_number:
                    k=np.append(k,count)
                    count+=1
        if (j==row_number) :
            k=np.append(k,0)
            count+=1
    return k

pne=pos_index_next_element()

def getting_column_vector(): # set values of column in column index vector
    y=np.array([])
    for i in range(row_number):
        for j in range(column_number):
            if sheet.cell(i,j).value != 0:
                y=np.append(y,j)
            else:
                pass
    return y

column_vector=getting_column_vector()

def getting_row_starting_index(): #set row starting index vector
    ev=np.array([])
    rsi=np.array([])
    for i in range( row_number):
        s=0
        m=0
        for j in range(column_number):
            if value(i,j) != 0:
                ev=np.append(ev,value(i,j))
                s+=1
            if s == 1 and m==0:
                rsi=np.append(rsi,(len(ev)-1))
                m+=1
    return rsi    

RSI=getting_row_starting_index()    

class Sparse():
    def __init__(self):
        # index              0  1  2  3  4  5  6   7  8  9  10     
        self.aa =  np.array([1, 5, 6, 7, 8, 2, 9, 10, 3, 11, 4])
        self.pne = np.array([2, 3, 4, 0, 6, 7, 0,  9, 0, 11, 0])
        self.ci =  np.array([1, 2, 3, 4, 1, 2, 4,  1, 3,  1, 4])
        self.rsi = np.array([1, 5, 8, 10])
        self.n = 4

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
            if val == 0 and self.getter(i,j)==0:
                break     
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
                # possible buggy
                if  self.ci[int(self.rsi[i-1 ])]>j:
                    self.rsi[i-1]=len(self.aa)
                return
            if self.pne[si] == 0:
                break
            si = self.pne[si] -1

    def setrow(self,i,row):
        for c in range(0, self.n ):
            self.setter(i, c+1, row[c] )
    
    def gaussEleimation(self):
        # Assuming A is a square matrix
        m = self.r
        for i in range(1,m):
            for j in range(i+1,m+1):
                self.setrow(j, self.getrow(j) - self.getter(j,i) * self.getrow(i) / self.getter(i,i) )
        #Back substitution, let the solution be x = ones(5)
        x = np.ones(self.r)
        for i in reversed(range(1, self.r + 1)):
            sum = 0
            for j in range(i+1, self.r + 1):
                sum += self.getter(i,j) * x[j -1]
            x[i-1] = ( self.getter(i, self.n) - sum )/ self.getter(i,i)
        return x
    
            
    
    def pMatrix(self):
        for i in range(self.r):
            for j in range(self.n):
                print(self.getter(i+1, j+1), end=" ")
            print("\n")
    
sp = Sparse()
# print(pne )
sp.n=column_number
sp.r=row_number
sp.aa = element_vector
sp.pne = np.array([], dtype="int")


# pne ko sahi kara hai
for i in range(len(pne)):
    if pne[i] == 0:
        sp.pne = np.append(sp.pne, [0])
    else:
        sp.pne = np.append(sp.pne, int(pne[i] + 1) )

sp.ci = np.array( column_vector +1, dtype="int")
sp.rsi = np.array(  RSI +1 , dtype="int")

sp.pMatrix()
x = sp.gaussEleimation()

print("\nELEMENT VECTOR:",sp.aa)
print("\nColumn vector::",sp.ci)
print("\nPNE::::::::::::",sp.pne)
print("\nRSI::::::::::::",sp.rsi)
print("\n\nANSWER:::::::::",x)