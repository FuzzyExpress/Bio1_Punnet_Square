import tabulate, copy, os, sys
from PIL import Image
from rich.console import Console
from io import StringIO

global mode, path;
from Classes import *

os.chdir(os.path.dirname(__file__))


# Start of config.
# Instructions:
# Define PTop and PSide by end of file.


# Human Gene Examples

UseCats = True

if not UseCats:   # see Cats for instructions
    path = 'Abstract'

    E = Gene('Eyes', 'Blue',    'E', '#0099ff', False)
    e = Gene('Eyes', 'Purple',  'e', '#6600cc', True )

    H = Gene('Hair', 'Pink',    'H', '#ff99ff', False, 200)
    h = Gene('Hair', 'Green',   'h', '#00ff00', True,  200)

    F = Gene('Face', 'Soft',    'F', '#999999', False)
    f = Gene('Face', 'Sharp',   'f', '#ffffff', True )

    S = Gene('Skin', 'Light',   'S', '#f2e6d9', False, 0)
    s = Gene('Skin', 'Dark',    's', '#604020', True,  0)


    # Human Parent Examples
    #Top = Parent([E, H], [e, h])
    #PTop = Parent([E, H, S], [e, h, s])
    PTop  = Parent([E, H, F, S], [e, h, f, s])
    PSide = Parent([E, H, F, S], [e, h, f, s])


# Car Gene Examples
if UseCats:
    # Relative folder for images
    # stock options: 'AbstractCats' 'Abstract'
    path = 'AbstractCats'

    # you can define traits with the make gene function.
    #   First spot is for the effect, 2nd for Dominant, 3rd for Recessive 
    #   4th is the the letter, 5th & 6th are table colors, and last is Z depth.
    #   when compositing final images, layers are sorted by Z. 
    C, c = MakeGene('Eyes', 'Yellow', 'Green', 'C', '#ffff00', '#99ff33', 130)

    # or by defining both parts of a gene
    S = Gene('Stripes', 'Yes',  'S', '#f2e6d9', False, 5)
    s = Gene('Stripes', 'No',   's', '#604020', True,  5)

    W = Gene('Wiskers', 'Long',   'W', '#cccccc', False, 200)
    w = Gene('Wiskers', 'Short',  'w', '#999999', True,  200)

    E = Gene('Ears', 'Fluffy',  'E', '#ffffff', False, 180)
    e = Gene('Ears', 'NoFluf',  'e', '#777777', True,  180)

    F = Gene('Face', 'Gray',    'F', '#808080', False, 0)
    f = Gene('Face', 'Orange',  'f', '#ff6600', True,  0)

    N = Gene('Nose', 'Pink',   'N', '#ff66ff', False, 10)
    n = Gene('Nose', 'Dark',   'n', '#660066', True,  10)


    # Cat Parent Examples
    # PTop  = Parent([C, S, W, E, F, N], [c, s, w, e, f, n])
    # PSide = Parent([C, S, W, E, F, N], [c, s, w, e, f, n])

    PTop  = Parent([C, W, E, F, N], [c, w, e, f, n])
    PSide = Parent([C, W, E, F, N], [c, w, e, f, n])

    # if you want to make a smaller square by dropping genes 
    #   with images need to make correct characters, you can 
    #   put the desired gene in the `extra` list.
    # redefining exiting variables overwrite previous ones.
    PTop  = Parent([C, W, E, F], [c, w, e, f])
    PSide = Parent([C, W, E, F], [c, w, e, f])
    # PSide = Parent([c, w, e, f, n], [c, w, e, f, n])

    extra = [N]

# Example random parents generator
RNG = False
if RNG:

    RNGT = [[], []]
    RNGS = [[], []]

    # Cats with 5 genes
    rngs = [[C, W, E, F, N], [c, w, e, f, n]]

    for x in range(5):
        RNGT[0].append(rng(rngs[0][x], rngs[1][x]))
        RNGT[1].append(rng(rngs[0][x], rngs[1][x]))
        RNGS[0].append(rng(rngs[0][x], rngs[1][x]))
        RNGS[1].append(rng(rngs[0][x], rngs[1][x]))

    print(RNGT, RNGS, sep='\n')

    PTop  = Parent(RNGT[0], RNGT[1])
    PSide = Parent(RNGS[0], RNGS[1])

