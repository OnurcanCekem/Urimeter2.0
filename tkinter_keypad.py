"""
 * tkinter_keypad_bar.py
 *
 *  Created on: May 27, 2022
 *  Last update: June 27, 2022
 *      Author: onurc
 *  Description: Tkinter test program for keypad to test the lambda function.
 """
from tkinter import *
import tkinter


root = Tk()
root.geometry("800x480") # windows grootte 

# Show input
input_label = tkinter.Label(root, text="Meting [ml]:")
input_label.grid(column=0, row=0, sticky=tkinter.W, padx=5, pady=5)
input_entry = tkinter.Entry(root)
input_entry.grid(column=1, row=0, sticky=tkinter.E, padx=5, pady=5)

index = 0

def buttonPressed(button):
    global index
    #print("Hello there button " + str(button))
    print(".get " + input_entry.get())
    print("index: " + str(index))

    # Keypad 1-9
    if(button >= 1) and (button <= 9):
        print("Keypad 1")
        input_entry.insert(index,str(button))
        index = index + 1
    
    elif(button == 10):
        print(".")
        input_entry.insert(index,".")
        index = index + 1
    
    # Clear button
    elif(button == 11):
        print("clear " + str(1))
        index = index - 1
        input_entry.delete(index)
        if(index < 0):
            index = 0
    
    # Add data to database button
    elif(button == 12):
        print("add data")
        for i in range(0,index):
            input_entry.delete(0)
    # Delete last data from database button
    elif(button == 13):
        print("Reserved, IDK")




root.title("Keypad")
#btn1=Button(root,command=lambda: buttonPressed(1), text='1').grid(row=4,column=0)
btn1=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(1), text='1').grid(row=4,column=0)
btn2=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(2), text='2').grid(row=4,column=1)
btn3=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(3), text='3').grid(row=4,column=2)
btn4=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(4), text='4').grid(row=3,column=0)
btn5=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(5), text='5').grid(row=3,column=1)
btn6=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(6), text='6').grid(row=3,column=2)
btn7=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(7), text='7').grid(row=2,column=0)
btn8=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(8), text='8').grid(row=2,column=1)
btn9=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(9), text='9').grid(row=2,column=2)
btn9=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(10), text='.').grid(row=4,column=4)

delete_btn =Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',20,'bold'),command=lambda: buttonPressed(11), text='clear').grid(row=2,column=4)
adddata_btn=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',15,'bold'),command=lambda: buttonPressed(12), text='add data').grid(row=1,column=4)

#btn2=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command= lambda:
#print("Button 2 "), text='2').grid(row=4,column=1)

root.mainloop()