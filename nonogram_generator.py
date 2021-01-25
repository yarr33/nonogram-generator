# nonogram generator
# by yarr
#
# please make sure that you choose the right file
#
# LoL
#

import tkinter as tk
from tkinter import filedialog
from cv2 import imread, rotate, cv2
from PIL import Image, ImageDraw, ImageFont
import math
import os

pageSize = 4

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

vCodeOffset = 0
hCodeOffset = 0

print(end = "reading image... ")

image = imread(file_path)

print("done")

print(end = "scanning image... ")

height, width, channels = image.shape

result = []
y = 0

maxOffset = 0

for yz in image:
    x = 0
    row = []
    enc = 0
    for xz in yz:
        black = (list(xz) == [0,0,0])
        if(black):
            enc += 1
        else:
            if(enc):
                row.append(enc)
            enc = 0
        #print(end=["⬜","⬛"][int(black)])
        x += 1
    if(enc):
        row.append(enc)
    if(len(row) > maxOffset):
        maxOffset = len(row)
    result.append(row)
    y += 1

vCodeOffset = maxOffset

image = rotate(image, cv2.ROTATE_90_CLOCKWISE)

resultRot = []
y = 0

height, width, channels = image.shape

maxOffset = 0

for yz in image:
    x = 0
    row = []
    enc = 0
    for xz in yz:
        black = (list(xz) == [0,0,0])
        if(black):
            enc += 1
        else:
            if(enc):
                row.append(enc)
            enc = 0
        #print(end=["⬜","⬛"][int(black)])
        x += 1
    if(enc):
        row.append(enc)
    if(len(row) > maxOffset):
        maxOffset = len(row)
    resultRot.append(row)
    y += 1

hCodeOffset = maxOffset

print("done")

print(end="rendering image... ")

sideOffset = 50 * pageSize
topOffset = 60 * pageSize

if( hCodeOffset <= vCodeOffset):
    pixelSize = int( ( (595 * pageSize - sideOffset * 2) / pageSize) / (height + vCodeOffset))
else:
    pixelSize = int( ( (842 * pageSize - topOffset * 2) / pageSize) / (width + hCodeOffset))

topCodeOffset = hCodeOffset * pixelSize * pageSize
sideCodeOffset = vCodeOffset * pixelSize * pageSize

fnt = ImageFont.truetype('arial.ttf', 20 * pageSize)
smlfnt = ImageFont.truetype('arial.ttf', 13 * pageSize)
smlnmfnt = ImageFont.truetype('arial.ttf', math.floor(13 * pageSize * pixelSize/18))

img = Image.new('RGB', (595 * pageSize, 842 * pageSize), color = (240,240,240))
imgDraw = ImageDraw.Draw(img)

index = 0

for c in range(sideOffset + sideCodeOffset, sideOffset + sideCodeOffset + height * pixelSize * pageSize + 1, pixelSize * pageSize):
    imgDraw.line([(c,topOffset),(c,topOffset + topCodeOffset + width * pixelSize * pageSize)], fill=(0,0,0), width=1 * pageSize)
    if( index < height):
        numList = resultRot[index]
        if (len(numList)):
            for numIndex in range(len(numList)):
                w, h = imgDraw.textsize(str(numList[numIndex]), font=smlnmfnt)
                imgDraw.text((c - w/2 + pixelSize / 2 * pageSize, topOffset + topCodeOffset - pixelSize * pageSize * (numIndex + 1)), str(numList[numIndex]), font=smlnmfnt, fill=(0,0,0))
        index+=1

index = 0

for c in range(topOffset + topCodeOffset,topOffset + topCodeOffset + width * pixelSize * pageSize + 1, pixelSize * pageSize):
    imgDraw.line([(sideOffset, c),(sideOffset + sideCodeOffset + height * pixelSize * pageSize, c)], fill=(0,0,0), width=1 * pageSize)
    if( index < width):
        numList = list(reversed(result[index]))
        if (len(numList)):
            for numIndex in range(len(numList)):
                w, h = imgDraw.textsize(str(numList[numIndex]), font=smlnmfnt)
                imgDraw.text((sideOffset + sideCodeOffset - pixelSize * pageSize * (numIndex + 1) - w/2 + (pixelSize * pageSize / 2), c - h/2 + pixelSize / 2 * pageSize), str(numList[numIndex]), font=smlnmfnt, fill=(0,0,0))
        index+=1


imgDraw.text((0, 0), os.path.splitext(os.path.basename(file_path))[0] + " - nonogram   page size "+str(pageSize), font = fnt ,fill=(0,0,0))

imgDraw.text((0, 842 * pageSize - 15 * pageSize), "Generated using yarr's image-to-nonogram tool", font = smlfnt ,fill=(0,0,0))

print("done")

print(end="saving image...")

img.save(os.path.dirname(os.path.abspath(file_path)) + "\\" + os.path.splitext(os.path.basename(file_path))[0] + "-nonogram.png")

print("done")

print("image saved in " + os.path.dirname(os.path.abspath(file_path)) + "\\" + os.path.splitext(os.path.basename(file_path))[0] + "-nonogram.png")
