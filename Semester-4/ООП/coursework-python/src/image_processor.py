import cv2
import matplotlib.pyplot as plt

from src.lib.get_text_len_on_image import get_text_len_on_image


class ImageProcessor:
    cascade = None
    image = None

    def __init__(self, path):
        self.image = cv2.imread(path)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        self.cascade = cv2.CascadeClassifier('src/cascades/haarcascade_russian_plate_number.xml')

        plt.imshow(self.image)

    def get_image(self):
        return self.image

    def enlarge_plt_display(self, image, scale_factor):
        width = int(image.shape[1] * scale_factor / 100)
        height = int(image.shape[0] * scale_factor / 100)
        dim = (width, height)
        plt.figure(figsize=dim)
        plt.axis('off')
        plt.imshow(image)

        return image

    # Определяет все возможные варианты рамок рамку и обводит их
    def carplate_detect(self, image):
        if self.cascade is None:
            return image

        carplate_overlay = image.copy()  # Create overlay to display rectangle of detected car plates
        carplate_rects = self.cascade.detectMultiScale(carplate_overlay, scaleFactor=1.1, minNeighbors=8)

        if len(carplate_rects) == 0:
            return carplate_overlay

        for x, y, w, h in carplate_rects:
            # Вырезаем область номерного знака
            carplate_img = image[y:y + h, x:x + w]
            # Получаем длину текста на вырезанном изображении
            text_len = get_text_len_on_image(carplate_img)

            # Обводим рамку только если длина текста больше 7
            if text_len > 7:
                cv2.rectangle(carplate_overlay, (x, y), (x + w, y + h), (255, 0, 0), 5)

        return carplate_overlay

    # Вырезает рамку из цельного изображения
    def carplate_extract(self, image):
        if self.cascade is None:
            return

        result = []

        carplate_rects =  self.cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=8)

        for x, y, w, h in carplate_rects:
            carplate_img = image[y:y + h, x:x + w]

            text_len = get_text_len_on_image(carplate_img)

            if text_len > 7:
                result.append(carplate_img)

        return result

    def increase_contrast(self, image):
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2Lab)
        l_channel, a, b = cv2.split(lab)

        # Применяем CLAHE (Contrast Limited Adaptive Histogram Equalization) на L-канал
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l_channel)

        # Объединяем каналы обратно
        limg = cv2.merge((cl, a, b))
        final_image = cv2.cvtColor(limg, cv2.COLOR_Lab2RGB)
        return final_image

    def enlarge_img(self, image, scale_percent):
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return resized_image

    def make_gray(self, image):
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image_gray = cv2.GaussianBlur(image_gray, (3, 3), 0)
        plt.axis('off')
        plt.imshow(image_gray, cmap='gray')

        return image_gray