"""
Run complex array viewer
"""

from complex_array_viewer import MultiAngleViewer

files = [
    r"C:\Users\grp66007\Documents\BCDI_Recons\Data_prep\00\output_00_2023-08-07_11.01.npy",
    r"C:\Users\grp66007\Documents\BCDI_Recons\Data_prep\01\output_01_2023-08-07_14.42.npy",
    r"C:\Users\grp66007\Documents\BCDI_Recons\Data_prep\02\output_02_2023-08-07_15.46.npy",
    r"C:\Users\grp66007\Documents\BCDI_Recons\Data_prep\03\output_03_2023-08-07_16.49.npy",
    r"C:\Users\grp66007\Documents\BCDI_Recons\Data_prep\04\output_04_2023-08-07_17.53.npy",
    r"C:\Users\grp66007\Documents\BCDI_Recons\Data_prep\05\output_05_2023-08-07_18.56.npy"
]
# files = [
#     r"C:\Users\grp66007\Documents\BCDI_Recons\Data_prep\%02d\output_%02d_norm_ph0_CM.npy" % (n, n)
#     for n in range(0, 6)
# ]
"""
        id |   00  |   01  |   02  |   03  |   04  |   05
        --------------------------------------------------
     state |  C_25 |  C_30 |  C_35 |  C_40 |  D_35 |  D_30
"""
titles = ['2.5V', '3.0V', '3.5V', '4.0V', '3.5V', '3.0V']
MultiAngleViewer(files, figure_dpi=80, ncols=3, titles=titles)

