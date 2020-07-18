import pygame

"""
GameObject created by Lukas Peraza
for 15-112 F15 Pygame Optional Lecture, 11/11/15
http://blog.lukasperaza.com/getting-started-with-pygame/
"""
class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, radius):
        super(GameObject, self).__init__()
        # x, y define the center of the object
        self.x, self.y, self.image, self.radius = x, y, image, radius
        self.baseImage = image.copy()  # non-rotated version of image
        w, h = image.get_size()
        self.updateRect()
        self.velocity = (0, 0)
        self.angle = 0

    def updateRect(self, w=0, h=0):
        # update the object's rect attribute with the new x,y coordinates
        if w == 0 and h == 0:
            w, h = self.image.get_size()

        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)

    def update(self, screenWidth, screenHeight, w=0, h=0):
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        vx, vy = self.velocity
        self.x += vx
        self.y += vy
        self.updateRect(w, h)

    def changePic(self, image):
        self.baseImage = image.copy()
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
