from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *

from subprocess import *

import os
import json

print("This PyEditor Terminal, inputs are taken here")
class App():
    def __init__(self,app):
        if os.path.exists(os.getcwd()+ "/settings.json"):
            with open("./settings.json") as file:
                configData=json.load(file)
        else:
             configTemplate={
                 "font":"cascadia code",
                 "defaultFontSize":16,
                 "author":"Pratyush Jha"
             }
             with open(os.getcwd()+"/settings.json", "w+") as file:
                 json.dump(configTemplate,file)
                 print("Settings File created please run the app again")       
        self.app=app
        self.app.title("PyEditor")
        self.app.geometry(f"{app.winfo_screenwidth()}x{app.winfo_screenheight()}+0+0")

        #Variables
        self.file_path=''
        self.default_font_size=configData["defaultFontSize"]
        self.font=configData["font"]
        
        # Main Frame
        self.mainFrame=Frame(background='black',bd=5,relief=SOLID)
        self.mainFrame.pack(expand=True,fill=BOTH)

        # Menu Bar
        menuBar=Menu(self.mainFrame)
        # File Menu
        fileMenu=Menu(menuBar,tearoff=False)
        fileMenu.add_command(label='Save File',accelerator='Ctrl+S',command=self.save_file)
        fileMenu.add_command(label='Save As',accelerator='Alt+S',command=self.save_as_file)
        fileMenu.add_command(label='Open File',accelerator='Ctrl+O',command=self.open_file)
        fileMenu.add_command(label='New File',accelerator='Ctrl+N',command=self.new_file)
        fileMenu.add_separator()
        fileMenu.add_command(label='Close',accelerator='Alt+F4',command=self.app.destroy)
        #Edit Menu
        editMenu=Menu(menuBar,tearoff=False)
        editMenu.add_command(label='Cut',accelerator='Ctrl+X',command=self.cut)
        editMenu.add_command(label='Copy',accelerator='Ctrl+C',command=self.copy)
        editMenu.add_command(label='Paste',accelerator='Ctrl+V',command=self.paste)
        editMenu.add_separator()
        editMenu.add_command(label='Increase Font Size',accelerator='Ctrl+P',command=self.change_fontsize_inc)
        editMenu.add_command(label='Decrease Font Size',accelerator='Ctrl+M',command=self.change_fontsize_dec)
        editMenu.add_separator()
        editMenu.add_command(label='Run Program',accelerator='Alt+B',command=self.run_file)
        editMenu.add_separator()
        editMenu.add_command(label='Clear Editor',accelerator='Alt+V',command=self.clear_editor)
        editMenu.add_command(label='Clear Output',accelerator='Alt+C',command=self.clear_output)
        # Theme Menu
        themeMenu=Menu(menuBar,tearoff=False)
        themeMenu.add_command(label='Dark +',command=self.dark_theme)
        themeMenu.add_command(label='Light',command=self.light_theme)
        themeMenu.add_command(label='Monokai',command=self.monakai_theme)
        themeMenu.add_command(label='One Dark',command=self.twilight_theme)

        menuBar.add_cascade(label='File',menu=fileMenu)
        menuBar.add_cascade(label='Edit',menu=editMenu)
        menuBar.add_cascade(label='Theme',menu=themeMenu)
        menuBar.add_separator()
        menuBar.add_command(label='Run Progam',command=self.run_file)
        menuBar.add_separator()
        menuBar.add_command(label='Cut',command=self.cut)
        menuBar.add_command(label='Copy',command=self.copy)
        menuBar.add_command(label='Paste',command=self.paste)

        self.app.config(menu=menuBar)
        # Editor Text Feild
        self.editFrame=Frame(self.mainFrame)
        self.editFrame.place(x=0,y=0,relwidth=1,height=500)

        scrollY=Scrollbar(self.editFrame,orient=VERTICAL,background='black')
        scrollY.pack(side=RIGHT,fill=Y)
        self.textFeild=Text(self.editFrame,background='black',foreground='white',font=(self.font,self.default_font_size,'bold'),insertbackground='white',yscrollcommand=scrollY.set)
        scrollY.config(command=self.textFeild.yview)
        self.textFeild.pack(expand=True,fill=BOTH)
        # Output Frame
        self.outputFrame=Frame(self.mainFrame,background='white')
        self.outputFrame.place(x=0,y=500,relwidth=1,height=220)

        scrollY=Scrollbar(self.outputFrame,orient=VERTICAL)
        scrollY.pack(side=RIGHT,fill=Y)
        self.outputFeild=Text(self.outputFrame,background='black',foreground='white',font=(self.font,self.default_font_size,'bold'),insertbackground='white',yscrollcommand=scrollY.set)
        scrollY.config(command=self.outputFeild.yview)
        self.outputFeild.pack(expand=True,fill=BOTH)
        
        # SHORTCUTS
        self.app.bind('<Control-p>',self.change_fontsize_inc)
        self.app.bind('<Control-m>',self.change_fontsize_dec)
        self.app.bind('<Alt-s>',self.save_as_file)
        self.app.bind('<Control-s>',self.save_file)
        self.app.bind('<Control-o>',self.open_file)
        self.app.bind('<Control-n>',self.new_file)
        self.app.bind('<Alt-c>',self.clear_output)
        self.app.bind('<Alt-v>',self.clear_editor)
        self.app.bind('<Alt-b>',self.run_file)

        # Functions
    def light_theme(self):
        self.textFeild.config(background='white',foreground='black',insertbackground='black')  
        self.outputFeild.config(background='white',foreground='black',insertbackground='black')
        self.mainFrame.config(background='white')  
      
    def dark_theme(self):
        self.textFeild.config(background='black',foreground='white',insertbackground='white')      
        self.outputFeild.config(background='black',foreground='white',insertbackground='white') 
        self.mainFrame.config(background='black')     
 

    def monakai_theme(self):
        self.textFeild.config(background='#272822',foreground='white',insertbackground='white')      
        self.outputFeild.config(background='#272822',foreground='white',insertbackground='white')
        self.mainFrame.config(background='#272822')      
 
    def twilight_theme(self):
        self.textFeild.config(background='#28171E',foreground='white',insertbackground='white')      
        self.outputFeild.config(background='#28171E',foreground='white',insertbackground='white')
        self.mainFrame.config(background='#28171E')     

    def change_fontsize_inc(self,event=None):
        self.default_font_size+=1
        self.textFeild.config(font=(self.font,self.default_font_size,'bold'))
    def change_fontsize_dec(self,event=None):
        self.default_font_size-=1
        self.textFeild.config(font=(self.font,self.default_font_size,'bold'))

    def save_as_file(self,event=None):
        path=asksaveasfilename(filetypes=[("Python Program","*.py"),("All Files",'*.*')],defaultextension=('.py'))
        if path != '':
            self.file_path=path
            file=open(self.file_path,'w')
            file.write(self.textFeild.get('1.0',END))
            file.close()
            self.outputFeild.delete('1.0',END)    
            message=f"File Saved In Path {self.file_path}"
            self.outputFeild.delete('1.0',END)
            self.outputFeild.insert('1.0',message)
    def save_file(self,event=None):
        if self.file_path == '':
            self.save_as_file()
        else:
            file=open(self.file_path,'w')    
            file.write(self.textFeild.get('1.0',END))
    def open_file(self,event=None):
        path=askopenfilename(filetypes=[("Python Program","*.py"),("All Files","*.*")],defaultextension=(".py"))
        if path != '':
            self.file_path=path
            file=open(self.file_path,'r')
            data=file.read()
            self.textFeild.delete('1.0',END)
            self.outputFeild.delete('1.0',END)
            self.textFeild.insert('1.0',data)
            self.app.title(self.file_path+" - PyEditor")
        else:
            showerror('Error',"There was an error opening the file")    
    def new_file(self,event=None):
        question=askyesno("Confirm","If you click yes the current file will be closed and will not be saved, do you want to create a new file")
        if question == True:
            self.textFeild.delete('1.0',END)
            self.outputFeild.delete('1.0',END)
            self.file_path=''
    def clear_output(self,event=None):
            self.outputFeild.delete('1.0',END)
    def clear_editor(self,event=None):
            self.textFeild.delete('1.0',END)
    def run_file(self,event=None):
        if self.file_path == '':
            showerror('Error',"There are either no files opened or the opened file is not saved")
        else:
           command=f'python "{self.file_path}"'    
           run=Popen(command,stdout=PIPE,stderr=PIPE,shell=True)
           output,error=run.communicate()
           self.outputFeild.delete('1.0',END)
           self.outputFeild.insert('1.0',output)
           self.outputFeild.insert('1.0',error)
    def cut(self):
        self.textFeild.event_generate(("<<Cut>>"))

    def copy(self):
        self.textFeild.event_generate(("<<Copy>>"))
    
    def paste(self):
        self.textFeild.event_generate(("<<Paste>>"))          



app=Tk()
construtor=App(app)        
app.mainloop()
