import struct
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageProcessor:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.image_data = []

    def read_image(self, filename):

        with open(filename, 'rb') as f:
            # Чтение заголовка
            self.width, self.height = struct.unpack('HH', f.read(4))  # 2 байта на ширину и высоту
            data = f.read()  # Считывание данных пикселей
            
            self.image_data = []
            index = 0
            #тут гпт генерил, вроде понятно, но с хуйней с битами надо разобраться
            #если не оч понятно что откуда,  глянь сперва файл где генерятся  image,станет понятнее
            while index < len(data):
                byte = data[index]
                flag = (byte >> 7) & 1  # Извлечение флага
                if flag == 0:
                    # Полный пиксель 
                    #извлекаем пиксель в соотвествии с тем, скок у него было бит-места
                    red = (byte >> 4) & 0b111
                    green = (byte >> 2) & 0b11
                    blue = byte & 0b11
                elif flag == 1:
                    next_bits = (byte >> 6) & 1
                    if next_bits == 0:
                        # Эквивалентный пиксель
                        red = (byte >> 5) & 0b11
                        green = (byte >> 3) & 0b11
                        blue = (byte >> 1) & 0b11
                    elif next_bits == 1:
                        if (byte >> 5) & 1 == 0:
                            # Красные тона
                            red = (byte >> 4) & 0b111
                            green = (byte >> 1) & 0b1
                            blue = byte & 0b1
                        else:
                            # Сине-зелёные тона
                            red = (byte >> 4) & 0b1
                            green = (byte >> 2) & 0b11
                            blue = byte & 0b11
                self.image_data.append((red * 32, green * 64, blue * 64))  # Приводим цвета к 8-битной шкале
                index += 1

    def save_image(self, filename):
        with open(filename, 'wb') as f:
            # Записываем заголовок как еблан а лабнике говорил
            f.write(struct.pack('HH', self.width, self.height))
            # Записываем пиксели
            for (red, green, blue) in self.image_data:
                # Определяем тип пикселя и упаковываем его
                byte = (red // 32) << 4 | (green // 64) << 2 | (blue // 64)
                f.write(struct.pack('B', byte))

    def get_image(self):
        #конвертим пиксели в изображение для вывода 
        img = Image.new('RGB', (self.width, self.height))
        img.putdata(self.image_data)
        return img

#чисто интерфейс
class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor - Lab Work")
        self.processor = ImageProcessor()

        # Создаем кнопки и элементы интерфейса
        self.canvas = Canvas(root, width=300, height=300)
        self.canvas.pack()

        self.load_button = Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.save_button = Button(root, text="Save Image", command=self.save_image)
        self.save_button.pack()

        self.scale_label = Label(root, text="Scale:")
        self.scale_label.pack()
#размер можно сразу поставить от 1000 и до 5000
        self.scale = Scale(root, from_=100, to=3500, orient=HORIZONTAL, command=self.rescale_image)
        self.scale.set(100)
        self.scale.pack()

        self.image_on_canvas = None
        self.image_tk = None

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.processor.read_image(file_path)
            self.display_image()

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".bin")
        if file_path:
            self.processor.save_image(file_path)

    def display_image(self):
        img = self.processor.get_image()
        self.image_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

    def rescale_image(self, scale_value):
        scale_factor = int(scale_value) / 100
        width = int(self.processor.width * scale_factor)
        height = int(self.processor.height * scale_factor)

        img = self.processor.get_image().resize((width, height), Image.NEAREST)
        self.image_tk = ImageTk.PhotoImage(img)
        
        # Очищаем Canvas и заново рисуем изображение с новым масштабом
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)
        # Изменяем размер только изображения, но не Canvas
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))


if __name__ == "__main__":
    root = Tk()
    app = ImageEditorApp(root)
    root.mainloop()