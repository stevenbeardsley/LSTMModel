from tkinter import *
from tkinter.ttk import Treeview

def createDataSetWindow(path):
        window = Tk("Dataset")
        window.geometry("500x400")
        DB = Treeview(window,height=12)

        DB['columns'] = ('Price','Date')
        DB.column("#0",width=0,stretch=NO)
        DB.column("Price",width=50,stretch=NO)
        DB.column("Date",anchor=W,width=100)

        #Create Headings
        DB.heading("#0",text='',anchor=W)
        DB.heading("Price",text='ID',anchor= CENTER)
        DB.heading('Date',text='Name',anchor=W)
        DB.grid (row=0,column=0)


def createStartWindow():
    root.geometry("600x400")  # Set the window size (Width x Height)
    titleFont = ("Helvetica", 16, "bold")
    title = Label(root, text="Stock analysis program",font =titleFont)
    title.grid(row=0,column=2, columnspan=2,pady=5, padx=5)

    filePathText  = Label(text = "Enter stock Ticker: ")
    filePathText.grid(row =1, column = 0, columnspan=2,padx=10)
    filePathInput = Entry(root, width=50, text="example/file/path")
    filePathInput.grid(row=1, column=2, columnspan=3)
    analyseButton = Button(text="Analyse!", bg="lightgreen")
    analyseButton.grid(row=3, column=2, padx=10,pady=10,ipadx=5,ipady=5)
    seeDataSetButton = Button(text = "See data set",command =lambda: createDataSetWindow(filePathInput.get()))
    seeDataSetButton.grid(row=3, column=3, padx=5, pady=5,ipadx=5,ipady=5)

    decriptionText = Label(text="How this tool works: \n 1. Uses a famous algorithm \n2. blah blah blah \n3.blahdy blah blah")
    decriptionText.grid(row=4,column=2, padx=5,pady=10)
    
def main(root):
    
    createStartWindow()

root = Tk()
root.title("Stock analysis tool")

main(root)
root.mainloop()