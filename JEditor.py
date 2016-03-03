'''
First Python GUI try with Tkinter
@Jehad Oumer  https://github.com/JehadOumer
'''



from Tkinter import *
import tkMessageBox
import tkFileDialog
import os
import webbrowser
root=Tk()
root.title('JEditor')


#declering text manipulation functions
def copy():
    text_area.event_generate("<<Copy>>")

def paste():
    text_area.event_generate("<<Paste>>")

def undo():
    text_area.event_generate("<<Undo>>")

def redo(event=None):
    text_area.event_generate("<<Redo>>")
    return 'break'
def cut():
    text_area.event_generate("<<Cut>>")
def select_all(event=None):
    text_area.tag_add(SEL,"1.0", END)
    return 'break'

def find():
    find=Toplevel(root)
    find.title("Find Text")
    find.geometry('360x60')
    find.transient(root)
    Label(find,text="Find All:").grid(column=0,row=0,)
    text_var=StringVar()
    text_field=Entry(find,width=30,textvariable=text_var)
    text_field.grid(column=1,row=0,)
    text_field.focus_set()
    case_var=IntVar()
    Checkbutton(find, text="Case Sensitive", variable=case_var).grid(column=1,row=1,)
    Button(find,text="Find", underline=0,
    command=lambda:search_text(text_var.get(),case_var.get(),text_area,find,text_field)).grid(column=2,row=0,)

    def close_find():
        text_area.tag_remove("matched",'1.0',END)
        find.destroy()
    find.protocol('WM_DELETE_WINDOW',close_find)

def search_text(keyword,case_senstive,text_area,find,text_field):
    text_area.tag_remove('match','1.0',END)
    count=0
    if keyword:
        position='1.0'
        while True:
            position=text_area.search(keyword,position,nocase=case_senstive,stopindex=END)
            if not position: break
            last_position="%s+%dc" %(position,len(keyword))
            text_area.tag_add('matched', position, last_position)
            count+=1
            position=last_position
        text_area.tag_config('matched',foreground='red',background='yellow')
    text_field.focus_set()
    find.title('%d matches found'%count)
    #########################################################################
# defining about menu items
def about(event=None):
    tkMessageBox.showinfo("About","JEditor \nFirst Python GUI try")


def bug_box(event=None):
    tkMessageBox.showinfo("Bugs", "these bugs bugs me \nWatch out ! there is many bugs \n" )
########################################################################################
#quit JEditor Function
def quit_JEditor(event=None):
    if tkMessageBox.askyesno("QUIT!","really !! come one man , it is not that bad , is it ?"):
        root.destroy()

root.protocol('WM_DELETE_WINDOW',quit_JEditor)
    #######################################################################
    #Find and Higlight section
def update_line_num(event=None):
        text=''
        if show_line.get():
            endline,endcolumn=text_area.index('end-1c').split('.')
            text="\n".join(map(str,range(1,int(endline))))
        line_count.config(text=text,anchor='nw')

def highlight(interval=100):
    text_area.tag_remove("active_line",1.0,END)
    text_area.tag_add("active_line","insert linestart","insert lineend+1c")
    text_area.after(interval,toggle_highlight)

def toggle_highlight(event=None):
    toggle_var=highlight_line.get()
    undo_highlight if not toggle_var else highlight()

def undo_highlight():
    text_area.tag_remove("active_line",1.0.END)

###############################################################
# right click menu
def rightc_menu(event):
        right_cmenu.post(event.x_root, event.y_root)
        right_cmenu.focus_set()
# exit right click menu
def rightc_menu_focusout(event=None):
    right_cmenu.unpost()
########################################################################
# JEditor Temes
def theme_toggleing(event=None):
        global bg_color,fg_c
        toggle = theme_select.get()
        theme_colors = colors.get(toggle)
        fg_color, bg_color = theme_colors.split('.')
        fg_color, bg_color = '#'+fg_color, '#'+bg_color
        text_area.config(bg=bg_color, fg=fg_color)

########################################################################
#Defining New file Items Function s
def new(event=None):
    root.title("Untitled")
    global file_name
    file_name=None
    text_area.delete(1.0,END)

def open_file(event=None):
    global file_name
    file_name = tkFileDialog.askopenfilename(defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
    if file_name=="" :
        file_name=None
    else :
        root.title(os.path.basename(file_name) + " --JEditor")
        text_area.delete(1.0, END)
        file_opening=open(file_name,"r")
        text_area.insert(1.0,file_opening.read())
        file_opening.close()

def save(event=None):
    global file_name
    try:

        get_content=text_area.get(1.0,END)
        file_save=open(file_name, 'w')
        file_save.write(get_content)
        #file_save.close()
    except:
        save_as()

def save_as(event=None):
    try:
        save_as_file=tkFileDialog.asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt", filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
        file_opening=open(save_as_file,'w')
        text_content=text_area.get(1.0,END)
        file_opening.write(text_content)
        file_opening.close()
        root.title(os.path.basename(save_as_file)+" --JEditor")
    except:
        pass
#################################################################

#delering icons paths
new_icon=PhotoImage(file="icons/new.gif")
save_icon=PhotoImage(file="icons/save.gif")
open_icon=PhotoImage(file="icons/open.gif")
undo_icon=PhotoImage(file="icons/undo.gif")
redo_icon=PhotoImage(file="icons/redo.gif")
cut_icon=PhotoImage(file="icons/cut.gif")
copy_icon=PhotoImage(file="icons/copy.gif")
paste_icon=PhotoImage(file="icons/paste.gif")
quit_icon=PhotoImage(file="icons/quit.gif")
find_icon=PhotoImage(file="icons/find.gif")
selectall_icon = PhotoImage(file='icons/select_all.gif')
about_icon = PhotoImage(file='icons/about.gif')
bug_icon = PhotoImage(file='icons/bug.gif')

menu_bar = Menu(root) #menu frame
#create file menu
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='File', menu=file_menu)
#File menu sub items
file_menu.add_command(label="New", accelerator="Ctrl+N", compound=LEFT, image=new_icon, underline=0, command=new)
file_menu.add_command(label="Open", accelerator="Ctrl+O", compound=LEFT, image=open_icon, underline=0, command=open_file)
file_menu.add_command(label="Save", accelerator="Ctrl+S", compound=LEFT, image=save_icon, underline=0, command=save)
file_menu.add_command(label="Save As", accelerator="Shift+Ctrl+S", compound=LEFT, command=save_as)#add "Save As" Option
file_menu.add_separator()
file_menu.add_command(label="Quit", accelerator="Ctrl+Q",
compound=LEFT, image=quit_icon, underline=0, command=quit_JEditor)

#create edit menu
edit_menu=Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label='Edit', menu=edit_menu)
#Edit menu sub items
edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", compound=LEFT, image=undo_icon, command=undo)
edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", compound=LEFT, image=redo_icon, command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", accelerator="Ctrl+X", compound=LEFT, image=cut_icon, command=cut)
edit_menu.add_command(label="Copy", accelerator="Ctrl+C", compound=LEFT, image=copy_icon, command=copy)
edit_menu.add_command(label="Paste", accelerator="Ctrl+V", compound=LEFT, image=paste_icon, command=paste)
edit_menu.add_separator()
edit_menu.add_command(label="Select All", accelerator="Ctrl+A", compound=LEFT,image=selectall_icon, underline=7, command=select_all)
edit_menu.add_command(label="Find", accelerator="Ctrl+F", compound=LEFT, image=find_icon, underline=0,command=find)


#create view menu
view_menu=Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label='View', menu=view_menu)

show_line=IntVar()
show_line.set(1)
view_menu.add_checkbutton(label="Show Line Number", variable=show_line)
highlight_line=IntVar()
view_menu.add_checkbutton(label="Highlight Current Line",offvalue=0, onvalue=1, variable=highlight_line,command=toggle_highlight)
theme_menu=Menu(menu_bar,tearoff=0)
view_menu.add_cascade(label="Themes", menu=theme_menu)
#themes colors
colors= {
'1. Default White': '000000.FFFFFF',
'2. Greygarious Grey':'83406A.D1D4D1',
'3. Lovely Lavender':'202B4B.E1E1FF' ,
'4. Aquamarine': '5B8340.D1E7E0',
'5. Bold Beige': '4B4620.FFF0E1',
'6. Night Mode': 'f8f8ff.696969',
'7. Cobalt Blue':'ffffBB.3333aa',
'8. Olive Green': 'D1E7E0.5B8340',
}
theme_select=StringVar()
theme_select.set('1. Default White')
for t in sorted(colors):
    theme_menu.add_radiobutton(label=t,variable=theme_select, command=theme_toggleing)


#create About menu
about_menu=Menu(menu_bar,tearoff=0)
#About Menu items
menu_bar.add_cascade(label='About', menu=about_menu)
about_menu.add_command(label="About",image=about_icon,compound=LEFT,command=about)
about_menu.add_command(label="Bugs", image=bug_icon, compound=LEFT,command=bug_box)




#create tool bar
tool_bar_frame=Frame(root,)
#declering tools
tools = ['new' ,'open', 'save', 'cut', 'copy', 'paste','select_all', 'undo', 'redo','find', 'about']
for t, tool in enumerate(tools):
    tools_gif = PhotoImage(file='icons/'+tool+'.gif')
    je= eval(tool)
    tool_bar = Button(tool_bar_frame, image=tools_gif, command=je)
    tool_bar.image = tools_gif
    tool_bar.pack(side=LEFT)

tool_bar_frame.pack(fill="x")

#indexing box style
line_count=Label(root,width=2, bg="antique white")
line_count.pack(side=LEFT,fill=Y)

# text area
text_area=Text(root, undo=1)
text_area.pack(expand=YES,fill=BOTH)
#text area active line tag style

text_area.tag_config("active_line", background="Ivory3")
scroll_bar=Scrollbar(text_area)
text_area.config(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=text_area.yview)
scroll_bar.pack(side=RIGHT,fill=Y)


#right click menu
right_cmenu=Menu(text_area,tearoff=0)
for t in ('copy','cut','paste','undo','redo','select_all'):
    exec_ute=eval(t)
    right_cmenu.add_command(label=t,compound=LEFT, command=exec_ute)


#key press binds
text_area.bind('<Control-y>', redo)
text_area.bind('<Control-Y>', redo)
text_area.bind('<Control-N>',new)
text_area.bind('<Control-n>',new)
text_area.bind('<Control-S>',save)
text_area.bind('<Control-s>',save)
text_area.bind('<Control-O>',open_file)
text_area.bind('<Control-o>',open_file)
text_area.bind("<Any-KeyPress>",update_line_num)
text_area.bind("<Control-A>",select_all)
text_area.bind("<Control-a>",select_all)
right_cmenu.bind("<FocusOut>",rightc_menu_focusout)
text_area.bind("<Button-3>",rightc_menu)


root.config(menu=menu_bar)
root.geometry('350x350')
root.mainloop() #main loop of the parent window
