from pyrogram import Client, filters
from pyrogram.errors import FloodWait

import time
from time import sleep

from PIL import Image as PImage

from textwrap import wrap

from wand.color import Color
from wand.image import Image as WImage
from wand.drawing import Drawing
from wand.compat import nested

import math

LETTER_MAPPING = {
    'а': 'а',
    'б': 'б',
    'в': 'в',
    'г': 'г',
    'д': 'д',
    'е': 'е',
    'ё': 'ё',
    'ж': 'ж',
    'з': 'з',
    'и': 'и',
    'й': 'й',
    'к': 'к',
    'л': 'л',
    'м': 'м',
    'н': 'н',
    'о': 'о',
    'п': 'п',
    'р': 'р',
    'с': 'с',
    'т': 'т',
    'у': 'у',
    'ф': 'ф',
    'х': 'х',
    'ц': 'ц',
    'ч': 'ч',
    'ш': 'ш',
    'щ': 'щ',
    'ъ': 'ъ',
    'ы': 'ы',
    'ь': 'ь',
    'э': 'э',
    'ю': 'ю',
    'я': 'я',

    'a': 'a',
    'b': 'b',
    'c': 'c',
    'd': 'd',
    'e': 'e',
    'f': 'f',
    'g': 'g',
    'h': 'h',
    'i': 'i',
    'j': 'j',
    'k': 'k',
    'l': 'l',
    'm': 'm',
    'n': 'n',
    'o': 'o',
    'p': 'p',
    'q': 'q',
    'r': 'r',
    's': 's',
    't': 't',
    'u': 'u',
    'v': 'v',
    'w': 'w',
    'x': 'x',
    'y': 'y',
    'z': 'z',

    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    '0': '0',

    ' ': 'spc',
    '.': 'dot',
    ',': 'com',
    '!': '!',
    '?': '?',
    ':': ':',
    ';': ';',
    '(': '(',
    ')': ')',
    '-': '-',
}

DIR_FONT_FUNPICS_TRANSPARENT = 'letters_funpics_transparent'
DIR_FONT_FUNPICS = 'letters_funpics'
NIL = 'nil'

LETTERS_HANDMADE = 'абвгдеёжзиклмнопрстуфхцчшщъыьэбя '

FONTS_IMAGES = {}

for font_dir in [DIR_FONT_FUNPICS_TRANSPARENT, DIR_FONT_FUNPICS]:
    FONTS_IMAGES[font_dir] = {
        letter: PImage.open(f'{font_dir}/{LETTER_MAPPING[letter]}.png')
        for letter in LETTER_MAPPING
    }
    FONTS_IMAGES[font_dir][NIL] = PImage.open(f'{font_dir}/nil.png')

DIR_FONT_HANDMADE = 'letters'
FONT_HANDMADE = {
    letter: PImage.open(f'{DIR_FONT_HANDMADE}/{LETTER_MAPPING[letter]}.png')
    for letter in LETTERS_HANDMADE
}
FONT_HANDMADE[NIL] = PImage.open(f'{DIR_FONT_HANDMADE}/nil.png')

ROW_SIZE = 16

STICKER_FILENAME = 'result.webp'

app = Client("my_account")


def split_by_n(text, n):
    result = []

    for start in range(0, len(text), n):
        result.append(text[start:start+n])

    return result


def print_sticker(msg, text, font_images):
    msg.delete()

    total_width = 0
    total_height = 0

    for batch_letters in split_by_n(text, ROW_SIZE):
        images = [font_images[l] if l in font_images else font_images[NIL] for l in batch_letters]
        widths, heights = zip(*(i.size for i in images))

        total_width = max(total_width, sum(widths))
        total_height += max(heights)

    new_im = PImage.new('RGBA', (total_width, total_height))

    y_offset = 0

    for batch_letters in split_by_n(text, ROW_SIZE):
        images = [font_images[l] if l in font_images else font_images[NIL] for l in batch_letters]
        widths, heights = zip(*(i.size for i in images))

        x_offset = 0
        for im in images:
            new_im.paste(im, (x_offset, y_offset))
            x_offset += im.size[0]

        y_offset += max(heights)

    new_im.save(STICKER_FILENAME)

    reply_message_id = None
    if msg.reply_to_message:
        reply_message_id = msg.reply_to_message.message_id

    sent = False
    while not sent:
        try:
            app.send_sticker(
                chat_id=msg.chat.id,
                sticker=STICKER_FILENAME,
                disable_notification=True,
                reply_to_message_id=reply_message_id,
            )

            sent = True

        except FloodWait as e:
            print(f'FloodWait. Sleeping {e.x}...')
            sleep(e.x)


FONT_MAPPING = {
    'slimamif': 'SlimamifMedium',
    'rough': 'XBAND Rough Cyrillic AA',
    'sgraffiti': 'Sprite Graffiti',
}

FONT_SIZE = 512
WRAP_ATTEMPTS = 100


def word_wrap(image, ctx, text, roi_width, roi_height, font_size):
    """Break long text to multiple lines, and reduce point size
    until all text fits within a bounding box."""
    mutable_message = text
    attempts = WRAP_ATTEMPTS

    ctx.font_size = font_size

    def eval_metrics(txt):
        """Quick helper function to calculate width/height of text."""
        metrics = ctx.get_font_metrics(image, txt, True)
        return (metrics.text_width, metrics.text_height)

    def shrink_text():
        """Reduce point-size & restore original text"""
        ctx.font_size *= 0.96

    columns = len(mutable_message)

    roi_width = roi_width
    roi_height = roi_height

    while ctx.font_size > 0 and attempts:
        attempts -= 1
        width, height = eval_metrics(mutable_message)

        # print(width, height, 'roi:  ', roi_width, roi_height)

        if height > roi_height:
            font_size *= 0.96
            shrink_text()

            wrapped_width = width
            while wrapped_width < roi_width and columns < len(mutable_message):
                columns += 1
                mutable_message = '\n'.join(wrap(text, columns))
                wrapped_width, _ = eval_metrics(mutable_message)

            if wrapped_width > roi_height:
                columns -= 1
                mutable_message = '\n'.join(wrap(text, columns))

        elif width > roi_width:
            while columns > 0:
                columns -= 1
                mutable_message = '\n'.join(wrap(text, columns))
                wrapped_width, _ = eval_metrics(mutable_message)
                if wrapped_width <= roi_width:
                    break

            if columns < 1:
                shrink_text()
                columns = 1
                mutable_message = '\n'.join(wrap(text, columns))
        else:
            break

    if attempts < 1:
        raise RuntimeError('Unable to calculate word_wrap for "', text, '" in ', WRAP_ATTEMPTS, 'attempts.')

    print(f'Attempts: {WRAP_ATTEMPTS - attempts}/{WRAP_ATTEMPTS}. Font size: {ctx.font_size}.')

    return mutable_message, ctx.font_size


def print_sticker_font(msg, text, font_name):
    msg.delete()

    WIDTH = 512
    HEIGHT = 512

    with Drawing() as draw:
        with WImage(width=WIDTH, height=HEIGHT, background=Color('white')) as img:
            img.format = 'png'
            with Color('#FDFDFD') as white:
                twenty_percent = int(65535 * 0.05)  # Note: percent must be calculated from Quantum
                img.transparent_color(white, alpha=0.0, fuzz=twenty_percent)

            draw.font_family = FONT_MAPPING[font_name] # FONT_MAPPING[font_name]
            draw.font_size = FONT_SIZE
            draw.push()
            draw.font_weight = 700
            draw.fill_color = Color('hsl(0%, 0%, 0%)')
            draw.fill_color = Color('RED')

            mutable_message, font_size = word_wrap(
                img, draw, text,
                WIDTH, HEIGHT, FONT_SIZE,
            )
            print(mutable_message)
            draw.text(0, math.ceil(font_size), mutable_message)

            draw.pop()
            draw(img)
            img.save(filename=STICKER_FILENAME)

    reply_message_id = None
    if msg.reply_to_message:
        reply_message_id = msg.reply_to_message.message_id

    sent = False
    while not sent:
        try:
            app.send_sticker(
                chat_id=msg.chat.id,
                sticker=STICKER_FILENAME,
                disable_notification=True,
                reply_to_message_id=reply_message_id,
            )

            sent = True

        except FloodWait as e:
            print(f'FloodWait. Sleeping {e.x}...')
            sleep(e.x)


@app.on_message(filters.command("font-fun", prefixes=".") & filters.me)
def print_font(_, msg):
    text = msg.text.lower().split(".font-fun ", maxsplit=1)[1]
    print_sticker(msg, text, FONTS_IMAGES[DIR_FONT_FUNPICS])


@app.on_message(filters.command("font-fun-tp", prefixes=".") & filters.me)
def print_font_transparent(_, msg):
    text = msg.text.lower().split(".font-fun-tp ", maxsplit=1)[1]
    print_sticker(msg, text, FONTS_IMAGES[DIR_FONT_FUNPICS_TRANSPARENT])


@app.on_message(filters.command("font-simple", prefixes=".") & filters.me)
def print_font_transparent(_, msg):
    text = msg.text.lower().split(".font-simple ", maxsplit=1)[1]
    print_sticker(msg, text, FONT_HANDMADE)


@app.on_message(filters.command("font-custom", prefixes=".") & filters.me)
def print_font_transparent(_, msg):
    prefix = ".font-custom "
    font_name, text = msg.text[len(prefix):].split(" ", maxsplit=1)

    print_sticker_font(msg, text, font_name)


app.run()
