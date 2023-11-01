# complex_array_viewer
Simple tk interface for viewing 3D complex numpy arrays.

![screenshot](gui_screenshot.png)

**Version 0.2**

| By Dan Porter | 
| --- |
| Diamond Light Source |
| 2023 |


#### To run viewer:
```commandline
$ python -m complex_array_viewer 'file.npy'
```

or in python:
```python
from complex_array_viewer import ComplexArrayViewer
ComplexArrayViewer('file.npy', figure_dpi=80)

from complex_array_viewer import MultiAngleViewer
MultiAngleViewer([f'file{n}.npy' for n in range(6)], figure_dpi=80, ncols=3)
```

#### Requires:
*numpy, matplotlib, tkinter*


#### Usage:
Start by clicking "Load" to load a complex 3D .npy file.

The magnitudes and phases will be displayed with a slider to scroll through the slices.

The axis of slicing can be choosen, and various options can be altered, including:

- Mask the data below amplitudes of a value
- View the log of the amplitudes
- View the phases in Degrees (rather than phases)
- View the absolute phases (|phase < 0|)
- View the sin of the phases
- View the differential
- Colormap (cyclic colormaps are twilight and hsv)
- Colormap limits