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


##################################################
class Player(GameObject):
    @staticmethod
    def init():
        #different player images for each weapon
        Player.rifleImage, Player.rect = load_image('playerRifle.png', -1)
        Player.rifleImage = pygame.transform.rotate(pygame.transform.scale(Player.rifleImage.convert_alpha(),
            (65, 160)), -90)

        Player.pistolImage, Player.rect = load_image('playerPistol.png', -1)
        Player.pistolImage = pygame.transform.rotate(pygame.transform.scale(Player.pistolImage.convert_alpha(),
            (65, 160)), -90)

        Player.sniperImage, Player.rect = load_image('playerSniper.png', -1)
        Player.sniperImage = pygame.transform.rotate(pygame.transform.scale(Player.sniperImage.convert_alpha(),
            (65, 160)), -90)

        Player.shotgunImage, Player.rect = load_image('playerShotgun.png', -1)
        Player.shotgunImage = pygame.transform.rotate(pygame.transform.scale(Player.shotgunImage.convert_alpha(),
            (65, 160)), -90)

        Player.submachineImage, Player.rect = load_image('playerSub.png', -1)
        Player.submachineImage = pygame.transform.rotate(pygame.transform.scale(Player.submachineImage.convert_alpha(),
            (65, 160)), -90)

    def __init__(self, x, y):
        super(Player, self).__init__(x, y, Player.pistolImage, 30)
        print(Player.rect)
        self.health = 100
        self.speed = 3
        self.angle = 90
        self.x = x
        self.y = y

        pygame.sprite.Sprite.__init__(self)
        self.lastVelocity = [0,0]
        self._position = [self.x, self.y]
        self.originalPosition = [self.x, self.y]
        self.rect = self.image.get_rect()

    def update(self, screenWidth, screenHeight, keysDown, midCoordinates, x=0, y=0):
        cX, cY = midCoordinates

        #spin around
        if x != 0 and y != 0:
            self.angle = 360-math.atan2(y-cY,x-cX)*180/math.pi

        #movement
        else:
            self.lastVelocity = [0,0]

            if (keysDown(pygame.K_RIGHT) or keysDown(pygame.K_d)) and (keysDown(pygame.K_LEFT) or keysDown(pygame.K_a)):
                self.lastVelocity[0] = 0
            elif keysDown(pygame.K_LEFT) or keysDown(pygame.K_a):
                self.x -= self.speed
                self.lastVelocity[0] = +self.speed
            elif keysDown(pygame.K_RIGHT) or keysDown(pygame.K_d):
                self.x += self.speed
                self.lastVelocity[0] = -self.speed

            if (keysDown(pygame.K_DOWN) or keysDown(pygame.K_s)) and (keysDown(pygame.K_UP) or keysDown(pygame.K_w)):
                self.lastVelocity[1] = 0
            elif keysDown(pygame.K_UP) or keysDown(pygame.K_w):
                self.y -= self.speed
                self.lastVelocity[1] = +self.speed
            elif keysDown(pygame.K_DOWN) or keysDown(pygame.K_s):
                self.y += self.speed
                self.lastVelocity[1] = -self.speed

            self._position = [self.x, self.y]

        self.rect.center = self._position

        super(Player, self).update(screenWidth, screenHeight)

        return (self.lastVelocity)

    #move character backwards after collision
    def moveBack(self):
        self.x += self.lastVelocity[0]
        self.y += self.lastVelocity[1]
        #self._position = self.oldPosition
        self._position = [self.x, self.y]
        self.rect.center = self._position
        return self.lastVelocity

    #taking damage
    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True

    #change player picture with each weapon
    def changePic(self, gun):
        if gun == "pistol":
            super(Player, self).changePic(Player.pistolImage)
        elif gun == "sniper":
            super(Player, self).changePic(Player.sniperImage)
        elif gun == "rifle":
            super(Player, self).changePic(Player.rifleImage)
        elif gun == "shotgun":
            super(Player, self).changePic(Player.shotgunImage)
        else:
            super(Player, self).changePic(Player.submachineImage)

###############################################

class Friend(GameObject):
    @staticmethod
    def init():
        Friend.friendImage, Friend.rect = load_image('friend.png', -1)
        Friend.friendImage = pygame.transform.rotate(pygame.transform.scale(Friend.friendImage.convert_alpha(),
            (65, 100)), -90)

    def __init__(self, x, y):
        super(Friend, self).__init__(x, y, Friend.friendImage, 30)
        self.health = 150
        self.weapon = "pistol"
        self.speed = 4
        self.angle = 90
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)

        self.rect = self.image.get_rect()
        self.aimX = 0
        self.aimY = 0
        self.dx = 0
        self.dy = 0
        self.targetX = 400
        self.targetY = 300

    def update(self, screenWidth, screenHeight, clock, aimx, aimy, target):
        self.aimX = aimx
        self.aimY = aimy

        if clock%30 == 0:
            distance = 150
            XList = [random.randint(-distance, -30), random.randint(30, distance)]
            YList = [random.randint(-distance, -30), random.randint(30, distance)]
            randX, randY = 0, 0

            if target == "quad1":
                randX = XList[1]
                randY = YList[1]
            elif target == "quad2":
                randX = XList[0]
                randY = YList[1]
            elif target == "quad3":
                randX = XList[1]
                randY = YList[0]
            elif target == "quad4":
                randX = XList[0]
                randY = YList[0]

            self.targetX = 400 + randX
            self.targetY = 300 + randY

        self.dx, self.dy = (self.x - self.targetX, self.y - self.targetY)

        while abs(self.dx) > self.speed or abs(self.dy) > self.speed:
            self.dx /= 1.1
            self.dy /= 1.1

        self.x -= self.dx
        self.y -= self.dy
        self.angle = 360-math.atan2(self.aimY - self.y, self.aimX - self.x)*180/math.pi
        self.rect.center = [self.x, self.y]
        super(Friend, self).update(screenWidth, screenHeight)
