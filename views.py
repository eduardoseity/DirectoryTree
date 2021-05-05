from tkinter import Tk, Label, Button, filedialog, ttk, Frame, Entry, simpledialog, Checkbutton, IntVar, messagebox
import platform
import tkmacosx
from models import Tree
import os
import subprocess

class StartApp:
    def __init__(self):
        self.mainWindow()
        # self.groupsList = []
        pass

    def mainWindow(self):
        self.lastDir = "."
        self.mainWin = Tk()
        self.mainWin.title("Abridor de arquivos")
        h = self.mainWin.winfo_screenheight()
        h=300
        size = "300x" + str(h)
        self.lastH = self.mainWin.winfo_height()
        self.collapsed = False
        self.mainWin.geometry(size)
        self.minWidth = 300
        self.minHeight = 400
        self.mainWin.minsize(self.minWidth,self.minHeight)
        s = ttk.Style(self.mainWin)
        s.theme_use('default')

        frame1 = Frame(self.mainWin)
        frame1.pack(fill="x")


        addGroupButton = Button(frame1,text="Adicionar grupo...",fg="Black",command=self.addNewGroup)
        addGroupButton.pack(side="left",padx=5,pady=0)

        self.topmostVar = IntVar()
        alwayOnTopButton = Checkbutton(frame1, text="Manter no topo", fg="black", variable=self.topmostVar, command=lambda:self.mainWindowOnTop(self.topmostVar.get()))
        alwayOnTopButton.pack(side="right",padx=5,pady=5)


        frame1_1 = Frame(self.mainWin)
        frame1_1.pack(fill="x")

        addDirButton = Button(frame1_1,text="Adicionar diretório...",fg="Black",command=self.addDirectory)
        addDirButton.pack(side="left",padx=5,pady=5)

        colorWhiteButton = tkmacosx.Button(frame1_1,text="",bg="white",borderless=1,width=25,command=lambda:self.changeColor("white"))
        colorWhiteButton.pack(side="left",padx=0,pady=5)

        colorRedButton = tkmacosx.Button(frame1_1,text="",bg="#FFAAAA",borderless=1,width=25,command=lambda:self.changeColor("red"))
        colorRedButton.pack(side="left",padx=0,pady=5)

        colorYellowButton = tkmacosx.Button(frame1_1,text="",bg="#FFFFAA",borderless=1,width=25,command=lambda:self.changeColor("yellow"))
        colorYellowButton.pack(side="left",padx=0,pady=5)

        colorGreenButton = tkmacosx.Button(frame1_1,text="",bg="#AAFFAA",borderless=1,width=25,command=lambda:self.changeColor("green"))
        colorGreenButton.pack(side="left",padx=0,pady=5)

        self.collapseButton = Button(frame1_1,text="▲",fg="Black",command=self.collapseWindow)
        self.collapseButton.pack(side="right",padx=5,pady=5)


        frame2 = Frame(self.mainWin)
        frame2.pack(side="top",fill="both",expand=1)

        self.style = ttk.Style()
        self.style.map('Treeview', foreground=self.fixed_map('foreground'),background=self.fixed_map('background'))

        self.tree = ttk.Treeview(frame2)
        self.tree['columns'] = ('nodeName')

        self.tree.column('nodeName',width=50, anchor='w')
        self.tree.heading('nodeName', text='Caminho')
        self.tree.column('#0', anchor='w')
        self.tree.heading('#0', text='Diretório')
        self.tree.bind("<Double-1>",self.nodeClick)
        self.tree.tag_configure('file', foreground='#0000FF')
        self.tree.tag_configure('white', background='#FFFFFF')
        self.tree.tag_configure('red', background='#FFAAAA')
        self.tree.tag_configure('yellow', background='#FFFFAA')
        self.tree.tag_configure('green', background='#AAFFAA')

        self.tree.pack(side="top",fill="both",expand=1,padx=5,pady=5)

        frame3 = Frame(self.mainWin)
        frame3.pack(side="top",fill="x",expand=0)

        deleteButton = Button(frame3,text="Excluir",command=lambda:self.deleteItem(self.tree.focus()))
        deleteButton.pack(side="left",padx=5,pady=10)

    def fixed_map(self,option):
    # Fix for setting text colour for Tkinter 8.6.9
    # From: https://core.tcl.tk/tk/info/509cafafae
    #
    # Returns the style map for 'option' with any styles starting with
    # ('!disabled', '!selected', ...) filtered out.

    # style.map() returns an empty list for missing options, so this
    # should be future-safe.
        return [elm for elm in self.style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]

    def askYesNo(self, title, msg, default):
        self.mainWindowOnTop(False)
        ret = messagebox.askyesno(title=title,message=msg,default=default)
        self.mainWindowOnTop(self.topmostVar.get())
        return ret

    def changeColor(self,color):
        selectedItemId = self.tree.focus()
        if selectedItemId == "":
            self.warningDialog("Selecione um item")
            return 0
        
        tags = self.tree.item(selectedItemId,"tags")
        tags = (tags[0],color)
        self.tree.item(selectedItemId,tags=tags)
        self.tree.selection_set("")

    def deleteItem(self,id):
        if id == "":
            return 0
        dlg = self.askYesNo("Excluir item","Excluir item selecionado?","no")
        if dlg:
            self.tree.delete(id)

    def collapseWindow(self):
        if not self.collapsed:
            self.lastH = self.mainWin.winfo_height()
            self.mainWin.minsize(self.minWidth,70)
            self.mainWin.resizable(True,False)
            self.mainWin.geometry(str(self.mainWin.winfo_width())+"x"+str(70))
            self.collapseButton.configure(text="▼")
            self.collapsed = True
        else:
            self.mainWin.minsize(self.minWidth,self.minHeight)
            self.mainWin.resizable(True,True)
            self.mainWin.geometry(str(self.mainWin.winfo_width())+"x"+str(self.lastH))
            self.collapseButton.configure(text="▲")
            self.collapsed = False


    def mainWindowOnTop(self,topmost):
        if topmost:
            self.mainWin.attributes('-topmost', True)
        else:
            self.mainWin.attributes('-topmost', False)

    def addNewGroup(self):
        self.mainWindowOnTop(False)
        groupName = simpledialog.askstring(title="Nome do grupo",prompt="Nome do grupo")
        self.mainWindowOnTop(self.topmostVar.get())
        if (groupName == "" or groupName == None):
            return 0
        
        try:
            self.tree.insert(parent="",index="end",iid=groupName,text=groupName,tags=("group"))
        except Exception as e:
            self.warningDialog("Já existe um grupo chamado " + groupName)

        self.tree.focus(groupName)
        self.tree.selection_set(groupName)
        # self.groupsList.append(groupName)

    def addNode(self,groupName,treeList):
        for index, item in enumerate(treeList):
            values = (item[0])
            parent = item[2]
            id = item[1]
            itemType = item[4]
            self.tree.insert(parent=parent,index='end',iid=id,text=values,values=(item[3],),tags=(itemType))

            # if index == 0:
            #     # Main node
            #     self.tree.insert(parent=groupName,index='end',iid=treeList[0][1],text=treeList[0][0],tags=("folder"))
            # else:
            #     # Childs
            #     self.tree.insert(parent=parent,index='end',iid=id,text=values,values=(item[3],),tags=(itemType))
    
    def nodeClick(self,click):
        item = self.tree.focus()
        values = self.tree.item(item).values()
        listValues = list(values)
        if listValues[4][0] == 'group':
            return 0
        filePath = listValues[2]
        filePath = os.path.normpath(filePath[0])
        try:
            if platform.system() == "Windows":
                subprocess.run(["explorer", filePath], shell=True)
            elif platform.system() == "Darwin":
                subprocess.run(["open",filePath], check=True)
        except Exception as e:
            print(e)

    def warningDialog(self,msg):
        self.mainWindowOnTop(False)
        messagebox.showwarning(message=msg)
        self.mainWindowOnTop(self.topmostVar.get())

    def addDirectory(self):
        selectedItemId = self.tree.focus()
        selectedItemParent = self.tree.parent(selectedItemId)
        
        if selectedItemId == "":
            self.warningDialog("Selecione um grupo!")
            return 0
        
        if selectedItemParent != "":
            self.warningDialog("Selecione um grupo!")
            return 0

        self.mainWindowOnTop(False)
        
        dir = filedialog.askdirectory(initialdir=self.lastDir,title="Adicionar diretório")
        self.mainWindowOnTop(self.topmostVar.get())
        
        if dir == "":
            return 0
        self.lastDir = dir
        treeList = Tree.listFiles(dir, selectedItemId)
        self.addNode(selectedItemId,treeList)
    
    # def sendGroup(self,treeList,groupName,dialog):
    #     dialog.destroy()
    #     self.addNode(groupName,treeList)
    #     pass
        
    # def chooseGroup(self,treeList):
    #     dialog = Tk()
    #     dialog.title("Escolher grupo")
    #     s = ttk.Style(dialog)
    #     s.theme_use('alt')

    #     label = Label(dialog,text="Escolha um grupo",fg="Black")
    #     label.grid(row=0,column=0,padx=10,pady=10)

    #     groupCombobox = ttk.Combobox(dialog,values=self.groupsList,foreground="black")
    #     groupCombobox.grid(row=0,column=1,padx=10,pady=10)

    #     button = Button(dialog,text="Ok",fg="black",command=lambda: self.sendGroup(treeList,groupCombobox.get(),dialog))
    #     button.grid(row=1,column=0,padx=10,pady=10)

    #     dialog.mainloop()

if __name__ == "__main__":
    app = StartApp()
    app.mainWin.mainloop()
    pass