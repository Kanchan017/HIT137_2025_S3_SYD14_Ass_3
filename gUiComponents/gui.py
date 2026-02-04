import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np

from models.image_model import ImageModel
from processors.image_processor import ImageProcessor


class PhotoEnhancerGUI:
    def __init__(self, root):
        self.root = root
        root.title("Photo Enhancer")
        root.geometry("1000x700")

        self.model = ImageModel()

        self._build_menu()
        self._build_ui()

    def _build_menu(self):
        menubar = tk.Menu(self.root)
        filem = tk.Menu(menubar, tearoff=0)
        filem.add_command(label="Open", command=self.open_file)
        filem.add_command(label="Save", command=self.save_file)
        filem.add_command(label="Save As", command=self.save_file_as)
        filem.add_separator()
        filem.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filem)

        editm = tk.Menu(menubar, tearoff=0)
        editm.add_command(label="Undo", command=self.undo)
        editm.add_command(label="Redo", command=self.redo)
        menubar.add_cascade(label="Edit", menu=editm)

        self.root.config(menu=menubar)

    def _build_ui(self):
        main = ttk.Frame(self.root)
        main.pack(fill=tk.BOTH, expand=True)

        controls = ttk.Frame(main, width=260)
        controls.pack(side=tk.LEFT, fill=tk.Y)

        disp = ttk.Frame(main)
        disp.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Label(disp, bg="#333")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        ttk.Label(controls, text="Effects", font=(None, 12, 'bold')).pack(pady=6)

        ttk.Button(controls, text="Grayscale", command=self.grayscale).pack(fill=tk.X, padx=6, pady=2)

        ttk.Label(controls, text="Blur (ksize)").pack(anchor=tk.W, padx=6)
        self.blur_var = tk.IntVar(value=3)
        ttk.Scale(controls, from_=1, to=25, variable=self.blur_var, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=6)
        ttk.Button(controls, text="Apply Blur", command=self.blur).pack(fill=tk.X, padx=6, pady=2)

        ttk.Button(controls, text="Canny Edges", command=self.edges).pack(fill=tk.X, padx=6, pady=2)

        ttk.Label(controls, text="Brightness").pack(anchor=tk.W, padx=6)
        self.bright_var = tk.IntVar(value=0)
        ttk.Scale(controls, from_=-100, to=100, variable=self.bright_var, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=6)

        ttk.Label(controls, text="Contrast (x)").pack(anchor=tk.W, padx=6)
        self.contrast_var = tk.DoubleVar(value=1.0)
        ttk.Scale(controls, from_=0.1, to=3.0, variable=self.contrast_var, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=6)
        ttk.Button(controls, text="Apply Bright/Contrast", command=self.brightness_contrast).pack(fill=tk.X, padx=6, pady=4)

        ttk.Separator(controls).pack(fill=tk.X, pady=6, padx=6)

        ttk.Label(controls, text="Rotate / Flip", font=(None, 10)).pack(anchor=tk.W, padx=6)
        ttk.Button(controls, text="Rotate 90°", command=lambda: self.rotate(90)).pack(fill=tk.X, padx=6, pady=2)
        ttk.Button(controls, text="Rotate 180°", command=lambda: self.rotate(180)).pack(fill=tk.X, padx=6, pady=2)
        ttk.Button(controls, text="Rotate 270°", command=lambda: self.rotate(270)).pack(fill=tk.X, padx=6, pady=2)
        ttk.Button(controls, text="Flip H", command=lambda: self.flip('horizontal')).pack(fill=tk.X, padx=6, pady=2)
        ttk.Button(controls, text="Flip V", command=lambda: self.flip('vertical')).pack(fill=tk.X, padx=6, pady=2)

        ttk.Separator(controls).pack(fill=tk.X, pady=6, padx=6)

        ttk.Label(controls, text="Resize / Scale").pack(anchor=tk.W, padx=6)
        self.scale_var = tk.IntVar(value=100)
        ttk.Scale(controls, from_=10, to=200, variable=self.scale_var, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=6)
        ttk.Button(controls, text="Apply Scale", command=self.resize).pack(fill=tk.X, padx=6, pady=4)

        self.status = ttk.Label(self.root, text="No image loaded", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        self._photo_image = None

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All files", "*")])
        if not path:
            return
        try:
            img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Unable to read image")
            self.model = ImageModel(img, filename=path)
            self._update_image_display()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image: {e}")

    def save_file(self):
        cur = self.model.current()
        if cur is None:
            messagebox.showinfo("Save", "No image to save")
            return
        fname = self.model.filename()
        if not fname:
            return self.save_file_as()
        try:
            ext = os.path.splitext(fname)[1]
            is_success, buffer = cv2.imencode(ext, cur)
            if is_success:
                buffer.tofile(fname)
                messagebox.showinfo("Saved", f"Saved to {fname}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_file_as(self):
        cur = self.model.current()
        if cur is None:
            messagebox.showinfo("Save As", "No image to save")
            return
        path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG','*.png'),('JPEG','*.jpg'),('BMP','*.bmp')])
        if not path:
            return
        try:
            ext = os.path.splitext(path)[1]
            is_success, buffer = cv2.imencode(ext, cur)
            if is_success:
                buffer.tofile(path)
                self.model._filename = path
                messagebox.showinfo("Saved", f"Saved to {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _update_image_display(self):
        img = self.model.current()
        if img is None:
            self.canvas.config(image='')
            self.status.config(text="No image loaded")
            return
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil = Image.fromarray(rgb)
        w = self.canvas.winfo_width() or 800
        h = self.canvas.winfo_height() or 600
        pil.thumbnail((w, h))
        self._photo_image = ImageTk.PhotoImage(pil)
        self.canvas.config(image=self._photo_image)
        fn = self.model.filename() or '<unsaved>'
        h0, w0 = img.shape[:2]
        self.status.config(text=f"{os.path.basename(fn)} — {w0}x{h0}")

    def _apply_and_refresh(self, img_out):
        self.model.set_image(img_out)
        self._update_image_display()

    def grayscale(self):
        cur = self.model.current()
        if cur is None:
            return
        g = ImageProcessor.to_grayscale(cur)
        g_bgr = cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)
        self._apply_and_refresh(g_bgr)

    def blur(self):
        cur = self.model.current()
        if cur is None:
            return
        k = self.blur_var.get()
        out = ImageProcessor.apply_blur(cur, ksize=k)
        self._apply_and_refresh(out)

    def edges(self):
        cur = self.model.current()
        if cur is None:
            return
        out = ImageProcessor.canny_edges(cur)
        self._apply_and_refresh(out)

    def brightness_contrast(self):
        cur = self.model.current()
        if cur is None:
            return
        b = self.bright_var.get()
        c = self.contrast_var.get()
        out = ImageProcessor.adjust_brightness_contrast(cur, brightness=b, contrast=c)
        self._apply_and_refresh(out)

    def rotate(self, angle):
        cur = self.model.current()
        if cur is None:
            return
        out = ImageProcessor.rotate(cur, angle)
        self._apply_and_refresh(out)

    def flip(self, mode):
        cur = self.model.current()
        if cur is None:
            return
        out = ImageProcessor.flip(cur, mode)
        self._apply_and_refresh(out)

    def resize(self):
        cur = self.model.current()
        if cur is None:
            return
        scale = self.scale_var.get()
        out = ImageProcessor.resize_scale(cur, scale_percent=scale)
        self._apply_and_refresh(out)

    def undo(self):
        if self.model.undo():
            self._update_image_display()

    def redo(self):
        if self.model.redo():
            self._update_image_display()
