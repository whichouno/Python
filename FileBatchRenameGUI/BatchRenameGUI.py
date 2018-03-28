from tkinter.filedialog import *

class BatchRenameGUI:
    def __init__(self,top):
        self.__top = top
        self.__text_path = StringVar()
        self.__check_usestrpath = IntVar()
        self.__check_filtefile = IntVar()
        self.__ENTRY_PATH_WIDTH = 30
        self.__ENTRY_IDPATTERN_WIDT = 30
        self.__ENTRY_NEWFILENAMEFORMAT = 30

    def __rename(self,original_path, id_pattern, newfilename_format):
        if(original_path == '' or id_pattern == '' or newfilename_format == ''):
            return
        filenamelist = os.listdir(original_path)
        for filename in filenamelist:
            filepath = os.path.join(original_path, filename)
            if (os.path.isdir(filepath)):
                continue
            if (filename.startswith('.')):
                continue
            pattern = re.compile(id_pattern)
            match = pattern.search(filename)
            if (match):
                placeholder_count = newfilename_format.count('*')
                id = str(int(match.group(1))).zfill(placeholder_count)
                newfilename = re.sub('\*{' + str(placeholder_count) + '}', id, newfilename_format) + \
                              os.path.splitext(filename)[1]
                newfilepath = os.path.join(original_path, newfilename)
                os.rename(filepath, newfilepath)
        self.__update_listbox(self.__entry_path.get())

    def __selectfile(self,ev=None):
        filename = str(self.__listbox.get(self.__listbox.curselection()))
        filename = (filename[0:filename.rfind('.')]) if ('.' in filename) else filename
        if not os.path.isdir(filename):
            self.__listbox.config(selectbackground='skyblue')
            self.__entry_id_pattern.delete(0, END)
            self.__entry_id_pattern.insert(0, filename)
            self.__entry_newfilename_format.delete(0, END)
            self.__entry_newfilename_format.insert(0, filename)
        else:
            self.__listbox.config(selectbackground='white')

    def __update_listbox(self,path):
        filelist = os.listdir(path)
        filelist.sort()
        os.chdir(path)
        self.__listbox.delete(0, END)
        for eachfile in filelist:
            if(self.__check_filtefile.get()):
                if (os.path.isdir(eachfile)):
                    continue
                if (eachfile.startswith('.')):
                    continue
            self.__listbox.insert(END, eachfile)

    def __adddata_to_listbox(self):
        if(self.__check_usestrpath.get()):
            path = self.__entry_path.get()
        else:
            path = askdirectory(initialdir=os.path.curdir,title='Choose a directory')
        if(path != ''):
            self.__text_path.set(path)
            self.__update_listbox(path)

    def __check_path_event(self):
        if(self.__check_usestrpath.get()):
            self.__entry_path['state'] = 'normal'
        else:
            self.__entry_path['state'] = 'readonly'#readonly or disable

    def __check_filte_event(self):
        if (self.__check_filtefile.get()):
            pass
        else:
            pass

    def generate_label_entry(self):
        frame = Frame(self.__top)
        frame.grid(column=0,row=0,sticky=(N,W,E,S))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        #路径标签
        label_path = Label(frame, text='Directory Path:')
        label_path.grid(row=0,column=0,sticky=(E))
        #路径输入框
        self.__entry_path = Entry(frame, width=self.__ENTRY_PATH_WIDTH, textvariable=self.__text_path, state='readonly')
        self.__entry_path.grid(row=0, column=1, sticky=(W))
        self.__entry_path.bind('<Return>', lambda path: self.__update_listbox(path=self.__entry_path.get()))
        #文件编号正则标签
        label_id_pattern = Label(frame, text='ID Pattern :')
        label_id_pattern.grid(row=1, column=0, sticky=(E))
        #文件编号正则输入框
        self.__entry_id_pattern = Entry(frame, width=self.__ENTRY_IDPATTERN_WIDT)
        self.__entry_id_pattern.grid(row=1, column=1, sticky=(W))
        #新文件格式标签
        label_newfilename_format = Label(frame, text='New Filename Format :')
        label_newfilename_format.grid(row=2, column=0, sticky=(E))
        #新文件格式输入框
        self.__entry_newfilename_format = Entry(frame, width=self.__ENTRY_NEWFILENAMEFORMAT)
        self.__entry_newfilename_format.grid(row=2, column=1, sticky=(W))
        frame.pack()

    def generate_listbox(self):
        frame = Frame(self.__top)
        scrbllbar = Scrollbar(frame)
        scrbllbar.pack(side=RIGHT, fill=Y)
        self.__listbox = Listbox(frame, height=15, width=50, yscrollcommand=scrbllbar.set)
        self.__listbox.bind('<Double-1>', self.__selectfile)
        self.__listbox.pack(side=LEFT, fill=BOTH)
        frame.pack()

    def generate_button(self):
        frame = Frame(self.__top)
        #使用字符串路径复选框
        checkbutton_use_stringpath = Checkbutton(frame, text='Use string path', variable=self.__check_usestrpath, command=self.__check_path_event)
        checkbutton_use_stringpath.grid(row=0, column=0)
        # 过滤文件复选框
        checkbutton_filte_file = Checkbutton(frame, text='Filt file', variable=self.__check_filtefile, command=self.__check_filte_event)
        checkbutton_filte_file.grid(row=0, column=1)
        #打开按钮
        button_open= Button(frame, text='Open', command=self.__adddata_to_listbox)
        button_open.grid(row=0, column=2)
        #重命名按钮
        button_rename = Button(frame, text='Rename', command=lambda :self.__rename(self.__entry_path.get(), self.__entry_id_pattern.get(), self.__entry_newfilename_format.get()))
        button_rename.grid(row=0, column=3)
        frame.pack()

def main():
    #窗口设置
    root = Tk()
    root.title('BatchRename')
    root.geometry('500x380+700+300')
    root.resizable(width=FALSE,height=FALSE)
    #root.wm_attributes('-topmost',1)#窗口置顶,影响opendialog
    brg = BatchRenameGUI(root)
    brg.generate_label_entry()
    brg.generate_listbox()
    brg.generate_button()
    root.mainloop()

if __name__=='__main__':
    main()