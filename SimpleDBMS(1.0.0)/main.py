import os
import sys
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
from tkinter import *
from tkinter import filedialog, ttk, messagebox
import mysql.connector as mysql
import sqlalchemy
from colorama2.decor import *
import io

loc = os.getcwd()

def cursor_spin():
    for spinner in "◜◝◞◟":
        sys.stdout.write(spinner)
        sys.stdout.flush()
        time.sleep(0.03)
        sys.stdout.write("\b")

def doc(name):
    txt = Toplevel(main)
    txt.grab_set()
    txt.focus_force()
    txt.protocol("WM_DELETE_WINDOW", lambda: [txt.grab_release(), txt.destroy()])
    
    txt.resizable(False, False)
    txt.title("{} SimpleDBMS(1.0.0)".format(name))
    txt.iconphoto(False, PhotoImage(file = "{}\\UI requirement files\\images\\icon.png".format(loc)))

    Txt = Text(txt)
    Txt.insert(1.0, open("{}\\UI requirement files\\documents\\{}.txt".format(loc, name), "r").read())
    Txt.configure(state = "disabled")
    Txt.pack()

    txt.mainloop()

class Import:
    def __init__(self, manipulation = True, sql = False):
        global df, file
        if manipulation == True:
            if sql == False:
                Checkfile = filedialog.askopenfilename(title = "Open File", filetypes = [("Comma Sperated Values(CSV) files", ".csv"), ("Excel Worksheets(XLS)", ".xls")])
                try:
                    if Checkfile == "":
                        colPrint("green", "\n\nFile Opened:")
                        colPrint("yellow", "None")
                    else:
                        if Checkfile[-1] == "v":
                            df = pd.read_csv(Checkfile)
                            colPrint("green", "\n\nFile Opened:")
                            colPrint("yellow", Checkfile)
                            print(df)
                        else:
                            df = pd.read_excel(Checkfile)
                            colPrint("green", "\n\nFile Opened:")
                            colPrint("yellow", Checkfile)
                            print(df)


                        file = Checkfile
                        self.window_update()
                        
                    
                except Exception as err:
                    colPrint("red", "\n\nError: {}".format(err))
                    messagebox.showerror("ERROR", err)


            else:

                    def sqlImport():
                        global df, file
                        try:
                            connection = mysql.connect(host = host.get(),
                                                    user = user.get(),
                                                    password = pwrd.get(),
                                                    database = db.get())
                            cursor = connection.cursor()
                            cursor.execute("SELECT * FROM {};".format(table.get()))

                            df = pd.DataFrame(cursor.fetchall(), columns = [i[0] for i in cursor.description])
                            file = [host.get(), user.get(), pwrd.get(), db.get(), table.get()]

                            colPrint("green", "\n\nFile Opened:")
                            colPrint("yellow", file[0] + " :" + file[1] + " :" + file[3] + " :" + file[4])
                            print(df)

                            Sql.destroy()

                            self.window_update()

                        except Exception as err:
                            if err == "1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '' at line 1":
                                colPrint("red", "\n\nError: Database Name and/or Table Name Entry boxes/box are/is not filled")
                                messagebox.showerror("ERROR", "Database Name and/or Table Name Entry boxes/box are/is not filled")
                            else:
                                colPrint("red", "\n\nError: {}".format(err))
                                messagebox.showerror("ERROR", err)

                    Sql = Toplevel(main)
                    Sql.focus_force()
                    Sql.grab_set()
                    
                    Sql.resizable(False, False)

                    Sql.title("Import From MySQL")

                    Sql.iconphoto(False, PhotoImage(file = "{}\\UI requirement files\\images\\icon.png".format(loc)))
                    
                    Sql.protocol("WM_DELETE_WINDOW", lambda: [Sql.grab_release(), colPrint("green", "\n\nFile Opened:"), colPrint("yellow", "None"), Sql.destroy()])

                    LabelFrameImpSql = LabelFrame(Sql)
                    LabelFrameImpSql.pack(fill = "x", padx = 10, pady = 10)
                    
                    host = Label(LabelFrameImpSql, text = "Enter the Host Name:", font = 30).grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "w")
                    host = Entry(LabelFrameImpSql)
                    host.grid(row = 0, column = 1, padx = 5, pady = 5)
                    
                    user = Label(LabelFrameImpSql, text = "Enter the User Name:", font = 30).grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "w")
                    user = Entry(LabelFrameImpSql)
                    user.grid(row = 1, column = 1, padx = 5, pady = 5)
                    
                    pwrd = Label(LabelFrameImpSql, text = "Enter the Password:", font = 30).grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "w")
                    pwrd = Entry(LabelFrameImpSql, show = "*")
                    pwrd.grid(row = 2, column = 1)
                    
                    db = Label(LabelFrameImpSql, text = "Enter the Database Name:", font = 30).grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "w")
                    db = Entry(LabelFrameImpSql)
                    db.grid(row = 3, column = 1)
                    
                    table = Label(LabelFrameImpSql, text = "Enter the Table Name", font = 30).grid(row = 4, column = 0, padx = 5, pady = 5, sticky = "w")
                    table = Entry(LabelFrameImpSql)
                    table.grid(row = 4, column = 1)
                    
                    imp = Button(LabelFrameImpSql, text = "📥", font = 90, bg = "white", relief = "groove", command = sqlImport)
                    imp.grid(row = 5, column = 0, columnspan = 2, padx = 5, pady = 5)
           
        else:
            self.window_update()

    def window_update(self):
        for widgets in status.winfo_children():
            widgets.destroy()

        display.update(df)
        
        manipulationSpinboxInsertRow["to"] = len(df)
        manipulationSpinboxInsertColumn["to"] = len(df.columns)
        analysisScaleGetRows["to"] = len(df)

        manipulationListboxSortRows.delete(0, END)
        manipulationListboxSortColumns.delete(0, END)
        analysisListboxGetColumns.delete(0, END)
        analysisListboxGetUnique.delete(0, END)
        analysisListbox1Pivot.delete(0, END)
        analysisListbox2Pivot.delete(0, END)
        analysisListbox1Function.delete(0, END)

        for i in range(len(df.columns)):
            item = list(df.columns)[i]
            manipulationListboxSortRows.insert(i, item)
            analysisListboxGetColumns.insert(i, item)
            analysisListboxGetUnique.insert(i, item)
            analysisListbox1Pivot.insert(i, item)
            analysisListbox2Pivot.insert(i, item)
            analysisListbox1Function.insert(i, item)

        for i in range(len(df)):
            manipulationListboxSortColumns.insert(i, list(df.index)[i])

        for i in range(len(["Min", "Max", "Count", "Avg", "Sum", "Mean"])):
            item = ["Min", "Max", "Count", "Avg", "Sum", "Mean"][i]
            analysisListbox2Function.insert(i, item)

        if type(file) != list:
            statusButton = Button(status, text = "{}".format(file), font = 20, fg = "red", activebackground = "orange", relief = "flat", command = lambda: os.startfile(file))
            statusButton.pack(side = "left")

        else:
            Label(status, text = "{} : {} : {} : {}".format(file[0], file[1], file[3], file[4]), font = 20, fg = "red").pack(side = "left")
        
        Label(status, text = "{} rows X {} columns".format(len(df.index), len(df.columns)), font = 20, fg = "red").pack(side = "right")

        File.entryconfig(3, state = "normal")
        File.entryconfig(4, state = "normal")

def Export(sql = False):
    if sql == False:
        saveAsLocation = filedialog.asksaveasfilename(title = "Save As...", filetypes = [("Comma Sperated Values(CSV) files", ".csv"), ("Excel Worksheets(XLS)", ".xls"), ("Hypertext Markup Language(HTML) files", "*.html")], defaultextension = [("Comma Sperated Values(CSV) files", ".csv"), ("Excel Worksheets(XLS)", ".xls"), ("Hypertext Markup Language(HTML) files", "*.html")])
        os.system("chmod 755 {}".format(saveAsLocation))

        try:
            if saveAsLocation == "":
                colPrint("green", "\n\nFile Saved:")
                colPrint("yellow", "None")
            else:
                if saveAsLocation[-1] == "v":
                    df.to_csv(saveAsLocation, index = False)
                    colPrint("green", "\n\nFile Saved:")
                elif saveAsLocation[-1] == "s":
                    df.to_excel(saveAsLocation, index = False)
                    colPrint("green", "\n\nFile Saved:")
                else:
                    df.to_html(saveAsLocation, index = False)
                    colPrint("green", "\n\nFile Saved:")

                colPrint("yellow", saveAsLocation)
                print(df)
        except Exception as err:
            colPrint("red", "\n\nError: {}".format(err))
            messagebox.showerror("ERROR", err)

    else:
        def sqlExport():
            try:
                engine = sqlalchemy.create_engine("mysql+pymysql://{}:{}@{}/{}".format(user.get(), pwrd.get(), host.get(), db.get()))
                
                df.to_sql(table.get(), engine, index = False, if_exists = "replace")
                
                colPrint("green", "\n\nFile Saved:")
                colPrint("yellow", host.get() + " :" + user.get() + " :" + db.get() + " :" + table.get())
                print(df)

                Sql.destroy()
            except Exception as err:
                colPrint("red", "\n\nError: {}".format(err))
                messagebox.showerror("ERROR", err)

        Sql = Toplevel(main)
        Sql.focus_force()
        Sql.grab_set()
        
        Sql.resizable(False, False)

        Sql.title("Export To MySQL")

        Sql.iconphoto(False, PhotoImage(file = "{}\\UI requirement files\\images\\icon.png".format(loc)))
        
        Sql.protocol("WM_DELETE_WINDOW", lambda: [Sql.grab_release(), colPrint("green", "\n\nFile Exported:"), colPrint("yellow", "None"), Sql.destroy()])

        LabelFrameImpSql = LabelFrame(Sql)
        LabelFrameImpSql.pack(fill = "x", padx = 10, pady = 10)
        
        host = Label(LabelFrameImpSql, text = "Enter the Host Name:", font = 30).grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "w")
        host = Entry(LabelFrameImpSql)
        host.grid(row = 0, column = 1, padx = 5, pady = 5)
        
        user = Label(LabelFrameImpSql, text = "Enter the User Name:", font = 30).grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "w")
        user = Entry(LabelFrameImpSql)
        user.grid(row = 1, column = 1, padx = 5, pady = 5)
        
        pwrd = Label(LabelFrameImpSql, text = "Enter the Password:", font = 30).grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "w")
        pwrd = Entry(LabelFrameImpSql, show = "*")
        pwrd.grid(row = 2, column = 1)
        
        db = Label(LabelFrameImpSql, text = "Enter the Database Name:", font = 30).grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "w")
        db = Entry(LabelFrameImpSql)
        db.grid(row = 3, column = 1)
        
        table = Label(LabelFrameImpSql, text = "Enter the Table Name", font = 30).grid(row = 4, column = 0, padx = 5, pady = 5, sticky = "w")
        table = Entry(LabelFrameImpSql)
        table.grid(row = 4, column = 1)
        
        exp = Button(LabelFrameImpSql, text = "📥", font = 90, bg = "white", relief = "groove", command = sqlExport)
        exp.grid(row = 5, column = 0, columnspan = 2, padx = 5, pady = 5)

def rounded_rect(canvas, x, y, w, h_, c_):
    global arc1, arc2, arc3, arc4, line1, line2, line3, line4

    arc1 = canvas.create_arc( x,   y,   x+2*c_,   y+2*c_, outline = settings.backgroundColor.comp_color, start= 90, extent=90, style="arc")
    arc2 = canvas.create_arc(x+w-2*c_, y+h_-2*c_, x+w, y+h_, outline = settings.backgroundColor.comp_color, start=270, extent=90, style="arc")
    arc3 = canvas.create_arc(x+w-2*c_, y,   x+w, y+2*c_, outline = settings.backgroundColor.comp_color,  start=  0, extent=90, style="arc")
    arc4 = canvas.create_arc(x,   y+h_-2*c_, x+2*c_,   y+h_, outline = settings.backgroundColor.comp_color, start=180, extent=90, style="arc")
    line1 = canvas.create_line(x+c_, y, x+w-c_, y, fill = settings.backgroundColor.comp_color)
    line2 = canvas.create_line(x+c_, y+h_, x+w-c_, y+h_, fill = settings.backgroundColor.comp_color)
    line3 = canvas.create_line(x,   y+c_, x, y+h_-c_, fill = settings.backgroundColor.comp_color)
    line4 = canvas.create_line(x+w, y+c_, x+w, y+h_-c_, fill = settings.backgroundColor.comp_color)

class settings:
    class backgroundColor:
        ori_color, comp_color = "#000000", "#ffffff"
    
        def bgColorUI():
            bgColorWin = Toplevel(main)
            bgColorWin.grab_set()
            bgColorWin.focus_force()

            bgColorWin.resizable(False, False)
            bgColorWin.iconphoto(False, PhotoImage(file = "{}\\UI requirement files\\images\\icon.png".format(loc)))

            labelframe = LabelFrame(bgColorWin)
            labelframe.pack(padx = 10, pady = 10)

            label_n_spinboxFrame = Frame(labelframe)
            label_n_spinboxFrame.pack(padx = 5, pady = 5)
            
            buttonsFrame = Frame(labelframe)
            buttonsFrame.pack(padx = 5, pady = 5)

            R = Label(label_n_spinboxFrame, text = "R(0 - 255)", font = 30, fg = "red").grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "w")
            G = Label(label_n_spinboxFrame, text = "G(0 - 255)", font = 30, fg = "green").grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "w")
            B = Label(label_n_spinboxFrame, text = "B(0 - 255)", font = 30, fg = "blue").grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "w")
            
            R = Spinbox(label_n_spinboxFrame, from_ = 0, to = 255)
            G = Spinbox(label_n_spinboxFrame, from_ = 0, to = 255)
            B = Spinbox(label_n_spinboxFrame, from_ = 0, to = 255)
            R.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "w")
            G.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = "w")
            B.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = "w")

            def get(state = None):
                bg = "#%02x%02x%02x" % ((int(R.get()), int(G.get()), int(B.get())))
                comp_bg = "#%02x%02x%02x" % ((255 - int(R.get()), 255 - int(G.get()), 255 - int(B.get())))

                def changes(bg, comp_bg):
                    display.config(bg = bg)


                    manipulation_toolbar.config(bg = bg)

                    manipulation_canvas.config(bg = bg)
                    manipulation_canvas.itemconfig(arc1, outline = comp_bg)
                    manipulation_canvas.itemconfig(arc2, outline = comp_bg)
                    manipulation_canvas.itemconfig(arc3, outline = comp_bg)
                    manipulation_canvas.itemconfig(arc4, outline = comp_bg)
                    manipulation_canvas.itemconfig(line1, fill = comp_bg)
                    manipulation_canvas.itemconfig(line2, fill = comp_bg)
                    manipulation_canvas.itemconfig(line3, fill = comp_bg)
                    manipulation_canvas.itemconfig(line4, fill = comp_bg)

                    manipulationHeading.config(bg = comp_bg, fg = bg)

                    manipulationInsertRow.config(bg = bg, fg = comp_bg)
                    manipulationLabelInsertRow.config(bg = bg, fg = comp_bg)
                    manipulationSpinboxInsertRow.config(bg = bg, fg = comp_bg)
                    manipulationButtonInsertRow.config(bg = bg, fg = comp_bg)
                    
                    manipulationButtonInsertRow.config(bg = bg, fg = comp_bg)
                    manipulationLabelInsertColumn.config(bg = bg, fg = comp_bg)
                    manipulationSpinboxInsertColumn.config(bg = bg, fg = comp_bg)
                    mainpulationButtonInsertColumn.config(bg = bg, fg = comp_bg)

                    manipulationDelete.config(bg = bg, fg = comp_bg)
                    manipulationButtonDeleteRows.config(bg = bg, fg = comp_bg)
                    manipulationButtonDeleteColumns.config(bg = bg, fg = comp_bg)

                    manipulationAppend.config(bg = bg, fg = comp_bg)
                    manipulationButtonAppendFile.config(bg = bg, fg = comp_bg)
                    manipulationButtonAppendMySQL.config(bg = bg, fg = comp_bg)

                    manipulationTranspose.config(bg = bg, fg = comp_bg)
                    manipulationButtonTranspose.config(bg = bg, fg = comp_bg)

                    manipulationSortRows.config(bg = bg, fg = comp_bg)      
                    manipulationLabelSortRows.config(bg = bg, fg = comp_bg)
                    manipulationListboxSortRows.config(bg = bg, fg = comp_bg)
                    manipulationButtonSortRows.config(bg = bg, fg = comp_bg)

                    analysis_toolbar.config(bg = bg)
                    
                    analysis_canvas.config(bg = bg)    
                    analysis_canvas.itemconfig(arc1, outline = comp_bg)
                    analysis_canvas.itemconfig(arc2, outline = comp_bg)
                    analysis_canvas.itemconfig(arc3, outline = comp_bg)
                    analysis_canvas.itemconfig(arc4, outline = comp_bg)
                    analysis_canvas.itemconfig(line1, fill = comp_bg)
                    analysis_canvas.itemconfig(line2, fill = comp_bg)
                    analysis_canvas.itemconfig(line3, fill = comp_bg)
                    analysis_canvas.itemconfig(line4, fill = comp_bg)

                    analysisHeading.config(bg = comp_bg, fg = bg)

                    analysisGetrows.config(bg = bg, fg = comp_bg)
                    analysisScaleGetRows.config(bg, bg, fg = comp_bg)
                    analysisButtonGetTopGetRows.config(bg = bg, fg = comp_bg)
                    analysisButtonGetBottomGetRows.config(bg = bg, fg = comp_bg)
                    
                    analysisGetcolumns.config(bg = bg, fg = comp_bg)
                    analysisListboxGetColumns.config(bg = bg, fg = comp_bg)
                    analysisButtonGetColumns.config(bg = bg, fg = comp_bg)

                    analysisStatistics.config(bg = bg, fg = comp_bg)
                    analysisButtonGetStats.config(bg = bg, fg = comp_bg)

                    analysisInformation.config(bg = bg, fg = comp_bg)
                    analysisButtonGetInfo.config(bg = bg, fg = comp_bg)

                    analysisUnique.config(bg = bg, fg = comp_bg)
                    analysisListboxGetUnique(bg = bg, fg = comp_bg)
                    analysisButtonGetUnique.config(bg = bg, fg = comp_bg)

                    analysisPivot.config(bg = bg, fg = comp_bg)
                    analysisLabel1Pivot.config(bg = bg, fg = comp_bg)
                    analysisListbox1Pivot.config(bg = bg, fg = comp_bg)
                    analysisLabel2Pivot.config(bg = bg, fg = comp_bg)
                    analysisListbox2Pivot.config(bg = bg,  fg = comp_bg)
                    analysisButtonPivotGetTable.config(bg = bg, fg = comp_bg)

                    analysisFunction.config(bg = bg, fg = comp_bg)
                    analysisFrameFunctionLabels.config(bg = bg)
                    analysisLabel1Function.config(bg = bg, fg = comp_bg)
                    analysisLabel2Function.config(bg = bg, fg = comp_bg)
                    analysisFrameFunctionListboxes.config(bg = bg)
                    analysisListbox1Function.config(bg = bg, fg = comp_bg)
                    analysisListbox2Function.config(bg = bg, fg = comp_bg)
                    anlaysisFrameFunctionButtons.config(bg = bg)
                    analysisButtonFucntion.config(bg = bg, fg = comp_bg)


                    visualization_toolbar.config(bg = bg)

                    visualization_canvas.config(bg = bg)
                    visualization_canvas.itemconfig(arc1, outline = comp_bg)
                    visualization_canvas.itemconfig(arc2, outline = comp_bg)
                    visualization_canvas.itemconfig(arc3, outline = comp_bg)
                    visualization_canvas.itemconfig(arc4, outline = comp_bg)
                    visualization_canvas.itemconfig(line1, fill = comp_bg)
                    visualization_canvas.itemconfig(line2, fill = comp_bg)
                    visualization_canvas.itemconfig(line3, fill = comp_bg)
                    visualization_canvas.itemconfig(line4, fill = comp_bg)
                    visualizationHeading.config(bg = comp_bg, fg = bg)

                    visualizationHeading.config(bg = bg)

                    visualizationsCharttype.config(bg = bg, fg = comp_bg)
                    visualizationListboxChartType.config(bg = bg, fg = comp_bg)
                    
                    visualizationDatavis.config(bg = bg, fg = comp_bg)
                    visualizationLabelxDatavis.config(bg = bg, fg = comp_bg)
                    visualizationLabelyDatavis.config(bg = bg, fg = comp_bg)
                    
                    visualizationLabelling.config(bg = bg, fg = comp_bg)

class ShowData:
    
    def __init__(self, parent): 
        
        canvas = Canvas(parent, bg = "white", relief = "sunken", bd = 5)
        canvas.grid(row = 1, column = 1, sticky = "news")
        
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(1, weight=1)

        scrollbarx = ttk.Scrollbar(parent, orient = "horizontal", command = canvas.xview)
        scrollbarx.grid(row = 0, column = 1, sticky = "news")
        
        scrollbary = ttk.Scrollbar(parent, orient = "vertical", command = canvas.yview)
        scrollbary.grid(row = 1, column = 0, sticky = "news")

        canvas.config(xscrollcommand = scrollbarx.set, yscrollcommand = scrollbary.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

        self.frame = Frame(canvas)
        self.frame.pack(fill = "both", expand = True)

        canvas.create_window((0,0), window = self.frame, anchor = "nw")

    def df(self, dataframe):
        
        progress = ttk.Progressbar(status, orient = HORIZONTAL, length = 300, mode = "determinate")
        progress.pack()
        
        colNum = len(dataframe.columns)
        rowNum = len(dataframe.index)

        blank = Label(self.frame, relief = "raised")
        blank.grid(row = 0, column = 0, sticky = "news")

        for i in range(rowNum):
            index = Label(self.frame, text = list(dataframe.index)[i], relief = "raised", bg = "grey")
            index.grid(row = i + 1, column = 0, sticky = "news", ipadx = 10, ipady = 10)
            
        progress["value"] += 10
        progress.update_idletasks()
        
        for i in range(colNum):
            head = Label(self.frame, text = list(dataframe.columns)[i], relief = "raised", bg = "orange")
            head.grid(row = 0, column = i + 1, sticky = "news", ipadx = 10, ipady = 10)

        progress["value"] += 10
        progress.update_idletasks()
            
        for i in range(rowNum):
            progress["value"] += 80/rowNum
            progress.update_idletasks()
            for j in range(colNum):
                cell = Label(self.frame, text = dataframe.loc[dataframe.index[i]][dataframe.columns[j]], relief = "ridge")
                cell.grid(row = i + 1, column = j + 1, sticky = "news")
                    
        progress.destroy() 
        
    def clear(self):
        
        for widgets in self.frame.winfo_children():
            widgets.destroy()

    def update(self, dataframe):
        
        self.clear()
        self.df(dataframe)

class toolbar:
    class _manipu_:
        class Insert:
            def row():
                def insert():
                    new_row = rowvalues.get().split(",")
                    for i in range(len(new_row)):
                        new_row[i] = eval(new_row[i].strip())

                    new_row = pd.DataFrame([new_row], columns = list(df.columns))
                    
                    
                    manipulationrowinsertspinbox = int(manipulationSpinboxInsertRow.get())

                    top = df.head(manipulationrowinsertspinbox).append(new_row, ignore_index = True)
                    Df = top.append(df.tail(abs(len(df) - manipulationrowinsertspinbox)), ignore_index = True)
                    if type(file) != list:
                        if file[-1] == "v":
                            Df.to_csv(file, index = False)
                            
                        else:
                            Df.to_excel(file, index = False)
                            
                        rowToInsert.destroy()
                        display.update(Df)
                    else:
                        engine = create_engine("mysql+pymysql://{}:{}@{}/{}".format(file[1], file[2], file[0], file[3]))
                        Df.to_sql(file[4], engine, index = False, if_exists = "replace")
                        rowToInsert.destroy()
                        display.update(Df)

                rowToInsert = Toplevel(main)
                rowToInsert.title("Insert Row")

                rowToInsert.grab_set()

                Label(rowToInsert, text = "Enter the row values here seperated by commas(example: \"a\", \"b\",2, \"d\"):").pack(fill = "x", padx = 5, pady = 5)

                rowvalues = Entry(rowToInsert)
                rowvalues.pack(fill = "x", padx = 5, pady = 5)

                insertRowvalues = Button(rowToInsert, text = "Insert", bg = "white", relief = "groove", command = insert).pack(fill = "x", padx = 5, pady = 5)

                rowToInsert.mainloop()

            def column():
                def insert():
                    
                    new_col = colvalues.get().split(",")
                    for i in range(len(new_col)):
                        new_col[i] = eval(new_col[i])
                            
                    
                    manipulationcolumninsertspinbox = int(manipulationSpinboxInsertColumn.get())

                    df.insert(manipulationcolumninsertspinbox, newColName.get(), new_col)

                    Df = df.copy()

                    if type(file) != list:

                        if file[-1] == "v":
                            Df.to_csv(file, index = False)
                                
                        else:
                            Df.to_excel(file, index = False)
                                
                        colToInsert.destroy()
                        display.update(Df)

                    else:
                        engine = create_engine("mysql+pymysql://{}:{}@{}/{}".format(file[1], file[2], file[0], file[3]))
                        Df.to_sql(file[4], engine, index = False, if_exists = "replace")
                        colToInsert.destroy()
                        display.update(Df)


                colToInsert = Toplevel(main)
                colToInsert.title("Insert Column")

                colToInsert.grab_set()

                Label(colToInsert, text = "Enter the row values here sepearated by commas(example: \"a\", \"b\",2, \"d\"):").pack(fill = "x", padx = 5, pady = 5)

                colvalues = Entry(colToInsert)
                colvalues.pack(fill = "x", padx = 5, pady = 5)

                Label(colToInsert, text = "Enter the new column's name:").pack(fill = "x", padx = 5, pady = (10, 5))

                newColName = Entry(colToInsert)
                newColName.pack(fill = "x", padx = 5, pady = (5, 10))

                Button(colToInsert, text = "Insert", bg = "white", relief = "groove", command = insert).pack(fill = "x", padx = 5, pady = 5)

                colToInsert.mainloop()

        class Delete:
            def row():
                def drop():
                    if type(file) != list:
                        drop_rows = rowIndices.get().split(",")
                        for i in range(len(drop_rows)):
                            drop_rows[i] = eval(drop_rows[i])

                    print(drop_rows)

                    df.drop(labels = drop_rows, axis = 0, inplace = True)
                    Df = df.copy()
                    if file[-1] == "v":
                        Df.to_csv(file, index = False)

                    else:
                        Df.to_excel(file, index = False)

                    display.update(Df)

                rowToDel = Toplevel(main)
                rowToDel.title("Delete Row(s)")

                rowToDel.grab_set()

                Label(rowToDel, text = "Enter the index/indices of the roe/roes to delete seperated by commas(example: 1, 2, 101,5,0):").pack(fill = "x", padx = 5, pady = 5)

                rowIndices = Entry(rowToDel)
                rowIndices.pack(fill = "x", padx = 5, pady = 5)

                deleteRows = Button(rowToDel, text = "Delete", bg = "white", relief = "groove", command = drop)
                deleteRows.pack(fill = "x", padx = 5, pady = 5)

            def column():
                def drop():
                    drop_cols = colIndices.get().split(",")
                    for i in range(len(drop_cols)):
                        drop_cols[i] = str((drop_cols[i])).strip()

                    df.drop(labels = drop_cols, axis = 1, inplace = True)

                    Df = df.copy()

                    if file[-1] == "v":
                        Df.to_csv(file, index= False)

                    else:
                        Df.to_excel(file, index = False)

                    display.update(Df)

                colToDel = Toplevel(main)
                colToDel.title("Delete column(s)")
                    
                colToDel.grab_set()

                Label(colToDel, text = "Enter the label/labels of the column/columns to delete seperated by commas(example: 1, 2, 101,5, 0):").pack(fill = "x", padx = 5, pady = 5)

                colIndices = Entry(colToDel)
                colIndices.pack(fill = "x", padx = 5, pady = 5)

                deletecol = Button(colToDel, text = "Delete", bg = "white", relief = "groove", command = drop)
                deletecol.pack(fill = "x", padx = 5, pady = 5)

        class appendDf:
            def File():
                global df
                DfFile = filedialog.askopenfilename(title = "Open a File to append", filetypes = [("Comma Sperated Values(CSV) files", ".csv"), ("Excel Worksheets(XLS)", ".xls")])
                
                if DfFile != "" or DfFile != None:
                    try: 
                        if DfFile[-1] == "v":
                            Df = pd.read_csv(DfFile)
                        else:
                            Df = pd.read_excel(DfFile)
                        df = pd.concat([df, Df], ignore_index = True)
                        
                        if type(file) != list:
                            if file[-1] == "v":
                                df.to_csv(file, index = False)
                            else:
                                df.to_excel(file, index = False)
                        else:
                            engine = create_engine("mysql+pymysql://{}:{}@{}/{}".format(file[1], file[2], file[0], file[3]))
                            df.to_sql(file[4], engine, index = False, if_exists = "replace")

                        display.update(df)

                    except Exception as err:
                        colPrint("red", "\n\nError: {}".format(err))
                        messagebox.showerror("ERROR", err)

            def SQL():
                    def append():
                        global df
                        connection = mysql.connect(host = host.get(),
                                                user = user.get(),
                                                password = pwrd.get(),
                                                database = db.get())
                        cursor = connection.cursor()
                        cursor.execute("SELECT * FROM {};".format(table.get()))

                        DF = pd.DataFrame(cursor.fetchall(), columns = [i[0] for i in cursor.description])#
                        DfFile = [host.get(), user.get(), pwrd.get(), db.get(), table.get()]

                        if DfFile != None:
                            try:
                                df = pd.concat([df, DF], ignore_index = True)

                                if type(file) != list:
                                    if file[-1] == "v":
                                        df.to_csv(file, index = False)
                                    else:
                                        df.to_excel(file, index = False)
                                else:
                                    engine = create_engine("mysql+pymysql://{}:{}@{}/{}".format(file[1], file[2], file[0], file[3]))
                                    df.to_sql(file[4], engine, index = False, if_exists = "replace")

                            except Exception as err:
                                colPrint("red", "\n\nError: {}".format(err))
                                messagebox.showerror("ERROR", err)
                                
                        Sql.destroy()

                        display.update(df)

                except Exception as err:
                    if err == "1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '' at line 1":
                        colPrint("red", "\n\nError: Database Name and/or Table Name Entry boxes/box are/is not filled")
                        messagebox.showerror("ERROR", "Database Name and/or Table Name Entry boxes/box are/is not filled")
                    else:
                        colPrint("red", "\n\nError: {}".format(err))
                        messagebox.showerror("ERROR", err)

                Sql = Toplevel(main)
                Sql.focus_force()
                Sql.grab_set()
                
                Sql.resizable(False, False)

                #Toplevel window title
                Sql.title("Import From MySQL to append")

                #Toplevel window icon
                Sql.iconphoto(False, PhotoImage(file = "{}\\UI requirement files\\images\\icon.png".format(loc)))
                
                Sql.protocol("WM_DELETE_WINDOW", lambda: [Sql.grab_release(), colPrint("green", "\n\nFile Opened:"), colPrint("yellow", "None"), Sql.destroy()])

                LabelFrameImpSql = LabelFrame(Sql)
                LabelFrameImpSql.pack(fill = "x", padx = 10, pady = 10)
                
                host = Label(LabelFrameImpSql, text = "Enter the Host Name:", font = 30).grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "w")
                host = Entry(LabelFrameImpSql)
                host.grid(row = 0, column = 1, padx = 5, pady = 5)
                
                user = Label(LabelFrameImpSql, text = "Enter the User Name:", font = 30).grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "w")
                user = Entry(LabelFrameImpSql)
                user.grid(row = 1, column = 1, padx = 5, pady = 5)
                
                pwrd = Label(LabelFrameImpSql, text = "Enter the Password:", font = 30).grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "w")
                pwrd = Entry(LabelFrameImpSql, show = "*")
                pwrd.grid(row = 2, column = 1)
                
                db = Label(LabelFrameImpSql, text = "Enter the Database Name:", font = 30).grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "w")
                db = Entry(LabelFrameImpSql)
                db.grid(row = 3, column = 1)
                
                table = Label(LabelFrameImpSql, text = "Enter the Table Name", font = 30).grid(row = 4, column = 0, padx = 5, pady = 5, sticky = "w")
                table = Entry(LabelFrameImpSql)
                table.grid(row = 4, column = 1)
                
                imp = Button(LabelFrameImpSql, text = "📥", font = 90, bg = "white", relief = "groove", command = append)
                imp.grid(row = 5, column = 0, columnspan = 2, padx = 5, pady = 5)
                

        def transposeDF():
            global df
            if type(file) != list:
                df = pd.DataFrame(df.transpose())
                if file[-1] == "v":
                    df.to_csv(file, index = False)

                else:
                    df.to_excel(file, index = False)

            else:
                colPrint("red", "Error: Can't transpose a MySQL Table")
                messagebox.showerror("ERROR", "Can't transpose a MySQL Table")

            display.update(df)
            
        def update():
            if type(file) == list:
                def run():
                    connection = mysql.connect(host = file[0],
                                                        user = file[1],
                                                        password = file[2],
                                                        database = file[3])
                    cursor = connection.cursor()
                    cursor.execute("UPDATE {} SET {} WHERE {};".format(file[4], setEntry.get(), conditionEntry.get()))
                    cursor.execute("SELECT * FROM {}".format(file[4]))
                    df = pd.DataFrame(cursor.fetchall(), columns)
                    display.update(df)

                updateTable = Toplevel(main)
                updateTable.title("Update Table")
                
                setEntryLabel = Label(updateTable, text = "Enter your update information:")
                setEntry = Entry(updateTable)
                conditionEntryLabel = Label(updateTable, text = "Enter your conditions:")
                conditionEntry = Entry(updateTable)
                updateButton = Button(update, text = "Update", bg = "White", relief = "groove", command = run)
                
                setEntryLavel.pack(fill = "x", padx = 5, pady = 5)
                setEntry.pack(fill = "x", padx = 5, pady = (5, 7))
                conditionEntryLabel.pack(fill = "x", padx = 5, pady = (7, 5))
                conditionEntry.pack(fill = "x", padx = 5, pady = (5, 7))
                updateButton.pack(fill = "x", padx = 5, pady = (7, 5))
                
            else:
                def run():
                    oldvals = setEntry.get().split(",")
                    for i in oldvals:
                        oldvals[i] = oldvals[i].strip()
                        
                    newvals = conditionEntry.get().split(",")
                    for i in newvals:
                        newvals[i] = newvals[i].strip()
                        
                    for i in range(len(oldvals)):
                        df["{}".format(columnchosen)] = df["{}".format(columnchosen)].replace(oldvals[i], newvals[i])
                    
                    display.update(df)
                    
                updateTable = Toplevel(main)
                updateTable.title("Update Table")
                
                clicked = StringVar()
                clicked.set("Column Name")
                
                columnchosen = OptionMenu(updateTable, clicked, *list(df.columns.values))
                setEntryLabel = Label(updateTable, text = "Enter values from the column you want to replace:")
                setEntry = Entry(updateTable)
                conditionEntryLabel = Label(updateTable, text = "Enter the new values:")
                conditionEntry = Entry(updateTable)
                updateButton = Button(update, text = "Update", bg = "White", relief = "groove", command = run)
                
                setEntryLavel.pack(fill = "x", padx = 5, pady = 5)
                setEntry.pack(fill = "x", padx = 5, pady = 5)
                conditionEntryLabel.pack(fill = "x", padx = 5, pady = 5)
                conditionEntry.pack(fill = "x", padx = 5, pady = (5, 7))
                updateButton.pack(fill = "x", padx = 5, pady = (7, 5))
                
        class sort:
            def row(asc = True):
                if asc == True:
                    if type(file) != list:
                        for i in manipulationListboxSortRows.curselection():
                            df.sort_values(by = [str(manipulationListboxSortRows.get(i))], axis = 0, ascending = asc, inplace = True)
                            display.update(df)
                    else:
                        connection = mysql.connect(host = file[0],
                                                            user = file[1],
                                                            password = file[2],
                                                            database = file[3])
                        cursor = connection.cursor()
                        cursor.execute("SELECT * FROM {} ORDER BY {} ASC;".format(file[4], df.columns.values[manipulationListboxSortRows.curselection()]))
                        df = pd.DataFrame(cursor.fetchall(), columns)
                        display.update(df)
                elif asc == False:
                    if type(file) != list:
                        for i in manipulationListboxSortRows.curselection():
                            df.sort_values(by = [str(manipulationListboxSortRows.get(i))], axis = 0, ascending = desc, inplace = True)
                            display.update(df)
                    else:
                        connection = mysql.connect(host = file[0],
                                                            user = file[1],
                                                            password = file[2],
                                                            database = file[3])
                        cursor = connection.cursor()
                        cursor.execute("SELECT * FROM {} ORDER BY {} DESC;".format(file[4], df.columns.values[manipulationListboxSortRows.curselection()]))
                        df = pd.DataFrame(cursor.fetchall(), columns)
                        display.update(df)

    class _anly_:
        class Rows:
            def TopRows():
                anlyDf = df.head(analysisScaleGetRows.get())
                colPrint("yellow", "\n\nAnalytical Output: ")
                print(file, "\n", anlyDf)
                display.update(anlyDf)

            def BottomRows():
                anlyDf = df.tail(analysisScaleGetRows.get())
                anlyDf.index = range(len(anlyDf))
                colPrint("yellow", "\n\nAnalytical Output:")
                print(file, "\n", anlyDf)
                display.update(anlyDf)

            def custom():
                def getcustomrows():

                    col = df[columnSelected.get()]
                    try:
                        cond = eval(condition.get())
                    except:
                        cond = condition.get()
                    
                    if conditionSelected.get() == ">":
                        anlyDf = df[col > cond]
                        colPrint("yellow", "\n\nAnalystical Output: ")
                        print(file, "\n", anlyDf)
                        display.update(anlyDf)    

                    elif conditionSelected.get() == "<":
                        anlyDf = df[col < cond]
                        colPrint("yellow", "\n\nAnalystical Output: ")
                        print(file, "\n", anlyDf)
                        display.update(anlyDf)  

                    elif conditionSelected.get() == "≥":
                        anlyDf = df[col >= cond] 
                        colPrint("yellow", "\n\nAnalystical Output: ")
                        print(file, "\n", anlyDf)
                        display.update(anlyDf) 

                    elif conditionSelected.get() == "≤":
                        anlyDf = df[col <= cond]  
                        colPrint("yellow", "\n\nAnalystical Output: ")
                        print(file, "\n", anlyDf)
                        display.update(anlyDf)

                    elif conditionSelected.get() == "=":
                        anlyDf = df[col == cond]  
                        colPrint("yellow", "\n\nAnalystical Output: ")
                        print(file, "\n", anlyDf)
                        display.update(anlyDf)

                    elif conditionSelected.get() == "≠":
                        anlyDf = df[col != cond]  
                        colPrint("yellow", "\n\nAnalystical Output: ")
                        print(file, "\n", anlyDf)
                        display.update(anlyDf)

                def secCondi(condi):
                    def getcustomrows():
                        col = df[columnSelected.get()]
                        col2 = df[columnSelected2.get()]
                        try:
                            cond = eval(condition.get())
                        except:
                            cond = condition.get()
                            
                        try:
                            cond2 = eval(condition2.get())
                        except:
                            cond2 = condition2.get()
                            


                        if condi == "and":
                            
                            if conditionSelected.get() == ">" and conditionSelected2.get() == ">":
                                anlyDf = df[(col > cond) & (col2 > cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)  

                            elif conditionSelected.get() == ">" and conditionSelected2.get() == "<":
                                anlyDf = df[(col > cond) & (col2 < cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)  

                            elif conditionSelected.get() == ">" and conditionSelected2.get() == "≥":
                                anlyDf = df[(col > cond) & (col2 >= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == ">" and conditionSelected2.get() == "≤":
                                anlyDf = df[(col > cond) & (col2 <= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == ">" and conditionSelected2.get() == "=":
                                anlyDf = df[(col > cond) & (col2 == cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == ">" and conditionSelected2.get() == "≠":
                                anlyDf = df[(col > cond) & (col2 != cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "<" and conditionSelected2.get() == ">":
                                anlyDf = df[(col < cond) & (col2 > cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "<" and conditionSelected2.get() == "<":
                                anlyDf = df[(col < cond) & (col2 < cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)  

                            elif conditionSelected.get() == "<" and conditionSelected2.get() == "≥":
                                anlyDf = df[(col < cond) & (col2 >= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "<" and conditionSelected2.get() == "≤":
                                anlyDf = df[(col < cond) & (col2 <= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "<" and conditionSelected2.get() == "=":
                                anlyDf = df[(col < cond) & (col2 == cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "<" and conditionSelected2.get() == "≠":
                                anlyDf = df[(col < cond) & (col2 != cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)  

                            elif conditionSelected.get() == "≥" and conditionSelected2.get() == ">":
                                anlyDf = df[(col >= cond) & (col2 > cond2)] 
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≥" and conditionSelected2.get() == "<":
                                anlyDf = df[(col >= cond) & (col2 < cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)  

                            elif conditionSelected.get() == "≥" and conditionSelected2.get() == "≥":
                                anlyDf = df[(col >= cond) & (col2 >= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≥" and conditionSelected2.get() == "≤":
                                anlyDf = df[(col >= cond) & (col2 <= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≥" and conditionSelected2.get() == "=":
                                anlyDf = df[(col >= cond) & (col2 == cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≥" and conditionSelected2.get() == "≠":
                                anlyDf = df[(col >= cond) & (col2 != cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)  

                            elif conditionSelected.get() == "≤" and conditionSelected2.get() == ">":
                                anlyDf = df[(col <= cond) & (col2 > cond2)] 
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≤" and conditionSelected2.get() == "<":
                                anlyDf = df[(col <= cond) & (col2 < cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)  

                            elif conditionSelected.get() == "≤" and conditionSelected2.get() == "≥":
                                anlyDf = df[(col <= cond) & (col2 >= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≤" and conditionSelected2.get() == "≤":
                                anlyDf = df[(col <= cond) & (col2 <= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≤" and conditionSelected2.get() == "=":
                                anlyDf = df[(col <= cond) & (col2 == cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≤" and conditionSelected2.get() == "≠":
                                anlyDf = df[(col <= cond) & (col2 != cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "=" and conditionSelected2.get() == ">":
                                anlyDf = df[(col == cond) & (col2 > cond2)] 
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "=" and conditionSelected2.get() == "<":
                                anlyDf = df[(col == cond) & (col2 < cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)  

                            elif conditionSelected.get() == "=" and conditionSelected2.get() == "≥":
                                anlyDf = df[(col == cond) & (col2 >= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "=" and conditionSelected2.get() == "≤":
                                anlyDf = df[(col == cond) & (col2 <= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "=" and conditionSelected2.get() == "=":
                                anlyDf = df[(col == cond) & (col2 == cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "=" and conditionSelected2.get() == "≠":
                                anlyDf = df[(col == cond) & (col2 != cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≠" and conditionSelected2.get() == "<":
                                anlyDf = df[(col != cond) & (col2 < cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)  

                            elif conditionSelected.get() == "≠" and conditionSelected2.get() == "≥":
                                anlyDf = df[(col != cond) & (col2 >= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≠" and conditionSelected2.get() == "≤":
                                anlyDf = df[(col != cond) & (col2 <= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≠" and conditionSelected2.get() == "=":
                                anlyDf = df[(col != cond) & (col2 == cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≠" and conditionSelected2.get() == "≠":
                                anlyDf = df[(col != cond) & (col2 != cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                        elif condi == "or":
                            if conditionSelected.get() == ">" and conditionSelected2.get() == ">":
                                anlyDf = df[(col > cond) | (col2 > cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)  

                            elif conditionSelected.get() == ">" and conditionSelected2.get() == "<":
                                anlyDf = df[(col > cond) | (col2 < cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)  

                            elif conditionSelected.get() == ">" and conditionSelected2.get() == "≥":
                                anlyDf = df[(col > cond) | (col2 >= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == ">" and conditionSelected2.get() == "≤":
                                anlyDf = df[(col > cond) | (col2 <= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == ">" and conditionSelected2.get() == "=":
                                anlyDf = df[(col > cond) | (col2 == cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == ">" and conditionSelected2.get() == "≠":
                                anlyDf = df[(col > cond) | (col2 != cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "<" and conditionSelected2.get() == ">":
                                anlyDf = df[(col < cond) | (col2 > cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "<" and conditionSelected2.get() == "<":
                                anlyDf = df[(col < cond) | (col2 < cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)  

                            elif conditionSelected.get() == "<" and conditionSelected2.get() == "≥":
                                anlyDf = df[(col < cond) | (col2 >= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "<" and conditionSelected2.get() == "≤":
                                anlyDf = df[(col < cond) | (col2 <= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "<" and conditionSelected2.get() == "=":
                                anlyDf = df[(col < cond) | (col2 == cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "<" and conditionSelected2.get() == "≠":
                                anlyDf = df[(col < cond) | (col2 != cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)  

                            elif conditionSelected.get() == "≥" and conditionSelected2.get() == ">":
                                anlyDf = df[(col >= cond) | (col2 > cond2)] 
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≥" and conditionSelected2.get() == "<":
                                anlyDf = df[(col >= cond) | (col2 < cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)  

                            elif conditionSelected.get() == "≥" and conditionSelected2.get() == "≥":
                                anlyDf = df[(col >= cond) | (col2 >= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≥" and conditionSelected2.get() == "≤":
                                anlyDf = df[(col >= cond) | (col2 <= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≥" and conditionSelected2.get() == "=":
                                anlyDf = df[(col >= cond) | (col2 == cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≥" and conditionSelected2.get() == "≠":
                                anlyDf = df[(col >= cond) | (col2 != cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)  

                            elif conditionSelected.get() == "≤" and conditionSelected2.get() == ">":
                                anlyDf = df[(col <= cond) | (col2 > cond2)] 
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≤" and conditionSelected2.get() == "<":
                                anlyDf = df[(col <= cond) | (col2 < cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)  

                            elif conditionSelected.get() == "≤" and conditionSelected2.get() == "≥":
                                anlyDf = df[(col <= cond) | (col2 >= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≤" and conditionSelected2.get() == "≤":
                                anlyDf = df[(col <= cond) | (col2 <= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≤" and conditionSelected2.get() == "=":
                                anlyDf = df[(col <= cond) | (col2 == cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≤" and conditionSelected2.get() == "≠":
                                anlyDf = df[(col <= cond) | (col2 != cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "=" and conditionSelected2.get() == ">":
                                anlyDf = df[(col == cond) | (col2 > cond2)] 
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "=" and conditionSelected2.get() == "<":
                                anlyDf = df[(col == cond) | (col2 < cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)  

                            elif conditionSelected.get() == "=" and conditionSelected2.get() == "≥":
                                anlyDf = df[(col == cond) | (col2 >= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "=" and conditionSelected2.get() == "≤":
                                anlyDf = df[(col == cond) | (col2 <= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "=" and conditionSelected2.get() == "=":
                                anlyDf = df[(col == cond) | (col2 == cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "=" and conditionSelected2.get() == "≠":
                                anlyDf = df[(col == cond) | (col2 != cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≠" and conditionSelected2.get() == "<":
                                anlyDf = df[(col != cond) | (col2 < cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)  

                            elif conditionSelected.get() == "≠" and conditionSelected2.get() == "≥":
                                anlyDf = df[(col != cond) | (col2 >= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≠" and conditionSelected2.get() == "≤":
                                anlyDf = df[(col != cond) | (col2 <= cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≠" and conditionSelected2.get() == "=":
                                anlyDf = df[(col != cond) | (col2 == cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)

                            elif conditionSelected.get() == "≠" and conditionSelected2.get() == "≠":
                                anlyDf = df[(col != cond) | (col2 != cond2)]
                                colPrint("yellow", "\n\nAnalystical Output: ")
                                print(file, "\n", anlyDf)
                                display.update(anlyDf)


                    andButton.destroy()
                    orButton.destroy()
                    getRows.destroy()

                    Label(CustomCondition, text = "\nEnter your 2nd condition to get custom row(s)").pack(fill = "x", padx = 5, pady = 5)

                    columnSelected2 = StringVar()
                    columnSelected2.set("Column Name")
                    ColumnName2 = OptionMenu(CustomCondition, columnSelected2, *list(df.columns.values))
                    ColumnName2.pack(padx = 5, pady = 5)

                    conditionSelected2 = StringVar()
                    conditionSelected2.set("Select Operator")
                    operators2 = OptionMenu(CustomCondition, conditionSelected2, *[">", "<", "≥", "≤", "=", "≠"])
                    operators2.pack(padx = 5, pady = 5)

                    condition2 = Entry(CustomCondition)
                    condition2.pack(padx = 5, pady = 5)

                    getRows2 = Button(CustomCondition, text = "Get Row(s)", bg = "White", relief = "groove", command = getcustomrows)
                    getRows2.pack(fill = "x", padx = 5, pady = 5)

                CustomCondition = Toplevel(main)
                CustomCondition.geometry("300x333")
                CustomCondition.title("Get Custom Row(s)")
                CustomCondition.iconphoto(False, PhotoImage(file = "{}\\UI requirement files\\images\\icon.png".format(loc)))

                Label(CustomCondition, text = "Enter your condition to get custom row(s)").pack(fill = "x", padx = 5, pady = 5)

                columnSelected = StringVar()
                columnSelected.set("Column Name")
                ColumnName = OptionMenu(CustomCondition, columnSelected, *list(df.columns.values))
                ColumnName.pack(padx = 5, pady = 5)

                conditionSelected = StringVar()
                conditionSelected.set("Select Operator")
                operators = OptionMenu(CustomCondition, conditionSelected, *[">", "<", "≥", "≤", "=", "≠"])
                operators.pack(padx = 5, pady = 5)

                condition = Entry(CustomCondition)
                condition.pack(padx = 5, pady = 5)

                andButton = Button(CustomCondition, text = "&", command = lambda : secCondi("and"))
                orButton = Button(CustomCondition, text = "|", command = lambda : secCondi("or"))
                andButton.pack(padx = 5, pady = 5)
                orButton.pack(padx = 5, pady = 5)

                getRows = Button(CustomCondition, text = "Get Row(s)", bg = "White", relief = "groove", command = getcustomrows)
                getRows.pack(fill = "x", padx = 5, pady = 5)
                
        class Columns:
            def getColumns():
                choice = []
                for i in analysisListboxGetColumns.curselection():
                    choice.append(analysisListboxGetColumns.get(i))
                anlyDf = df.loc[:, choice]
                colPrint("yellow", "\n\nAnalytical Output: ")
                print(file, "\n", anlyDf)
                display.update(anlyDf)
                
            def getUniques():
                choice = analysisListboxGetUnique.curselection()[0]
                choice = df.loc[:, analysisListboxGetUnique.get(choice)].unique()
                anlyDf = pd.DataFrame(choice)
                anlyDf.columns = [df.columns[analysisListboxGetUnique.curselection()[0]]]
                colPrint("yellow", "\n\nAnalytical Output:")
                print(file, "\n", anlyDf)
                display.update(anlyDf)
                
        class PivotTable:
            def __init__(self):
                index = []
                for i in analysisListbox1Pivot.curselection():
                    index.append(analysisListbox1Pivot.get(i))
                    
                col = []
                for i in analysisListbox2Pivot.curselection():
                    col.append(analysisListbox2Pivot.get(i)) 
                try:
                    anlyDf = df.pivot_table(index = index, values = col)

                    colPrint("yellow", "\n\nAnalytical Output:")
                    print(file, "\n", anlyDf)
                    display.update(anlyDf)
                except Exception as err:
                    colPrint("red", "\n\nError: {}".format(err))
                    messagebox.showerror("ERROR", err)
                
        class AnalyFuncs:
            def __init__(self):
                
                choice = []
                for i in analysisListbox1Function.curselection():
                    choice.append(analysisListbox1Function.get(i))
                
                
                    
                func = []
                for i in analysisListbox2Function.curselection():
                    func.append(analysisListbox2Function.get(i).lower()) 
                    
                anlyDf = df.groupby(choice).agg(func)
                colPrint("yellow", "\n\nAnalytical Output: ")
                print(file, "\n", anlyDf)
                display.update(anlyDf)
                                    
                
        class More:
            def getStats():
                anlyDf = df.describe()
                colPrint("yellow", "\n\nAnalytical Output: ")
                print(file, "\n", anlyDf)
                display.update(anlyDf)
                
            def getInfo():
                buf = io.StringIO()
                df.info(buf = buf)
                anlyDfInfo = buf.getvalue()
                colPrint("yellow", "\n\nAnalytical Output: ")
                print(file, "\n", anlyDfInfo)
                display.clear()
                TXT = Text(display.frame)
                TXT.pack()
                TXT.insert(END, anlyDfInfo)
                TXT["state"] = "disabled"

    class _vis_:
        def chart(charttype):
            if charttype == "Line Chart":
                
                def chart1(download = False):
                    x = list(df["Track_Name"])[0 : 5]
                    y = list(df["Speechiness"])[0 : 5]
                    
                    fig = plt.figure(figsize = (10, 5))
                    
                    plt.grid(color = "#95a5a6", linestyle = "--", linewidth = 2, axis = "y", alpha = 0.7)
                    plt.grid(color = "#95a5a6", linestyle = "--", linewidth = 2, axis = "x", alpha = 0.7)
                    
                    plt.xlabel("Track Names", fontweight = "bold", fontsize = 15)
                    plt.ylabel("Speechiness", fontweight = "bold", fontsize = 15)
                    plt.title("Speechines of Top 5 Song on spotify 2019", fontweight = "bold", fontsize = 20)
                    plt.xticks(rotation = 60)
                    
                    plt.plot(x, y)
                    
                    if download == True:
                        pdf = messagebox.askquestion(title = "Save Figure", message = "Do you want to save the file as pdf?")
                        if pdf == "yes":
                            plt.savefig("C:\\Users\\pc\\Downloads\\Speechines of Top 5 Song on spotify 2019.pdf")
                        else:
                            png = messagebox.askquestion(title = "Save Figure", message = "Do you want to save the figure as png?")
                            if png == "yes":
                                plt.savefig("C:\\Users\\pc\\Downloads\\Speechines of Top 5 Song on spotify 2019.png")
                                
                    elif download == False:
                        colPrint("yellow", "\n\nVisualization Output: ")
                        plt.show()
                
                def chart2(download = False):
                    x = list(df["Sl_No"])
                    y = [list(df["Beats_Per_Minute"]), list(df["Energy"])]
                    
                    fig = plt.figure(figsize = (10, 5))
                    
                    plt.xlabel("Sl_No", fontweight = "bold", fontsize = 15)
                    plt.ylabel("Values", fontweight = "bold", fontsize = 15)
                    plt.title("Beats Per Minute and Energy of all the Tracks", fontweight = "bold", fontsize = 20)
                    
                    plt.plot(x, y[0], linestyle = "dashed", marker = "o", markerfacecolor = "red", color = "green")
                    plt.plot(x, y[1], linestyle = "dotted", marker = "d", markerfacecolor = "cyan", color = "orange")
                    
                    plt.legend(["Beats Per Minute", "Energy"])
                    plt.grid(color = "#95a5a6", linestyle = "--", linewidth = 2, axis = "y", alpha = 0.7)
                    plt.grid(color = "#95a5a6", linestyle = "--", linewidth = 2, axis = "x", alpha = 0.7)
                    
                    if download == True:
                        pdf = messagebox.askquestion(title = "Save Figure", message = "Do you want to save the file as pdf?")
                        if pdf == "yes":
                            plt.savefig("C:\\Users\\pc\\Downloads\\Beats Per Minute and Energy of all the Tracks.pdf")
                        else:
                            png = messagebox.askquestion(title = "Save Figure", message = "Do you want to save the figure as png?")
                            if png == "yes":
                                plt.savefig("C:\\Users\\pc\\Downloads\\Beats Per Minute and Energy of all the Tracks.png")
                                
                    elif download == False:
                        colPrint("yellow", "\n\nVisualization Output: ")
                        plt.show()
                    
                LineChartWin = Toplevel(main)
                LineChartWin.title("Line Chart")
                LineChartWin.iconphoto(False, PhotoImage(file = "{}\\UI requirement files\\images\\icon.png".format(loc)))
                
                Chart1 = Button(LineChartWin, text = "Speechines of Top 5 Song on spotify 2019", bg = "white", relief = "groove", command = chart1)
                Chart1Download = Button(LineChartWin, text = "👈 Download", bg = "white", relief = "groove", command = lambda: chart1(True))
                Chart2 = Button(LineChartWin, text = "Beats Per Minute and Energy of all the Tracks", bg = "white", relief = "groove", command = chart2)
                Chart2Download = Button(LineChartWin, text = "👈 Download", bg = "white", relief = "groove", command = lambda: chart2(True))
                
                Chart1.grid(row = 0, column = 0, sticky = "news")
                Chart1Download.grid(row = 0, column = 1, sticky = "news")
                Chart2.grid(row = 1, column = 0, sticky = "news")
                Chart2Download.grid(row = 1, column = 1, sticky = "news")

            elif charttype == "Bar Chart":
                def chart1(download = False):
                    keys = list(df[df["Artist_Name"] == "Ed Sheeran"]["Track_Name"])
                    values = list(df[(df["Artist_Name"] == "Ed Sheeran")]["Popularity"])
                    
                    fig = plt.figure(figsize = (10, 5))
                    
                    plt.xlabel("Track Names", fontweight = "bold", fontsize = 15)
                    plt.ylabel("Popularity", fontweight = "bold", fontsize = 15)
                    plt.title("Ed Sheeran's Songs among TOP 50 in 2019 on Spotify", fontweight = "bold", fontsize = 20)
                    
                    plt.bar(keys, values, color = ["red", "green", "blue", "yellow"], width = 0.4)
                    
                    plt.grid(color = "#95a5a6", linestyle = "--", linewidth = 2, axis = "y", alpha = 0.7)
                    plt.xticks(rotation = 60)
                    
                    if download == True:
                        pdf = messagebox.askquestion(title = "Save Figure", message = "Do you want to save the file as pdf?")
                        if pdf == "yes":
                            plt.savefig("C:\\Users\\pc\\Downloads\\Popularity of different Ed Sheeran Songs among Top 50 songs of 2019 on Spotify.pdf")
                        else:
                            png = messagebox.askquestion(title = "Save Figure", message = "Do you want to save the figure as png?")
                            if png == "yes":
                                plt.savefig("C:\\Users\\pc\\Downloads\\Popularity of different Ed Sheeran Songs among Top 50 songs of 2019 on Spotify.png")
                                
                    elif download == False:
                        colPrint("yellow", "\n\nVisualization Output: ")
                        plt.show()
                                
                    
                def chart2(download = False):
                    artistname = ["Ed Sheeran", "Lil Nas X", "Lewis Capaldi"]
                    popularity = []
                    danceability = []
                    liveness = []
                    for i in artistname:
                        popularity.append(max(list(df[(df["Artist_Name"] == i)]["Popularity"])))
                        danceability.append(max(list(df[(df["Artist_Name"] == i)]["Danceability"])))
                        liveness.append(max(list(df[(df["Artist_Name"] == i)]["Liveness"])))

                    barWidth = 0.25
                    br1 = np.arange(len(popularity))
                    br2 = [x + barWidth for x in br1]
                    br3 = [x + barWidth for x in br2]
                    
                    fig = plt.figure(figsize = (10, 5))
                        
                    plt.bar(br1, popularity, color = 'r', width = barWidth, edgecolor = 'grey', label = 'Popularity')
                    plt.bar(br2, danceability, color = 'g', width = barWidth, edgecolor = 'grey', label = 'Danceability')
                    plt.bar(br3, liveness, color = 'b', width = barWidth, edgecolor = 'grey', label = "Liveness")
                    
                    plt.grid(color = "#95a5a6", linestyle = "--", linewidth = 2, axis = "y", alpha = 0.7)
                    plt.xlabel("Artist Names", fontweight = 'bold', fontsize = 15)
                    plt.ylabel("Values", fontweight = 'bold', fontsize = 15)
                    plt.xticks([r + barWidth for r in range(len(popularity))],
                              artistname)
                    plt.title("Comparing the poplularity, dancebility and liveness of diffrent songs with highest values", fontweight = "bold", fontsize = 20)
                                    
                    plt.legend()
                    
                    if download == True:
                        pdf = messagebox.askquestion(title = "Save Figure", message = "Do you want to save the file as pdf?")
                        if pdf == "yes":
                            plt.savefig("C:\\Users\\pc\\Downloads\\Popularity of different Ed Sheeran Songs among Top 50 songs of 2019 on Spotify.pdf")
                        else:
                            png = messagebox.askquestion(title = "Save Figure", message = "Do you want to save the figure as png?")
                            if png == "yes":
                                plt.savefig("C:\\Users\\pc\\Downloads\\Popularity of different Ed Sheeran Songs among Top 50 songs of 2019 on Spotify.png")
                                
                    elif download == False:
                        colPrint("yellow", "\n\nVisualization Output: ")
                        plt.show()
                
                barchartWin = Toplevel(main)
                barchartWin.title("Bar Chart")
                barchartWin.iconphoto(False, PhotoImage(file = "{}\\UI requirement files\\images\\icon.png".format(loc)))
                

                Chart1 = Button(barchartWin, text = "Popularity of different Ed Sheeran Songs among Top 50 songs of 2019 on Spotify", bg = "white", relief = "groove", command = chart1)
                Chart1Download = Button(barchartWin, text = "👈 Download", bg = "white", relief = "groove", command = lambda: chart1(True))
                Chart2 = Button(barchartWin, text = "Comparing the poplularity, dancebility and liveness of diffrent songs with highest values of those, by Ed Sheeran, Lil Nas X, Lewis Capaldi", bg = "white", relief = "groove", command = chart2)
                Chart2Download = Button(barchartWin, text = "👈 Download", bg = "white", relief = "groove", command = lambda: chart2(True))
                
                Chart1.grid(row = 0, column = 0, sticky = "news")
                Chart1Download.grid(row = 0, column = 1, sticky = "news")
                Chart2.grid(row = 1, column = 0, sticky = "news")
                Chart2Download.grid(row = 1, column = 1, sticky = "news")
                
            elif charttype == "Histogram":
                def chart1(download = False):
                    music_length = list(df["Length"])
                    maxlength = max(music_length)
                    parts = []
                    appendvalue = 0
                    for i in range(8):
                        parts.append(appendvalue)
                        appendvalue += maxlength / 10
                    
                    fig, ax = plt.subplots(figsize = (10, 7))
                    ax.hist(music_length, bins = parts, facecolor = "red", alpha = 1, ec = "black")
                    
                    plt.grid(color = "#95a5a6", linestyle = "--", linewidth = 2, axis = "y", alpha = 0.7)
                    plt.xlabel("Music Length", fontweight = 'bold', fontsize = 15)
                    plt.ylabel("Number of Tracks", fontweight = 'bold', fontsize = 15)
                    plt.title("Number of Songs belonging to different groups(among 10 of them) on the basis of thier lengths", fontweight = "bold", fontsize = 20)
                    
                    if download == True:
                        pdf = messagebox.askquestion(title = "Save Figure", message = "Do you want to save the file as pdf?")
                        if pdf == "yes":
                            plt.savefig("C:\\Users\\pc\\Downloads\\Number of Songs belonging to different groups(among 10 of them) on the basis of thier lengths.pdf")
                        else:
                            png = messagebox.askquestion(title = "Save Figure", message = "Do you want to save the figure as png?")
                            if png == "yes":
                                plt.savefig("C:\\Users\\pc\\Downloads\\Number of Songs belonging to different groups(among 10 of them) on the basis of thier lengths.png")
                                
                    elif download == False:
                        colPrint("yellow", "\n\nVisualization Output: ")
                        plt.show()
                
                def chart2(download = False):
                    music_valence = list(df["Valence"])
                    maxvalence = max(music_valence)
                    parts = []
                    appendvalue = 0
                    for i in range(8):
                        parts.append(appendvalue)
                        appendvalue += maxvalence / 8
                    
                    fig, ax = plt.subplots(figsize = (10, 7))
                    N, bins, patches = ax.hist(music_valence, bins = parts)
                    
                    fracs = ((N**(1/5)) / N.max())
                    norm = colors.Normalize(fracs.min(), fracs.max())
                    for thisfrac, thispatch in zip(fracs, patches):
                        color = plt.cm.viridis(norm(thisfrac))
                        thispatch.set_facecolor(color)
                    
                    plt.grid(color = "#95a5a6", linestyle = "--", linewidth = 2, axis = "y", alpha = 0.7)
                    plt.xlabel("Music Valence", fontweight = 'bold', fontsize = 15)
                    plt.ylabel("Number of Tracks", fontweight = 'bold', fontsize = 15)
                    plt.title("Number of Songs belonging to different groups(among 8 of them) on the basis of thier length", fontweight = "bold", fontsize = 20)
                    
                    if download == True:
                        pdf = messagebox.askquestion(title = "Save Figure", message = "Do you want to save the file as pdf?")
                        if pdf == "yes":
                            plt.savefig("C:\\Users\\pc\\Downloads\\Number of Songs belonging to different groups(among 8 of them) on the basis of thier length.pdf")
                        else:
                            png = messagebox.askquestion(title = "Save Figure", message = "Do you want to save the figure as png?")
                            if png == "yes":
                                plt.savefig("C:\\Users\\pc\\Downloads\\Number of Songs belonging to different groups(among 8 of them) on the basis of thier length.png")
                                
                    elif download == False:
                        colPrint("yellow", "\n\nVisualization Output: ")
                        plt.show()
                
                HistogramWin = Toplevel(main)
                HistogramWin.title("Histogram")
                HistogramWin.iconphoto(False, PhotoImage(file = "{}\\UI requirement files\\images\\icon.png".format(loc)))
                
                Chart1 = Button(HistogramWin, text = "Number of Songs belonging to different groups(among 10 of them) on the basis of thier lengths", bg = "white", relief = "groove", command = chart1)
                Chart1Download = Button(HistogramWin, text = "👈 Download", bg = "white", relief = "groove", command = lambda: chart1(True))
                Chart2 = Button(HistogramWin, text = "Number of Songs belonging to different groups(among 8 of them) on the basis of thier length", bg = "white", relief = "groove", command = chart2)
                Chart2Download = Button(HistogramWin, text = "👈 Download", bg = "white", relief = "groove", command = lambda: chart2(True))
                
                Chart1.grid(row = 0, column = 0, sticky = "news")
                Chart1Download.grid(row = 0, column = 1, sticky = "news")
                Chart2.grid(row = 1, column = 0, sticky = "news")
                Chart2Download.grid(row = 1, column = 1, sticky = "news")
				
if __name__ == "__main__":
    colPrint("magenta", "+----------------------------- WELCOME TO SimpleDBMS -------------------------------+")
    colPrint("magenta", "|                                                           IP Project                                                               |")
    colPrint("magenta", "|                                                         Prepared by:                                                            |")
    colPrint("magenta", "|                                             Saiyam Jain, XII-B, 16618876                                               |")
    colPrint("magenta", "+--------------------------------------------------------------------------------------------+\n")
    
    
    print("Creating the GUI... ", end = "")
    cursor_spin()

    main = Tk()
    main.focus_force()

    main.title("SimpleDBMS(1.0.0)")
    main.iconphoto(False, PhotoImage(file = "{}\\UI requirement files\\images\\icon.png".format(loc)))
    main.geometry("1060x700")
    cursor_spin()

    menubar = Menu(main)
    main.config(menu = menubar)

    File = Menu(menubar, tearoff = 0, bg = "white")
    File.add_command(label = "Open", command = Import)
    File.add_command(label = "Import from MySQL", command = lambda: Import(sql = True))
    File.add_separator()
    File.add_command(label = "Save as...", state = "disabled", command = Export)
    File.add_command(label = "Export to Mysql", state = "disabled", command = lambda: Export(sql = True))
    File.add_separator()
    File.add_command(label = "Close", command = main.destroy)
    File.add_command(label = "Refresh", command = main.update)
    menubar.add_cascade(label = "File", menu = File)

    More = Menu(menubar, tearoff = 0, background = "white")
    More.add_command(label = "About", command = lambda: doc("About"))
    More.add_command(label = "See the source code", command = lambda: doc("Source code"))
    menubar.add_cascade(label = "More", menu = More) 

    cursor_spin()
    
    front = Frame(main)
    front.pack(fill = "both", side = "top", expand = True)

    outputFrame = Frame(front, relief = "raised", bd = 3)
    display = Frame(front, bg = settings.backgroundColor.ori_color)
    Tabs = Frame(front, bg = settings.backgroundColor.ori_color, relief = "raised")
    outputFrame.pack(fill = "x", side = "top", ipadx = 5, ipady = 5)
    display.pack(fill = BOTH, side = "left", expand = True)
    Tabs.pack(fill = "y", side = "right")

    cursor_spin()
    
    style = ttk.Style(Tabs)
    style.configure("TNotebook")
    style.theme_create("tabswin", parent = "alt", settings = {
                       "TNotebook": {"configure" : {"tabmargins" : [2, 3, 2, 0],
                                                    "tabposition" : "nw"}},
                       "TNotebook.Tab" : {"configure" : {"padding" : [5, 1], "background" : "#52d0ff"},
                                          "map" : {"background" : [("selected", "#c5e4ef")],
                                                   "expand" : [("selected", [1, 1, 1, 0])]}}})
    style.theme_use("tabswin")

    display = ShowData(display)
    tabs = ttk.Notebook(Tabs)
    tabs.pack(fill = "both", expand = True)

    manipulation = Frame(tabs, bg = settings.backgroundColor.ori_color, bd = 5)
    analysis = Frame(tabs, bg = settings.backgroundColor.ori_color, bd = 5)
    visualization = Frame(tabs, bg = settings.backgroundColor.ori_color, bd = 5)
    manipulation.pack(padx = 20, pady = 20)
    analysis.pack(padx = 20, pady = 20)
    visualization.pack(padx = 20, pady = 20)

    manipulation_canvas = Canvas(manipulation, bg = settings.backgroundColor.ori_color, bd = 0, highlightthickness = 0, relief = "ridge")
    manipulationScrollbar = ttk.Scrollbar(manipulation, orient = "vertical", command = manipulation_canvas.yview)
    manipulation_canvas.pack(fill = "both", side = "left", padx = 10, pady = 10, expand = True)
    manipulationScrollbar.pack(fill = "y", side = "right", padx = 5, expand = True)
    manipulation_canvas.config(yscrollcommand = manipulationScrollbar.set)
    manipulation_canvas.bind("<Configure>", lambda e: manipulation_canvas.configure(scrollregion = manipulation_canvas.bbox("all")))

    analysis_canvas = Canvas(analysis, bg = settings.backgroundColor.ori_color, bd = 0, highlightthickness = 0, relief = "ridge")
    analysisScrollbar = ttk.Scrollbar(analysis, orient = "vertical", command = analysis_canvas.yview)
    analysis_canvas.pack(fill = "both", side = "left", padx = 10, pady = 10, expand = True)
    analysisScrollbar.pack(fill = "y", side = "right", padx = 5, expand = True)
    analysis_canvas.config(yscrollcommand = analysisScrollbar.set)
    analysis_canvas.bind("<Configure>", lambda e: analysis_canvas.configure(scrollregion = analysis_canvas.bbox("all")))

    visualization_canvas = Canvas(visualization, bg = settings.backgroundColor.ori_color, bd = 0, highlightthickness = 0, relief = "ridge")
    visualizationScrollbar = ttk.Scrollbar(visualization, orient = "vertical", command = visualization_canvas.yview)
    visualization_canvas.pack(fill = "both", side = "left", padx = 10, pady = 10, expand = True)
    visualizationScrollbar.pack(fill = "y", side = "right", padx = 5, expand = True)
    visualization_canvas.config(yscrollcommand = visualizationScrollbar.set)
    visualization_canvas.bind("<Configure>", lambda e: visualization_canvas.configure(scrollregion = visualization_canvas.bbox("all")))

    tabs.add(manipulation, text = "MANIPULATION 🛠")
    tabs.add(analysis, text = "ANALYSIS 🔍")
    tabs.add(visualization, text = "VISUALIZATION 📊")

    rounded_rect(manipulation_canvas, 10, 10, 327, 540, 10)
    rounded_rect(analysis_canvas, 10, 10, 302, 712, 10)
    rounded_rect(visualization_canvas, 10, 10, 327, 168, 10)
    
    manipulation_toolbar = Frame(manipulation, bg = settings.backgroundColor.ori_color, height = 530, width = 280)
    analysis_toolbar = Frame(analysis, bg = settings.backgroundColor.ori_color, height = 530, width = 280)
    visualization_toolbar = Frame(visualization, bg = settings.backgroundColor.ori_color, height = 530, width = 280)
    manipulation_toolbar.pack(fill = "y")
    analysis_toolbar.pack(fill = "y")
    visualization_toolbar.pack(fill = "y")
    manipulation_canvas.create_window(20, 20, anchor = "nw", window = manipulation_toolbar)
    analysis_canvas.create_window(20, 20, anchor = "nw", window = analysis_toolbar)
    visualization_canvas.create_window(20, 20, anchor = "nw", window = visualization_toolbar)

    cursor_spin()
    
    manipulationHeading = Label(manipulation_toolbar, text = "MANIPULATION TOOLBAR", font = 30, bg = settings.backgroundColor.comp_color, fg = settings.backgroundColor.ori_color)
    manipulationInsertRow = LabelFrame(manipulation_toolbar, text = "Insert Row", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", font = 10)
    manipulationInsertColumn = LabelFrame(manipulation_toolbar, text = "Insert Column", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", font = 10)
    manipulationDelete = LabelFrame(manipulation_toolbar, text = "Delete", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", font = 10)
    manipulationAppend = LabelFrame(manipulation_toolbar, text = "Append a DataFrame", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", font = 10)
    manipulationTranspose = LabelFrame(manipulation_toolbar, text = "Transpose Table", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", font = 10)
    manipulationUpdate = LabelFrame(manipulation_toolbar, text = "Update Data", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", font = 10)
    manipulationSortRows = LabelFrame(manipulation_toolbar, text = "Sort Rows", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", font = 10)
    manipulationSortColumns = LabelFrame(manipulation_toolbar, text = "Sort Columns", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", font = 10)
    manipulationHeading.grid(row = 0, column = 0, columnspan = 2, sticky = "news")
    manipulationInsertRow.grid(row = 1, column = 0, columnspan = 2, sticky = "news")
    manipulationInsertColumn.grid(row = 2, column = 0, columnspan = 2, sticky = "news")
    manipulationDelete.grid(row = 3, column = 0, sticky = "news")
    manipulationAppend.grid(row = 3, column = 1, sticky = "news")
    manipulationTranspose.grid(row = 4, column = 0, sticky = "news")
    manipulationUpdate.grid(row = 4, column = 1, sticky = "news")
    manipulationSortRows.grid(row = 5, column = 0, columnspan = 2, sticky = "news")

    analysisHeading = Label(analysis_toolbar, text = "ANALYSIS TOOLBAR", font = 30, bg = settings.backgroundColor.comp_color, fg = settings.backgroundColor.ori_color)
    analysisGetrows = LabelFrame(analysis_toolbar, text = "Row(s)", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", font = 10)
    analysisGetcolumns = LabelFrame(analysis_toolbar, text = "Column(s)", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", font = 10)
    analysisStatistics = LabelFrame(analysis_toolbar, text = "Statistics", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", font = 10)
    analysisInformation = LabelFrame(analysis_toolbar, text = "Data Info", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", font = 10)
    analysisUnique = LabelFrame(analysis_toolbar, text = "Get Unique", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", font = 10)
    analysisPivot = LabelFrame(analysis_toolbar, text = "Pivot DataFrame", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", font = 10)
    analysisFunction = LabelFrame(analysis_toolbar, text = "Analytical Functions", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", font = 10)
    analysisHeading.grid(row = 0, column = 0, columnspan = 2, sticky = "news")
    analysisGetrows.grid(row = 1, column = 0, sticky = "news")
    analysisGetcolumns.grid(row = 1, column = 1, sticky = "news")
    analysisStatistics.grid(row = 2, column = 0, sticky = "news")
    analysisInformation.grid(row = 2, column = 1, sticky = "news")
    analysisUnique.grid(row = 3, column = 0, sticky = "news", columnspan = 2)
    analysisPivot.grid(row = 4, column = 0, sticky = "news", columnspan = 2)
    analysisFunction.grid(row = 5, column = 0, sticky = "news", columnspan = 2)

    visualizationHeading = Label(visualization_toolbar, text = "VISUALIZATION TOOLBAR", font = 30, bg = settings.backgroundColor.comp_color, fg = settings.backgroundColor.ori_color)
    visualizationCharttype = LabelFrame(visualization_toolbar, text = "Plot Type", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", font = 10)
    visualizationHeading.grid(row = 0, column = 0, columnspan = 2, sticky = "news")
    visualizationCharttype.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "news")


    cursor_spin()
    
    manipulationLabelInsertRow = Label(manipulationInsertRow, text = "Row Position:", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color)
    manipulationLabelInsertColumn = Label(manipulationInsertColumn, text = "Column Position:", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color)
    manipulationSpinboxInsertRow = ttk.Spinbox(manipulationInsertRow, from_ = 0, to = 0, width = 31, wrap = True) 
    manipulationSpinboxInsertColumn = ttk.Spinbox(manipulationInsertColumn, from_ = 0, to = 0, width = 28, wrap = True)
    manipulationButtonInsertRow = Button(manipulationInsertRow, text = "Insert ↓", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = toolbar._manipu_.Insert.row)
    mainpulationButtonInsertColumn = Button(manipulationInsertColumn, text = "Insert ↓", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = toolbar._manipu_.Insert.column)
    manipulationLabelInsertRow.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "news")
    manipulationLabelInsertColumn.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "news")
    manipulationSpinboxInsertRow.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "news")
    manipulationSpinboxInsertColumn.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "news")
    manipulationButtonInsertRow.grid(row = 1, column = 0, columnspan = 2,  padx = 5, pady = 5, sticky = "news")
    mainpulationButtonInsertColumn.grid(row = 1, column = 0, columnspan = 2,  padx = 5, pady = 5, sticky = "news")
    
    manipulationButtonDeleteRows = Button(manipulationDelete, text = "✂ Row(s)", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = toolbar._manipu_.Delete.row)
    manipulationButtonDeleteColumns = Button(manipulationDelete, text = "✂ Column(s)", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = toolbar._manipu_.Delete.column)
    manipulationButtonDeleteRows.pack(fill = "x", padx = 5, pady = 5, expand = True)
    manipulationButtonDeleteColumns.pack(fill = "x", padx = 5, pady = 5, expand = True)
    
    manipulationButtonAppendFile = Button(manipulationAppend, text = "Open a File 📂", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = toolbar._manipu_.appendDf.File)
    manipulationButtonAppendMySQL = Button(manipulationAppend, text = "Import from MySQL 📥", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = toolbar._manipu_.appendDf.SQL)
    manipulationButtonAppendFile.pack(fill = "x", padx = 5, pady = 5)
    manipulationButtonAppendMySQL.pack(fill = "x", padx = 5, pady = 5)

    manipulationButtonTranspose = Button(manipulationTranspose, text = "Transpose ⚙", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = toolbar._manipu_.transposeDF)
    manipulationButtonTranspose.pack(fill = "x", padx = 5, pady = 5, expand = True)

    manipulationButtonTranspose = Button(manipulationUpdate, text = "Update ✍", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = toolbar._manipu_.update)
    manipulationButtonTranspose.pack(fill = "x", padx = 5, pady = 5, expand = True)
    
    manipulationLabelSortRows = Label(manipulationSortRows, text = "By:", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color)
    manipulationLabelSortColumns = Label(manipulationSortColumns, text = "By:", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color)
    manipulationListboxSortRows = Listbox(manipulationSortRows, selectmode = "single", height = 3, width = 43)
    manipulationListboxSortColumns = Listbox(manipulationSortColumns, selectmode = "single", height = 3, width = 43)
    manipulationButtonSortRowsAsc = Button(manipulationSortRows, text = "Sort Rows 🗃 (Asc)", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = toolbar._manipu_.sort.row)
    manipulationButtonSortRowsDesc = Button(manipulationSortRows, text = "Sort Rows 🗃 (Desc)", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = lambda: toolbar._manipu_.sort.row(asc = False))
    manipulationLabelSortRows.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "news")
    manipulationLabelSortColumns.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "news")
    manipulationListboxSortRows.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "news")
    manipulationListboxSortColumns.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "news")
    manipulationButtonSortRowsAsc.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = "news")
    manipulationButtonSortRowsDesc.grid(row = 2, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = "news")

    cursor_spin()
    
    analysisScaleGetRows = Scale(analysisGetrows, from_ = 0, to = 0, orient = "horizontal", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color)
    analysisButtonGetTopGetRows = Button(analysisGetrows, text = "Get Top Rows 👆", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = toolbar._anly_.Rows.TopRows)
    analysisButtonGetBottomGetRows = Button(analysisGetrows, text = "Get Bottom Rows 👇", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = toolbar._anly_.Rows.BottomRows)
    analysisButtonGetCustomRows = Button(analysisGetrows, text = "Custom ⚖", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = toolbar._anly_.Rows.custom)
    analysisScaleGetRows.pack(fill = "x", padx = 5, pady = 5)
    analysisButtonGetTopGetRows.pack(fill = "x", padx = 5, pady = 5)
    analysisButtonGetBottomGetRows.pack(fill = "x", padx = 5, pady = (2, 5))
    analysisButtonGetCustomRows.pack(fill = "x", padx = 5, pady = (15, 5))


    analysisListboxGetColumns = Listbox(analysisGetcolumns, selectmode = "multiple", height = 5, exportselection = 0)
    analysisButtonGetColumns = Button(analysisGetcolumns, text = "Get Columns", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = toolbar._anly_.Columns.getColumns)
    analysisListboxGetColumns.pack(fill = "x", padx = 5, pady = 5)
    analysisButtonGetColumns.pack(fill = "x", padx = 5, pady = 5)

    analysisButtonGetStats = Button(analysisStatistics, text = "Get Stats 📈", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = toolbar._anly_.More.getStats)
    analysisButtonGetStats.pack(fill = "x", padx = 5, pady = 5)

    analysisButtonGetInfo = Button(analysisInformation, text = "Get Info", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = toolbar._anly_.More.getInfo)
    analysisButtonGetInfo.pack(fill = "x", padx = 5, pady = 5)

    analysisListboxGetUnique = Listbox(analysisUnique, selectmode = "single", height = 3, exportselection = 0)
    analysisButtonGetUnique = Button(analysisUnique, text = "Get Uniques", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = toolbar._anly_.Columns.getUniques)
    analysisListboxGetUnique.pack(fill = "x", padx = 5, pady = 5)
    analysisButtonGetUnique.pack(fill = "x", padx = 5, pady = 5)

    analysisLabel1Pivot = Label(analysisPivot, text = "For index:", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color)
    analysisLabel2Pivot = Label(analysisPivot, text = "For values:", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color)
    analysisListbox1Pivot = Listbox(analysisPivot, selectmode = "single", height = 3, exportselection = 0)
    analysisListbox2Pivot = Listbox(analysisPivot, selectmode = "multiple", height = 3, exportselection = 0)
    analysisButtonPivotGetTable = Button(analysisPivot, text = "Get Table", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = toolbar._anly_.PivotTable)
    analysisLabel1Pivot.grid(row = 0, column = 0, sticky = "news", padx = 5, pady = 5)
    analysisListbox1Pivot.grid(row = 1, column = 0, sticky = "news", padx = 5, pady = 5)
    analysisLabel2Pivot.grid(row = 0, column = 1, sticky = "news", padx = 5, pady = 5)
    analysisListbox2Pivot.grid(row = 1, column = 1, sticky = "news", padx = 5, pady = 5)
    analysisButtonPivotGetTable.grid(row = 2, column = 0, columnspan = 2, sticky = "news", padx = 5, pady = 5)
    analysisPivot.grid_rowconfigure(0, weight=1)
    analysisPivot.grid_columnconfigure(0, weight=1)

    analysisFrameFunctionLabels = Frame(analysisFunction, bg = settings.backgroundColor.ori_color)
    analysisFrameFunctionListboxes = Frame(analysisFunction, bg = settings.backgroundColor.ori_color)
    anlaysisFrameFunctionButtons = Frame(analysisFunction, bg = settings.backgroundColor.ori_color)
    analysisLabel1Function = Label(analysisFrameFunctionLabels, text = "Select column:", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color)
    analysisLabel2Function = Label(analysisFrameFunctionLabels, text = "Select function(s):", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color)
    analysisListbox1Function = Listbox(analysisFrameFunctionListboxes, selectmode = "single", height = 3, exportselection = 0)
    analysisListbox2Function = Listbox(analysisFrameFunctionListboxes, selectmode = "multiple", height = 3, exportselection = 0)
    analysisButtonFucntion = Button(anlaysisFrameFunctionButtons, text = "Get Data", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = toolbar._anly_.AnalyFuncs)
    analysisFrameFunctionLabels.pack(fill = "x", padx = 5, pady = 5)
    analysisFrameFunctionListboxes.pack(fill = "x", padx = 5, pady = 5)
    anlaysisFrameFunctionButtons.pack(fill = "x", padx = 5, pady = 5)
    analysisLabel1Function.pack(fill = "x", padx = 5, side = "left", expand  = True)
    analysisLabel2Function.pack(fill = "x", padx = 5, side = "right", expand = True)
    analysisListbox1Function.pack(fill = "x", padx = 5, side = "left", expand  = True)
    analysisListbox2Function.pack(fill = "x", padx = 5, side = "right", expand = True)
    analysisButtonFucntion.pack(fill = "x")

    cursor_spin()
    
        
    visualizationListboxChartType = Listbox(visualizationCharttype, selectmode = "single", height = 3, width = 46)
    visualize = Button(visualizationCharttype, text = "Visualize", bg = settings.backgroundColor.ori_color, fg = settings.backgroundColor.comp_color, relief = "groove", command = lambda: toolbar._vis_.chart(visualizationListboxChartType.get(visualizationListboxChartType.curselection())))
    visualizationListboxChartType.pack(fill = "x", padx = 5, pady = 5)
    visualize.pack(fill = "x", padx = 5, pady = 5)
    visualizationListboxChartType.insert(0, "Line Chart")
    visualizationListboxChartType.insert(1, "Bar Chart")
    visualizationListboxChartType.insert(2, "Histogram")
    

    cursor_spin()

    status = Frame(main, bd = 2, relief = "sunken", height = 30)
    status.pack(fill = "x", side = "bottom")

    cursor_spin()
    colPrint("green", "DONE")
    
    main.mainloop()

    colPrint("red", "\nSoftware closed")
    time.sleep(1)
    