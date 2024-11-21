import tabulate, copy, os, sys
from PIL import Image
from rich.console import Console
from io import StringIO
from Classes import *


os.chdir(os.path.dirname(__file__))

# Import Config!
from Config import * 


print('Parent  Top:',  PTop.visible)
print('Parent Side:', PSide.visible)

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

TableTop  = Top
TableSide = Side


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
table = '   ' + tabulate.tabulate(TSquare, tablefmt="rounded_grid").replace('\n', '\n   ')
print(table)
file = open('./out.txt', 'w')
print(table, file=file)


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
offset = (round(len(Side)*width/2), 0)
parTile = (offset[0], offset[0])

ImageSquare = Image.new('RGBA', (len(Top)*width+offset[0], len(Side)*height))

ImageSquare.paste( CompileChar(PTop.visible + extra, parTile, False),  (0, 0) )
ImageSquare.paste( CompileChar(PSide.visible + extra, parTile, False), (0, offset[0]) )

for u in range(len(Square)):
    for v in range(len(Square[u])):
        tile = CompileChar(Square[u][v] + extra, (width, height))
        # print(f'Building Image; Tile: {Square[u][v]}')
        ImageSquare.paste( tile, (u*width+offset[0], v*height+offset[1]), tile )

print('Done! Showing Image.')
ImageSquare.show()

exit()
i = Image.open('')
i.resize()


# Square[2][2][2].image.show()