from gameObject import *
from imports import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'Images')
RESOURCES_DIR = 'Images'

# function to help load images, from pygame documentation (https://www.pygame.org/docs/tut/chimp.py.html)
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    return image, image.get_rect()

#power up superclass
class PowerUp(GameObject):
    locations = set()

    def init():
        HealthUp.init()
        Nuke.init()
        Freeze.init()

    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        PowerUp.locations.add((int(x), int(y)))
        self.timeOnScreen = 0
        super(PowerUp, self).__init__(x, y, image, 15)

    def update(self, screenWidth, screenHeight):
        super(PowerUp, self).update(screenWidth, screenHeight, 30, 30)

class HealthUp(PowerUp):
    @staticmethod
    def init():
        HealthUp.healthImage, HealthUp.rect = load_image('heart.png', -1)
        HealthUp.healthImage = pygame.transform.rotate(pygame.transform.scale(HealthUp.healthImage.convert_alpha(),
            (30, 30)), 0)

    def __init__(self, x, y):
        super(HealthUp, self).__init__(x, y, HealthUp.healthImage)

class Nuke(PowerUp):
    @staticmethod
    def init():
        Nuke.nukeImage, Nuke.rect = load_image('nuke.png', -1)
        Nuke.nukeImage = pygame.transform.rotate(pygame.transform.scale(Nuke.nukeImage.convert_alpha(),
            (30, 30)), 0)

    def __init__(self, x, y):
        super(Nuke, self).__init__(x, y, Nuke.nukeImage)

class Freeze(PowerUp):
    @staticmethod
    def init():
        Freeze.freezeImage, Freeze.rect = load_image('snow.png', -1)
        Freeze.freezeImage = pygame.transform.rotate(pygame.transform.scale(Freeze.freezeImage.convert_alpha(),
            (30, 30)), 0)

    def __init__(self, x, y):
        super(Freeze, self).__init__(x, y, Freeze.freezeImage)
