from gameObject import *
from imports import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'Images')

# define configuration variables here
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

#exploding barrel object
class Barrel(GameObject):
    def __init__(self, x, y, game):
        self.size = 50
        self.x = x
        self.y = y
        self.health = 50
        image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(image, (255, 0, 0), (self.size // 2, self.size // 2), self.size //2+1)
        pygame.draw.circle(image, (100, 100, 100), (self.size // 2, self.size // 2), self.size //2)
        pygame.draw.circle(image, (0, 0, 0), (self.size // 2, self.size // 2), self.size //2, 1)
        super(Barrel, self).__init__(x, y, image, self.size //2)

    def update(self, screenWidth, screenHeight):
        super(Barrel, self).update(screenWidth, screenHeight)

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True

#########################################

#bullet object
class Bullet(GameObject):

    def __init__(self, x, y, width, height, midCoordinates, spread, size, range, speed, color):
        cX, cY = midCoordinates
        self.size = size
        self.range = range
        image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(image, color, (size // 2, size // 2), size //2)

        super(Bullet, self).__init__(cX, cY, image, self.size //2)
        vx, vy = (cX - x, cY - y)

        if abs(vx) == 0:
            vx += 9
        elif abs(vy) == 0:
            vy += 9

        while abs(vx) < 7*speed or abs(vy) < 7*speed:
            vx *= 1.1
            vy *= 1.1

        while abs(vx) > 10*speed or abs(vy) > 10*speed:
            vx /= 1.1
            vy /= 1.1

        self.spread = spread
        spreadX = random.randint(-self.spread, self.spread)
        spreadY = random.randint(-self.spread, self.spread)

        self.velocity = -vx+spreadX, -vy+spreadY
        self.timeOnScreen = 0
        self.drag = 3
        self.rect = self.image.get_rect()
        self.traveled = 0

    def update(self, screenWidth, screenHeight, keysDown, walls):
        vx, vy = self.velocity
        self.traveled += max(abs(vx), abs(vy))

        super(Bullet, self).update(screenWidth, screenHeight)
        self.timeOnScreen += 1

        #remove after it travels a cartain distance
        if self.traveled > self.range:
            self.kill()
            return

        #only add drage after the bullet has been on screen for 5 ms
        if self.timeOnScreen > 5:
            if keysDown(pygame.K_LEFT) or keysDown(pygame.K_a):
                self.x += self.drag
            if keysDown(pygame.K_RIGHT) or keysDown(pygame.K_d):
                self.x -= self.drag
            if keysDown(pygame.K_UP) or keysDown(pygame.K_w):
                self.y += self.drag
            if keysDown(pygame.K_DOWN) or keysDown(pygame.K_s):
                self.y -= self.drag

        self.rect.center = [self.x, self.y]
