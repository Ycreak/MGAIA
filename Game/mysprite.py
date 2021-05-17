import pygame
from pygame.locals import *
import os
import math


class MySprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, w, h):
        super(MySprite, self).__init__()
        # adding all the images to sprite array
        self.images = self.load_images(image)

        # index value to get the image from the array
        # initially it is 0
        self.index = 0

        # now the image that we will display will be the index from the image array
        self.image = self.images[math.floor(self.index)]

        # creating a rect at position x,y (5,5) of size (150,198) which is the size of sprite
        self.rect = pygame.Rect(x, y, w, h)

    def load_images(self, path):
        """
        Loads all images in directory. The directory must only contain images.

        Args:
            path: The relative or absolute path to the directory to load images from.

        Returns:
            List of images.
        """
        images = []
        temp_list = []
        for file_name in os.listdir(path):
            temp_list.append(file_name)

        temp_list = sorted(temp_list)

        for file_name in temp_list:
            image = pygame.image.load(path + os.sep + file_name)
            image = pygame.transform.scale(image, (120, 150))
            images.append(image)

        return images

    def update(self):
        # when the update method is called, we will increment the index
        print('index:', self.index)
        self.index += 0.02

        # if the index is larger than the total images
        if self.index >= len(self.images):
            print(self.index, 'time for next icon')
            # we will make the index to 0 again
            self.index = 0

        # finally we will update the image that will be displayed
        self.image = self.images[math.floor(self.index)]
