from gameObject import *
from imports import *
from powerups import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'Images')

# define configuration variables here
RESOURCES_DIR = 'Images'

def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    return image, image.get_rect()

class Zombie(GameObject):
    count = 0
    CX = 400
    CY = 300
    speed = 1
    @staticmethod
    def init():
        Zombie.zombieImage, Zombie.rect = load_image('zombie.png', -1)
        Zombie.zombieImage = pygame.transform.rotate(pygame.transform.scale(Zombie.zombieImage.convert_alpha(),
            (65, 100)), -90)

        Zombie.miniZombie, Zombie.rect = load_image('miniZombie.png', -1)
        Zombie.miniZombie = pygame.transform.rotate(pygame.transform.scale(Zombie.miniZombie.convert_alpha(),
            (47, 70)), -90)

        Zombie.tankZombie, Zombie.rect = load_image('tankZombie.png', -1)
        Zombie.tankZombie = pygame.transform.rotate(pygame.transform.scale(Zombie.tankZombie.convert_alpha(),
            (98, 150)), -90)

        Zombie.bombZombie, Zombie.rect = load_image('bombZombie.png', -1)
        Zombie.bombZombie = pygame.transform.rotate(pygame.transform.scale(Zombie.bombZombie.convert_alpha(),
            (65, 100)), -90)

    def __init__(self, x, y, health, speed, tx = 400, ty = 300):
        self.health = health
        self.speed = speed
        Zombie.count += 1
        self.targetX = tx
        self.targetY = ty

        self.angle = 360-math.atan2(self.targetY - y, self.targetX - x)*180/math.pi
        self.x = x
        self.y = y
        self.lastHitTime = 1000
        self.dx = 0
        self.dy = 0
        super(Zombie, self).__init__(x, y, Zombie.zombieImage, 30)

        self.rect = self.image.get_rect()
        self.timeOnScreen = 0
        self.targetTime = 0

    def update(self, screenWidth, screenHeight, walls, clock, freeze):
        speed = 1

        if freeze == True:
            speed = .3

        if clock%10 == 0:
            distance = min(150, 100 + 10 * (Zombie.count))

            randX = random.randint(-distance, distance)
            randY = random.randint(-distance, distance)

            self.dx, self.dy = (self.x - self.targetX + randX, self.y - self.targetY + randY)

        while abs(self.dx) > self.speed or abs(self.dy) > self.speed:
            self.dx /= 1.1
            self.dy /= 1.1

        self.x -= self.dx*speed
        self.y -= self.dy*speed

        self.angle = 360-math.atan2(self.targetY - self.y, self.targetX - self.x)*180/math.pi
        self.rect.center = [self.x, self.y]
        super(Zombie, self).update(screenWidth, screenHeight, 60, 60)

    def resetTarget(self, tx, ty):
        self.targetX = tx
        self.targetY = ty

    def hit(self, damage, game):
        self.health -= damage
        if self.health <= 0:
            Zombie.count -= 1
            powerUpSpawn = random.randint(0, 20)
            if powerUpSpawn <= 2:
                game.powerUps.add(HealthUp(self.x, self.y))
            elif powerUpSpawn == 3:
                game.powerUps.add(Nuke(self.x, self.y))
            elif powerUpSpawn == 4:
                game.powerUps.add(Freeze(self.x, self.y))
            self.kill()

            return True
        return False

class BombZombie(Zombie):
    def __init__(self, x, y, health, speed, tx = 400, ty = 300):
        self.health = health
        self.speed = speed
        Zombie.count += 1
        self.targetX = tx
        self.targetY = ty

        self.angle = 360-math.atan2(self.targetY - y, self.targetX - x)*180/math.pi
        self.x = x
        self.y = y
        self.lastHitTime = 1000
        self.dx = 0
        self.dy = 0
        super(Zombie, self).__init__(x, y, Zombie.bombZombie, 30)

        self.rect = self.image.get_rect()
        self.timeOnScreen = 0
        self.targetTime = 0


class miniZombie(Zombie):
    def __init__(self, x, y, health, speed, tx = 400, ty = 300):
        self.health = health
        self.speed = speed
        Zombie.count += 1
        self.targetX = tx
        self.targetY = ty

        self.angle = 360-math.atan2(self.targetY - y, self.targetX - x)*180/math.pi
        self.x = x
        self.y = y
        self.lastHitTime = 1000
        self.dx = 0
        self.dy = 0
        super(Zombie, self).__init__(x, y, Zombie.miniZombie, 30)

        self.rect = self.image.get_rect()
        self.timeOnScreen = 0
        self.targetTime = 0

class tankZombie(Zombie):
    def __init__(self, x, y, health, speed, tx = 400, ty = 300):
        self.health = health
        self.speed = speed
        Zombie.count += 1
        self.targetX = tx
        self.targetY = ty

        self.angle = 360-math.atan2(self.targetY - y, self.targetX - x)*180/math.pi
        self.x = x
        self.y = y
        self.lastHitTime = 1000
        self.dx = 0
        self.dy = 0
        super(Zombie, self).__init__(x, y, Zombie.tankZombie, 30)

        self.rect = self.image.get_rect()
        self.timeOnScreen = 0
        self.targetTime = 0
