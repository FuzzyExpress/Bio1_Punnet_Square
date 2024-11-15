import tabulate, copy, os, sys
from PIL import Image
from rich.console import Console
from io import StringIO

os.chdir(os.path.dirname(__file__))
global mode; mode = False

def ColorString(str, style):
    buffer = StringIO()
    console = Console(file=buffer, force_terminal=True)
    console.print(str, style=style, end='')
    str = buffer.getvalue()
    return str


class Gene:
    def __init__(self, effects, type, char, hex, rsv = True, z = 100):
        self.effects    = effects
        self.type       = type
        self.rsv        = rsv
        char            = ColorString(char, f'{hex} r')
        self.char       = char      
        self.z          = z
        self.image      = Image.open(f'./Images/{self.effects}_{self.type}.png') 

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
    def __init__(self, setOne, setTwo):
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
        
    

...

E = Gene('Eyes', 'Blue',    'E', '#0099ff', False)
e = Gene('Eyes', 'Purple',  'e', '#6600cc', True )

H = Gene('Hair', 'Pink',    'H', '#ff99ff', False, 200)
h = Gene('Hair', 'Green',   'h', '#00ff00', True,  200)

F = Gene('Face', 'Soft',    'F', '#999999', False)
f = Gene('Face', 'Sharp',   'f', '#ffffff', True )

S = Gene('Skin', 'Light',   'S', '#f2e6d9', False, 0)
s = Gene('Skin', 'Dark',    's', '#604020', True,  0)

#Top = Parent([E, H], [e, h])
#PTop = Parent([E, H, S], [e, h, s])
PTop  = Parent([E, H, F, S], [e, h, f, s])
PSide = Parent([E, H, F, S], [e, h, f, s])

print(PTop.visible)
print(PSide.visible)

# Top  = [[E], [e]]
# Top  = [[E, H], [E, h], [e, H], [e, h]]
# Side = [[E, H], [E, h], [e, H], [e, h]]
# Side = Top.copy

Top  = PTop.face
Side = PSide.face

Square = []

def Combo(x, y):
    tile = []
    for u in x:
        for v in y:
            try:
                tile.append(u*v)
            except TypeError:...

    return tile       


for x in Top:
    row = []
    for y in Side:
        row.append(Combo(x, y))

    Square.append(row)

def table(Table):
    Table = []
    for each in Top:
        row = [] #''
        for item in each:
            row.append(item)
            # row += item
        Table.append(row)
    return Table

TableTop  = table(Top)
TableSide = table(Side)


combos = {}
for u in Square: 
    for v in u:
        try:
            if v == None: continue
            key = []
            for i in v:
                key.append(i.toString(True))
            key = ' • ' + ',\t'.join(key)
            combos[key] += 1
        except: combos[key] = 1;


TSquare = copy.deepcopy(Square)

TSquare.insert(0, TableTop)
TSquare[0].insert(0, None)
for x in range(len(TSquare)-1):
    TSquare[x+1].insert(0, TableSide[x])


for u in range(len(TSquare)):
    for v in range(len(TSquare[u])):
        if TSquare[u][v] == None: TSquare[u][v] = 'HI!'; continue;
        tile = ''   
        for each in TSquare[u][v]:
            if u == 0 or v == 0: tile += '\033[1m'
            tile += each.toString()
        TSquare[u][v] = tile

print(ColorString("Punnet Square:", 'b'))
print('   ' + tabulate.tabulate(TSquare, tablefmt="rounded_grid").replace('\n', '\n   '))


print(ColorString("\nTrait Counts:", 'b'))
for each in combos:
    print(f'{each}:\t{combos[each]},\t{ round(( combos[each] / ( len(PTop.face)*len(PTop.face) ) ) * 100, 1) }%')



# Pillow Image Making

Images = {}

def CompileChar(tile, size, compile = True):
    tile.sort(key=lambda gene: gene.z, reverse=False)

    try:
        if not compile: raise Exception("Compile Disabled")
        return Images[str(tile)]

    except:
        print(f'Building Tile: {tile}')

        base = Image.new('RGBA', size)
        for w in tile:
            i = w.image.resize(size)
            base.paste(i, (0,0), i)
        if compile:
            Images[str(tile)] = base
        return base

# tiles:
width, height = 100, 100
offset = (round(len(Top)*width/2), 0)
parTile = (offset[0], offset[0])

ImageSquare = Image.new('RGBA', (len(Top)*width+offset[0], len(Side)*height))

ImageSquare.paste( CompileChar(PTop.visible, parTile, False),  (0, 0) )
ImageSquare.paste( CompileChar(PSide.visible, parTile, False), (0, offset[0]) )

for u in range(len(Square)):
    for v in range(len(Square[u])):
        # print(f'Building Image; Tile: {Square[u][v]}')
        tile = CompileChar(Square[u][v], (width, height))
        ImageSquare.paste( tile, (u*width+offset[0], v*height+offset[1]), tile )

print('Done! Showing Image.')
ImageSquare.show()

exit()
i = Image.open('')
i.resize()


# Square[2][2][2].image.show()