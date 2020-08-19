import xlrd
import numpy as np


xls_file= xlrd.open_workbook('sample_question.xls')#get file ...... xls_file is the object created first ..... xlrd.open_workbook is command defined in xlrd package
#xls_file= xlrd.open_workbook('test.xls')#get file ...... xls_file is the object created first ..... xlrd.open_workbook is command defined in xlrd package

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
    for i in range(5):
        for j in range(6):
            if value(i,j) != 0: 
                if j!=5:
                    k=np.append(k,count)
                    count+=1
        if (j==5) :
            k=np.append(k,0)
            count+=1
    return k

pne=pos_index_next_element()

def getting_column_vector(): # set values of column in column index vector
    y=np.array([])
    for i in range(5):
        for j in range(6):
            if sheet.cell(i,j).value != 0:
                y=np.append(y,j)
            else:
                pass
    return y

column_vector=getting_column_vector()

def getting_row_starting_index(): #set row starting index vector
    ev=np.array([])
    rsi=np.array([])
    for i in range(5):
        s=0
        m=0
        for j in range(6):
            if value(i,j) != 0:
                ev=np.append(ev,value(i,j))
                s+=1
            if s == 1 and m==0:
                rsi=np.append(rsi,(len(ev)-1))
                m+=1
    return rsi    

RSI=getting_row_starting_index()                    

class Sparse(): # class defined for operation on vectors
    def __init__(self):
        # index              0  1  2  3  4   5    6    7  8  9  10   11  12 13   
        # location           1  2  3  4  5   6    7    8  9  10  11  12  13 14  15  
        self.aa =  np.array([1, 5, 6, 7, 8, 2, 9, 10, 3, 11, 4])
        self.pne = np.array([1, 2, 3, 0, 5, 6, 0,  8, 0, 10, 0])
        self.ci =  np.array([0, 1, 2, 3, 0, 1, 3,  0, 2,  0, 3])
        self.rsi = np.array([0, 4, 7, 9])
        self.n = 4
        self.r = 4
        

    def getter(self, i, j): # WORKING
        si = int(self.rsi[i]) #starting index m kahan se start karunga
        while True:
            if self.ci[si] == j: # column ki value at given index
                return self.aa[si]
            if self.pne[si] == 0:
                break
            si = int(self.pne[si])   
        return 0
    
    def getrow(self,i): # WORKING
        row = np.array([])
        for x in range(self.n):
            row = np.append(row,self.getter(i,x))  
        return row
    
    def setter(self, i , j , val): # WORKING
        index=int(self.rsi[i])  #index starting from one
        while True:
            if val==0 and self.getter(i,j)==0:
                break
            if  self.ci[index] == j:
                self.aa[index] = val #update the value and get out of funvction after execution
                break
            if  self.ci[ self.pne[index] ] > j or (self.pne[index] )  == 0 : #for appending the value i will do this
                self.aa= np.append(self.aa,val)
                self.pne=np.append(self.pne,index)
                self.ci=np.append(self.ci,j)
                self.pne[index-1]=len(self.aa)-1
                if  self.ci[int(self.rsi[i])]>j:
                    self.rsi[i]=len(self.aa)-1
                break
            if self.pne[index] == 0:    
                break
            index = int(self.pne[index])
        return             
    
    #what set row is doing it is taking a row and calls setter function some n times and modifies the 3 vectors
    
    def setrow(self,i,row): # WORKING
        for x in range(self.n):
            self.setter(i,x,row[x])
    

    def pMatrix(self): # WORKING
        A=np.empty((self.r,self.n))
        for i in range(self.r):
            for j in range(self.n):
                A[i][j] = self.getter(i,j)
        print(A)
    
    def gaussEleimation(self):
            # Assuming A is a square matrix
        m = self.n
        for i in range(self.r - 1):
            for j in range(i + 1, self.r):
                #b[j] = b[j] - A[j,i] * b[i] / A[i,i]
                self.setrow(j, self.getrow(j) - self.getter(j,i) * self.getrow(i) / self.getter(i,i) )
        #Back substitution, let the solution be x = b
        # x = np.ones(rows)
        # for i in reversed(range(column)):
        #     sum = 0
        #     for j in range(i+1,m):
        #     sum += A[i,j] * x[j]
        #     x[i] = (b[i] - sum )/A[i,i]
        # return x
    
sp = Sparse()
# sp.n=column_number
# sp.r=row_number
# sp.aa = element_vector
# sp.pne = pne
# sp.ci = column_vector
# sp.rsi = RSI
#sp.gaussEleimation()

sp.pMatrix()        

# sp.setter(2,0,0)
# sp.setter(2,1,3)
# sp.setter(2,2,6)
# sp.setter(2,2,7)
#sp.setter(2,3,8)
#sp.setter(2,5,3)

sp.setrow(2,[1,2,3,4])
sp.pMatrix()        
