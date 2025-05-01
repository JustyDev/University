import easyocr


class CarPlateOCR:
    allowed_chars = "ABEKMHOPCTYX0123456789"

    path_img = None
    recognized_text = ''

    def __init__(self, path_img):
        self.path_img = path_img

    def recognize_text(self):
        text = easyocr.Reader(["en"]).readtext(self.path_img, detail=0, paragraph=True, text_threshold=0.9, allowlist=self.allowed_chars)

        if not text:
            self.recognized_text = ''
            return

        self.recognized_text = ''.join(text)

    def replace_zeros(self, string):
        """Заменяет нули на букву O в позициях 1, 5 и 6"""
        result = list(string)

        # Позиции 1, 5, 6 (индексы 0, 4, 5)
        positions = [0, 4, 5]

        for pos in positions:
            if pos < len(result) and result[pos] == '0':
                result[pos] = 'O'

        positions_revert = [1, 2, 3, 6, 7, 8]

        for pos in positions_revert:
            if pos < len(result) and result[pos] == 'O':
                result[pos] = '0'

        return ''.join(result)

    def process_string(self, string):
        # Проверяем длину строки
        if len(string) <= 6:
            return string

        # Оставляем первые 6 символов без изменений
        first_part = string[:6]

        # Для символов начиная с 7-го, оставляем только цифры
        second_part = ''.join(char for char in string[6:] if char.isdigit())

        # Объединяем части строки
        result = first_part + second_part

        return result

    def normalize_car_number(self, text):
        # Удаляем все пробелы из строки
        text = text.replace(" ", "")

        if len(text) >= 9:
            text = text[:9]

        text = text.upper()
        text = self.replace_zeros(text)
        text = self.process_string(text)

        return text

    def get_car_number(self):
        self.recognize_text()

        return self.normalize_car_number(self.recognized_text)

