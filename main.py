import tkinter as tk
from gUiComponents.gui import PhotoEnhancerGUI

def main():
    root = tk.Tk()
    app = PhotoEnhancerGUI(root)
    def onResize(_ev=None):
        app._update_image_display()
    root.bind('<Configure>', onResize)
    root.mainloop()
    
if __name__ == '__main__':
    main()