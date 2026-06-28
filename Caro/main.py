import tkinter as tk
from frontend import CaroGameUI

def main():
    root = tk.Tk()
    app = CaroGameUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
