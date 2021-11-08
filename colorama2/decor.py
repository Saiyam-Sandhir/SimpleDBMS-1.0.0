import sys
sys.path.insert(0, "G:\SimpleDBMS\Packages\Colorama2")

import colorama2.ImpColorama as ImpColorama

def colPrint(color, string):

        
        if ImpColorama.check() == True:
            from colorama import Fore, Style
            
            if color == "red": print(Fore.RED + string, Style.RESET_ALL)
            elif color == "blue": print(Fore.BLUE + string, Style.RESET_ALL)
            elif color == "green": print(Fore.GREEN + string, Style.RESET_ALL)
            elif color == "yellow": print(Fore.YELLOW + string, Style.RESET_ALL)
            elif color == "magenta": print(Fore.MAGENTA + string, Style.RESET_ALL)
            else: print(string)
        
        else: print(string)


