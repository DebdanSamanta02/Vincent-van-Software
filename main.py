from customtkinter import *
from PIL import Image, ImageGrab
from tkinter import filedialog, font
from CTkToolTip import *
from CTkColorPicker import *
from CTkMessagebox import *
import math

deactivate_automatic_dpi_awareness()
set_window_scaling(1.0)  # window geometry dimensions

# root window settings
root = CTk()
root._fg_color='#DEDEDE'
root.iconbitmap('.\images\main.ico')
root.title('Vincent van Software')
root.geometry('1000x515')
set_appearance_mode('dark')

# ---------- GLOBAL VARIABLES ----------
# prev and curr represents end points of drawing variables
prev = [0,0]
curr = [0,0]

#property variables
shapeSelect = StringVar() #current shape
prevShape = StringVar() #previous shape
prevShape.set('Pen')

color = StringVar() #current color
color.set('black')

size = StringVar() #stroke-width

#setColor = StringVar()

currentText = StringVar() #text variable

fontSize = StringVar() #text-size
fontSize.set('20')

activity_list = [] #stores current activity FOR DEBUGGING ONLY
redo_list = [] #redo data
undo_list = [] #undo data

nextAct = True #maintains if current Act is finished [True=Yes, False=No]

count = 0 #debugging to maintain shapeSelect display on switching text

#widget-properties
hoverColor = '#FFB4FC'
borderColor = '#73192B'
#frameColor = '#DEDEDE'
frameColor = 'transparent'
tipDelay = 0.7

fontList = [] #stores list of Font Styles
for i in font.families():
    fontList.append(i)
fontStyle = StringVar() #stores Font Style
fontStyle.set('Arial')

# ---------- FRAME GUI -----------
#TOP frame
frame1 = CTkScrollableFrame(master=root, 
                height=45, 
                width=975, 
                fg_color=frameColor,
                bg_color=frameColor,
                orientation='horizontal',
                scrollbar_button_hover_color='#262626')
frame1.grid(row=0,column=0)
#MAIN frame
frame2 = CTkFrame(master=root, 
                height=350, 
                width=1000,
                fg_color=frameColor,
                bg_color=frameColor)
frame2.grid(row=1,column=0)
#ICONS frame (on left)
left = CTkFrame(frame1, 
                height=75, 
                width=500, 
                corner_radius=400000, 
                fg_color=frameColor,
                bg_color=frameColor)
left.grid(row=0, column=0, sticky='w')
#ICONS frame (on right)
right = CTkFrame(frame1,
            height=75, 
            width=500, 
            corner_radius=400000, 
            fg_color=frameColor,
            bg_color=frameColor)
right.grid(row=0, column=1, sticky='e')
#END frame
frame3 = CTkFrame(master=root, 
                height=60, 
                width=1000, 
                fg_color=frameColor,
                bg_color=frameColor)
frame3.grid(row=2,column=0)

#CANVAS
canvas = CTkCanvas(frame2, 
                height=400, 
                width=1000, 
                bg='white')
canvas.grid(row=0, column=0)

def buttons_on_left():
    #save
    saveimg = CTkImage(light_image=Image.open(".\images\save.jpeg"),
                       dark_image=Image.open(".\images\save.jpeg"),
                       size=(30, 30))
    save = CTkButton(left, 
                    width=8, 
                    corner_radius=80, 
                    fg_color='transparent', 
                    image=saveimg, text="",
                    command=saveImage,
                    hover_color=hoverColor,
                    border_color=borderColor,
                    border_width=2)
    save.grid(row=0,column=0,padx=4)
    save_tip = CTkToolTip(save, delay=tipDelay, message='Save\nMove window to top left of screen before Saving')

    #pen
    penimg = CTkImage(light_image=Image.open(".\images\pen.jpeg"),
                    dark_image=Image.open(".\images\pen.jpeg"),
                    size=(30, 30))
    pen = CTkButton(left, 
                    width=8, 
                    corner_radius=80, 
                    image=penimg, text="",
                    fg_color='transparent',
                    command=usePen,
                    hover_color=hoverColor,
                    border_color=borderColor,
                    border_width=2)
    pen.grid(row=0, column=1, padx=4)
    pen_tip = CTkToolTip(pen, delay=tipDelay, message='Pen')

    #eraser
    eraseimg = CTkImage(light_image=Image.open(".\images\eraser.jpeg"),
                        dark_image=Image.open(".\images\eraser.jpeg"),
                        size=(30, 30))
    eraser = CTkButton(left, 
                       width=8, 
                       corner_radius=80, 
                       fg_color='transparent',
                       image=eraseimg, 
                       text="", 
                       command=useEraser,
                       hover_color=hoverColor,
                       border_color=borderColor,
                       border_width=2)
    eraser.grid(row=0, column=2, padx=4)
    erase_tip = CTkToolTip(eraser, delay=tipDelay, message='Eraser')

    #text box
    txtimg = CTkImage(light_image=Image.open(".\images\Text.png"),
                       dark_image=Image.open(".\images\Text.png"),
                       size=(30, 30))
    txt = CTkButton(left, 
                    width=8, 
                    corner_radius=80, 
                    fg_color='transparent', 
                    image=txtimg, text="", 
                    command=writeText,
                    hover_color=hoverColor,
                    border_color=borderColor,
                    border_width=2)
    txt.grid(row=0, column=3, padx=4)
    txt_tip = CTkToolTip(txt, delay=tipDelay, message='Text Box\nGuide: Press once and click on Canvas to make a Text Box \nType Text \nOn completion, Press this button again\nPLEASE MOVE WINDOW TO TOP LEFT CORNER OF SCREEN BEFORE WRITING')

    #color selection
    clrimg = CTkImage(light_image=Image.open(".\images\colorwheel.jpeg"),
                    dark_image=Image.open(".\images\colorwheel.jpeg"),
                    size=(30, 30))
    clr = CTkButton(left, 
                    width=8, 
                    corner_radius=80,
                    fg_color='transparent', 
                    image=clrimg, 
                    text="", 
                    command=colorBox,
                    hover_color=hoverColor,
                    border_color=borderColor,
                    border_width=2)
    clr.grid(row=0,column=4,padx=4)
    clr_tip = CTkToolTip(clr, delay=tipDelay, message ='Color Selection')

    #marker
    arrimg = CTkImage(light_image=Image.open(".\images\Arrow.png"),
                    dark_image=Image.open(".\images\Arrow.png"),
                    size=(50, 50))
    dir = CTkLabel(left,
                   width=0, 
                   corner_radius=30, 
                   image=arrimg, 
                   bg_color='transparent', 
                   text="")
    dir.grid(row=0,column=5)
    dir_tip = CTkToolTip(dir, delay = 0.01, message='This doesn\'t do anything :)')

    #current color
    currcol = CTkLabel(left, 
                    corner_radius=10, 
                    fg_color=color.get(), 
                    text='CURRENTLY')
    currcol.grid(row=0, column=6)
    currcol_tip = CTkToolTip(currcol, delay=tipDelay, message='Shows CURRENTLY SELECTED color\nEraser Color is always WHITE')
    fake = CTkLabel(left, 
                    width=8, 
                    fg_color='transparent', 
                    text='')
    fake.grid(row=0, column=7)

    #shapes
    global shapeSelect
    options_shape = ['Line', 'Rectangle', 'Oval', 'Triangle', 'Hexagon', 'Diamond', 'Arrow Head']
    shape_menu = CTkOptionMenu(left, 
                        width=1, 
                        height=38, 
                        corner_radius=30, 
                        values=options_shape, 
                        variable=shapeSelect,
                        hover=True)
    shape_menu.set('Pen')
    shape_menu.grid(row=0, column=8, padx=4)
    shape_tip = CTkToolTip(shape_menu, delay=tipDelay, message='Shows Selected Shape \nAlt-Click and draw on Canvas for Spray Paint\nWhile Spray Painting, hold and drag fast for Scattered Spray and drag slow for Denser Spray')

def buttons_on_right():
    #font selector
    global fontStyle
    font_menu = CTkOptionMenu(right, 
                        width=1, 
                        height=38, 
                        corner_radius=30, 
                        values=fontList, 
                        variable=fontStyle,
                        hover=True)
    font_menu.set('Arial')
    font_menu.grid(row=0, column=0, padx=4)
    #print(fontStyle.get())
    font_tip = CTkToolTip(font_menu, delay=tipDelay, message='Select Font Style')

    #font-size
    global fontSize
    fontSizeMenu = CTkEntry(right,
                            width=80,
                            corner_radius=30,
                            textvariable=fontSize,
                            font=('Arial', 20),
                            text_color='black',
                            fg_color=frameColor,
                            bg_color=frameColor,
                            border_color=borderColor,
                            border_width=2)
    fontSizeMenu.grid(row=0, column=1, padx=4)
    fontsize_tip = CTkToolTip(fontSizeMenu, delay=tipDelay, message='Set Font Size')

    #size
    options = ['Weight(px): 01', 'Weight(px): 02', 'Weight(px): 03', 'Weight(px): 04', 'Weight(px): 05', 'Weight(px): 06', 'Weight(px): 07', 'Weight(px): 08', 'Weight(px): 09', 'Weight(px): 10', 'Weight(px): 15', 'Weight(px): 20']
    szlst = CTkOptionMenu(right, 
                        width=1, 
                        height=38, 
                        corner_radius=30, 
                        values=options, 
                        variable=size,
                        hover=True)
    szlst.set('Weight: 01')
    szlst.grid(row=0,column=2,padx=4)
    szlst_tip = CTkToolTip(szlst, delay=tipDelay, message='Select Stroke Width for Pen and Eraser')

def buttons_on_bottom():
    #undo
    undoimg = CTkImage(light_image=Image.open(".\images\goback.jpeg"),
                       dark_image=Image.open(".\images\goback.jpeg"),
                       size=(30, 30))
    undo = CTkButton(frame3, 
                    width=8, 
                    corner_radius=80, 
                    fg_color='transparent', 
                    image=undoimg, 
                    text="", 
                    command=undoFn,
                    hover_color=hoverColor,
                    border_color=borderColor,
                    border_width=2)
    undo.grid(row=0,column=0,padx=4,pady=2)
    undo_tip = CTkToolTip(undo, delay=tipDelay, message='UNDO \nGoes back one step')

    #redo
    redoimg = CTkImage(light_image=Image.open(".\images\comeback.jpeg"),
                       dark_image=Image.open(".\images\comeback.jpeg"),
                       size=(30, 30))
    redo = CTkButton(frame3, 
                    width=8, 
                    corner_radius=80, 
                    fg_color='transparent', 
                    image=redoimg, 
                    text="", 
                    command=redoFn,
                    hover_color=hoverColor,
                    border_color=borderColor,
                    border_width=2)
    redo.grid(row=0,column=1,padx=4,pady=2)
    redo_tip = CTkToolTip(redo, delay=tipDelay, message='REDO \nREDOES one step UNDO')

    #delete
    delimg = CTkImage(light_image=Image.open(".\images\delete.jpeg"),
                    dark_image=Image.open(".\images\delete.jpeg"),
                    size=(30, 30))
    dele = CTkButton(frame3, 
                    width=8,
                    corner_radius=80, 
                    fg_color='transparent', 
                    image=delimg, text="", 
                    command=clearAll,
                    hover_color=hoverColor,
                    border_color=borderColor,
                    border_width=2)
    dele.grid(row=0,column=2,padx=4,pady=2)
    del_tip = CTkToolTip(dele, delay=tipDelay, message='Clear All')

# ---------- FUNCTIONALITY ENGINE -----------
def saveImage():
    msg = CTkMessagebox(title='Vincent van Software',
                        message='Save File?', 
                        icon='info', 
                        option_1='Yes', 
                        option_2='No',
                        justify = 'center')
    ans = msg.get()
    if(ans == 'Yes'):
        fileLoc = filedialog.asksaveasfilename(defaultextension='jpeg')
        x = root.winfo_rootx() 
        y = root.winfo_rooty()
        img = ImageGrab.grab(bbox=(x, y+92, x+1255, y+599))
        img.save(fileLoc)
        img.show()
def usePen():
    shapeSelect.set('Pen')
    #color.set('black')
    canvas["cursor"] = "hand2"
def useEraser():
    shapeSelect.set('Eraser')
    #color.set('white')
    '''
    #current color
    currcol = CTkLabel(left, corner_radius=10, fg_color=color.get(), text='CURRENTLY')
    currcol.grid(row=0, column=6)
    fake = CTkLabel(left, width=8, fg_color='transparent', text='')
    fake.grid(row=0, column=7)
    currcol_tip = CTkToolTip(currcol, delay=tipDelay, message='Shows CURRENTLY SELECTED color')
    '''
def colorBox():
    chosencol = AskColor(initial_color='black', title='COLOR SELECTION')
    color.set(chosencol.get())

    #current color
    currcol = CTkLabel(left, corner_radius=10, fg_color=color.get(), text='CURRENTLY')
    currcol.grid(row=0, column=6)
    fake = CTkLabel(left, width=8, fg_color='transparent', text='')
    fake.grid(row=0, column=7)
    currcol_tip = CTkToolTip(currcol, delay=tipDelay, message='Shows CURRENTLY SELECTED color')
def getsize():
    global fontSize
    n = 0
    for i in fontSize.get():
        n *= 10
        n += (ord(i)-48)
    return n

textpaint_prevshape = StringVar()
textpaint_prevshape.set('BLANK')
def writeText():
    '''
        1. An Entry is created at mouse pointer position on canvas on pressing Text Option
        2. After writing Text on Entry and pressing Text Option again, a Text Widget is created at same position
            Text Widget is canvas.create_text(...)
    '''
    global textpaint_prevshape #stores shape before implementing text before prevShape is reset to text in next iter
    if(textpaint_prevshape.get() == 'BLANK'): #BLANK ensures that txtpaint_prevshape is not reset to text in next iters
        textpaint_prevshape.set(prevShape.get())

    global count, entry, X, Y, nextAct, redo_list, undo_list, activity_list, debug_count
    count += 1
    if(count == 2):
        count = 0
    shapeSelect.set('Text')

    if(nextAct):
        redo_list = []
        undo_list = []
        nextAct = False

    if(count == 0):
        entry.destroy()
        activity = canvas.create_text(X+35, Y+18, 
                        font=(fontStyle.get(), getsize()), 
                        fill=color.get(), 
                        text=currentText.get())
        
        undo_list.append(activity)
        redo_list.append([X+35, Y+18, color.get(), currentText.get(), (fontStyle.get(), getsize()), "", 'Text'])
        shapeSelect.set(textpaint_prevshape.get())
        #print(prevShape.get())
        currentText.set(" ")
        nextAct = True
        debug_count = 0 #same function as count

def clearAll():
    msg = CTkMessagebox(title='Vincent van Software',
                        message='Clear All?', 
                        icon='question', 
                        option_1='Yes', 
                        option_2='No',
                        justify = 'center')
    ans = msg.get()
    if(ans == 'Yes'):
        canvas.delete('all')

def undoFn():
    '''
        Activities are stored as [Int] in order, .delete(i) deletes Activity #i but cannot be recreated as such    
    '''
    global undo_list
    if undo_list:
        for i in undo_list:
            canvas.delete(i)
    undo_list = [] #clearing undo list to maintain [1] stack depth
def redoFn(): 
    '''
        stores a nested list containing data of coords., fill/outline color and shape type  
        appending the redone activity to undo_list ensures an inf. back-and-forth on undo/redo operations
    '''
    global undo_list
    if redo_list:
        if(redo_list[0][6] == 'Pen'):
            for i in redo_list:
                activity = canvas.create_polygon(i[0], i[1], 
                                                i[2], i[3], 
                                                fill=i[4], 
                                                outline=i[4], 
                                                width=i[5])
                undo_list.append(activity)
        elif(redo_list[0][6] == 'Eraser'):
            for i in redo_list:
                activity = canvas.create_polygon(i[0], i[1], 
                                                i[2], i[3], 
                                                fill=i[4], 
                                                outline=i[4], 
                                                width=i[5])
                undo_list.append(activity)
        elif(redo_list[0][6] == 'Line' ):
            for i in redo_list:
                activity = canvas.create_line(i[0], i[1], 
                                            i[2], i[3], 
                                            fill=i[4], 
                                            width=i[5])
                undo_list.append(activity)
        elif(redo_list[0][6] == 'Rectangle'):
            for i in redo_list:
                activity = canvas.create_rectangle(i[0], i[1], 
                                                i[2], i[3], 
                                                outline=i[4], 
                                                width=i[5])
                undo_list.append(activity)
        elif(redo_list[0][6] == 'Oval'):
            for i in redo_list:
                activity = canvas.create_oval(i[0], i[1], 
                                            i[2], i[3], 
                                            outline=i[4], width=i[5])
                undo_list.append(activity)
        elif(redo_list[0][6] == 'Spray'):
            for i in redo_list:
                activity = canvas.create_arc(i[0], i[1], 
                                            i[2], i[3], 
                                            fill=i[4], 
                                            outline=i[4], 
                                            width=i[5])
                undo_list.append(activity)
        elif(redo_list[0][6] == 'Text'):
            for i in redo_list:
                activity = canvas.create_text(i[0], i[1], 
                                            fill=i[2], 
                                            text=i[3], 
                                            font=i[4])
                undo_list.append(activity)
        elif(redo_list[0][6] == 'Triangle'):
            for i in redo_list:
                activity = canvas.create_polygon(i[0], i[1], 
                                                i[2], i[3], 
                                                2*i[0]-i[2], i[3],
                                                fill='', 
                                                outline=i[4], 
                                                width=i[5])
                undo_list.append(activity)
        elif(redo_list[0][6] == 'Hexagon'):
            for i in redo_list:
                d = (i[0]-i[2])**2 + (i[1]-i[3])**2
                d = math.sqrt(d)

                activity = canvas.create_polygon(i[0], i[1],
                                                i[2], i[3],
                                                i[2], i[3]+d,
                                                i[0], 2*i[3]+d-i[1],
                                                2*i[0]-i[2],i[3]+d, 
                                                2*i[0]-i[2], i[3], 
                                                fill='', 
                                                outline=i[4], 
                                                width=i[5])
                undo_list.append(activity)
        elif(redo_list[0][6] == 'Diamond'):
            for i in redo_list:
                activity = canvas.create_polygon(i[0], i[1], 
                                                i[2], i[3], 
                                                i[0], 2*i[3]-i[1], 
                                                2*i[0]-i[2], i[3], 
                                                fill='', 
                                                outline=i[4], 
                                                width=i[5])
                undo_list.append(activity)
        elif(redo_list[0][6] == 'Arrow Head'):
            for i in redo_list:
                activity = canvas.create_polygon(i[0], i[1], 
                                                i[2], i[3], 
                                                i[0], 0-2*i[1]+i[3], 
                                                2*i[0]-i[2], i[3],
                                                fill='', 
                                                outline=i[4], 
                                                width=i[5])
                undo_list.append(activity)
def paint(event):
    global prev, curr, activity_list, redo_list, undo_list, nextAct, altpaint_prevshape
    sz = 0

    if(prevShape.get() != 'Spray Paint'):
        altpaint_prevshape.set('BLANK')

    if(shapeSelect.get() != prevShape.get()):
        redo_list = []

    if(shapeSelect.get() == 'Pen'):
        if event.type == '6' and nextAct:
            nextAct = False
            activity_list = []
            redo_list = []
        elif event.type == '5':
            nextAct = True

        x, y = event.x, event.y
        curr = [x, y]
        if prev != [0,0]:
            wd = size.get()
            sz = (ord(wd[-2])-48) * 10 + (ord(wd[-1])-48)

            activity = canvas.create_polygon(prev[0], prev[1], 
                                            curr[0], curr[1], 
                                            fill=color.get(), 
                                            outline=color.get(), 
                                            width=sz)
            
            activity_list.append(activity)
            undo_list=activity_list
            redo_list.append([prev[0], prev[1], curr[0], curr[1], color.get(), sz, 'Pen'])
        prev = [0,0] if event.type == "5" else curr

        if(event.type == '5'):
            if activity_list:
                canvas.delete(activity_list.pop()) #to eliminate a colored blob in last step because next current index is not found
            if redo_list:
                redo_list.pop()
            activity_list = []

    #eraser is equivalent to pen except color is set at white, and cursor is changed to [target]
    elif(shapeSelect.get() == 'Eraser'):
        if event.type == '6' and nextAct:
            canvas["cursor"] = "target"
            nextAct = False
            activity_list = []
            redo_list = []
        elif event.type == '5':
            nextAct = True

        x, y = event.x, event.y
        curr = [x, y]
        if prev != [0,0]:
            wd = size.get()
            sz = (ord(wd[-2])-48) * 10 + (ord(wd[-1])-48)

            activity = canvas.create_polygon(prev[0], prev[1], 
                                            curr[0], curr[1], 
                                            fill='white', 
                                            outline='white', 
                                            width=sz)
            
            activity_list.append(activity)
            undo_list=activity_list
            redo_list.append([prev[0], prev[1], curr[0], curr[1], color.get(), sz, 'Pen'])
        prev = [0,0] if event.type == "5" else curr

        if(event.type == '5'):
            if activity_list:
                canvas.delete(activity_list.pop())
            if redo_list:
                redo_list.pop()
            activity_list = []

    elif(shapeSelect.get() == 'Line'):
        if activity_list:
            canvas.delete(activity_list.pop()) #ensures dynamically drawn line
        x, y = event.x, event.y
        curr = [x, y]
        if prev != [0,0]:
            wd = size.get()
            sz = (ord(wd[-2])-48) * 10 + (ord(wd[-1])-48)

            activity = canvas.create_line(prev[0], prev[1], 
                                        curr[0], curr[1], 
                                        fill=color.get(),  
                                        width=sz)
            
            activity_list.append(activity)
            undo_list=activity_list
        if(event.type == '6' and nextAct) :
            nextAct = False
            prev = curr
        if(event.type == '5'):
            redo_list.append([prev[0], prev[1], curr[0], curr[1], color.get(), sz, 'Line'])
            prev = [0,0]
            nextAct = True
            activity_list = []

    elif(shapeSelect.get() == 'Rectangle'):
        if activity_list:
            canvas.delete(activity_list.pop()) #ensures dynamically drawn rectangle
        x, y = event.x, event.y
        curr = [x, y]
        if prev != [0,0]:
            wd = size.get()
            sz = (ord(wd[-2])-48) * 10 + (ord(wd[-1])-48)

            activity = canvas.create_rectangle(prev[0], prev[1], 
                                            curr[0], curr[1], 
                                            outline=color.get(),  
                                            width=sz)
            
            activity_list.append(activity)
            undo_list=activity_list
        if(event.type == '6' and nextAct) :
            nextAct = False
            prev = curr
        if(event.type == '5'):
            redo_list.append([prev[0], prev[1], curr[0], curr[1], color.get(), sz, 'Rectangle'])
            prev = [0,0]
            nextAct = True
            activity_list = []

    elif(shapeSelect.get() == 'Oval'):
        if activity_list:
            canvas.delete(activity_list.pop()) #ensures dynamically drawn oval
        x, y = event.x, event.y
        curr = [x, y]
        if prev != [0,0]:
            wd = size.get()
            sz = (ord(wd[-2])-48) * 10 + (ord(wd[-1])-48)

            activity = canvas.create_oval(prev[0], prev[1], 
                                            curr[0], curr[1], 
                                            outline=color.get(),  
                                            width=sz)
            
            activity_list.append(activity)
            undo_list=activity_list
        if(event.type == '6' and nextAct) :
            nextAct = False
            prev = curr
        if(event.type == '5'):
            redo_list.append([prev[0], prev[1], curr[0], curr[1], color.get(), sz, 'Oval'])
            prev = [0,0]
            nextAct = True
            activity_list = []

    elif(shapeSelect.get() == 'Triangle'):
        if activity_list:
            canvas.delete(activity_list.pop()) #ensures dynamically drawn triangle
        x, y = event.x, event.y
        curr = [x, y]
        if prev != [0,0]:
            wd = size.get()
            sz = (ord(wd[-2])-48) * 10 + (ord(wd[-1])-48)

            activity = canvas.create_polygon(prev[0],prev[1],
                                            curr[0],curr[1],
                                            2*prev[0]-curr[0],curr[1],
                                            fill='',
                                            outline=color.get(),
                                            width=sz)
            
            activity_list.append(activity)

            undo_list=activity_list
        if(event.type == '6' and nextAct) :
            nextAct = False
            prev = curr
        if(event.type == '5'):
            redo_list.append([prev[0], prev[1], curr[0], curr[1], color.get(), sz, 'Triangle'])
            prev = [0,0]
            nextAct = True
            activity_list = []

    elif(shapeSelect.get() == 'Arrow Head'):
        if activity_list:
            canvas.delete(activity_list.pop()) #ensures dynamically drawn arrow
        x, y = event.x, event.y
        curr = [x, y]
        if prev != [0,0]:
            wd = size.get()
            sz = (ord(wd[-2])-48) * 10 + (ord(wd[-1])-48)

            activity = canvas.create_polygon(prev[0],prev[1],
                                            curr[0],curr[1],
                                            prev[0], 2*prev[1]-curr[1],
                                            2*prev[0]-curr[0],curr[1],
                                            fill='',
                                            outline=color.get(),
                                            width=sz)
            
            activity_list.append(activity)

            undo_list=activity_list
        if(event.type == '6' and nextAct) :
            nextAct = False
            prev = curr
        if(event.type == '5'):
            redo_list.append([prev[0], prev[1], curr[0], curr[1], color.get(), sz, 'Arrow Head'])
            prev = [0,0]
            nextAct = True
            activity_list = []

    elif(shapeSelect.get() == 'Diamond'):
        if activity_list:
            canvas.delete(activity_list.pop()) #ensures dynamically drawn diamond
        x, y = event.x, event.y
        curr = [x, y]
        if prev != [0,0]:
            wd = size.get()
            sz = (ord(wd[-2])-48) * 10 + (ord(wd[-1])-48)

            activity = canvas.create_polygon(prev[0],prev[1],
                                            curr[0],curr[1],
                                            prev[0], 2*curr[1]-prev[1],
                                            2*prev[0]-curr[0],curr[1],
                                            fill='',
                                            outline=color.get(),
                                            width=sz)
            
            activity_list.append(activity)

            undo_list=activity_list
        if(event.type == '6' and nextAct) :
            nextAct = False
            prev = curr
        if(event.type == '5'):
            redo_list.append([prev[0], prev[1], curr[0], curr[1], color.get(), sz, 'Diamond'])
            prev = [0,0]
            nextAct = True
            activity_list = []

    elif(shapeSelect.get() == 'Hexagon'):
        if activity_list:
            canvas.delete(activity_list.pop()) #ensures dynamically drawn hexagon
        x, y = event.x, event.y
        curr = [x, y]
        if prev != [0,0]:
            wd = size.get()
            sz = (ord(wd[-2])-48) * 10 + (ord(wd[-1])-48)

            d = (prev[0]-curr[0]) ** 2 + (prev[1]-curr[1]) ** 2
            d = math.sqrt(d)
            activity = canvas.create_polygon(prev[0], prev[1],
                                            curr[0], curr[1],
                                            curr[0], curr[1]+d,
                                            prev[0], 2*curr[1]+d-prev[1],
                                            2*prev[0] - curr[0], curr[1]+d,
                                            2*prev[0] - curr[0], curr[1],
                                            fill='',
                                            outline=color.get(),
                                            width=sz)
            
            activity_list.append(activity)

            undo_list=activity_list
        if(event.type == '6' and nextAct) :
            nextAct = False
            prev = curr
        if(event.type == '5'):
            redo_list.append([prev[0], prev[1], curr[0], curr[1], color.get(), sz, 'Hexagon'])
            prev = [0,0]
            nextAct = True
            activity_list = []

    prevShape.set(shapeSelect.get()) #setting prevShape to current shape for NEXT ITER

altpaint_prevshape = StringVar() 
#stores shape before implementing alt-paint before prevShape is reset to alt-paint in next iter
altpaint_prevshape.set('BLANK')
def altpaint(event):
    #alt-paint creates a spray pattern
    global altpaint_prevshape
    if(altpaint_prevshape.get() == 'BLANK'): #BLANK ensures that altpaint_prevshape is not reset to alt-paint in next iters
        altpaint_prevshape.set(prevShape.get()) 

    global prev, curr, activity_list, redo_list, undo_list, nextAct
    if(prevShape.get() != 'Spray Paint'):
        redo_list = []

    if(event.type == '5'):
        shapeSelect.set(altpaint_prevshape.get())
        activity_list = []
        #altpaint_prevshape.set('BLANK') #BLANK ensures that altpaint_prevshape is not reset to alt-paint in next iters
    if(event.type == '6'):
        x, y = event.x, event.y
        shapeSelect.set('Spray Paint')
        activity = canvas.create_arc(x, y, x+2, y+2, fill=color.get(), outline=color.get(), width=1)
        activity_list.append(activity)
        undo_list=activity_list
        redo_list.append([x, y, x+2, y+2, color.get(), 1, 'Spray'])

        prevShape.set(shapeSelect.get()) #setting prevShape to current shape for NEXT ITER

debug_count = 0 #count variable debug #2
def textpaint(event):
    global count, entry, X, Y, debug_count, textpaint_prevshape
    if(shapeSelect.get() == 'Text' and debug_count == 0):
        X, Y = event.x, event.y
        entry = CTkEntry(canvas, 
                        textvariable=currentText,
                        width=300,
                        height=40, 
                        border_width=2, 
                        fg_color='transparent', 
                        bg_color='transparent', 
                        font=(fontStyle.get(), getsize()+3),
                        text_color=color.get())
        entry.place(x=X, y=Y)
        entry.focus_force() #forces focus on entry to type in text
        count = 1
        debug_count = 1
        prevShape.set(shapeSelect.get())
        #prevShape.set('Text')

#executing the GUI next
buttons_on_left()
buttons_on_right()
buttons_on_bottom()

# --------- MOUSE POINTER FUNCTIONS ----------
canvas.bind("<B1-Motion>", paint)
canvas.bind("<ButtonRelease-1>", paint)
canvas.bind("<B3-Motion>", altpaint)
canvas.bind("<ButtonRelease-3>", altpaint)
canvas.bind("<Return>", textpaint)
canvas.bind("<Button-1>", textpaint)

root.resizable(False, False)

root.mainloop() #main root loop