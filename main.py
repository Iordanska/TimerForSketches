import os
import random
from time import sleep
from tkinter import *
from tkinter.filedialog import askdirectory

import pygame
from PIL import Image, ImageTk


class Gui:

    def __init__(self, root):

        self.image_rendered = None
        self.path = None
        self.counter = 0
        self.time = 0
        self.image_size_coef = 700
        self.images_paths = []

        self.root = root
        self.root.title('Timer fo sketches')
        self.root.state('zoomed')

        # menu
        self.menu_bar = Menu(root)
        self.root.config(menu=self.menu_bar)

        self.menu_bar.add_command(label='Open Folder', command=self.start)

        self.time_chose_var = IntVar()
        self.time_chose_var.set(10)

        self.timemenu = Menu(self.menu_bar, tearoff=0)
        self.timemenu.add_radiobutton(label="1 min", variable=self.time_chose_var, value=10)
        self.timemenu.add_radiobutton(label="2 min", variable=self.time_chose_var, value=120)
        self.timemenu.add_radiobutton(label="5 min", variable=self.time_chose_var, value=300)
        self.timemenu.add_radiobutton(label="10 min", variable=self.time_chose_var, value=600)
        self.timemenu.add_radiobutton(label="15 min", variable=self.time_chose_var, value=900)

        self.menu_bar.add_cascade(label="Time", menu=self.timemenu)

        # working space
        self.clock_face = Label(root, text='{:02d}:{:02d}'.format(0, 0), font='Arial 30 bold')
        self.clock_face.pack()
        self.frame = Frame(root)
        self.frame.pack()
        self.frame.place(relheight=0.85, relwidth=0.9, relx=0.5, rely=0.5, anchor=CENTER)
        self.image_displayed = Label(self.frame, font='Arial 25 bold')
        self.image_displayed.pack()
        self.next_btn = Button(root, text="Next", font='Arial 20 bold', width=20, command=self.next_image)

        # sound
        self.sound = 'sound.mp3'
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(self.sound)

    def set_time(self):
        self.time = self.time_chose_var.get()

    def start(self):
        self.load_images_paths()
        if len(self.images_paths) == 0:
            self.image_displayed.config(text='NO IMAGES FOUND!')
        random.shuffle(self.images_paths)

        self.next_btn.pack(side=BOTTOM)

        self.show_image()

    def load_images_paths(self):
        # self.images_paths = os.listdir(self.path)
        self.path = askdirectory()
        for address, dirs, files in os.walk(self.path):
            for name in files:
                full_address = os.path.join(address, name)
                if full_address.endswith(('jpeg', 'jpg', 'png')):
                    self.images_paths.append(full_address)

    def show_image(self):
        self.render_image()
        self.count_time()
        pygame.mixer.music.play()

    def count_time(self):
        try:
            self.set_time()
            time = self.time
            while time:
                m, s = divmod(int(time), 60)
                min_sec_format = '{:02d}:{:02d}'.format(m, s)
                self.clock_face.config(text=min_sec_format)
                self.clock_face.update()
                sleep(1)
                time -= 1

            min_sec_format = '{:02d}:{:02d}'.format(0, 0)
            self.clock_face.config(text=min_sec_format)
            self.clock_face.update()
        except TclError:
            pass

    def render_image(self):
        file = self.images_paths[self.counter]
        image = Image.open(os.path.join(self.path, file))

        aspect_ratio = image.size[0] / image.size[1]
        calc_width = int(aspect_ratio * self.image_size_coef)

        image_resized = image.resize((calc_width, self.image_size_coef), Image.LANCZOS)
        self.image_rendered = ImageTk.PhotoImage(image_resized)
        self.image_displayed.config(image=self.image_rendered)

    def next_image(self):
        pygame.mixer.music.pause()
        self.counter += 1
        if self.counter == len(self.images_paths) - 1:
            self.counter = 0
        self.show_image()


def main():
    root = Tk()
    my_prog = Gui(root=root)
    root.mainloop()


if __name__ == '__main__':
    main()
