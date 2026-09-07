from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QFileDialog 
import os
from PyQt5.QtGui import QPixmap # оптимизированная для показа на экране картинка
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from PyQt5.QtCore import Qt
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)


# extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']

app = QApplication([])
main = QWidget()
main.resize(900, 600)

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFilenameList():
    extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir() 
    files = os.listdir(workdir)
    list_filenames = filter(files, extensions)
    lw_list.addItems(list_filenames)

class ImadgeProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'New_image/'

    def loadImadge(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        label.hide()
        pixmapimage = QPixmap(path) # Создаем экземпляр класса с путем к картинке
        w, h = label.width(), label.height() # Получаем высоту и ширину label
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio) # Сжимаем картинку под нужный размер если она больше 
        label.setPixmap(pixmapimage) # Устанавлеваем картинку на label
        label.show()

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    
    def blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def _grayscale_(self):
        self.image = ImageOps.grayscale(self.image)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def left(self):
        self.image = self.image.rotate(90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
        
    def right(self):
        self.image = self.image.rotate(270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def contrast(self):
        self.image = ImageEnhance.Contrast(self.image)
        self.image = self.image.enhance(1.5)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def mirror(self):
        self.image = ImageOps.mirror(self.image)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


# def do_grayscale(self):
#         gray = ImageOps.grayscale(self.original)
#         self.changed.append(gray)
#         gray.save('gray.jpg') 
#ImageEnhance.Contrast(dog)

def showChosenImage():
    if lw_list.currentRow() >= 0:
        filename = lw_list.currentItem().text()
        workimadge.loadImadge(filename)
        image_path = os.path.join(workdir, workimadge.filename)
        workimadge.showImage(image_path)



lw_list = QListWidget()
label = QLabel('Картинка')
btn_folder = QPushButton('Папка')
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirror =QPushButton('Зеркало')
btn_sharpen =QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')
btn_blur = QPushButton('Блюр')
btn_contrast = QPushButton('Контраст')

v1 = QVBoxLayout()
v2 = QVBoxLayout()
h1 = QHBoxLayout()
h2 = QHBoxLayout()
H = QHBoxLayout()

v1.addWidget(btn_folder)
v1.addWidget(lw_list)

h1.addWidget(btn_left)
h1.addWidget(btn_right)
h1.addWidget(btn_mirror)
h1.addWidget(btn_sharpen)
h2.addWidget(btn_bw)
h2.addWidget(btn_blur)
h2.addWidget(btn_contrast)

v2.addWidget(label)
v2.addLayout(h1)
v2.addLayout(h2)

H.addLayout(v1, 20)
H.addLayout(v2, 80)

main.setLayout(H)

workdir = ''

workimadge = ImadgeProcessor()
btn_folder.clicked.connect(showFilenameList)
btn_blur.clicked.connect(workimadge.blur)
btn_bw.clicked.connect(workimadge._grayscale_)
btn_left.clicked.connect(workimadge.left)
btn_right.clicked.connect(workimadge.right)
btn_contrast.clicked.connect(workimadge.contrast)
btn_mirror.clicked.connect(workimadge.mirror)
btn_sharpen.clicked.connect(workimadge.sharpen)
lw_list.currentRowChanged.connect(showChosenImage)


main.show()
app.exec_()

