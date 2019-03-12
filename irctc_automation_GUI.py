from tkinter import *
from PIL import ImageTk
import requests
import shutil

# initialize window
window = Tk()
window.geometry('640x480')
window.title("IRCTC")

# create canvas for drawing
canvas = Canvas(window,bg="gray", width = 640, height = 480)
canvas.place_configure(x=0, y=0, width = 640, height = 480)


def login_irctc():
    print('Login Button was Clicked!')


lbl = Label(window, text="Username")
lbl.grid(column=0, row=0)
txt = Entry(window,width=10)
txt.grid(column=1, row=0)
btn = Button(window, text="Login", command=login_irctc)
btn.grid(column=1, row=0)


# start program
window.mainloop()



"""
#nlpCaptchaImg

URL = 'https://irctclive.nlpcaptcha.in/index.php/media/getit/YkFrMHd5MCtPTWFrcU1rbzBwUnJJdkhlV3F2emNYSUJRYnpHQ01tUWJtT3BTdTY4VjJ0czdYTTlub3hiOENGR3V6MFZpRlFna3lVeDY3NE13dGFlMUE9PQ=='

def OpenImage(URL):
    # retrieve and download image
    image = open('image.png', 'wb')
    r = requests.get(URL,stream=True)
    if r.status_code == 200:
        with image as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    image.close()
    return image

# load image with PIL and draw to canvas
#IMG = ImageTk.PhotoImage(file = 'image.png')
#canvas.create_image(10, 10, image = IMG, anchor = NW)

"""
