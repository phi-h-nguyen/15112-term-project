"""
SUVIVIO 0.5: ZOMBIES
15-112 Fall 2019 Term Project
Phi Henry Nguyen

-Images from https://www.freepik.com/
-PySroll/Pytmx code from https://github.com/bitcraft/pyscroll
-Map created with Tiled (https://www.mapeditor.org/)
 and images from https://craftpix.net/freebies/free-battle-location-top-down-game-tileset-pack-1/
-music from https://www.youtube.com/watch?v=XZFclikgn1o
"""

from imports import *

#configuration variables, helps with loading images/files
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'Images')

RESOURCES_DIR = 'Images'
MAP_FILENAME = 'map.tmx'

pygame.font.init()
statFont = pygame.font.SysFont("ebrima", 25)
startFont = pygame.font.SysFont("ebrima", 35)
shopFont = pygame.font.SysFont("ebrima", 20)
gameOverFont = pygame.font.SysFont("ebrima", 40)

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

def init_screen(width, height):
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    return screen

# make loading maps a little easier, from pyscroll
def get_map(filename):
    return os.path.join(data_dir, filename)

def helpScreen(screen):
    help = True

    backButton = False
    while help:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #click
                x,y = ((event.pos))
                if (15 < x < 120) and (15 < y < 70):
                    gameIntro(screen)
                    help = False

            elif (event.type == pygame.MOUSEMOTION and event.buttons == (0, 0, 0)): #motion
                x,y = ((event.pos))
                if (15 < x < 120) and (15 < y < 70):
                    backButton = True

                else:
                    backButton = False

        startImage, rect = load_image("help.png")
        screen.blit(startImage, (0,0))
        if backButton == True:
            pygame.draw.rect(screen, (0, 150, 0), (15, 15, 105, 52), 0)
            startText = startFont.render("Back", False, (0,0,0))
            screen.blit(startText, (30, 16))

        pygame.display.update()

###################################################################################

def gameIntro(screen):
    intro = True
    nextMode = None
    loaded = False
    startButton, loadButton, howButton = False, False, False
    weapons, round, points, regen, kills, health = None, None, None, None, None, None
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #click
                x,y = ((event.pos))

                if (280 < x < 390) and (290 < y < 360):
                    intro = False
                    nextMode = "Game"
                elif (407 < x < 520) and (290 < y < 360):
                    f = open("save.txt", "r+")
                    content = str(f.read()).split("\n")
                    weapons = dict()
                    zombies = dict()
                    for i in range(6):
                        line = content[i].split()
                        weapons[line[0]] = int(line[1])
                    for i in range(4):
                        line = content[6+i].split()
                        zombies[line[0]] = int(line[1])
                    round = int(content[10])
                    points = int(content[11])
                    regen = int(content[12])
                    kills = int(content[13])
                    health = int(content[14])
                    loaded = True
                    intro = False
                    nextMode = "Game"

                elif (280 < x < 520) and (375 < y < 450):
                    intro = False
                    nextMode = "How"

            elif (event.type == pygame.MOUSEMOTION and event.buttons == (0, 0, 0)): #motion
                x,y = ((event.pos))
                if (280 < x < 390) and (290 < y < 360):
                    startButton = True
                    howButton = False
                    loadButton = False

                elif (407 < x < 520) and (290 < y < 360):
                    startButton = False
                    howButton = False
                    loadButton = True

                elif (280 < x < 520) and (375 < y < 450):
                    howButton = True
                    startButton = False
                    loadButton = False

                else:
                    startButton, loadButton, howButton = False, False, False

        startImage, rect = load_image("start.png")
        screen.blit(startImage, (0,0))
        if startButton == True:
            pygame.draw.rect(screen, (0, 150, 0), (280, 287, 111, 75), 0)
            startText = startFont.render("Start", False, (0,0,0))
            screen.blit(startText, (300, 300))
        elif loadButton == True:
            pygame.draw.rect(screen, (0, 150, 0), (407, 287, 111, 75), 0)
            startText = startFont.render("Load", False, (0,0,0))
            screen.blit(startText, (427, 300))

        elif howButton == True:
            pygame.draw.rect(screen, (0, 150, 0), (280, 375, 240, 75), 0)
            startText = startFont.render("How to Play", False, (0,0,0))
            screen.blit(startText, (310, 387))

        pygame.display.update()

    if nextMode == "Game":
        game = Game()
        if loaded == True:
            game.init(weapons, round, points, regen, kills, zombies, health)
        else:
            game.init()
        game.run()

    if nextMode == "How":
        helpScreen(screen)

######################################################

def shopMode(game, screen):
    shop = True
    nextMode = None
    backButton, pistol, rifle, shotgun, sniper, submachine, health, exitButton = False, False, False, False, False, False, False, False

    while shop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #click
                x,y = ((event.pos))
                if (15 < x < 120) and (15 < y < 70):
                    shop = False
                    game.paused = False

                elif (682 < x < 787) and (15 < y < 70):
                    f = open("save.txt", "w+")
                    for item in game.weaponLevels:
                        f.write(item + " " + str(game.weaponLevels[item]))
                        f.write("\n")
                    for item in game.zombieScores:
                        f.write(item + " " + str(game.zombieScores[item]))
                        f.write("\n")
                    f.write(str(game.round) + "\n")
                    f.write(str(game.points) + "\n")
                    f.write(str(game.regen) + "\n")
                    f.write(str(game.kills) + "\n")
                    f.write(str(game.player.health) + "\n")
                    f.close()
                    print("saved")

                elif (50 < x < 115) and (170 < y < 200):
                    price = 1500 + (game.weaponLevels["pistol"] - 1) * 250
                    if game.points >= price:
                        game.weaponLevels["pistol"] += 1
                        game.points -= price

                elif (90 < x < 155) and (315 < y < 345):
                    price = 2000 + (game.weaponLevels["rifle"]) * 250
                    if game.points >= price:
                        if "rifle" not in game.inventory:
                            game.inventory.append("rifle")
                            game.weaponLevels["rifle"] = 1
                        else:
                            game.weaponLevels["rifle"] += 1
                        game.points -= price

                elif (130 < x < 190) and (480 < y < 510):
                    price = 2000 + (game.weaponLevels["sniper"]) * 250
                    if game.points >= price:
                        if "sniper" not in game.inventory:
                            game.inventory.append("sniper")
                            game.weaponLevels["sniper"] = 1
                        else:
                            game.weaponLevels["sniper"] += 1
                        game.points -= price

                elif (480 < x < 540) and (160 < y < 190):
                    price = 2000 + (game.weaponLevels["shotgun"]) * 250
                    if game.points >= price:
                        if "shotgun" not in game.inventory:
                            game.inventory.append("shotgun")
                            game.weaponLevels["shotgun"] = 1
                        else:
                            game.weaponLevels["shotgun"] += 1
                        game.points -= price

                elif (480 < x < 540) and (315 < y < 345):
                    price = 2000 + (game.weaponLevels["submachine"]) * 250
                    if game.points >= price:
                        if "submachine" not in game.inventory:
                            game.inventory.append("submachine")
                            game.weaponLevels["submachine"] = 1
                        else:
                            game.weaponLevels["submachine"] += 1
                        game.points -= price

                elif (540 < x < 600) and (480 < y < 510):
                    if game.regen == 0 and game.points >= 5000:
                        game.regen = 1
                        game.points -= 5000


            elif (event.type == pygame.MOUSEMOTION and event.buttons == (0, 0, 0)): #motion
                x,y = ((event.pos))

                if (15 < x < 120) and (15 < y < 70):
                    backButton = True

                elif (682 < x < 787) and (15 < y < 70):
                    exitButton = True

                elif (40 < x < 130) and (150 < y < 220):
                    pistol = True

                elif (40 < x < 265) and (300 < y < 360):
                    rifle = True

                elif (45 < x < 310) and (480 < y < 530):
                    sniper = True

                elif (450 < x < 580) and (155 < y < 205):
                    shotgun = True

                elif (450 < x < 595) and (310 < y < 380):
                    submachine = True

                elif (510 < x < 620) and (460 < y < 560):
                    health = True

                else:
                    backButton, pistol, rifle, shotgun, sniper, submachine, health, exitButton = False, False, False, False, False, False, False, False

            elif event.type == pygame.KEYDOWN:
                if event.key == 32:
                    shop = False
                    game.paused = False

        shopImage, rect = load_image("shop.png")
        screen.blit(shopImage, (0,0))

        #weapon levels
        gun = "pistol"
        startText = shopFont.render(f"Level {(game.weaponLevels[gun])+1}", False, (0,0,0))
        screen.blit(startText, (130,  118))

        gun = "rifle"
        startText = shopFont.render(f"Level {(game.weaponLevels[gun])+1}", False, (0,0,0))
        screen.blit(startText, (211,  267))

        gun = "sniper"
        startText = shopFont.render(f"Level {(game.weaponLevels[gun])+1}", False, (0,0,0))
        screen.blit(startText, (147,  442))

        gun = "shotgun"
        startText = shopFont.render(f"Level {(game.weaponLevels[gun])+1}", False, (0,0,0))
        screen.blit(startText, (560,  120))

        gun = "submachine"
        startText = shopFont.render(f"Level {(game.weaponLevels[gun])+1}", False, (0,0,0))
        screen.blit(startText, (600,  272))

        startText = shopFont.render(f"Points: {game.points}", False, (0,0,0))
        screen.blit(startText, (13,  70))

        #ADD BUY/UPGRADE BUTTONS

        if backButton == True:
            pygame.draw.rect(screen, (0, 150, 0), (15, 15, 105, 52), 0)
            startText = startFont.render("Back", False, (0,0,0))
            screen.blit(startText, (30, 16))

        elif exitButton == True:
            pygame.draw.rect(screen, (0, 150, 0), (682, 15, 105, 52), 0)
            startText = startFont.render("Save", False, (0,0,0))
            screen.blit(startText, (697, 16))

        elif pistol == True:
            price = 1500 + (game.weaponLevels["pistol"] - 1) * 250
            pygame.draw.rect(screen, (0, 150, 0), (50, 170, 65, 30), 0)
            startText = shopFont.render("Buy", False, (0,0,0))
            screen.blit(startText, (65, 170))
            cost = price


        elif rifle == True:
            price = 2000 + (game.weaponLevels["rifle"]) * 250
            pygame.draw.rect(screen, (0, 150, 0), (90, 315, 65, 30), 0)
            startText = shopFont.render("Buy", False, (0,0,0))
            screen.blit(startText, (105, 315))
            cost = price


        elif sniper == True:
            price = 2000 + (game.weaponLevels["sniper"]) * 250
            pygame.draw.rect(screen, (0, 150, 0), (130, 480, 65, 30), 0)
            startText = shopFont.render("Buy", False, (0,0,0))
            screen.blit(startText, (145, 480))
            cost = price


        elif shotgun == True:
            price = 2000 + (game.weaponLevels["shotgun"]) * 250
            pygame.draw.rect(screen, (0, 150, 0), (480, 160, 65, 30), 0)
            startText = shopFont.render("Buy", False, (0,0,0))
            screen.blit(startText, (495, 160))
            cost = price


        elif submachine == True:
            price = 2000 + (game.weaponLevels["submachine"]) * 250
            pygame.draw.rect(screen, (0, 150, 0), (480, 315, 65, 30), 0)
            startText = shopFont.render("Buy", False, (0,0,0))
            screen.blit(startText, (495, 315))
            cost = price

        elif health == True:
            pygame.draw.rect(screen, (0, 150, 0), (540, 480, 65, 30), 0)
            startText = shopFont.render("Buy", False, (0,0,0))
            screen.blit(startText, (555, 480))
            if game.regen == 1:
                cost = "bought"
            else:
                cost = 5000

        else:
            cost = None

        if cost == "bought":
            startText = shopFont.render("In inventory", False, (0,0,0))
            text_rect = startText.get_rect(center=(400, 560))
            screen.blit(startText, (text_rect))
        elif cost != None and game.points < cost:
            startText = shopFont.render(f"Not enough points ({cost})", False, (0,0,0))
            text_rect = startText.get_rect(center=(400, 560))
            screen.blit(startText, (text_rect))
        elif cost != None:
            startText = shopFont.render(f"Cost: {cost}", False, (0,0,0))
            text_rect = startText.get_rect(center=(400, 560))
            screen.blit(startText, (text_rect))

        pygame.display.update()

#########################################################


"""
Modified Pygame framework created by Lukas Peraza
for 15-112 F15 Pygame Optional Lecture, 11/11/15
http://blog.lukasperaza.com/getting-started-with-pygame/
"""
class Game(object):
    filename = get_map(MAP_FILENAME)

    #procedurally chooses which zombies to spawn
    #based on the user's playing
    def getRoundStats(self):
        #numZombies, Health, list of zombies to be spawned
        total = 0
        for item in self.zombieScores:
            total += self.zombieScores[item]

        numZombies = 8 + 4*(self.round - 1)
        health = 50 + 15*(self.round - 1)

        minZombies = int(numZombies/6)

        n =  max(minZombies, int((self.zombieScores["normal"]/total) * numZombies))
        b =  max(minZombies, int((self.zombieScores["bomb"]/total) * numZombies))
        m =  max(minZombies, int((self.zombieScores["mini"]/total) * numZombies))
        t = max(minZombies, int((self.zombieScores["tank"]/total) * numZombies))

        numNormal = ["n"] * n
        numBomb = ["b"] * b
        numMini = ["m"] * m
        numTank = ["t"] * t

        zombies = numNormal + numBomb + numMini + numTank

        while len(zombies) > numZombies:
            if b >= n and b >= m and b >= t:
                zombies.remove("b")
            elif m >= b and m >= n and m >= t:
                zombies.remove("m")
            elif t >= b and t >= b and t >= n:
                zombies.remove("t")
            else:
                zombies.remove("n")

            n = zombies.count("n")
            b = zombies.count("b")
            m = zombies.count("m")
            t = zombies.count("t")


        while len(zombies) < numZombies:
            if b <= n and b <= m and b <= t:
                zombies.append("b")
            elif m <= b and m <= n and m <= t:
                zombies.append("m")
            elif t <= b and t <= b and t <= n:
                zombies.append("t")
            else:
                zombies.append("n")
            n = zombies.count("n")
            b = zombies.count("b")
            m = zombies.count("m")
            t = zombies.count("t")

        random.shuffle(zombies)
        return numZombies, health, zombies

    def init(self, weapons = False, round = 1, points = 0, regen = 0, kills = 0, zombies = False, health = 100):
        screen = init_screen(800, 600)
        self.midCoordinates = 800//2, 600//2
        Zombie.count = 0
        self.paused = False
        self.gameOver = False
        # load data from pytmx
        tmx_data = load_pygame(self.filename)
        self.freezeImage, self.freezeRect = load_image('snow.png', -1)
        self.freezeImage = pygame.transform.rotate(pygame.transform.scale(self.freezeImage.convert_alpha(), (60, 60)), 0)

        # setup level geometry with simple pygame rects, loaded from pytmx
        self.walls = list()
        for object in tmx_data.objects:
            self.walls.append(pygame.Rect(
                object.x, object.y,
                object.width, object.height))

        # create new data source for pyscroll
        map_data = pyscroll.data.TiledMapData(tmx_data)

        self.map_layer = pyscroll.BufferedRenderer(map_data, screen.get_size(), clamp_camera=False, tall_sprites=1)
        self.zoom = 1
        self.map_layer.zoom = self.zoom

        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=2)

        Player.init()
        Friend.init()
        Zombie.init()
        PowerUp.init()
        self.player = Player(1600, 1600)
        self.player.health = health
        self.friendAI = Friend(200, 200)

        self.player.position = self.map_layer.map_rect.center
        self.group.add(self.player)
        self.regen = regen

        self.bullets = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        self.bombZombies = pygame.sprite.Group()
        self.barrels = pygame.sprite.Group()
        self.fragments = pygame.sprite.Group()
        self.powerUps = pygame.sprite.Group()
        self.friend = pygame.sprite.Group()
        self.friend.add(self.friendAI)
        self.fBullets = pygame.sprite.Group()
        self.melee = pygame.sprite.Group()

        self.hits = {"normal" : 0,
                     "bomb": 0,
                     "mini": 0,
                     "tank": 0 }

        self.zombieTimes = {"normal" : 0,
                               "bomb": 0,
                               "mini": 0,
                               "tank": 0 }

        if zombies == False:
            self.zombieScores = {"normal" : 1,
                                   "bomb": 1,
                                   "mini": 1,
                                   "tank": 1 }
        else:
            self.zombieScores = zombies

        self.kills = kills
        self.points = points
        self.weaponsList = [ "pistol", "rifle", "shotgun", "sniper", "submachine"]
        self.inventory = [ "pistol"]

        # Weapon : (spread, size, shotDelay, range, speed, shots, color)
        self.gunStats =  {"rifle": (1, 8, 1, 700, 1.5, 1, (0,0,0)),
                        "shotgun": (2, 4, 30, 300, 1, 10, (0,0,0)),
                         "pistol": (0, 6, 25, 600, 1, 1, (0,0,0)),
                     "submachine": (2, 6, 1, 500, 1, 2, (0,0,0)),
                         "sniper": (0, 12, 50, 1000, 2, 1, (0,0,0)),
                          "melee": (0, 20, 30, 50, .5, 1, (0,162,232)),
                          "ai-gun": (0, 6, 25, 600, 1, 1, (0,0,100))}

        self.gunDamage = {"rifle": 20,
                        "shotgun": 12,
                         "pistol": 15,
                     "submachine": 10,
                         "sniper": 100,
                         "melee": 50,
                         "ai-gun": 5}

        self.gunMaxAmmo = {"rifle": 25,
                        "shotgun": 6,
                         "pistol": 12,
                     "submachine": 45,
                         "sniper": 5,
                         "melee": None,
                         "ai-gun": None}

        self.gunAmmo = {"rifle": 25,
                        "shotgun": 6,
                         "pistol": 12,
                     "submachine": 45,
                         "sniper": 5,
                         "melee": None,
                         "ai-gun": None}

        self.weaponPoints = {"rifle": 10,
                           "shotgun": 2,
                            "pistol": 10,
                        "submachine": 5,
                            "sniper": 15,
                             "melee": 25,
                            "ai-gun": 2}

        if weapons == False:
            self.weaponLevels = {"rifle": 0,
                               "shotgun": 0,
                                "pistol": 1,
                            "submachine": 0,
                                "sniper": 0,
                                "ai-gun": 1}
        else:
            self.weaponLevels = weapons
            for weapon in self.weaponLevels:
                if self.weaponLevels[weapon] != 0 and weapon not in self.inventory and weapon != "ai-gun":
                    self.inventory.append(weapon)

        self.round = round
        self.spawnedZombies = 0
        self.numZombies, self.zombieHealth, self.zombieList = self.getRoundStats()

        self.zombieDict = {"normal": self.zombieList.count("n"),
                           "bomb": self.zombieList.count("b"),
                           "mini": self.zombieList.count("m"),
                           "tank": self.zombieList.count("t")}

        for gun in self.gunStats:
            spread, size, delay, _range, speed, shots, color = self.gunStats[gun]
            self.gunStats[gun] = spread, int(size*self.zoom), delay, (_range*self.zoom), (speed*self.zoom), shots, color

        self.weaponIndex = 0
        self.weapon = self.inventory[self.weaponIndex]
        self.lastShotTime = 1000
        self.freezeTime = 0
        self.freeze = False
        self.nukeTime = 0
        self.reloadTime = 0
        self.reloading = False
        self.roundTime = 400
        self.hitTime = 0
        self.scrollX = 0
        self.scrollY = 0
        self.clock = 0

        for i in range(100):
            x = random.randint(-1600, 1600)
            y = random.randint(-1600, 1600)
            self.barrels.add(Barrel(200+x, 200+y, self))

    #shoot
    def mousePressed(self, x, y):
        if self.gameOver == False:
            spread, size, delay, _range, speed, shots, color = self.gunStats[self.weapon]

            if self.lastShotTime > delay and self.gunAmmo[self.weapon] > 0 and self.reloading == False:

                for i in range(shots):
                    self.bullets.add(Bullet(x, y, self.width, self.height, self.midCoordinates, spread, size, _range, speed, color))
                    self.lastShotTime = 0

                self.gunAmmo[self.weapon] -= 1
            elif self.gunAmmo[self.weapon] <= 0 and self.reloading == False:
                self.reloading = True
                self.reloadTime = 100
                self.gunAmmo[self.weapon] = self.gunMaxAmmo[self.weapon]

        #go back to home screen
        if self.gameOver == True:
            print("GAME OVER")
            self.playing == False
            screen = pygame.display.set_mode((800, 600))
            gameIntro(screen)

    def mouseReleased(self, x, y):
        if self.gameOver == False:
            spread, size, delay, _range, speed, shots, color = self.gunStats[self.weapon]
            if (self.weapon == "rifle" or self.weapon == "submachine") and self.lastShotTime > delay and self.gunAmmo[self.weapon] > 0 and self.reloading == False:
                for i in range(shots):
                    self.bullets.add(Bullet(x, y, self.width, self.height, self.midCoordinates, spread, size, _range, speed, color))
                    self.lastShotTime = 0
                self.gunAmmo[self.weapon] -= 1

    #change weapons
    def otherMousePressed(self, event, x, y):
        if self.gameOver == False:
            if event == 4 and self.reloading == False:
                self.weaponIndex += 1
                self.weapon = self.inventory[self.weaponIndex % len(self.inventory)]
                self.lastShotTime = 1000
                self.player.changePic(self.weapon)
            elif event == 5 and self.reloading == False:
                self.weaponIndex -= 1
                self.weapon = self.inventory[self.weaponIndex % len(self.inventory)]
                self.lastShotTime = 1000
                self.player.changePic(self.weapon)
            elif event == 6 and self.reloading == False:
                spread, size, delay, _range, speed, shots, color = self.gunStats["melee"]
                if self.lastShotTime > delay:
                    self.melee.add(Bullet(x, y, self.width, self.height, self.midCoordinates, spread, size, _range, speed, color))
                    self.lastShotTime = 0
            else:
                self.powerUps.add(HealthUp(x, y))

    #aim player
    def mouseMotion(self, x, y):
        if self.gameOver == False:
            self.group.update(self.width, self.height, self.isKeyPressed, self.midCoordinates, x, y)

    def mouseDrag(self, x, y):
        if self.gameOver == False:
            self.group.update(self.width, self.height, self.isKeyPressed, self.midCoordinates, x, y)

    def keyPressed(self, keyCode, modifier):
        if self.gameOver == False:
            if keyCode == 32: #space bar to go to shop
                self.paused = not self.paused
                shopMode(self, self.screen)
            elif keyCode == 114 and self.reloading == False: #reload with r
                self.reloading = True
                self.reloadTime = 100
                self.gunAmmo[self.weapon] = self.gunMaxAmmo[self.weapon]
            elif keyCode == 13:
                self.points += 1000

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        self.lastShotTime += 1
        self.clock += 1
        self.freezeTime -= 1
        self.nukeTime -= 1
        self.reloadTime -= 1
        self.hitTime -= 1
        self.roundTime -= 1
        if self.freezeTime > 0:
            self.freeze = True
        else:
            self.freeze = False

        if self.reloadTime > 0:
            self.reloading = True
        else:
            self.reloading = False

        #move player
        velocity = self.player.update(self.width, self.height, self.isKeyPressed, self.midCoordinates)
        scrollX, scrollY = velocity[0], velocity[1]
        velocity = self.checkPlayerCollision()
        if velocity != None:
            scrollX -= velocity[0]
            scrollY -= velocity[1]

        distance = 100000
        aimX = 0
        aimY = 0

        """
        quadrants:  1   2
                    3   4
        To keep the ai in the quadrant with least # of zombies
        """

        quads = {"quad1": 0,
                 "quad2": 0,
                 "quad3": 0,
                 "quad4": 0}
        target = "quad1"

        for zombie in self.zombies:
            #move zombies
            zombie.x += scrollX
            zombie.y += scrollY

            if (0 < zombie.x < 400) and (0 < zombie.y < 300):
                quads["quad1"] += 1
            elif (400 < zombie.x < 800) and (0 < zombie.y < 300):
                quads["quad2"] += 1
            elif (0 < zombie.x < 400) and (300 < zombie.y < 600):
                quads["quad3"] += 1
            elif (400 < zombie.x < 800) and (300 < zombie.y < 600):
                quads["quad4"] += 1

            #get closest zombie coordinates
            temp = math.sqrt( (400 - zombie.x)**2 + (300 - zombie.y)**2)
            if temp < distance:
                aimX = zombie.x
                aimY = zombie.y
                distance = temp

            if zombie.targetX != 400 and zombie.targetY != 300:
                zombie.targetX += scrollX
                zombie.targetY += scrollY
            zombie.lastHitTime += 1
            zombie.timeOnScreen += 1
            zombie.targetTime += 1
            if zombie.timeOnScreen > 800:
                zombie.resetTarget(Zombie.CX, Zombie.CY)

        for zombie in self.bombZombies:
            #move zombies
            zombie.x += scrollX
            zombie.y += scrollY

            if (0 < zombie.x < 400) and (0 < zombie.y < 300):
                quads["quad1"] += 1
            elif (400 < zombie.x < 800) and (0 < zombie.y < 300):
                quads["quad2"] += 1
            elif (0 < zombie.x < 400) and (300 < zombie.y < 600):
                quads["quad3"] += 1
            elif (400 < zombie.x < 800) and (300 < zombie.y < 600):
                quads["quad4"] += 1

            #get closest zombie coordinates
            temp = math.sqrt( (400 - zombie.x)**2 + (300 - zombie.y)**2)
            if temp < distance:
                aimX = zombie.x
                aimY = zombie.y
                distance = temp

            if zombie.targetX != 400 and zombie.targetY != 300:
                zombie.targetX += scrollX
                zombie.targetY += scrollY
            zombie.lastHitTime += 1
            zombie.timeOnScreen += 1
            zombie.targetTime += 1
            if zombie.targetTime > 800:
                zombie.resetTarget(Zombie.CX, Zombie.CY)

        target = max(quads, key=quads.get)


        for friend in self.friend:
            friend.x += scrollX
            friend.y += scrollY

        for barrel in self.barrels:
            barrel.x += scrollX
            barrel.y += scrollY

        for powerUp in self.powerUps:
            powerUp.x += scrollX
            powerUp.y += scrollY


        temp = set()
        for location in PowerUp.locations:
            x, y = location
            temp.add((x+scrollX, y+scrollY))
        PowerUp.locations = temp

        self.checkHit()

        #health regen
        if self.clock%100 == 0:
            if self.player.health < 100:
                self.player.health += self.regen

        #ai shooting
        if self.clock%20 == 0 and (0 < aimX < 800) and (0 < aimY < 600):
            spread, size, delay, _range, speed, shots, color = self.gunStats["ai-gun"]
            if self.player.health < 30:
                coordinates = (self.player.x, self.player.y)
            else:
                coordinates = (self.friendAI.x, self.friendAI.y)
            self.fBullets.add(Bullet(aimX, aimY, self.width, self.height, coordinates, spread, size, _range, speed, color))

        #spawn zombies
        if self.clock%50 == 0 and len(self.zombieList) > 0 and self.roundTime < 0:
            rand1 = random.randint(0, 600)
            rand2 = random.randint(0, 800)
            coordinates = random.choice([(1200, rand1), (rand2, -400), (-400, rand1), (rand2, 1200)])
            willGetPowerUp = random.randint(0, 3)
            zombieType = self.zombieList.pop()
            x, y = coordinates
            #randomly guard power ups
            if len(PowerUp.locations) > 0 and willGetPowerUp == 2:
                i, j = random.choice(list(PowerUp.locations))
                if zombieType == "b":
                    self.bombZombies.add(BombZombie(x, y, 0.8 * self.zombieHealth, 2, i, j))
                elif zombieType == "m":
                    self.zombies.add(miniZombie(x, y, 0.5 * self.zombieHealth, 4, i, j))
                elif zombieType == "t":
                    self.zombies.add(tankZombie(x, y, 3 * self.zombieHealth, 1.5, i, j))
                else:
                    self.zombies.add(Zombie(x, y, self.zombieHealth, 2, i, j))
            else:
                if zombieType == "b":
                    self.bombZombies.add(BombZombie(x, y, self.zombieHealth, 2))
                elif zombieType == "m":
                    self.zombies.add(miniZombie(x, y, 0.5 * self.zombieHealth, 4))
                elif zombieType == "t":
                    self.zombies.add(tankZombie(x, y, 3 * self.zombieHealth, 1.5))
                else:
                    self.zombies.add(Zombie(x, y, 0.8 * self.zombieHealth, 2))


            if self.clock%100:
                for zombie in self.zombies:
                    willGetPowerUp = random.randint(0, 3)
                    if len(PowerUp.locations) > 0 and willGetPowerUp == 2:
                        i, j = random.choice(list(PowerUp.locations))
                        zombie.targetTime = 0
                        zombie.resetTarget(i, j)
                for zombie in self.bombZombies:
                    willGetPowerUp = random.randint(0, 3)
                    if len(PowerUp.locations) > 0 and willGetPowerUp == 2:
                        i, j = random.choice(list(PowerUp.locations))
                        zombie.targetTime = 0
                        zombie.resetTarget(i, j)

        #incriment rounds
        elif len(self.zombieList) == 0 and Zombie.count == 0:
            for zombieType in self.zombieScores:
                self.zombieScores[zombieType] = int(math.sqrt(self.zombieTimes[zombieType]) * 2**(self.hits[zombieType])) // self.zombieDict[zombieType]

            self.round += 1
            self.numZombies, self.zombieHealth, self.zombieList = self.getRoundStats()

            self.zombieDict = {"normal": self.zombieList.count("n"),
                           "bomb": self.zombieList.count("b"),
                           "mini": self.zombieList.count("m"),
                           "tank": self.zombieList.count("t")}

            self.spawnedZombies = 0
            PowerUp.locations = set()
            self.roundTime = 400


        self.bullets.update(self.width, self.height, self.isKeyPressed, self.walls)
        self.fBullets.update(self.width, self.height, self.isKeyPressed, self.walls)
        self.melee.update(self.width, self.height, self.isKeyPressed, self.walls)
        self.zombies.update(self.width, self.height, self.walls, self.clock, self.freeze)
        self.bombZombies.update(self.width, self.height, self.walls, self.clock, self.freeze)
        self.barrels.update(self.width, self.height)
        self.fragments.update(self.width, self.height, self.isKeyPressed, self.walls)
        self.powerUps.update(self.width, self.height)
        self.friend.update(self.width, self.height, self.clock, aimX, aimY, target)


    #keep player in bounds
    def checkPlayerCollision(self):
        for sprite in self.group.sprites():
            if sprite.rect.collidelist(self.walls) > -1:
                return sprite.moveBack()

    #explode barrel
    def barrelExplode(self, barrel, melee = False):
        if melee == True:
            damage = self.gunDamage["melee"]
        else:
            damage = self.gunDamage[self.weapon] * (1.1**self.weaponLevels[self.weapon])


        if barrel.hit(damage):
            for i in range(15):
                midCoordinates = (barrel.x, barrel.y)
                x, y = 0,0
                while x == 0 and y == 0:
                    x = random.randint(-10, 10)
                    y = random.randint(-10, 10)
                size = random.randint(5,12)
                self.fragments.add(Bullet(barrel.x + x, barrel.y + y, self.width, self.height, midCoordinates, 0, size, 500, 1.5, (150, 0, 0)))

    #kill zombie
    def zombieKill(self, zombie):
        self.points += 30
        self.kills += 1
        if isinstance(zombie, BombZombie):
            self.zombieTimes["bomb"] += zombie.timeOnScreen
        elif isinstance(zombie, miniZombie):
            self.zombieTimes["mini"] += zombie.timeOnScreen
        elif isinstance(zombie, tankZombie):
            self.zombieTimes["tank"] += zombie.timeOnScreen
        else:
            self.zombieTimes["normal"] += zombie.timeOnScreen
        zombie.kill()

    def checkHit(self):

        damage = self.gunDamage[self.weapon] * (1.1**self.weaponLevels[self.weapon])

        #shooting zombies
        for zombie in pygame.sprite.groupcollide(self.zombies, self.bullets, False, True, pygame.sprite.collide_circle):
            self.points += self.weaponPoints[self.weapon]
            if zombie.hit(damage, self):
                self.zombieKill(zombie)

        #shooting bomb zombies
        for zombie in pygame.sprite.groupcollide(self.bombZombies, self.bullets, False, True, pygame.sprite.collide_circle):
            self.points += self.weaponPoints[self.weapon]
            if zombie.hit(damage, self):
                self.zombieKill(zombie)
                for i in range(10):
                    midCoordinates = (zombie.x, zombie.y)
                    x, y = 0,0
                    while x == 0 and y == 0:
                        x = random.randint(-10, 10)
                        y = random.randint(-10, 10)
                    size = random.randint(5,9)
                    self.fragments.add(Bullet(zombie.x + x, zombie.y + y, self.width, self.height, midCoordinates, 0, size, 500, 1, (100, 0, 0)))

        #punching bomb zombies
        for zombie in pygame.sprite.groupcollide(self.bombZombies, self.melee, False, False, pygame.sprite.collide_circle):
            self.points += self.weaponPoints["melee"]
            if zombie.hit(self.gunDamage["melee"], self):
                self.zombieKill(zombie)
                for i in range(10):
                    midCoordinates = (zombie.x, zombie.y)
                    x, y = 0,0
                    while x == 0 and y == 0:
                        x = random.randint(-10, 10)
                        y = random.randint(-10, 10)
                    size = random.randint(5,9)
                    self.fragments.add(Bullet(zombie.x + x, zombie.y + y, self.width, self.height, midCoordinates, 0, size, 500, 1, (100, 0, 0)))


        #punching zombies
        for zombie in pygame.sprite.groupcollide(self.zombies, self.melee, False, False, pygame.sprite.collide_circle):
            self.points += self.weaponPoints["melee"]
            if zombie.hit(self.gunDamage["melee"], self):
                 self.zombieKill(zombie)

        #ai shooting zombies
        for zombie in pygame.sprite.groupcollide(self.zombies, self.fBullets, False, True, pygame.sprite.collide_circle):
            self.points += self.weaponPoints["ai-gun"]
            if zombie.hit(self.gunDamage["ai-gun"], self):
                self.zombieKill(zombie)

        #ai shootinng bomb zombies
        for zombie in pygame.sprite.groupcollide(self.bombZombies, self.fBullets, False, True, pygame.sprite.collide_circle):
            self.points += self.weaponPoints["ai-gun"]
            if zombie.hit(self.gunDamage["ai-gun"], self):
                self.zombieKill(zombie)
                for i in range(10):
                    midCoordinates = (zombie.x, zombie.y)
                    x, y = 0,0
                    while x == 0 and y == 0:
                        x = random.randint(-10, 10)
                        y = random.randint(-10, 10)
                    size = random.randint(5,9)
                    self.fragments.add(Bullet(zombie.x + x, zombie.y + y, self.width, self.height, midCoordinates, 0, size, 500, 1, (100, 0, 0)))


        #shooting barrels
        for barrel in pygame.sprite.groupcollide(self.barrels, self.bullets, False, True, pygame.sprite.collide_circle):
            self.barrelExplode(barrel)

        #punching barrels
        for barrel in pygame.sprite.groupcollide(self.barrels, self.melee, False, False, pygame.sprite.collide_circle):
            self.barrelExplode(barrel, True)

        #ai shooting barrels
        for barrel in pygame.sprite.groupcollide(self.barrels, self.fBullets, False, True, pygame.sprite.collide_circle):
            self.barrelExplode(barrel)

        #zombies hit by barrels
        for zombie in pygame.sprite.groupcollide(self.zombies, self.fragments, False, True, pygame.sprite.collide_circle):
            self.points += 5
            if zombie.hit(25, self):
                self.zombieKill(zombie)

        #bomb zombies hit by barrels
        for zombie in pygame.sprite.groupcollide(self.bombZombies, self.fragments, False, True, pygame.sprite.collide_circle):
            self.points += 5
            if zombie.hit(25, self):
                self.zombieKill(zombie)
                for i in range(10):
                    midCoordinates = (zombie.x, zombie.y)
                    x, y = 0,0
                    while x == 0 and y == 0:
                        x = random.randint(-10, 10)
                        y = random.randint(-10, 10)
                    size = random.randint(5,9)
                    self.fragments.add(Bullet(zombie.x + x, zombie.y + y, self.width, self.height, midCoordinates, 0, size, 500, 1, (100, 0, 0)))

        #powerups
        for powerUp in self.powerUps:
            if (380 < powerUp.x < 420 and 280 < powerUp.y < 320):
                #health
                if isinstance(powerUp, HealthUp):
                    self.player.health = min(100, self.player.health + 15)
                    if (int(powerUp.x), int(powerUp.y)) in PowerUp.locations:
                        PowerUp.locations.remove( (int(powerUp.x), int(powerUp.y)) )
                    powerUp.kill()


                #nuke
                elif isinstance(powerUp, Nuke):
                    self.nukeTime = 10
                    for zombie in self.zombies:
                        if (0 < zombie.x < 800) and (0 < zombie.y < 600):
                            if zombie.hit(10000, self):
                                self.points += 30
                                self.kills += 1
                    for zombie in self.bombZombies:
                        if (0 < zombie.x < 800) and (0 < zombie.y < 600):
                            if zombie.hit(10000, self):
                                self.points += 30
                                self.kills += 1
                    self.points += 200

                    if (int(powerUp.x), int(powerUp.y)) in PowerUp.locations:
                        PowerUp.locations.remove( (int(powerUp.x), int(powerUp.y)) )
                    powerUp.kill()

                #freeze
                if isinstance(powerUp, Freeze):
                    self.freeze = True
                    self.freezeTime = max(300, self.freezeTime+300)

                    if (int(powerUp.x), int(powerUp.y)) in PowerUp.locations:
                        PowerUp.locations.remove( (int(powerUp.x), int(powerUp.y)) )
                    powerUp.kill()

            #delete powerups after a certain time
            powerUp.timeOnScreen += 1
            if powerUp.timeOnScreen > 1000:
                if (int(powerUp.x), int(powerUp.y)) in PowerUp.locations:
                    PowerUp.locations.remove( (int(powerUp.x), int(powerUp.y)) )
                powerUp.kill()

        #player hit by zombie
        for zombie in self.zombies:
            if (380 < zombie.x < 420 and 280 < zombie.y < 320) and zombie.lastHitTime > 30:
                zombie.lastHitTime = 0
                self.hitTime = 50
                if self.player.hit(10):
                    self.paused = True
                    self.gameOver = True

                if isinstance(zombie, BombZombie):
                    self.hits["bomb"] += 1
                elif isinstance(zombie, miniZombie):
                    self.hits["mini"] += 1
                elif isinstance(zombie, tankZombie):
                    self.hits["tank"] += 1
                else:
                    self.hits["normal"] += 1

        #player hit by fragments
        for fragment in self.fragments:
            if (370 < fragment.x < 430 and 270 < fragment.y < 330):
                self.hitTime = 50
                if self.player.hit(5):
                    self.paused = True
                    self.gameOver = True
                self.hits["bomb"] += .05
                fragment.kill()


    def drawStats(self, screen):
        #Health Bar:
        pygame.draw.rect(screen, (255, 0, 0), (200, 500, 400, 30), 0)
        width = max(0, int((self.player.health / 100) * 400))
        pygame.draw.rect(screen, (0, 255, 0), (200, 500, width, 30), 0)
        pygame.draw.rect(screen, (0, 0, 0), (200, 500, 400, 30), 5)

        #Weapon:
        weaponText = statFont.render(f"Weapon: {self.weapon.capitalize()} (Level {self.weaponLevels[self.weapon]})", False, (0,0,0))
        text_rect = weaponText.get_rect(center=(400, 560))
        screen.blit(weaponText, (text_rect))

        #Round/Number of Zombies
        zombieText = statFont.render(f"Zombies: {Zombie.count}", False, (0,0,0))
        screen.blit(zombieText, (10, 10))
        killsText = statFont.render(f"Kills: {self.kills}", False, (0,0,0))
        screen.blit(killsText, (10, 40))
        pointsText = statFont.render(f"Points: {self.points}", False, (0,0,0))
        screen.blit(pointsText, (10, 70))
        roundText = statFont.render(f"Round: {self.round}", False, (0,0,0))
        screen.blit(roundText, (10, 100))

        #weapon ammo
        if self.gunAmmo[self.weapon] <= 0:
            reloadText = statFont.render(f"Reload!", False, (0,0,0))
            text_rect = reloadText.get_rect(center=(400, 480))
            screen.blit(reloadText, (text_rect))
        elif self.reloading == True:
            if self.reloadTime > 75:
                reloadText = statFont.render(f"Reloading.", False, (0,0,0))
            elif self.reloadTime > 50:
                reloadText = statFont.render(f"Reloading..", False, (0,0,0))
            else:
                reloadText = statFont.render(f"Reloading...", False, (0,0,0))
            text_rect = reloadText.get_rect(center=(400, 480))
            screen.blit(reloadText, (text_rect))
        else:
            ammoText = statFont.render(f"{self.gunAmmo[self.weapon]} / {self.gunMaxAmmo[self.weapon]}", False, (0,0,0))
            text_rect = ammoText.get_rect(center=(400, 480))
            screen.blit(ammoText, (text_rect))



    def drawGameOver(self, screen):
        pygame.draw.rect(self.screenFlash, (0, 0, 0, 150), (0, 0, 800, 600))
        screen.blit(self.screenFlash, (0,0))

        gameOverText = gameOverFont.render(f"Game Over!", False, (255, 255, 255))
        text_rect = gameOverText.get_rect(center=(400, 50))
        screen.blit(gameOverText, (text_rect))

        messageText = startFont.render(f"Press anywhere to return Home", False, (255, 255, 255))
        text_rect = messageText.get_rect(center=(400, 150))
        screen.blit(messageText, (text_rect))

        messageText = statFont.render(f"{self.kills} Kills", False, (255, 255, 255))
        text_rect = messageText.get_rect(center=(400, 250))
        screen.blit(messageText, (text_rect))

        messageText = statFont.render(f"Round {self.round}", False, (255, 255, 255))
        text_rect = messageText.get_rect(center=(400, 285))
        screen.blit(messageText, (text_rect))

    def redrawAll(self, screen):
        self.group.center(self.player.rect.center)
        self.group.draw(screen)
        self.friend.draw(screen)
        self.powerUps.draw(screen)

        self.bullets.draw(screen)
        self.fragments.draw(screen)
        self.fBullets.draw(screen)

        self.zombies.draw(screen)
        self.bombZombies.draw(screen)
        self.barrels.draw(screen)
        self.melee.draw(screen)
        self.drawStats(screen)

        if self.gameOver == False:
            if self.hitTime > 0:
                if self.clock%5 == 0:
                    pygame.draw.rect(self.screenFlash, (250, 0, 0, 80), (0, 0, 800, 600))
                    screen.blit(self.screenFlash, (0,0))

            elif self.player.health < 20:
                if self.clock%15 == 0:
                    pygame.draw.rect(self.screenFlash, (250, 0, 0, 50), (0, 0, 800, 600))
                    screen.blit(self.screenFlash, (0,0))

            if self.freezeTime > 0:
                if self.freezeTime > 300:
                    temp = 300
                else:
                    temp = self.freezeTime
                trans = 15 + int(temp/10)
                pygame.draw.rect(self.screenFlash, (0, 0, 255, trans), (0, 0, 800, 600))
                screen.blit(self.screenFlash, (0,0))

            if self.nukeTime > 0:
                trans = int(self.nukeTime * 25)
                pygame.draw.rect(self.screenFlash, (255, 255, 150, trans), (0, 0, 800, 600))
                screen.blit(self.screenFlash, (0,0))

            if self.freeze == True:
                screen.blit(self.freezeImage, (10,140))

            if self.roundTime > 0:
                time = self.roundTime//80 + 1

                roundText = statFont.render(f"Round {self.round} starting in {time}...", False, (0,0,0))
                text_rect = roundText.get_rect(center=(400, 200))
                screen.blit(roundText, (text_rect))

        #GAME OVER SCREEN
        else:
            self.drawGameOver(screen)

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=800, height=600, fps=100, title="Survio 0.5: Zombies"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        self.screenFlash = pygame.Surface((800, 600), pygame.SRCALPHA)

        pygame.init()

    def run(self):
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.playing = True
        while self.playing:
            if self.paused == False:
                time = clock.tick(self.fps)
                self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mousePressed(*(event.pos))
                    else:
                        self.otherMousePressed(event.button, *(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    intro = False
                    pygame.quit()
            self.screen.fill(self.bgColor)
            self.redrawAll(self.screen)
            pygame.display.flip()
        pygame.quit()

def main():
    pygame.mixer.init()
    pygame.mixer.music.load("soundtrack.mp3")
    pygame.mixer.music.play(-1)

    screen = pygame.display.set_mode((800, 600))
    gameIntro(screen)

if __name__ == '__main__':
    main()
