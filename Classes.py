import tabulate, copy, os, sys
from PIL import Image
from rich.console import Console
from io import StringIO
from Classes import *


global mode, path; mode, path = False, 'AbstractCats';

def ColorString(str, style):
    buffer = StringIO()
    console = Console(file=buffer, force_terminal=True)
    console.print(str, style=style, end='')
    str = buffer.getvalue()
    return str


class Gene:
    def __init__(self, effects, type, char, hex, rsv = True, z = 100):
        global path;
        self.effects    = effects
        self.type       = type
        self.rsv        = rsv
        char            = ColorString(char, f'{hex} r')
        self.char       = char      
        self.z          = z
        self.image      = Image.open(f'./{path}/{self.effects}_{self.type}.png') 

    def __mul__(one, two):
        if one.effects == two.effects:
            if one.rsv == False:
                return one
            elif two.rsv == False:
                return two
            else: 
                return two
        else:
            raise TypeError("Type does not match.")

    def __str__(self, modeIn = None):  
        global mode
        modeThis = mode
        if modeIn == None:...
        else: modeThis = modeIn

        if not modeThis:
            return self.char
        else:
            return f"{self.char}: {self.type} {self.effects}"
        
    def toString(self, modeIn = None): return self.__str__(modeIn)
    def __repr__(self): return self.__str__()
    

class Parent:
    def __init__(self, setOne, setTwo, Extra = None):
 
        # Input validation
        if len(setOne) != len(setTwo): raise ValueError('Gene sets are not the same length.')
        self.visible = [] 
        for x in range(len(setOne)):
            if setOne[x].effects != setTwo[x].effects:
                raise TypeError(f'{setOne[x]} and {setTwo[x]} at index {x} are not the same type.')
            else:
                self.visible.append(setOne[x] * setTwo[x])

        self.setOne = setOne
        self.setTwo = setTwo
        self.face   = self.step(setOne, setTwo)
        self.extra  = Extra
        
    def layers(self):
        return self.visible + self.extra

    def step(self, setOne, setTwo):
        l = len(setOne)
        counter = []
        tile = []
        lists = setOne, setTwo

        # print(l)
        for i in range(l): counter.append(0)

            
        def binCounter(counter, x):
            if counter[x] == 0:
                counter[x] = 1
                return counter
            else:
                counter[x] = 0
                if x+1 < len(counter):
                    return binCounter(counter, x+1)
                else: return counter

        for i in range(2**l):
            this = []
            for i in range(l):
                c = copy.deepcopy(counter)
                c.reverse()
                this.append( lists[int(c[i])][i] )
            tile.append(this)
            # print(counter, this)

            counter = binCounter(counter, 0)


        
        that = []
        for each in tile:
            st = ''
            for s in each:
                st += str(s)

            that.append(st)


        # print(counter, ' '.join(that))
        return tile


        #if len(setOne) == 1: return this
        #return this + self.step(setOne[1:], setTwo[1:])
        
    
def MakeGene(effects, dom, res, char,         hexDom, hexRes, z):
    R = Gene(effects, dom,      char.upper(), hexDom,  False, z);
    r = Gene(effects, res,      char.lower(), hexRes,  True,  z);
    return [R, r];



# Humans
import random

def rng(D, r, P = 0.5):
    return r if P > random.random() else D