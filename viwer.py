import sys
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QLabel, QSlider, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MRIViewer(QWidget):
    def __init__(self, nii_path):
        super().__init__()
        self.setWindowTitle('3D MRI Slice Viewer')
        self.resize(600, 700)

        # Load NIfTI image
        self.img = nib.load(nii_path)
        self.data = self.img.get_fdata()
        self.slice_index = self.data.shape[2] // 2

        # UI Elements
        self.canvas = FigureCanvas(plt.figure())
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.data.shape[2] - 1)
        self.slider.setValue(self.slice_index)
        self.slider.valueChanged.connect(self.update_plot)

        self.label = QLabel(f"Slice: {self.slice_index}")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.canvas)
        layout.addWidget(self.slider)
        self.setLayout(layout)

        self.plot_slice()

    def plot_slice(self):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.imshow(self.data[:, :, self.slice_index].T, cmap='gray', origin='lower')
        ax.set_title(f"Slice {self.slice_index}")
        ax.axis('off')
        self.canvas.draw()

    def update_plot(self, value):
        self.slice_index = value
        self.label.setText(f"Slice: {self.slice_index}")
        self.plot_slice()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = MRIViewer("chris_t1.nii.gz")  # Make sure this file is in the same directory
    viewer.show()
    sys.exit(app.exec_())
