import struct
import random

#самый главный файл говна, получается у нас 4 вида пикселей - полный, эквивалетный, красные тона, сине-зеленые тона
# все легко, ток операции сдвига битов  разобрать , то есть на примере полного
#сгенерили красный, потом сместили его на 4(потому что нужно совободить по 2 для с и з) потом дописали сзади с и з и байт готов
# 
def generate_full_pixel():
    #фул пиксель(1 бит флаг и 7 бит цвета из лабы ) 1 бит флаг, 3 бита красный, 2 бита зелёный, 2 бита синий
    red = random.randint(0, 7)  # 3 бита для красного (0-7)
    green = random.randint(0, 3)  # 2 бита для зелёного (0-3)
    blue = random.randint(0, 3)  # 2 бита для синего (0-3)
    byte = (red << 4) | (green << 2) | blue  # Собираем байт
    return byte

def generate_equivalent_pixel():
    #эквивалетный (1 бит флагн и по 2 на каждый цвет
    red = random.randint(0, 3)  # 2 бита для красного (0-3)
    green = random.randint(0, 3)  # 2 бита для зелёного (0-3)
    blue = random.randint(0, 3)  # 2 бита для синего (0-3)
    byte = (1 << 7) | (red << 5) | (green << 3) | (blue << 1)  # Флаг 1, каналы собраны
    return byte

def generate_red_tones_pixel():
    #красные тона (1 бит флаг, 3 бита красный, по 1 биту на зелёный и синий
    red = random.randint(0, 7)  # 3 бита для красного (0-7)
    green = random.randint(0, 1)  # 1 бит для зелёного (0-1)
    blue = random.randint(0, 1)  # 1 бит для синего (0-1)
    byte = (1 << 7) | (1 << 6) | (red << 3) | (green << 1) | blue  # Флаг 11, каналы собраны
    return byte

def generate_blue_green_tones_pixel():
    # сине-зелёные тона (1 бит флаг, 1 бит красный, 2 бита зелёный, 2 бита синий
    red = random.randint(0, 1)  # 1 бит для красного (0-1)
    green = random.randint(0, 3)  # 2 бита для зелёного (0-3)
    blue = random.randint(0, 3)  # 2 бита для синего (0-3)
    byte = (1 << 7) | (1 << 6) | (1 << 5) | (red << 4) | (green << 2) | blue  # Флаг 111, каналы собраны
    return byte

def create_image(filename):
    #генерим изображение 16 на 16 пикселей
    width = 16  
    height = 16  
    pixel_data = []

    for _ in range(width * height // 4):
        pixel_data.append(generate_full_pixel())  
        pixel_data.append(generate_equivalent_pixel())  
        pixel_data.append(generate_red_tones_pixel())  
        pixel_data.append(generate_blue_green_tones_pixel())  

    with open(filename, 'wb') as f:
        # Записываем заголовок (ширина, высота)
        f.write(struct.pack('HH', width, height))
        # Записываем данные пикселей
        for byte in pixel_data:
            f.write(struct.pack('B', byte))

# Генерация примера изображения с большим количеством пикселей
create_image('image_1.bin')


#второй вариант генерации изображения, что бы было лучше видно что где ,
#  - по рядам, первые два ряда первый тип, 2 два вторйо тип и тд,  8 на 8**
def create_image_2(filename):
    width = 16  
    height = 16  
    pixel_data = []
    #добавляю по 2 строки пикселей одного типа
    for _ in range(width * 2):
        pixel_data.append(generate_full_pixel())
    for _ in range(width * 2):
        pixel_data.append(generate_equivalent_pixel())
    for _ in range(width * 2):
        pixel_data.append(generate_red_tones_pixel())
    for _ in range(width * 2):
        pixel_data.append(generate_blue_green_tones_pixel())

    with open(filename, 'wb') as f:
        # Записываем заголовок (ширина, высота)
        f.write(struct.pack('HH', width, height))
        # Записываем данные пикселей
        for byte in pixel_data:
            f.write(struct.pack('B', byte))


create_image_2('image_2.bin')