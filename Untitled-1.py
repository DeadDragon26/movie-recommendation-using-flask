from tkinter import *
def sum():
    a=int(ent1.get())
    b=int(ent2.get())
    s=a+b
    output.insert(1.0,str(s))
win=Tk() #creating the main window and storing the window object in 'win'
win.title('Sum of Numbers')
win.geometry('300x100') #setting the size of the window
text=Label(win, text='Enter the numbers in the below fields and click Add')
ent1 = Entry(win) 
ent2 = Entry(win) 
btn=Button(text='Add',command=sum)
output=Text(win,height=1,width=6)
text.pack()
ent1.pack()
ent2.pack()
output.pack()
btn.pack()
win.mainloop()
