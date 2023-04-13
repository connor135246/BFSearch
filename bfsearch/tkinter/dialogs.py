# dialogs


from tkinter import *
from tkinter import ttk


# an abstract dialog with buttons. inspired by/copied from tkinter.simpledialog.SimpleDialog.
# returns the index of the button pressed, or -1 if the window was closed with the X button or by pressing escape.
class Dialog(object):
    # buttons is a list of names of buttons.
    def __init__(self, parent, title, buttons, **kwargs):
        self.top = Toplevel(parent)
        self.top.title(title)

        self.pressed = -1

        self.buildDialog(buttons = buttons, **kwargs)
        self.buildButtons(buttons = buttons, **kwargs)

        # 'dlings' if you click on the main window while this dialog is still open
        self.top.bind("<Button-1>", self.check_outside)

        self.top.bind('<Escape>', self.cancel_window)
        self.top.protocol('WM_DELETE_WINDOW', self.cancel_window)
        self._set_transient(parent)
        self.top.resizable(False, False)

    def buildDialog(self, **kwargs):
        self.mainframe = ttk.Frame(self.top)
        self.mainframe.grid(column = 0, row = 0, sticky = (W, N, E, S), ipadx = 10, ipady = 5)
        pass

    def buildButtons(self, **kwargs):
        self.buttonframe = ttk.Frame(self.top, padding = (10, 0, 15, 10))
        self.buttonframe.columnconfigure(0, weight = 1)
        self.buttonframe.grid(column = 0, row = 1, sticky = (W, N, E, S))
        for index, name in enumerate(kwargs['buttons']):
            button = ttk.Button(self.buttonframe, text = name, command = (lambda self = self, index = index: self.finish(index)))
            button.grid(column = index, row = 0, sticky = (E, S), padx = 5, ipadx = 10)
            if index == 0:
                button.focus_set()

    # copy-pasted window centerer thing
    def _set_transient(self, parent, relx = 0.5, rely = 0.3):
        widget = self.top
        widget.withdraw() # Remain invisible while we figure out the geometry
        widget.transient(parent)
        widget.update_idletasks() # Actualize geometry information
        if parent.winfo_ismapped():
            m_width = parent.winfo_width()
            m_height = parent.winfo_height()
            m_x = parent.winfo_rootx()
            m_y = parent.winfo_rooty()
        else:
            m_width = parent.winfo_screenwidth()
            m_height = parent.winfo_screenheight()
            m_x = m_y = 0
        w_width = widget.winfo_reqwidth()
        w_height = widget.winfo_reqheight()
        x = m_x + (m_width - w_width) * relx
        y = m_y + (m_height - w_height) * rely
        if x+w_width > parent.winfo_screenwidth():
            x = parent.winfo_screenwidth() - w_width
        elif x < 0:
            x = 0
        if y+w_height > parent.winfo_screenheight():
            y = parent.winfo_screenheight() - w_height
        elif y < 0:
            y = 0
        widget.geometry("+%d+%d" % (x, y))
        widget.deiconify() # Become visible at the desired location

    def check_outside(self, event = None):
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        if event.x < 0 or event.x > width or event.y < 0 or event.y > height:
            self.top.bell()

    def cancel_window(self, event = None):
        self.finish(-1)

    def finish(self, pressed):
        self.pressed = pressed
        self.top.quit()

    def show(self):
        self.top.wait_visibility()
        self.top.grab_set()
        self.top.mainloop()
        self.top.destroy()
        return self.output()

    def output(self):
        return self.pressed


# a dialog with text and an image.
class InfoDialog(Dialog):
    def __init__(self, parent, title, buttons, text, imagepath, **kwargs):
        Dialog.__init__(self, parent, title, buttons, text = text, imagepath = imagepath, **kwargs)

    def buildDialog(self, **kwargs):
        super().buildDialog(**kwargs)

        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.columnconfigure(1, weight = 1)

        self.image = PhotoImage(file = kwargs['imagepath'])
        self.imagelabel = ttk.Label(self.mainframe, image = self.image, padding = (10, 5, 0, 5))
        self.imagelabel.grid(column = 0, row = 0, sticky = (W, N, E, S))

        self.mainlabel = ttk.Label(self.mainframe, text = kwargs['text'], wraplength = 450, padding = (0, 5, 10, 5))
        self.mainlabel.grid(column = 1, row = 0, sticky = (W, N, E, S))


# info dialog that also has a combobox.
# along with the index of the button pressed, returns the selection in the combobox.
class ComboboxDialog(InfoDialog):
    # contents is a list of values to put in the combobox. default is the index the combobox should start at.
    def __init__(self, parent, title, buttons, text, imagepath, contents, default = 0):
        InfoDialog.__init__(self, parent, title, buttons, text, imagepath, contents = contents, default = default)

    def buildDialog(self, **kwargs):
        super().buildDialog(**kwargs)

        self.combo = StringVar(self.mainframe)
        values = tuple(kwargs['contents'])
        self.combobox = ttk.Combobox(self.mainframe, textvariable = self.combo, values = values)
        self.combobox.state(["readonly"])
        self.combobox.grid(column = 0, row = 1, columnspan = 2, sticky = (W, N, E, S), padx = 30, pady = 5)
        default = kwargs['default']
        if default in range(len(values)):
            self.combobox.current(default)
        self.combobox.focus_set()

    def output(self):
        return self.pressed, self.combo.get()


# a custom dialog.
class CustomDialog(Dialog):
    # builder is a method to call that adds widgets to the dialog.
    def __init__(self, parent, title, buttons, builder, **kwargs):
        self.builder = builder
        Dialog.__init__(self, parent, title, buttons, **kwargs)

    def buildDialog(self, **kwargs):
        super().buildDialog(**kwargs)
        self.builder.__call__(self, **kwargs)
