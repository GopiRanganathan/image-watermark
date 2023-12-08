from tkinter import *
from tkinter import filedialog, colorchooser, ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

BG_COLOR = '#1E1E21'


# ------GLOBAL VARIABLES------

img = None
original_size=None
imagepath = None
rotate=0
image_canvas=None
xpos = 0
ypos = 0
opacity_value=255
color=(0, 0, 0)
font_size_value=15
font='arial.ttf'
line_height_value=1
is_single=True
main_text = ''
draw=None
is_marked = False
font_directories = [
        'C:/Windows/Fonts',  # Windows font directory
        # '/Library/Fonts',   # macOS font directory
        # '/usr/share/fonts'  # Linux font directory
        # Add more directories here as needed
    ]

all_fonts = []

for directory in font_directories:
    for font_file in os.listdir(directory):
        if font_file.endswith('.ttf'):
                all_fonts.append(font_file)


# ---------------------------------------COMMANDS--------------------------------------

# SHOW IMAGE
                
def get_img_path():
    global imagepath
    imagepath = filedialog.askopenfilename(title='Select image', filetypes=[('Image Files', ('*.jpg', '*.png', '*.jpeg'))])
    open_image()
    show_image()

def open_image():
    global img, original_height, original_size
    if imagepath:
        try:
            img = Image.open(fp=imagepath)
            original_size=img.size
            
             # Define maximum width and height for the resized image
            max_width = 600
            max_height = 600
            
            # Calculate the resizing factor for width and height
            width_ratio = max_width / img.width
            height_ratio = max_height / img.height
            
            # Use the smallest ratio to ensure that the image fits within the specified dimensions
            resize_ratio = min(width_ratio, height_ratio)
            
            # Calculate the new dimensions based on the resizing ratio
            new_width = int(img.width * resize_ratio)
            new_height = int(img.height * resize_ratio)

            img = img.resize(size=(new_width, new_height)) 
        except Exception as e:
            print("Error:", e)
        
def show_image():
    global image_canvas
    photo = ImageTk.PhotoImage(img)
    image_canvas = image_view.create_image(300, 300, image=photo)
    image_view.image = photo
      
        

        
# PICK COLOR

def pick_color():
    global color
    color_value = colorchooser.askcolor(title="Choose text color", initialcolor='blue')
    color=color_value[0]
    color_label.config(bg=color_value[1])


# SINGLE TEXT OR MULTIPLE TEXT
def single_or_multi():
   global is_single, main_text
   is_single = selected.get()
   main_text=''
   if is_single:
       main_text = watermark_txt.get()
   else:
        line_height.config(state='normal')
        line_height_value = int(line_height.get()) if line_height.get() != '' else 1
        for i in range(20):
                for j in range(20):
                     main_text+=watermark_txt.get() + '    '
                for _ in range(line_height_value):
                     main_text+='\n'
   return main_text
       


# ADD THE WATERMARK
def add_watermark():
    global is_marked, draw, img, font, font_size_value, opacity_value, rotate, main_text
    open_image()
    if img==None:
        messagebox.showinfo(title="No image", message="Please upload a image")
    else:
        img = img.convert("RGBA")
        text = Image.new('RGBA', (1000,1000), (255, 255, 255, 0))
        draw = ImageDraw.Draw(text, "RGBA")   
        font=font_name.get() if font_name.get() != '' else 'arial.ttf'
        font_size_value=int(font_size.get()) if font_size.get() != '' else 10
        font_tuple = ImageFont.truetype(font, font_size_value)
        opacity_value = int(opacity.get()) if opacity.get() != '' else 200
        color_value = color + (opacity_value,)
        rotate=int(deg_value.get()) if deg_value.get() != '' else 0
        
        
        if not watermark_txt.get():
            messagebox.showinfo(title="empty text", message="Please type something in the watermark text")

        single_or_multi()
        draw.text((xpos,ypos), main_text , fill=color_value, font=font_tuple)
        text=text.rotate(rotate)
        text = text.resize(size=img.size)
        img = Image.alpha_composite(img, text)
        show_image()
        
    
def up():
    global ypos
    ypos-=20
    add_watermark()

def down():
    global ypos
    ypos+=20
    add_watermark()

def left():
    global xpos
    xpos-=20
    add_watermark()
def right():
    global xpos
    xpos+=20
    add_watermark()

def activate_line():
    if not selected.get():
        line_height.config(state='normal')
    else:
        line_height.config(state='disable')

def save_image():
    global original_size, img
    savepath = filedialog.asksaveasfilename(title='Select image', filetypes=[('Image Files', ('*.jpg', '*.png', '*.jpeg'))])
    print(savepath)
    img=img.resize(original_size)
    img.save(f'{savepath}.png', format='png')

# ----------------------------------------UI-SETUP--------------------------------------

# WINDOW
window = Tk()
window.title("Image Water Marker")
window.minsize(width=1000, height=700)
window.configure(bg=BG_COLOR, padx=30, pady=30)

# IMAGE
image_view = Canvas(height=600, width=600, bg='black')
image_view.grid(row=0, column=0, rowspan=15, padx=20, pady=20)

# UPLOAD
upload_btn = Button(text="Upload Image", command=get_img_path)
upload_btn.grid(row=16, column=0)

# TEXT
txt_label = Label(text="Watermark text", bg=BG_COLOR, fg='white' )
txt_label.grid(row=1, column=1)

watermark_txt = Entry(width=65)
watermark_txt.grid(row=1, column=2, columnspan=7)

# FONT NAME
font_name_label = Label(text="Font", bg=BG_COLOR, fg='white')
font_name_label.grid(row=2, column=1)


font_name = ttk.Combobox(values=all_fonts, width=30)
font_name.grid(row=2, column=2, columnspan=3)

# FONT SIZE
font_size_label = Label(text="Font Size", bg=BG_COLOR, fg='white')
font_size_label.grid(row=2, column=6)

font_sizes = [size for size in range(2,73,2)]
font_size = ttk.Combobox(values=font_sizes, width=8)
font_size.grid(row=2, column=7)
# print(tkfont.families())

# COLOR
color_label = Label(bg='blue', width=4)
color_label.grid(row=3, column=1)

color_btn = Button(text="choose color", command=pick_color)
color_btn.grid(row=3, column=2)

# OPACITY
opacity_label = Label(text="Opacity", bg=BG_COLOR, fg='white')
opacity_label.grid(row=3, column=3)

opacity = Scale(from_=0, to=255, orient=HORIZONTAL, length=220, sliderrelief='ridge' )
opacity.grid(row=3, column=4, columnspan=4)
opacity.set(value=255)

# ROTATE
rotate_label = Label(text='Rotate', bg=BG_COLOR, fg='white' )
rotate_label.grid(row=6, column=1)
deg_value = Entry()
deg_value.grid(row=6, column=2)
deg_label = Label(text="(degree)", bg=BG_COLOR, fg='white')
deg_label.grid(row=6, column=3)

# POSITION
up_btn = Button(text="▲", command=up)
up_btn.grid(row=5, column=6)
down_btn = Button(text="▼", command=down)
down_btn.grid(row=7, column=6)
left_btn = Button(text="◀", command=left)
left_btn.grid(row=6, column=5, padx=25)
right_btn = Button(text="▶", command=right)
right_btn.grid(row=6, column=7, padx=25)

# SINGE TEXT OR MULTIPLE TEXT
selected = BooleanVar(value=True)
single_btn = Radiobutton(text="Single",  variable=selected, value=True, command=activate_line,  bg=BG_COLOR, fg='white', selectcolor='black', activebackground=BG_COLOR, activeforeground='white')
single_btn.grid(row=9, column=1)
multi_btn = Radiobutton(text="Multiple", variable=selected , value=False,command=activate_line, bg=BG_COLOR,  fg='white', selectcolor='black', activebackground=BG_COLOR, activeforeground='white') 
multi_btn.grid(row=9, column=2)

line_height_label = Label(text="Line height", bg=BG_COLOR, fg='white')
line_height_label.grid(row=9, column=5)
line_heights = [size for size in range(1, 10)]
line_height = ttk.Combobox(values=line_heights, width=8,  state='disable')
line_height.grid(row=9, column=6)


# ADD WATERMARK
add_watermark_btn = Button(text="Add watermark", command=add_watermark)
add_watermark_btn.grid(row=11, column=2, columnspan=3)

# SAVE IMAGE
save_btn = Button(text="Save image", command=save_image)
save_btn.grid(row=11, column=4, columnspan=3)




window.mainloop()

