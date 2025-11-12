import pikepdf
from os import *
import datetime
import signal


viola = "\033[35m"
giallo = "\033[33m"
ciano = "\033[96m"
rosso = "\033[31m"
reset = "\033[0m"

def handler(sig, frame):
    print("\n\n[!] Quit...")
    exit(0)

# collega SIGINT (Ctrl+C) alla funzione handler
signal.signal(signal.SIGINT, handler)

def Banner():
    banner = f"""{viola}
                                                              ____
██████╗ ██████╗ ███████╗   ██╗ ██████╗ ██╗███╗   ██╗████████╗|___ \\   
██╔══██╗██╔══██╗██╔════╝   ██║██╔═══██╗██║████╗  ██║╚══██╔══╝  __) |
██████╔╝██║  ██║█████╗     ██║██║   ██║██║██╔██╗ ██║   ██║    / __/
██╔═══╝ ██║  ██║██╔══╝██   ██║██║   ██║██║██║╚██╗██║   ██║   |_____|
██║     ██████╔╝██║   ╚█████╔╝╚██████╔╝██║██║ ╚████║   ██║   
╚═╝     ╚═════╝ ╚═╝    ╚════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝   ╚═╝                                                                              
    {reset}"""
    sottotitolo = f"{ciano}© A.Monti 2025{ciano}"
    utilizzo = f"""
{giallo}[-] Join PDF:{reset}
1) Rename the files that are to be merged like this: 00.pdf, 01.pdf, 02.pdf... etc.
2) Place them in the folder that contains PDFjoint.exe
3) Start PDFjoint.exe
\n{giallo}[-] Remove limitations:{reset}\nInsert the name of the file to unlock"""
    print(banner)
    print(sottotitolo)
    print(utilizzo)

scelta = "\nChoice: J) join PDf - R) remove limitations (CTRL+c to exit): "

def Controllo_nome(nome):
    nome_iniz = nome[0:-4]
    if nome.endswith(".pdf") and nome_iniz.isnumeric():
        return True
    else:
        return False

def Nome_file():
    now = datetime.datetime.now()
    return f"PJ_{now.day}{now.month}{now.year}_{now.hour}{now.minute}{now.second}.pdf"

def unisci():
    x = [a for a in listdir() if Controllo_nome(a)]

    if not x:
        print(f"\n{rosso}[!] There are no files to join{reset}")
        input("Press a key to exit...")
        exit()
    elif len(x) == 1:
        print(f"\n{rosso}[!] There is just one file{reset}")
        input("Press a key to exit...")
        exit()

    print("\nFiles to join")
    for i in range(0, len(x)):
        print(f"File {i+1}: {x[i]}")

    while True:
        nome_file = input("\nEnter the name of the final file >>> ")
        if nome_file == "":
            nome_file = Nome_file() 
        else:
            nome_file = nome_file + ".pdf"

        if nome_file in listdir():
            scelta = input(f"\n{giallo}[i] The file already exists, do you want to overwrite it? (y){reset} ")
            if scelta == "y" or scelta == "Y" or scelta == "":
                break
            else:
                print("[!] Quit...")
                exit()
        else:
            break

    pdf = pikepdf.Pdf.new()
    
    for file in x:
        src = pikepdf.Pdf.open(file)
        pdf.pages.extend(src.pages)
    
    pdf.save(nome_file)
    print(f"{ciano}[i] PDF successfully merged{ciano}")
    
        
def unprotect():
    filename = input("Enter the file to be unlocked: ")
    try:
        with pikepdf.open(filename, allow_overwriting_input=True) as pdf:
            print(f"[i] File {filename} opened correctly.")
            pdf.save(Nome_file())
    except:
        print(f"{rosso}[!] The file you uploaded is not a PDF file. Quit...{reset}")
        exit()
        
    print(f"{ciano}[i] File {filename} unlocked{ciano}")


## MAIN ------------------------------------
def main():
    Banner()

    while True:
        s = input(scelta)
        if (s == "J" or s == "j"):
            unisci()
            break
        elif (s == "R" or s == "r"):
            unprotect()
            break
        print(f"{giallo}[!] Incorrect choice{giallo}")

    exit() 
#-------------------------------------------

if __name__ == "__main__":
    main()