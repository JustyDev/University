import easyocr


def get_text_len_on_image(image):
    text = easyocr.Reader(["en"]).readtext(image, detail=0, paragraph=True, text_threshold=0.8)

    text = ''.join(text) if text else ''

    if not text or not text.strip():
        return 0

    return len(text.strip())