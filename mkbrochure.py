#!/usr/bin/env python3
import os
import fitz
import argparse

def showPDFonNewPage(page, src, pno, pos):
    spage = src[pno]

    if pos == 1:
        rect = page.rect
        rect.x1 = rect.x1/2
    elif pos == 2:
        rect = page.rect
        rect.x0 = rect.x1/2
    else:
        rect = page.rect


    if spage.rotation == 0:
        page.showPDFpage(rect, src, pno)
    else:

        # This handles images where the image is not stored as displayed, but the page rotation is set.
        # First the page is rendered into a pixmap at a resolution close to the image resolution and then
        # then the pixmap is shown on the new page
        imgList = spage.getImageList()
        if len(imgList) != 1:
            raise RuntimeError("Encountered a page with more than one image and rotation. Contact the developer to resolve this issue!")
        img = imgList[0]
        print(img)
        lmax = max(img[2], img[3])

        sw, sh = pageSize(spage)

        #pixmap = spage.getPixmap(colorspace=fitz.csGRAY)
        scale = lmax/ max(sw, sh)
        mat = fitz.Matrix(3.0, 3.0)
        pm = spage.getPixmap( matrix = mat, colorspace=fitz.csGRAY)
        page.insertImage(rect, pixmap = pm)
        print("extracted pixmap with res : width = {}, height = {}".format(pm.width, pm.height))

def pageSize(page):
    " Width and Height of the page. """
    dims = page.bound()[2:]
    return dims

def pageOrientation(page):
    """ Get the orientation for a pymupdf page object."""
    sw, sh = pageSize(page)
    print('page detected with width {} x height {}'.format(sw, sh))
    if sw < sh:
        return "portrait"
    else:
        return "landscape"

parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input file containing A4 pages")
parser.add_argument("--out", help="Output file")
parser.add_argument("--offset", type=int, help="Control the number of empty pages at front")
args = parser.parse_args()

infile_path = args.input
outfile_path = args.out if args.out is not None else ".".join(infile_path.split(".")[:-1])+"-A3bro.pdf"

doc = fitz.open()

pagesize="A3-L" # landscape A3 page
width, height = fitz.PaperSize(pagesize)

src = fitz.open(infile_path)
Npages = src.pageCount
print("pages in input = ", Npages)

# find the correct page ordering for the brochure
Nsheets = int( (Npages+3)/4 )
print("number of papers needed = ", Nsheets)
Nempty = int( (Nsheets*4) - Npages )
print("number of empty pages to fill = ", Nempty)

# calculate number of empty pages at the start/end
if Nempty in [0, 1]:
    NemptyAtBegin = 0
else:
    NemptyAtBegin = 1
if Nempty == 0:
    NemptyAtEnd = 0
else:
    NemptyAtEnd = Nempty - NemptyAtBegin

if args.offset:
    NemptyAtEnd -= args.offset
    NemptyAtBegin += args.offset

if Npages == 2:
    NemptyAtBegin = 0
    NemptyAtEnd = 0

print("number of empty pages at start/end = {}, {}".format(NemptyAtBegin, NemptyAtEnd))

pages = []

# start with empty pages
pages += [-1]*NemptyAtBegin
pages += [n for n in range(Npages)]
pages += [-1]*NemptyAtEnd
Ntot = len(pages)
print("number of pages including empty ones = ",Ntot)
print("pages = ", pages)

# shuffle pages for brochure
s = int(Ntot/2)

if Npages == 2:
    pages_order = [0, 1]
else:
    pages_order = [-1]*Ntot
    for i in range(1,Nsheets+1):
        b = [0]*4
        b[0] = s + 2 - 2*i
        b[1] = s - 1 + 2*i
        b[2] = s + 2*i
        b[3] = s + 1 - 2*i
        print("b = ",b)
        for j in range(1,5):
            index = 4*(i-1)+(j-1)
            print("index = ", index)
            print("b[j-1] = ", b[j-1])
            print("j = ",j)
            n =  pages[b[j-1]-1]
            pages_order[index] = n

is_first_subpage = True
for n in pages_order:
    is_empty_page = n < 0 # by convetion the empty pages were assigend a -1
    is_save_incremental = doc.pageCount > 0 # save incremental after first page
    if is_first_subpage:
        pos = 1
        is_first_subpage = False
        page = doc.newPage(-1, width = width, height = height)
    else:
        pos = 2
        is_first_subpage = True
        page = doc[-1]

    if not is_empty_page:
        showPDFonNewPage(page, src, n, pos=pos)

    doc.save(outfile_path,
             #garbage = 4, # eliminate duplicate objects
             deflate = True, # compress stuff where possible
             incremental=is_save_incremental)

    doc = fitz.open(outfile_path)
