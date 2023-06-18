import os   
import pygame
import tkinter as tk #for color picker
from tkinter import *
from pygame.locals import *
from tkinter import colorchooser
from functools import partial
from tkinter.filedialog import asksaveasfile
from tkinter import ttk


"""
VERSION 0.5
""" 


stroke = []
color = (255, 255, 255)  # Set white as the default color
stroke_size = 10 # default val as medium
filled = False
Equalize = False
#classes
class EmptyClass():    
    """Empty class avoid error if no drawing tool is selected""" 

    def MBdown(self):
        pass

    def MBHold(self):
        pass

class PaintBrush():
    def MBdown(self):
        self.prev_pos = pygame.mouse.get_pos()
        mtlist = []
        stroke.append(mtlist)

    def MBHold(self):
        # same thing as line
        current_pos = pygame.mouse.get_pos()
        stroke[-1].append("pygame.draw.line(screen, " + str(color) + ", " + str(self.prev_pos) + "," + str(current_pos) + ", "+ str(stroke_size) +")")
        self.prev_pos = current_pos
        

class CreateRectangle():
    def MBdown(self):
        self.start_pos = pygame.mouse.get_pos()
        stroke.append("pygame.draw.rect(screen, " + str(color) + ", pygame.Rect("+ str(self.start_pos) + "," + str((0,0)) + "), "+ str(stroke_size)+")")


    def MBHold(self):
        current_pos = pygame.mouse.get_pos()

        rec_height = current_pos[1] - self.start_pos[1]
        rec_width = current_pos[0] - self.start_pos[0]

        if rec_width < 0 and rec_height < 0:
            rect_pos = current_pos
        elif rec_height < 0:
            rect_pos = (self.start_pos[0], current_pos[1])
        elif rec_width < 0:
            rect_pos = (current_pos[0], self.start_pos[1])
        else:
            rect_pos = self.start_pos

        if Equalize:
            square_size = min(abs(rec_width), abs(rec_height))
            rect_wh = (square_size, square_size)
        else:
            rect_wh = (abs(rec_width), abs(rec_height))

        stroke.pop()
        if filled:
            stroke_size_l = ""
        else:
            stroke_size_l = stroke_size
        stroke.append("pygame.draw.rect(screen, " + str(color) + ", pygame.Rect("+ str(rect_pos) + "," + str(rect_wh) + "), "+ str(stroke_size_l)+")")

class CreateLine():
    def MBdown(self):
        self.start_pos =  pygame.mouse.get_pos()
        stroke.append("pygame.draw.line(screen, " + str(color) + ", " + str(self.start_pos) + "," + str(self.start_pos) + ", "+ str(stroke_size) +")")
    
    def MBHold(self):
        current_pos = pygame.mouse.get_pos()
        stroke.pop()
        stroke.append("pygame.draw.line(screen, " + str(color) + ", " + str(self.start_pos) + "," + str(current_pos) + ", "+ str(stroke_size) +")")
    
class CreateEllipse():

    def MBdown(self):
        self.start_pos =  pygame.mouse.get_pos()
        stroke.append("pygame.draw.ellipse(screen, " + str(color) + ", pygame.Rect(" + str(self.start_pos) + ", " + str((0,0)) + "), "+ str(stroke_size)+")")


    def MBHold(self):
        current_pos = pygame.mouse.get_pos()

        rec_height = current_pos[1] - self.start_pos[1]
        rec_width = current_pos[0] - self.start_pos[0]

        if rec_width < 0 and rec_height < 0:
            rect_pos = current_pos
        elif rec_height < 0:
            rect_pos = (self.start_pos[0], current_pos[1])
        elif rec_width < 0:
            rect_pos = (current_pos[0], self.start_pos[1])
        else:
            rect_pos = self.start_pos

        
        if Equalize: 
            square_size = min(abs(rec_width), abs(rec_height))
            rect_wh = (square_size, square_size)
        else:
            rect_wh = (abs(rec_width), abs(rec_height))
    
        stroke.pop()
        if filled: 
            stroke_size_l = ""
        else: 
            stroke_size_l = stroke_size             
        stroke.append("pygame.draw.ellipse(screen, " + str(color) + ", pygame.Rect(" + str(rect_pos) + ", " + str(rect_wh) + "), "+ str(stroke_size_l)+")")

#defined variables
def choose_color(): #for getting a color from the colorchooser module
    global color
    prev_color = color
    color, colorhex = colorchooser.askcolor(title ="Choose color") 
    if color == None: #avoid error if user doesnt choose a color as escaping returns color as None
        color = prev_color



bg_color_changed = False
window_fill_color = (0,0,0) #default bg color
def change_bg_color():
    global window_fill_color, bg_color_changed
    prev_color = window_fill_color 
    window_fill_color, BGhex = colorchooser.askcolor(title ="Choose background color")
    bg_color_changed = True
    if window_fill_color == None: #avoid error if user doesnt choose a color
        window_fill_color = prev_color
        bg_color_changed = False


current_tool = EmptyClass() #so it wont trhow up any errors if you try drawing bfr choosing


def choose_tool(name):
    global current_tool 
    if name == "brsh":
        current_tool = PaintBrush()
        drawbutton.config(bg="gray50")
        rectangleButton.config(bg="gray20")
        circleButton.config(bg="gray20")
        lineButton.config(bg="gray20")        
    
    elif name == "rect":
        current_tool = CreateRectangle()
        rectangleButton.config(bg="gray50")
        circleButton.config(bg="gray20")
        lineButton.config(bg="gray20")
        drawbutton.config(bg="gray20") 

    elif name == "circ":
        current_tool = CreateEllipse()
        rectangleButton.config(bg="gray20")
        circleButton.config(bg="gray50")
        lineButton.config(bg="gray20")
        drawbutton.config(bg="gray20") 

    elif name == "line":
        current_tool = CreateLine()
        rectangleButton.config(bg="gray20")
        circleButton.config(bg="gray20")
        lineButton.config(bg="gray50")
        drawbutton.config(bg="gray20") 


MAX_FPS = 60

running = True
drawing = False
# ------------- INITIALIZE TKINER  ------------- # 

root = tk.Tk()
root.config(bg="#283044")
root.title("Click2Draw V0.5")
button_font = ("Fixedsys", 14, "bold")
button_width = 17

# ------------- EMBED PYGAME WINDOW  ------------- # 

embed = tk.Frame(root, width = 500, height = 500, bg="#ffca18") #creates embed frame for pygame window
embed.grid(columnspan = 1, rowspan = 6) # Adds grid
embed.grid(column = 4,row=1)
root.resizable(False, False)
buttonwin = tk.Frame(root, width = 75, height = 500, bg="#ffca18")

buttonwin.grid(column=1, row=1)

# ------------- CREATE TKINTER WIDGETS  ------------- # 

Cpicklabel = Button(buttonwin, text="Change Color", font=button_font, fg="white", bg="gray20", width = button_width, command = choose_color)
drawbutton = Button(buttonwin, text="Paint Brush",              font=button_font, fg="white", bg="gray20", width = button_width, command= partial(choose_tool, "brsh"))
rectangleButton = Button(buttonwin, text="Create Rectangle",    font=button_font, fg="white", bg="gray20", width = button_width, command= partial(choose_tool, "rect"))
circleButton = Button(buttonwin, text="Create Circle",          font=button_font, fg="white", bg="gray20", width = button_width, command= partial(choose_tool, "circ"))
lineButton = Button(buttonwin, text="Create Line",              font=button_font, fg="white", bg="gray20", width = button_width,command= partial(choose_tool, "line"))
ToolLabel = Label(buttonwin, text="TOOLS",font=("Fixedsys", 24, "bold"), fg="black", bg="#ffca18",width = 9)


OptionLabel = Label(buttonwin, text="OPTIONS",font=("Fixedsys", 24, "bold"), fg="black", bg="#ffca18",width = 9)
BgpickButton = Button(buttonwin, text="Change BGColor", font=button_font, fg="white", bg="gray20", width = button_width, command = change_bg_color)

# ---- CHANGE STROKE SIZE ---- # 

stroke_sizes = {
    "XLarge": 20,
    "Large": 15,
    "Medium": 10,
    "Small": 5,
    "Tiny": 2
}

def change_stroke_size(event):
    global stroke_size
    size = stroke_sizes[event.widget.get()]
    stroke_size = size

stroke_size_var = tk.StringVar()
stroke_size_var.set("Medium")  # Set default value
stroke_size_dropdown = ttk.Combobox(buttonwin, textvariable=stroke_size_var, values=list(stroke_sizes.keys()), width=button_width, state="readonly", font=("Fixedsys", 13))
stroke_size_dropdown.bind("<<ComboboxSelected>>", change_stroke_size)

# ---- TOGGLE FILL ---- #

fill_dic = {
    "Fill": True,
    "No Fill": False,
}

def toggle_fill(event):
    global filled
    set_val = fill_dic[event.widget.get()]
    filled = set_val

fill_var = tk.StringVar()
fill_var.set("No Fill")  # Set default value
fill_dropdown = ttk.Combobox(buttonwin, textvariable=fill_var, values=list(fill_dic.keys()), width=button_width, state="readonly", font=("Fixedsys", 13))
fill_dropdown.bind("<<ComboboxSelected>>", toggle_fill)

# ---- TOGGLE CIRC/SQAURE ---- #

Equalize_opts = {
    "Equalize": True,
    "Free Form": False,
}

def toggle_equalize(event):
    global Equalize
    set_val = Equalize_opts[event.widget.get()]
    Equalize = set_val

eq_var = tk.StringVar()
eq_var.set("Free Form")  # Set default value
eq_dropdown = ttk.Combobox(buttonwin, textvariable=eq_var, values=list(Equalize_opts.keys()), width=button_width, state="readonly", font=("Fixedsys", 13))
eq_dropdown.bind("<<ComboboxSelected>>", toggle_equalize)

# ---- SAVE IMAGE ---- #

def save_image():
    pygame.image.save(screen, "image.png")

    #code for save as: 
    # error: cant open file and exported file is corrupted 


    # file_types = [('PNG Image', '*.png'), ('JPEG Image', '*.jpg')] 
    # file = asksaveasfile(filetypes=file_types, defaultextension='.png')
    # if file:
        # pygame.image.save(screen, file.name)
        # file.close()    

CommandLabel = Label(buttonwin, text="COMMANDS",font=("Fixedsys", 24, "bold"), fg="black", bg="#ffca18",width = 9)
save_button = Button(buttonwin, text="Export", font=button_font, fg="white", bg="gray20", width = button_width,command= save_image)

# ---- UNDO ---- #

def undo_function():
    global stroke
    if len(stroke) > 0:
        stroke.pop()

undo_button = Button(buttonwin, text="Undo", font=button_font, fg="white", bg="gray20", width = button_width,command= undo_function)

# ------------- CREATE TOOLBAR  ------------- # 

ToolLabel.grid(row=1,column=1)
drawbutton.grid(row=2, column=1)
rectangleButton.grid(row=4, column=1)
circleButton.grid(row=5, column=1)
lineButton.grid(row=6, column=1)

#ADD THE options like size, save, openm undo & redo
OptionLabel.grid(row=8,column=1)
Cpicklabel.grid(row=9, column=1)
BgpickButton.grid(row=10, column=1)
fill_dropdown.grid(row=11, column=1)
eq_dropdown.grid(row=12,column=1)
stroke_size_dropdown.grid(row=13, column=1)

CommandLabel.grid(row=14, column=1)
save_button.grid(row=15, column=1)
undo_button.grid(row=16, column=1)

os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'


# ------------- PYGAME ------------- # 

screen_resolution = win_width, win_height = (1000, 600)

screen = pygame.display.set_mode(screen_resolution)
clock = pygame.time.Clock()

pygame.init()
pygame.display.init()

# ------------- CLOSE PROGRAM ------------- # 

#custom func to close pygame when tkinter is closed
def quit_application():
    global running
    running = False
    pygame.quit()
    root.quit()
    print(len(stroke), "individual items on screen") 

root.protocol("WM_DELETE_WINDOW", quit_application) 


# ------------- MAIN LOOP ------------- # 

while running:
    screen.fill(window_fill_color)

    if len(stroke) > 0:
        for i in stroke:
            if isinstance(i, list):
                for j in i:
                    exec(j)
            else: 
                exec(i)

    for action in pygame.event.get():
        if action.type == QUIT:
            running = False
 
        elif action.type == pygame.MOUSEBUTTONUP and action.button == 1:
            drawing = False

        elif drawing:                  
            current_tool.MBHold()

        elif action.type == pygame.MOUSEBUTTONDOWN and action.button == 1: 
            current_tool.MBdown()
            drawing = True
    

    pygame.display.flip()
    root.update()




