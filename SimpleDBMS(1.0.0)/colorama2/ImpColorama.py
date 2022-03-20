from tkinter import messagebox
import os

def check():
        
    for i in range(2):
        
        try:
            import colorama
            
            check = True
            break
        
        except:
            if i == 0:
                check = False

                if messagebox.askquestion("SimpleDBMS", "\nWould you like to install the colorama package for better output experience?:") == "yes":
                    print(os.popen("pip install colorama").read())

                else:
                    break
                
            else:
                break
                        
    return check


            






