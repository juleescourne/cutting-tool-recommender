from tkinter import Toplevel, Label, LEFT, SOLID


class Popup(object):
    """Classe qui gère l'apparition de pop-ups informatifs au passage de la souris"""

    def __init__(self, widget):
        """Constructeur de la classe Popup

        Parameters
        ----------
        widget : any
            Element d'une fenetre tkinter qui active la popup au passage de la souris
        """
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showpopup(self, text):
        """Affiche le texte dans une popup

        Parameters
        ----------
        text : String
            Texte à afficher
        """
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidepopup(self):
        """Cache la popup"""
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreatePopup(widget, text):
    """Fonction qui affiche et cache la popup au passage du la souris

    Parameters
    ----------
    text : String
        Texte à afficher

    widget : any
        Element d'une fenetre tkinter qui active la popup au passage de la souris
    """
    toolTip = Popup(widget)

    def enter(event):
        toolTip.showpopup(text)

    def leave(event):
        toolTip.hidepopup()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
