"""
complex_array_viewer

By Dan Porter
Diamond Light Source Ltd
2023
"""

if __name__ == '__main__':

    import sys
    from complex_array_viewer import __version__, __date__, ComplexArrayViewer, start

    print('\ncomplex_array_viewer, version %s, %s\n By Dan Porter, Diamond Light Source Ltd.' % (__version__, __date__))

    if '.npy' in sys.argv[-1].lower():
        ComplexArrayViewer(sys.argv[-1])
    else:
        start()

