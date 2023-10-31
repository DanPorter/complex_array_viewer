"""
Complex Array Viewer
Definition of tkinter interface
"""


import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar2TkAgg

# Version
__version__ = '0.1.1'
__date__ = '2023-10-31'

# Fonts
TF = ["Times", 12]  # entry
BF = ["Times", 14]  # Buttons
SF = ["Times New Roman", 14]  # Title labels
MF = ["Courier", 8]  # fixed distance format
LF = ["Times", 14]  # Labels
HF = ["Courier", 12]  # Text widgets (big)
# Colours - background
bkg = 'snow'
ety = 'white'
btn = 'azure'  # 'light slate blue'
opt = 'azure'  # 'light slate blue'
btn2 = 'gold'
# Colours - active
btn_active = 'grey'
opt_active = 'grey'
# Colours - Fonts
txtcol = 'black'
btn_txt = 'black'
ety_txt = 'black'
opt_txt = 'black'
ttl_txt = 'black'
_figure_size = [14, 6]


def start():
    """Start viewer"""
    filename = filedialog.askopenfilename(
        title='Select .npy to open',
        filetypes=[('NPY file', '.npy'), ('All files', '.*')],
    )
    if filename:
        ComplexArrayViewer(filename)


class ComplexArrayViewer:
    """
    A standalone GUI window that displays multiple images using a list of filenames
        ComplexArrayViewer()
    """

    def __init__(self, filename=None, figure_dpi=100):
        """Initialise"""
        # Create Tk inter instance
        self.root = tk.Tk()
        self.root.wm_title(f'Complex Array Viewer   (Version: {__version__}, Date: {__date__})')
        # self.root.minsize(width=640, height=480)
        self.root.maxsize(width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.root.tk_setPalette(
            background=bkg,
            foreground=txtcol,
            activeBackground=opt_active,
            activeForeground=txtcol)

        self.data = np.zeros([100, 100, 100], dtype=np.complex)
        self.angs = np.rad2deg(np.angle(self.data))
        self.mags = np.abs(self.data)

        frame = tk.Frame(self.root)
        frame.pack(side=tk.LEFT, anchor=tk.N)

        # Variatbles
        self.filename = tk.StringVar(frame, '')
        _axes = ['axis 1', 'axis 2', 'axis 3']
        self._ax = 2
        self.ang_clim = [-180, 180]
        self.view_axis = tk.StringVar(frame, _axes[self._ax])
        self.view_index = tk.IntVar(frame, 0)
        self.logplot = tk.BooleanVar(frame, False)
        self.degplot = tk.BooleanVar(frame, False)
        self.absplot = tk.BooleanVar(frame, False)
        self.sinplot = tk.BooleanVar(frame, False)
        self.cmin = tk.DoubleVar(frame, 0)
        self.cmax = tk.DoubleVar(frame, np.max(self.mags))
        self.colormap = tk.StringVar(frame, 'twilight')
        all_colormaps = ['viridis', 'Spectral', 'plasma', 'inferno', 'Greys', 'Blues', 'winter', 'autumn',
                         'hot', 'hot_r', 'hsv', 'rainbow', 'jet', 'twilight', 'hsv']

        # ---Image title---
        frm = tk.Frame(frame)
        frm.pack(fill=tk.X, expand=tk.YES, padx=3, pady=3)

        var = tk.Label(frm, text='NPY file:', font=SF)
        var.pack(side=tk.LEFT, expand=tk.NO)
        var = tk.Label(frm, textvariable=self.filename, width=40, font=TF)
        var.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, padx=3)
        var = tk.Button(frm, text='Load', font=BF, bg=btn, activebackground=btn_active, command=self.btn_loadfile)
        var.pack(side=tk.LEFT, expand=tk.NO, padx=5)
        var = tk.Button(frm, text='Load Another', font=BF, bg=btn, activebackground=btn_active,
                        command=self.btn_loadnew)
        var.pack(side=tk.LEFT, expand=tk.NO, padx=5)

        # ---Options---
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

        var = tk.OptionMenu(frm, self.colormap, *all_colormaps, command=self.update_image)
        var.config(font=SF, bg=opt, activebackground=opt_active)
        var["menu"].config(bg=opt, bd=0, activebackground=opt_active)
        var.pack(side=tk.LEFT)

        var = tk.Label(frm, text='Mag. clim:', font=SF)
        var.pack(side=tk.LEFT, expand=tk.NO)
        var = tk.Entry(frm, textvariable=self.cmin, font=TF, width=6, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT)
        var.bind('<Return>', self.update_image)
        var.bind('<KP_Enter>', self.update_image)
        var = tk.Entry(frm, textvariable=self.cmax, font=TF, width=6, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT)
        var.bind('<Return>', self.update_image)
        var.bind('<KP_Enter>', self.update_image)

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
        self.tkscale = tk.Scale(frm, from_=0, to=100, variable=self.view_index, font=BF,
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
        self.fig = Figure(figsize=_figure_size, dpi=figure_dpi)
        self.fig.patch.set_facecolor('w')
        # Amplitude
        self.ax1 = self.fig.add_subplot(121)
        self.ax1_image = self.ax1.pcolormesh(self.mags[0], shading='auto')
        self.ax1.set_xlabel(u'Axis 0')
        self.ax1.set_ylabel(u'Axis 1')
        self.ax1.set_title('Magnitudes')
        self.ax1.set_xlim([0, 100])
        self.ax1.set_ylim([0, 100])
        self.cb1 = self.fig.colorbar(self.ax1_image, ax=self.ax1)
        self.ax1.axis('image')
        # Phase
        self.ax2 = self.fig.add_subplot(122)
        self.ax2_image = self.ax1.pcolormesh(self.angs[0], shading='auto')
        self.ax2.set_xlabel(u'Axis 0')
        self.ax2.set_ylabel(u'Axis 1')
        self.ax2.set_title('Angles')
        self.ax2.set_xlim([0, 100])
        self.ax2.set_ylim([0, 100])
        self.cb2 = self.fig.colorbar(self.ax2_image, ax=self.ax2)
        self.ax2.axis('image')

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
        if filename:
            self._loadfile(filename)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    "------------------------------------------------------------------------"
    "--------------------------General Functions-----------------------------"
    "------------------------------------------------------------------------"

    def _loadfile(self, filename):
        """Load NPY file"""
        data = np.load(filename)
        print(f'Filename: {filename}')
        print(f'Data shape: {data.shape}, type: {data.dtype}, max: {data.max()}, min: {data.min()}')
        if np.ndim(data) != 3:
            raise Exception('Numpy Data should have 3 dimensions.')
        self.filename.set(filename)
        self.data = data
        self.update_options()

    def update_options(self):
        """Get options"""
        self.mags = np.abs(self.data)
        mask = self.mags == 0
        self.mags[mask] = np.nan
        if self.logplot.get():
            self.mags = np.log10(self.mags)
        self.cmin.set(float(np.nanmin(self.mags)) if self.logplot.get() else 0)
        self.cmax.set(float(np.nanmax(self.mags)))

        self.angs = np.angle(self.data)
        clim = [-np.pi, np.pi]
        if self.absplot.get():
            self.angs = np.abs(self.angs)
            clim[0] = 0
        if self.sinplot.get():
            self.degplot.set(False)
            self.angs = np.sin(self.angs)
            clim = [-1, 1]
        if self.degplot.get():
            self.angs = np.rad2deg(self.angs)
            clim = [-180, 180]
        self.angs[mask] = np.nan
        self.ang_clim = clim

        self.update_axis()
        # self.cb1.update_normal(self.ax1_image)
        # self.cb2.update_normal(self.ax2_image)
        # self.toolbar.update()
        # self.fig.canvas.draw()

    def update_axis(self, event=None):
        """Get data size etc"""
        self._ax = int(self.view_axis.get()[-1]) - 1  # e.g. 'axis 1'
        shape = self.mags.shape
        self.tkscale.config(to=shape[self._ax])
        if self._ax == 0:
            self.ax1.set_xlabel(u'Axis 2')
            self.ax1.set_ylabel(u'Axis 3')
            self.ax2.set_xlabel(u'Axis 2')
            self.ax2.set_ylabel(u'Axis 3')
            self.ax1.set_xlim([0, shape[1]])
            self.ax1.set_ylim([0, shape[2]])
            self.ax2.set_xlim([0, shape[1]])
            self.ax2.set_ylim([0, shape[2]])
        elif self._ax == 1:
            self.ax1.set_xlabel(u'Axis 1')
            self.ax1.set_ylabel(u'Axis 3')
            self.ax2.set_xlabel(u'Axis 1')
            self.ax2.set_ylabel(u'Axis 3')
            self.ax1.set_xlim([0, shape[0]])
            self.ax1.set_ylim([0, shape[2]])
            self.ax2.set_xlim([0, shape[0]])
            self.ax2.set_ylim([0, shape[2]])
        else:
            self.ax1.set_xlabel(u'Axis 1')
            self.ax1.set_ylabel(u'Axis 2')
            self.ax2.set_xlabel(u'Axis 1')
            self.ax2.set_ylabel(u'Axis 2')
            self.ax1.set_xlim([0, shape[0]])
            self.ax1.set_ylim([0, shape[1]])
            self.ax2.set_xlim([0, shape[0]])
            self.ax2.set_ylim([0, shape[1]])
        self.view_index.set(shape[self._ax]//2)
        self.update_image()

    def update_image(self, event=None):
        """Plot image data"""
        idx = self.view_index.get()
        if self._ax == 0:
            im_mag = self.mags[idx, :, :]
            im_ang = self.angs[idx, :, :]
        elif self._ax == 1:
            im_mag = self.mags[:, idx, :]
            im_ang = self.angs[:, idx, :]
        else:
            im_mag = self.mags[:, :, idx]
            im_ang = self.angs[:, :, idx]
        self.ax1_image.remove()
        self.ax2_image.remove()
        colormap = self.colormap.get()
        mag_clim = [self.cmin.get(), self.cmax.get()]
        self.ax1_image = self.ax1.pcolormesh(im_mag, shading='auto', clim=mag_clim, cmap=colormap)
        self.ax2_image = self.ax2.pcolormesh(im_ang, shading='auto', clim=self.ang_clim, cmap=colormap)
        self.cb1.update_normal(self.ax1_image)
        self.cb2.update_normal(self.ax2_image)
        self.toolbar.update()
        self.fig.canvas.draw()

    "------------------------------------------------------------------------"
    "---------------------------Button Functions-----------------------------"
    "------------------------------------------------------------------------"

    def btn_loadfile(self, event=None):
        """Load NPY file"""
        filename = filedialog.askopenfilename(
            title='Select .npy to open',
            filetypes=[('NPY file', '.npy'), ('All files', '.*')],
            parent=self.root
        )
        if filename:
            self._loadfile(filename)

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

