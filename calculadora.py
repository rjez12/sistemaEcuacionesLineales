import tkinter as tk
from InterfasCalculadora import InterfasCalculadora

def main():
    root = tk.Tk()
    app = InterfasCalculadora(root)
    root.mainloop()

if __name__ == "__main__":
    main()