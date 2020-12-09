#!/usr/bin/env python3

# Script: digital-bard.py
# Date: February, 8th, 2019
# Author: Piotr Kapela

# Description:
# Digital Bard is a poem generator written for user amusement.
# It provides a graphical user interface based on tkinter package.

import tkinter.filedialog
import tkinter as tk
import tkinter.ttk as tkk
import random
import os

import db

class DigitalBard:

    def __init__(self, master):
        
        master.title("DigitalBard ver. 1.0.0")
        master.geometry("300x450")
        master.resizable(False, False)

        self.__buildMenu(master)
        self.__buildLayout(master)
        self.db_access = db.DB()

        return None

    def __buildMenu(self, master):

        master.option_add("*tearOff", False)
        menubar = tk.Menu(master)
        
        file_ = tk.Menu(menubar)
        file_.add_command(label="Open...", command=self.__fileOpen)
        file_.add_command(label="Save", command=self.__fileSave)
        file_.add_separator()
        file_.add_command(label="Print", command=lambda: print("Print"))

        help_ = tk.Menu(menubar)
        help_.add_command(label="About DigitalBard", command=lambda: print("About DigitalBard Place Holder"))
        
        menubar.add_cascade(menu=file_, label="File")
        menubar.add_cascade(menu=help_, label="Help")

        master.config(menu = menubar)

        return None
      
    def __buildLayout(self, master):

        # Toolbar
        toolbarFrame = tk.Frame(master, width=300, height=50, relief=tk.RAISED, borderwidth=2)
        toolbarFrame.pack_propagate(0)
        toolbarFrame.pack(fill=tk.BOTH)

        self.openIcon = tk.PhotoImage(file="./icons/Folder.gif")
        openBtn = tk.Button(toolbarFrame, text="Open", height=30, padx=20, image=self.openIcon, compound=tk.TOP, command=self.__fileOpen)
        openBtn.pack(side=tk.LEFT)
        
        self.saveIcon = tk.PhotoImage(file="./icons/Save.gif")
        saveBtn = tk.Button(toolbarFrame, text="Save", height=30, padx=20, image=self.saveIcon, compound=tk.TOP, command=self.__fileSave)
        saveBtn.pack_propagate(0)
        saveBtn.pack(side=tk.LEFT)

        self.dbIcon = tk.PhotoImage(file="./icons/Database.gif")
        databaseBtn = tk.Button(toolbarFrame, text="DB", height=30, padx=20, image=self.dbIcon, compound=tk.TOP, command=self.__buildDB)
        databaseBtn.pack(side=tk.LEFT)

        self.exitIcon = tk.PhotoImage(file="./icons/Exit.gif")
        quitBtn = tk.Button(toolbarFrame, text="Exit", height=30, padx=20, image=self.exitIcon, compound=tk.TOP, command=master.destroy)
        quitBtn.pack(side=tk.LEFT)

        # Center Frame
        outputFrame = tk.Frame(master)
        outputFrame.pack(expand=True, fill="both")
        self.poemOutput = tk.Message(outputFrame, text=self.__poemBuilder())
        self.poemOutput.config(bg="#faefe5", font=("times", 24, "italic"), justify=tk.CENTER)
        self.poemOutput.pack(expand=True, fill="both")

        # Bottom Frame
        navigationFrame = tk.Frame(master)
        navigationFrame.pack()
        composeBtn = tk.Button(navigationFrame, text="Compose", command=self.__composeEvent)
        composeBtn.pack()

        return None

    def __buildDB(self):
        
        # MainWindow
        dbWindow = tk.Toplevel()
        dbWindow.title("DB")
        dbWindow.geometry("400x250")
        dbWindow.resizable(False, False)

        # Toolbar
        toolbarFrame = tk.Frame(dbWindow, width=400, height=50, relief=tk.RAISED, borderwidth=2)
        toolbarFrame.pack_propagate(0)
        toolbarFrame.pack(fill=tk.BOTH)

        self.exitIconDB = tk.PhotoImage(file="./icons/Exit.gif")
        quitBtn = tk.Button(toolbarFrame, text="Exit", height=30, padx=20, image=self.exitIconDB, compound=tk.TOP, command=dbWindow.destroy)
        quitBtn.pack(side=tk.LEFT)

        self.removeIconDB = tk.PhotoImage(file="./icons/Remove.gif")
        removeBtn = tk.Button(toolbarFrame, text="Remove", height=30, padx=20, image=self.removeIconDB, compound=tk.TOP, command=self.__removeRecord)
        removeBtn.pack(side=tk.LEFT)

        self.addIconDB = tk.PhotoImage(file="./icons/Add.gif")
        addBtn = tk.Button(toolbarFrame, text="Add", height=30, padx=20, image=self.addIconDB, compound=tk.TOP, command=self.__insertRecord)
        addBtn.pack(side=tk.LEFT)

        self.loadIconDB = tk.PhotoImage(file="./icons/Upload.gif")
        loadBtn = tk.Button(toolbarFrame, text="Load", height=30, padx=20, image=self.loadIconDB, compound=tk.TOP, command=self.__loadRecord)
        loadBtn.pack(side=tk.LEFT)

        # DB Frame
        dbFrame = tk.Frame(dbWindow, bg="#faefe5")
        dbFrame.pack(expand=True, fill=tk.BOTH)

        # Creating DB interface and fetching records       
        self.db_results = self.db_access.return_records()
        self.treeItems = tkk.Treeview(dbFrame)

        self.treeItems["columns"] = ("one")
        self.treeItems.column("#0", width=30, stretch=tk.NO)
        self.treeItems.column("one", width=365, stretch=tk.NO)
        self.treeItems.heading("#0", text="ID", anchor=tk.W)
        self.treeItems.heading("one", text="Poem", anchor=tk.W)
        
        for row in self.db_results:
            self.treeItems.insert("", "end", text=row[0], values=(str(row[1]),))
        
        self.treeItems.pack()
      
        return None

    def __insertRecord(self):
        
        poem_text = self.poemOutput.cget("text").replace("\n"," ")
        poem_id = self.db_access.insert_record({"poem": poem_text})
        self.treeItems.insert("", "end", text=poem_id, values=(poem_text,))

        return None

    def __removeRecord(self):
        
        curItem = self.treeItems.focus()
        rowDic = self.treeItems.item(curItem)
        
        self.db_access.remove_record(rowDic.get("text"))
        self.treeItems.delete(curItem)

        return None

    def __loadRecord(self):
        
        rowDic = self.treeItems.item(self.treeItems.focus())
        poem = rowDic.get("values")[0].replace(". ",".\n")
        self.poemOutput.config(text=poem)

        return None

    def __poemBuilder(self):
        
        nouns = ("girl", "boy", "flower", "book", "clock", "bed", "cat", "dog", "sun", "moon")
        verbs = ("sang", "ran", "jumped", "screamed", "played", "walked", "stood")
        articles = ("The", "A")
        adverbs = ("happily", "viciously", "sadly", "colorfully", "joyfully", "stiffly", "gently", "easily", "sharply", "slowly")
        structures = (1 , 2)

        lines = random.randint(3,7)
        poem = ""

        while lines > 0:
            if random.choice(structures) == 1:
                poem += random.choice(articles) + " " + random.choice(nouns) + " " + random.choice(verbs) + " " + random.choice(adverbs) + "." + "\n"
                lines -= 1
            else:
                poem += random.choice(articles) + " " + random.choice(nouns) + " " + random.choice(verbs) + "." + "\n"
                lines -= 1
        
        return poem
    
    def __composeEvent(self):

        self.poemOutput.config(text=self.__poemBuilder())
        
        return None
    
    def __fileOpen(self):
        
        my_filetypes = [("text files", ".txt")]
        open_path = tk.filedialog.askopenfilename(initialdir=os.getcwd(), title="Please select a file:", filetypes=my_filetypes)
        
        if(open_path != ""):
            try:
                file = open(open_path, "r")
                self.poemOutput["text"] = file.read()
            except OSError:
                print("File not found")
            finally:
                file.close()

        return None

    def __fileSave(self):    
        
        my_filetypes = [("text files", ".txt")]
        save_path = tk.filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Create a file for saving:", filetypes=my_filetypes)
        
        if(save_path != ""):
            try:
                file = open(save_path, "w+")
                file.write(self.poemOutput["text"])
            except OSError:
                print("Save file error")
            finally:
                file.close()
    
        return None

def main():
    root = tk.Tk()
    app = DigitalBard(root)
    root.mainloop()

if __name__ == "__main__": main()