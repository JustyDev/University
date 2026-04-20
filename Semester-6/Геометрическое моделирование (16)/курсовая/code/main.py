from tkinter import Tk

from editor.app import EditorApp


def main():
    root = Tk()
    app = EditorApp(root)
    root.minsize(900, 560)
    root.mainloop()


if __name__ == "__main__":
    main()
