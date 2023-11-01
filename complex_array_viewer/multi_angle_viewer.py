"""
TK viwerer for multiple files
"""
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar2TkAgg

from complex_array_viewer import __version__, __date__, ComplexArrayViewer
from complex_array_viewer.main import bkg, txtcol, opt_active, SF, TF, ety, ety_txt, opt, BF
from complex_array_viewer.main import _figure_size, _diff3d


class MultiAngleViewer:
    """
    A standalone GUI window that displays multiple images using a list of filenames
        MultiAngleViewer()
    """

    def __init__(self, file_list=(), figure_dpi=100, ncols=4, titles=None):
        """Initialise"""
        # Create Tk inter instance
        self.root = tk.Tk()
        self.root.wm_title(f'Complex Array Multi-File-Viewer   (Version: {__version__}, Date: {__date__})')
        # self.root.minsize(width=640, height=480)
        self.root.maxsize(width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.root.tk_setPalette(
            background=bkg,
            foreground=txtcol,
            activeBackground=opt_active,
            activeForeground=txtcol
        )

        # Load files
        self.data = [np.load(filename) for filename in file_list]
        self.angs = [np.angle(data) for data in self.data]
        # self.mags = [np.abs(data) for data in self.data]
        print('\n'.join([f"{os.path.basename(f)}: {data.shape}" for f, data in zip(file_list, self.data)]))
        if titles is None:
            titles = [os.path.basename(f) for f in file_list]

        frame = tk.Frame(self.root)
        frame.pack(side=tk.LEFT, anchor=tk.N)

        # Variatbles
        _axes = ['axis 1', 'axis 2', 'axis 3']
        self._ax = 2
        self.ang_clim = [-np.pi, np.pi]
        self.view_axis = tk.StringVar(frame, _axes[self._ax])
        self.view_index = tk.IntVar(frame, self.data[0].shape[self._ax]//2)
        self.mask = tk.DoubleVar(frame, 0)
        self.logplot = tk.BooleanVar(frame, False)
        self.degplot = tk.BooleanVar(frame, False)
        self.absplot = tk.BooleanVar(frame, False)
        self.sinplot = tk.BooleanVar(frame, False)
        self.difplot = tk.BooleanVar(frame, False)
        self.colormap = tk.StringVar(frame, 'twilight')
        all_colormaps = ['viridis', 'Spectral', 'plasma', 'inferno', 'Greys', 'Blues', 'winter', 'autumn',
                         'hot', 'hot_r', 'hsv', 'rainbow', 'jet', 'twilight', 'hsv']

        # ---Options---
        frm = tk.LabelFrame(frame, text='Options', relief=tk.RIDGE)
        frm.pack(expand=tk.NO, pady=2, padx=5)

        frm = tk.LabelFrame(frame, text='Options', relief=tk.RIDGE)
        frm.pack(expand=tk.NO, pady=2, padx=5)

        var = tk.Checkbutton(frm, text='Log magnitude', variable=self.logplot, font=SF, command=self.update_options)
        var.pack(side=tk.LEFT, padx=6)
        var = tk.Checkbutton(frm, text='Degrees', variable=self.degplot, font=SF, command=self.update_options)
        var.pack(side=tk.LEFT, padx=6)
        var = tk.Checkbutton(frm, text='abs phase', variable=self.absplot, font=SF, command=self.update_options)
        var.pack(side=tk.LEFT, padx=6)
        var = tk.Checkbutton(frm, text='sin phase', variable=self.sinplot, font=SF, command=self.update_options)
        var.pack(side=tk.LEFT, padx=6)
        var = tk.Checkbutton(frm, text='Diff', variable=self.difplot, font=SF, command=self.update_options)
        var.pack(side=tk.LEFT, padx=6)

        var = tk.Label(frm, text='Mask <', font=SF)
        var.pack(side=tk.LEFT, expand=tk.NO, padx=6)
        var = tk.Entry(frm, textvariable=self.mask, font=TF, width=6, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT, padx=6)
        var.bind('<Return>', self.update_options)
        var.bind('<KP_Enter>', self.update_options)

        var = tk.OptionMenu(frm, self.colormap, *all_colormaps, command=self.update_image)
        var.config(font=SF, bg=opt, activebackground=opt_active)
        var["menu"].config(bg=opt, bd=0, activebackground=opt_active)
        var.pack(side=tk.LEFT)

        # ---Slider---
        frm = tk.Frame(frame)
        frm.pack(expand=tk.NO, pady=2, padx=5)

        var = tk.OptionMenu(frm, self.view_axis, *_axes, command=self.update_axis)
        var.config(font=SF, bg=opt, activebackground=opt_active)
        var["menu"].config(bg=opt, bd=0, activebackground=opt_active)
        var.pack(side=tk.LEFT)

        def inc():
            self.view_index.set(self.view_index.get() + 1)
            self.update_image()

        def dec():
            self.view_index.set(self.view_index.get() - 1)
            self.update_image()

        var = tk.Label(frm, text='Index:', font=TF, width=8)
        var.pack(side=tk.LEFT)
        var = tk.Button(frm, text='-', command=dec)
        var.pack(side=tk.LEFT)
        self.tkscale = tk.Scale(frm, from_=0, to=self.data[0].shape[-1], variable=self.view_index, font=BF,
                                sliderlength=30, orient=tk.HORIZONTAL, command=self.update_image, showvalue=True,
                                repeatdelay=300, resolution=1, length=300)
        # var.bind("<ButtonRelease-1>", callback)
        self.tkscale.pack(side=tk.LEFT, expand=tk.YES)
        var = tk.Button(frm, text='+', command=inc)
        var.pack(side=tk.LEFT)
        var = tk.Entry(frm, textvariable=self.view_index, font=TF, width=6, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT)
        var.bind('<Return>', self.update_image)
        var.bind('<KP_Enter>', self.update_image)

        # ---Images---
        # Number of plots
        nfiles = len(file_list)
        nrows = (nfiles // ncols) + (nfiles % ncols > 0)
        screen_width_inches = 0.95 * self.root.winfo_screenwidth() / float(figure_dpi)
        screen_height_inches = 0.6 * self.root.winfo_screenheight() / float(figure_dpi)
        # screen_width_inches = self.root.winfo_screenmmwidth() * 0.0393
        # screen_height_inches = self.root.winfo_screenmmheight() * 0.0393
        w, h = _figure_size
        fig_size = [
            w if w < screen_width_inches else screen_width_inches,
            nrows * h if nrows * h < screen_height_inches else screen_height_inches
        ]
        print(f"Screen size: {screen_width_inches}x{screen_height_inches} @ {figure_dpi} dpi")
        print(f"Fig size: {fig_size} @ {figure_dpi} dpi")
        self.fig = Figure(figsize=fig_size, dpi=figure_dpi)
        self.fig.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1, wspace=0.5, hspace=0.2)
        self.fig.patch.set_facecolor('w')
        self.axes = self.fig.subplots(nrows, ncols).flatten()

        self.axes_images = []
        self.axes_cbs = []
        cmap = self.colormap.get()
        for n in range(len(file_list)):
            img = self.angs[n][:, :, self.view_index.get()]
            self.axes_images.append(
                self.axes[n].pcolormesh(img, shading='auto', cmap=cmap)
            )
            self.axes[n].set_xlabel(u'Axis 0')
            self.axes[n].set_ylabel(u'Axis 1')
            self.axes[n].set_title(titles[n])
            self.axes[n].set_xlim([0, self.angs[n].shape[0]])
            self.axes[n].set_ylim([0, self.angs[n].shape[1]])
            self.axes[n].axis('image')
            self.axes_cbs.append(
                self.fig.colorbar(self.axes_images[-1], ax=self.axes[n])
            )
        for n in range(len(file_list), len(self.axes)):
            self.axes[n].set_axis_off()

        canvas = FigureCanvasTkAgg(self.fig, frame)
        canvas.get_tk_widget().configure(bg='black')
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES, padx=5, pady=2)

        # Toolbar
        frm = tk.Frame(frame)
        frm.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH, padx=5, pady=2)
        self.toolbar = NavigationToolbar2TkAgg(canvas, frm)
        self.toolbar.update()
        self.toolbar.pack(fill=tk.X, expand=tk.YES)

        "-------------------------Start Mainloop------------------------------"
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    "------------------------------------------------------------------------"
    "--------------------------General Functions-----------------------------"
    "------------------------------------------------------------------------"

    def update_options(self, event=None):
        """Get options"""

        self.angs = [np.angle(data) for data in self.data]
        clim = [-np.pi, np.pi]
        if self.absplot.get():
            self.angs = [np.abs(ang) for ang in self.angs]
            clim[0] = 0
        if self.sinplot.get():
            self.degplot.set(False)
            self.angs = [np.sin(ang) for ang in self.angs]
            clim = [-1, 1]
        if self.degplot.get():
            self.angs = [np.rad2deg(ang) for ang in self.angs]
            clim = [-180, 180]
        if self.difplot.get():
            self.angs = [_diff3d(ang) for ang in self.angs]
        # mask
        mask = self.mask.get()
        for n in range(len(self.data)):
            self.angs[n][np.abs(self.data[n]) <= mask] = np.nan
        self.ang_clim = clim
        self.update_image()

    def _update_axis(self):
        """Get data size etc"""
        self._ax = int(self.view_axis.get()[-1]) - 1  # e.g. 'axis 1'
        shape = self.data[0].shape
        self.tkscale.config(to=shape[self._ax])
        if self._ax == 0:
            for n in range(len(self.data)):
                self.axes[n].set_xlabel(u'Axis 2')
                self.axes[n].set_ylabel(u'Axis 3')
                self.axes[n].set_xlim([0, shape[1]])
                self.axes[n].set_ylim([0, shape[2]])
        elif self._ax == 1:
            for n in range(len(self.data)):
                self.axes[n].set_xlabel(u'Axis 1')
                self.axes[n].set_ylabel(u'Axis 3')
                self.axes[n].set_xlim([0, shape[0]])
                self.axes[n].set_ylim([0, shape[2]])
        else:
            for n in range(len(self.data)):
                self.axes[n].set_xlabel(u'Axis 1')
                self.axes[n].set_ylabel(u'Axis 2')
                self.axes[n].set_xlim([0, shape[0]])
                self.axes[n].set_ylim([0, shape[1]])
        self.view_index.set(shape[self._ax]//2)

    def update_axis(self, event=None):
        """Get data size etc"""
        self._update_axis()
        self.update_image()

    def update_image(self, event=None):
        """Plot image data"""
        idx = self.view_index.get()
        for n in range(len(self.data)):
            if self._ax == 0:
                im_ang = self.angs[n][idx, :, :]
            elif self._ax == 1:
                im_ang = self.angs[n][:, idx, :]
            else:
                im_ang = self.angs[n][:, :, idx]
            self.axes_images[n].remove()
            colormap = self.colormap.get()
            self.axes_images[n] = self.axes[n].pcolormesh(
                im_ang, shading='auto', clim=self.ang_clim, cmap=colormap
            )
            self.axes_cbs[n].update_normal(self.axes_images[n])
            self.axes_images[n].set_clim(self.ang_clim)
        self.toolbar.update()
        self.fig.canvas.draw()

    "------------------------------------------------------------------------"
    "---------------------------Button Functions-----------------------------"
    "------------------------------------------------------------------------"

    def btn_loadnew(self):
        filename = filedialog.askopenfilename(
            title='Select .npy to open',
            filetypes=[('NPY file', '.npy'), ('All files', '.*')],
            parent=self.root
        )
        if filename:
            ComplexArrayViewer(filename)

    def on_closing(self):
        """Closes the current window"""
        self.root.destroy()
