import re
import numpy as np
from .utilities import is_number
from pyevtk.hl import pointsToVTK

class dataslice:
    ''' A data slice object.
        
    Attributes:
        num: the slice number to be loaded
    ''' 
    
    def __init__(self,num):
        '''Return a dataslice object focused on the *num* time slice.'''

        self.num=num
        self.filename="p.{:02d}".format(num)

        ## open file and read data
        with open(self.filename,"r") as f:
            firstline=f.readline()
            secondline=f.readline()
            sumnumber=f.readline()
        
            ## read the simulation parameters until the TIME variable
            self.params={}
            name=f.readline()
            while name.strip()!="TIME":
                self.params[name.strip()]=f.readline().strip()
                name=f.readline()
            ## read the value of TIME
            self.params[name.strip()]=f.readline().strip()
                
            ## read the list of field names
            cols=list()
            for line in f:
                if is_number(line.strip()):
                    break
                else:
                    cols.append(line.strip())
            self.ncols=len(cols)

            ## read the data as one big vector                
            vectordata=[float(line.split("#",1)[0])]+[float(line.split("#",1)[0]) for line in f]
        
        self.nparticles=int(len(vectordata)/self.ncols)
        
        tmp=np.asarray(vectordata).reshape((self.nparticles,self.ncols))

        self.data={cols[i]:np.ascontiguousarray(tmp[:,i]) for i in range(len(cols))}

    def list_cols(self):
        ''' List the column names from the SPHC output file.'''
        for k in self.data.keys():
            print(k)
    

    def ToVTK(self,outname):
        ''' Convert data of current time slice to VTK format.'''
        return pointsToVTK(outname+"{}".format(self.num),self.getX(),self.getY(),self.getZ(),self.data)
        
    def get(self,colname):
        ''' Return the numpy array for the data column *colname*.'''
        return self.data["colname"]

    def getX(self):
        ''' Return the numpy array of particle position in the X-direction.'''
        return next( v for k,v in self.data.items() if k.startswith('X'))
    
    def getY(self):
        '''Return the numpy array of particle position in the Y-direction, if
problem dimension is grater than 1. Otherwise, return an array of
zeroes of the length of the particles.

        '''
        if int(self.params["Dimension"]) > 1:
            return next( v for k,v in self.data.items() if k.startswith('Y'))
        else:
            return self.getX()*0.


    def getZ(self):
        '''Return the numpy array of particle position in the Z-direction, if
        problem dimension is grater than 1. Otherwise, return an array
        of zeroes of the length of the particles.

        '''
        if int(self.params["Dimension"]) > 2:
            return next( v for k,v in self.data.items() if k.startswith('Z'))
        else:
            return self.getX()*0.



    
    
        
        

