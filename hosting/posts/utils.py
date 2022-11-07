import random
import os
import pytesseract
from pytils import translit

from PIL import Image


def slugify_instance_title(instance, save=False, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = translit.slugify(instance.title)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        # auto generate new slug
        rand_int = random.randint(300_000, 500_000)
        slug = f"{slug}-{rand_int}"
        return slugify_instance_title(instance, save=save, new_slug=slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance


def transcribe_image(instance, save=False, new_transcription=None):
    if new_transcription is not None:
        transcription = new_transcription
    else:
        try:
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

            print('****************', os.path.normpath(os.getcwd() + '/' + str(instance.image)))
            # sum_path = f'{os.getcwd()}'+f'{instance.image}'
            # final_path = fr'{sum_path}'
            # print(sum_path, '****************', final_path)
            # print(pytesseract.image_to_string(r'D:\Dev\mediahosting\hosting\media\posts\images\1a267872-5a11-11ed-bdf4-645d863b07fa.png'))
            # D:\Dev\mediahosting\hosting\media\posts\images\1a267872-5a11-11ed-bdf4-645d863b07fa.png
            # transcription = pytesseract.image_to_string(instance.image)
            transcription = pytesseract.image_to_string(Image.open(os.path.normpath(os.getcwd() + '/' + str(instance.image))))
        except Exception as exc:
            print('При обработке картинки произошел:', exc)
            transcription = ''

    instance.transcription = transcription
    if save:
        instance.save()
    return instance
