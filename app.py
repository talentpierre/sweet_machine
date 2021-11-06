#!/home/pi/venv/sweet-machine/bin/python3
'''main app'''

import time
import os
import sys
import RPi.GPIO as GPIO

import qrcode
import requests

import config

from importlib import import_module


display_module = f"displays.{config.display}"
display = import_module(display_module, ".")


def setup_pins():
    """Initialises the coin acceptor parameters and
    sets up a callback for button pushes and coin inserts.
    """
   # Defining GPIO BCM Mode
    GPIO.setmode(GPIO.BCM)

    # Setup GPIO Pins for coin acceptor, button and button-led
    GPIO.setwarnings(False)
    GPIO.setup(13, GPIO.OUT)
    GPIO.output(13, GPIO.LOW)
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # If the button is pushed, the callback method is called
    # (bouncetime for switch bounce)
    GPIO.add_event_detect(5, GPIO.RISING, callback=button_event, bouncetime=300)


def button_event(channel):
    """Registers a button push event"""
    config.LASTPUSHES = time.time()
    config.PUSHES = config.PUSHES + 1


def monitor_button():
    """Monitors coins inserted and buttons pushed"""
    time.sleep(0.2)

    # Detect if the button has been pushed
    if (time.time() - config.LASTPUSHES > 1) and (config.PUSHES > 0):
        button_pushed()


def button_pushed():
    """Starts payment process"""
    print("button pushed")
    payment_dict = get_payreq_information()

    qr_img = generate_qr(payment_dict["payreq"])
    display.draw_qr(qr_img)

    if was_payed(payment_dict["payment_id"]):
        display.update_thankyou_screen()
        GPIO.output(13, GPIO.HIGH)
        time.sleep(4)
    else:
        display.update_payment_failed()
        time.sleep(2)

    softreset()

def get_payreq_information():
    """Returns a dict with paymentrequest and payment id"""
    url = "https://api.opennode.com/v1/charges"
    payload = {
        "order_id": "",
        "ttl": 10,
        "description": "sweet-machine",
        "amount": 400
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": config.read_only_key
    }
    response = requests.request("POST", url, json=payload, headers=headers).json()
    payreq = response['data']['lightning_invoice']['payreq']
    payment_id = response['data']['id']
    return {
        "payreq":  payreq,
        "payment_id": payment_id
    }


def was_payed(payment_id):
    """Returns True if the payment was successful"""
    url = f"https://api.opennode.com/v1/charge/{str(payment_id)}"
    headers = {
        "Accept": "application/json",
        "Authorization": config.read_only_key
    }
    for _ in range(20):
        response = requests.request("GET", url, headers=headers).json()
        payment_status = response['data']['status']
        print(payment_status)
        if payment_status == 'paid':
            print('paid')
            return True
        time.sleep(2)
    return False


def generate_qr(payreq):
    """Generate a qr code from a payment request."""
    payreq_qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=1,
    )
    payreq_qr.add_data(payreq.upper())
    return payreq_qr.make_image()


def softreset():
    """Displays startup screen and deletes fiat amount
    """
    config.PUSHES = 0
    GPIO.cleanup()
    setup_pins()
    display.update_startup_screen()


def main():
    '''main function'''
    display.update_startup_screen()
    setup_pins()
    while True:
        monitor_button()


if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            display.update_shutdown_screen()
            GPIO.cleanup()
            sys.exit("Manually Interrupted")
        except Exception:
            GPIO.cleanup()
            os.execv("/home/pi/sweet_machine/app.py", [""])
