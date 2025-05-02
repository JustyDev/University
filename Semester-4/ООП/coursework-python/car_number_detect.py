import sys

from src.car_plate_ocr import CarPlateOCR
from src.image_processor import ImageProcessor
from src.lib.clear_folder import clear_folder
from src.lib.load_car_numbers import load_car_numbers
from src.lib.save_progress import save_progress

# База автомобильных номеров

db_path = "./allowed_car_numbers.txt"
db_numbers = load_car_numbers(db_path)

def main():
    # Проверяем, был ли передан аргумент с путем к файлу
    if len(sys.argv) != 2:
        print("Использование: python3 car_number_detect.py ./путь/до/изображения")
        sys.exit(1)

    image_path = sys.argv[1].strip()

    clear_folder('progress')

    ip = ImageProcessor(image_path)

    img = ip.get_image()
    img = ip.enlarge_plt_display(img, 1.2)

    save_progress(ip.carplate_detect(img), "1_car_plate_detect.jpg")

    # Обрезаем изображение, чтобы была видна только рамка
    crops = ip.carplate_extract(img)

    if len(crops) > 1:
        print("На изображении несколько автомобильных номеров")
        exit(1)

    if len(crops) < 1:
        print("На изображении не найден автомобильный номер")
        exit(1)

    img = ip.enlarge_img(crops[0], 300)

    save_progress(img, "2_car_plate_extract.jpg")

    # Увеличиваем контрастномть и делаем изображение серым
    img = ip.increase_contrast(img)
    img = ip.make_gray(img)

    save_progress(img, "3_grey_contrast.jpg")

    ocr = CarPlateOCR(img)

    number = ocr.get_car_number()

    print("Номер машины на фото: " + number)

    if number in db_numbers:
        print("Автомобиль найден в базе")
    else:
        print("Автомобиль не найден в базе")

if __name__ == "__main__":
    main()