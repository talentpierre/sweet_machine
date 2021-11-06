#!/usr/bin/python3

import time
import math

import config

from displays import messages
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw


def create_font(font, size):
    """Create fonts from resources. """
    # Construct paths to foder with fonts
    pathfreemono = Path.cwd().joinpath("resources", "fonts", "FreeMono.ttf")
    pathfreemonobold = Path.cwd().joinpath("resources", "fonts", "FreeMonoBold.ttf")
    pathsawasdee = Path.cwd().joinpath("resources", "fonts", "Sawasdee.ttf")

    if font == "freemono":
        return ImageFont.truetype(pathfreemono.as_posix(), size)
    if font == "freemonobold":
        return ImageFont.truetype(pathfreemonobold.as_posix(), size)
    print("Font not available")
    return None


def update_startup_screen():
    """Show startup screen on eInk Display
    """
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (32, 13),
        messages.startup_screen_1,
        fill=config.BLACK,
        font=create_font("freemono", 22),
    )
    draw.text(
        (18, 50),
        messages.startup_screen_2,
        fill=config.BLACK,
        font=create_font("freemonobold", 65 ),
    )
    draw.text(
        (140, 88),
        messages.startup_screen_3,
        fill=config.BLACK,
        font=create_font("freemono", 16),
    )

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_payment_failed():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (25, 10),
        messages.payment_failed_1,
        fill=config.BLACK,
        font=create_font("freemono", 24),
    )
    draw.text(
        (35, 50),
        messages.payment_failed_2,
        fill=config.BLACK,
        font=create_font("freemono", 21),
    )
    draw.text(
        (60, 90),
        messages.payment_failed_3,
        fill=config.BLACK,
        font=create_font("freemono", 21),
    )

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_thankyou_screen():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (40, 10),
        messages.thankyou_screen_1,
        fill=config.BLACK,
        font=create_font("freemono", 26),
    )
    draw.text(
        (70, 50),
        messages.thankyou_screen_2,
        fill=config.BLACK,
        font=create_font("freemono", 26),
    )
    draw.text(
        (15, 90),
        messages.thankyou_screen_3,
        fill=config.BLACK,
        font=create_font("freemono", 18),
    )

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))
    time.sleep(5)


def update_shutdown_screen():
    image, width, height, draw = init_screen(color=config.WHITE)

    draw.text(
        (20, 10),
        messages.shutdown_screen_1,
        fill=config.BLACK,
        font=create_font("freemono", 20 ),
    )
    draw.text(
        (35, 50),
        messages.shutdown_screen_2,
        fill=config.BLACK,
        font=create_font("freemono", 20),
    )
    draw.text(
        (60, 90),
        messages.shutdown_screen_3,
        fill=config.BLACK,
        font=create_font("freemono", 20),
    )

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def draw_qr(qr_img):
    """Draw a lnurl qr code on the e-ink screen
    """
    image, width, height, draw = init_screen(color=config.BLACK)

    qr_img = qr_img.resize((122, 122), resample=0)

    draw = ImageDraw.Draw(image)
    draw.bitmap((0, 0), qr_img, fill=config.WHITE)
    draw.text(
        (140, 35),
        messages.draw_qr_1,
        fill=config.WHITE,
        font=create_font("freemonobold", 22),
    )
    draw.text(
        (140, 55),
        messages.draw_qr_2,
        fill=config.WHITE,
        font=create_font("freemonobold", 22),
    )

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def update_blank_screen():
    image, width, height, draw = init_screen(color=config.WHITE)

    config.WAVESHARE.init(config.WAVESHARE.FULL_UPDATE)
    config.WAVESHARE.display(config.WAVESHARE.getbuffer(image))


def init_screen(color):
    """Prepare the screen for drawing and return the draw variables
    """
    image = Image.new("1", (config.WAVESHARE.height, config.WAVESHARE.width), color)
    # Set width and height of screen
    width, height = image.size
    # prepare for drawing
    draw = ImageDraw.Draw(image)
    return image, width, height, draw
