__author__ = 'Perkins'

from tkinter import *
from tkinter import filedialog
import logging
import shelve
import shutil as sut

import os
from fnmatch import fnmatch
class Application(Frame):

    DEFAULT_TEXT = "Choose"
    UNINITIALIZED = -1

    def __init__(self,parent,str_filename=''):
        Frame.__init__(self, parent)
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.str_filename = str_filename
        self.defaultDir = ''

        #get old values
        self.settings = shelve.open('UIState2')
        try:
            self.soldir = self.settings['soldir_last']
        except KeyError:
            self.soldir = Application.DEFAULT_TEXT

        try:
            self.student_soldir = self.settings['student_soldir']
        except KeyError:
            self.student_soldir = Application.DEFAULT_TEXT

        try:
            self.currentDir = self.settings['currentDir']
        except KeyError:
            self.currentDir = Application.UNINITIALIZED

        self.initialized = False
        self.numbDirs = Application.UNINITIALIZED

        #all the solution dirs
        self.solutiondir_Project6=os.path.join(self.soldir,"Project6")

        self.solutiondir_DataStoreCPP=os.path.join(os.path.join(self.soldir,"DataStore"),"Datastore.cpp")
        self.solutiondir_DataStoreh=os.path.join(os.path.join(self.soldir,"DataStore"),"Datastore.h")

        self.solutiondir_DataStoreFileCPP=os.path.join(os.path.join(self.soldir,"DataStore"),"Datastore_file.cpp")
        self.solutiondir_DataStoreFileh=os.path.join(os.path.join(self.soldir,"includes"),"Datastore_file.h")

        self.solutiondir_String_Databasecpp=os.path.join(os.path.join(self.soldir,"String_Database"),"String_Database.cpp")
        self.solutiondir_String_Databaseh=os.path.join(os.path.join(self.soldir,"includes"),"String_Database.h")

        # self.solutiondir_String_Datacpp=os.path.join(os.path.join(self.soldir,"String_Data"),"String_Data.cpp")
        # self.solutiondir_String_Datah=os.path.join(os.path.join(self.soldir,"includes"),"String_Data.h")

        #jplag folder
        self.jplagfolder = os.path.join(self.student_soldir,"jplag")

        self.create_widgets()

    def create_widgets(self):

        self.parent.title("CPSC 427 Project 6 helper")
        self.pack(fill=BOTH, expand=1)

        # self.columnconfigure(1, weight=1)
        # self.columnconfigure(3, pad=7)
        # self.rowconfigure(3, weight=1)
        # self.rowconfigure(5, pad=7)

        self.label1 = Label(self,text="This application cycles through and replaces files in the  solution folder with files from the students folders\The function you need to change is ",justify=LEFT)
        self.label1.grid(row=0,column=0,columnspan=5,sticky=W,padx=5,pady=5)

        #create a solution directory find button and label
        self.soldir_find_button=Button(self,text="Correct Solution location",command = self.get_solution_directory,padx=5,pady=5)
        self.soldir_find_button.grid(row=1,column=0,sticky=W,padx=5,pady=5)
        self.soldir_label = Label(self, justify=LEFT, text =self.soldir)
        self.soldir_label.grid(row=1,column=1,columnspan = 4,sticky=W,padx=5,pady=5)

        #create a student directory find button
        self.studentdir_find_button=Button(self,text="Student Solution location",command = self.get_student_solution_directory,padx=5,pady=5)
        self.studentdir_find_button.grid(row=2,column=0,sticky=W,padx=5,pady=5)
        self.student_soldir_label = Label(self, text=  self.student_soldir, justify=LEFT)
        self.student_soldir_label.grid(row=2,column=1,columnspan=4,sticky=W,padx=5,pady=5)

        #create next button
        self.next_button = Button(self,text="Next",command = self.do_next,state=DISABLED,padx=5,pady=5)
        self.next_button.grid(row=3,column=0,sticky=E+W)

        #create back button
        self.back_button = Button(self,text="Back",command = self.do_back,state=DISABLED,padx=5,pady=5)
        self.back_button.grid(row=3,column=1,sticky=E+W)

        #create reset button
        self.reset_button = Button(self,text="Reset",command = self.do_reset,state=DISABLED,padx=5,pady=5)
        self.reset_button.grid(row=3,column=2,sticky=E+W)

        #create run button
        self.run_button = Button(self,text="Run",command = self.run,state=DISABLED,padx=5,pady=5)
        self.run_button.grid(row=3,column=3,sticky=E+W)

        #where output goes
        self.output = Text(self,state=DISABLED)
        self.output.grid(row=4, column=0, columnspan=5, rowspan=1, padx=5,pady=5, sticky=E+W+S+N)

        self.enable_buttons()
    ############################
    #where all the work happens
    ###########################
    def run(self):
        #1 delete all outputfiles in solution directory
        self.silentremove(os.path.join(self.solutiondir_Project6,"Encryptfile1.txt"),False)
        self.silentremove(os.path.join(self.solutiondir_Project6,"Encryptfile2.txt"),False)
        self.silentremove(os.path.join(self.solutiondir_Project6,"noEncryptfile1.txt"),False)
        self.silentremove(os.path.join(self.solutiondir_Project6,"noEncryptfile2.txt"),False)

        self.silentremove(self.solutiondir_DataStoreCPP)
        self.silentremove(self.solutiondir_DataStoreh)
        self.silentremove(self.solutiondir_DataStoreFileCPP)
        self.silentremove(self.solutiondir_DataStoreFileh)
        self.silentremove(self.solutiondir_String_Databasecpp)
        self.silentremove(self.solutiondir_String_Databaseh)
        # self.silentremove(self.solutiondir_String_Datacpp)
        # self.silentremove(self.solutiondir_String_Datah)

        #2 build student files to copy
        studentdir = os.path.join(self.student_soldir,self.student_dirnames[self.currentDir])
        studentdir = self.getStudentProjectDir(studentdir)

        studentdir_DataStoreCPP=os.path.join(os.path.join(studentdir,"DataStore"),"Datastore.cpp")
        studentdir_DataStoreh=os.path.join(os.path.join(studentdir,"DataStore"),"Datastore.h")

        studentdir_DataStoreFileCPP=os.path.join(os.path.join(studentdir,"DataStore"),"Datastore_file.cpp")
        studentdir_DataStoreFileh=os.path.join(os.path.join(studentdir,"includes"),"Datastore_file.h")

        studentdir_String_Databasecpp=os.path.join(os.path.join(studentdir,"String_Database"),"String_Database.cpp")
        studentdir_String_Databaseh=os.path.join(os.path.join(studentdir,"includes"),"String_Database.h")

        #3copy above to jplag folder
        jplagStudentdir = os.path.join(self.jplagfolder,self.student_dirnames[self.currentDir])

        self.copyfile(studentdir_DataStoreCPP,os.path.join(jplagStudentdir,"Datastore.cpp") )
        self.copyfile(studentdir_DataStoreFileCPP,os.path.join(jplagStudentdir,"Datastore_file.cpp") )
        self.copyfile(studentdir_String_Databasecpp,os.path.join(jplagStudentdir,"String_Database.cpp") )

        #4 copy from student directory to solutiondirectory
        self.copyfile(studentdir_DataStoreCPP,self.solutiondir_DataStoreCPP )
        self.copyfile(studentdir_DataStoreh,self.solutiondir_DataStoreh )

        self.copyfile(studentdir_DataStoreFileCPP,self.solutiondir_DataStoreFileCPP )
        self.copyfile(studentdir_DataStoreFileh,self.solutiondir_DataStoreFileh )

        self.copyfile(studentdir_String_Databasecpp,self.solutiondir_String_Databasecpp )
        self.copyfile(studentdir_String_Databaseh,self.solutiondir_String_Databaseh )
        return

    def silentremove(self,filename,showError=True):
        try:
            os.remove(filename)
        except Exception as e: # this would be "except OSError, e:" before Python 2.6
            if showError==True:
                self.output.insert(END,"DELETE ERROR:"+str(e) + "\n" )

    def copyfile(self, src,dst):
        try:
            if not os.path.exists(os.path.dirname(dst)):
                dir = os.path.dirname(dst)
                os.makedirs(dir)
            sut.copyfile(src, dst)
        except Exception as e:
            self.output.insert(END,"COPY ERROR:"+str(e) + "Copying file " + dst+ "\n" )

    def getStudentProjectDir(self,dir):
        dirs = [name for name in os.listdir(dir)
                    if os.path.isdir(os.path.join(dir,name)) and "MACOS" not in name ]
        return os.path.join(dir,dirs[0])
    ############################

    def do_next(self):
        self.show_next(1)
    def do_back(self):
        self.show_next( -1)
    def do_reset(self):
        self.currentDir = 0
        self.show_next( 0)


    def show_next(self, increment_by=1):
        self.currentDir += increment_by
        if self.currentDir <0:
            self.currentDir = 0;
        if self.currentDir >=(self.numbDirs-1) and self.numbDirs>Application.UNINITIALIZED:
            self.currentDir = (self.numbDirs-1);
        self.settings['currentDir'] = self.currentDir  #save for later
        self.settings.sync()

        #lets find the current txt file associated with this student file
        if self.currentDir >= self.numbDirs:
            self.output.delete("1.0",END)
            self.output.insert(END,"DONE!")
            return

        #find text file
        for file in self.student_filenames:
            fn = self.student_dirnames[self.currentDir] + '*.txt'
            if fnmatch(file, fn):
                self.populate_output(file)
                return

        self.output.delete("1.0",END)
        self.output.insert(END,fn + "\nNOT FOUND!")


    def populate_output(self,fn):
        if len(fn) == 0:
            return
        fn = os.path.join(self.student_soldir,fn)
        self.output.delete("1.0",END)
        with open(fn) as f:
            self.output.insert(END,f.read())

    def get_solution_directory(self):
        #get solution directory
        self.soldir = filedialog.askdirectory()
        #set textbox value
        self.soldir_label.config(text=self.soldir)

        #save for later
        self.settings['soldir_last'] = self.soldir
        self.settings.sync()

        self.enable_buttons()

    def get_student_solution_directory(self):
        #get student directory
        self.student_soldir = filedialog.askdirectory()
        #set textbox value
        self.student_soldir_label.config(text=self.student_soldir)

        #save for later
        self.settings['student_soldir'] = self.student_soldir
        self.settings.sync()
        self.enable_buttons()

    def enable_buttons(self):
        if (self.soldir_label.cget("text") != Application.DEFAULT_TEXT
            and  self.student_soldir_label.cget("text") != Application.DEFAULT_TEXT
            and len(self.soldir_label.cget("text")) != 0
            and len(self.student_soldir_label.cget("text")) != 0):
            self.next_button.configure(state=NORMAL)
            self.output.configure(state=NORMAL)
            self.run_button.configure(state=NORMAL)
            self.reset_button.configure(state=NORMAL)
            self.back_button.configure(state=NORMAL)

            #build the directories
            if (self.initialized == False):
                self.student_dirnames = [name for name in os.listdir(self.student_soldir)
                                     if os.path.isdir(os.path.join(self.student_soldir,name))]

                self.student_filenames = [name for name in os.listdir(self.student_soldir)
                                     if os.path.isfile(os.path.join(self.student_soldir,name))]
                self.numbDirs = len(self.student_dirnames)
                self.initialized = True

        else:
            self.next_button.configure(state=DISABLED)
            self.output.configure(state=DISABLED)
            self.run_button.configure(state=DISABLED)
            self.reset_button.configure(state=DISABLED)
            self.back_button.configure(state=DISABLED)

def main():
    # Configure only in your main program clause
    logging.basicConfig(level=logging.DEBUG,
                        filename='UI.log', filemode='w',
                        format='%(name)s %(levelname)s %(message)s')
    root = Tk()
    app=Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()