import pygame
import webbrowser
from math import atan2, degrees
from random import randint
pygame.init()


# variables
wid = 800
hig = 600
phat = __file__[0:len(__file__)-7]
FPS = 60

cwid = wid / 16
chig = hig / 12


# color
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (255,0,0)
BLUE = (0, 0, 255)
PURPLE = (157, 0, 255)


# icon
icon = pygame.image.load(f'{phat}\\img\\icon.png')
pygame.display.set_icon(icon)


# screen
screen = pygame.display.set_mode((wid,hig))
pygame.display.set_caption("MyEpamGame2")


def save(mapp, phat):
    with open(phat, 'w') as f:
        for i in range(len(mapp)):
            world = ''
            for j in range(len(mapp[i])):
                world += str(mapp[i][j])
            world += '\n'
            f.write(world)


def load(phat):
    mapp = []
    with open(phat, 'r') as f:
        for line in f:
            mapp.append([])
            for i in range(len(line)-1):
                mapp[len(mapp)-1].append(int(line[i]))

    return mapp


def loadImg(sheet, imgs, line):
    asset = {}
    sheet = pygame.image.load(f'{phat}\\img\\{sheet}').convert_alpha()
    sheet = pygame.transform.scale(sheet, (500, 150))

    def getImg(sheet, wid, hig, frame, line):
        img = pygame.Surface((wid, hig)).convert_alpha()
        img.blit(sheet, (0, 0), ((frame * wid), (line * hig), wid, hig))
        img.set_colorkey((0,0,0))
        return img

    for i in range(len(imgs)):
        asset.update({imgs[i] : getImg(sheet, 50, 50, i, line)})

    return asset


#load img
items = ['barrier', 'dore1', 'dore2', 'flore', 'dore3', 'dore4', 'wall', 'bullet', 'reaktor', 'oil']
asset = loadImg('assets.png', items, 0)

lod = ['playerP', 'playerB', 'playerY', 'playerR', 'playerPI','enemy','shild']
characters = loadImg('assets.png', lod, 1)

helt = []
for i in range(10):
    helt.append(str(i+1))
hp_bar = loadImg('assets.png', helt, 2)


# load mapps
menu_bg = load(phat + 'mapp\\menu.txt')


def paint(mapp):
    mouse =  pygame.mouse.get_pos()
    j = int(mouse[0] // (cwid))
    i = int(mouse[1] // (chig))
  
    mapp[i][j] += 1
    if mapp[i][j] > len(items)-2:
        mapp[i][j] = 0

    return mapp


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 1
        self.y = 6
        self.skin = 0
        self.image = pygame.Surface((cwid, chig))
        self.image.blit(characters[lod[self.skin]], (0,0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(center = (self.x * cwid + (cwid / 2), self.y * chig + (chig / 2)))
        self.right = True
        self.left = True
        self.lastShot = 0
        # upgrade
        self.money = 0
        self.shootSpeed = 30
        self.shild = False


    def draw(self):
        screen.blit(characters[lod[self.skin]], (self.x * cwid, self.y * chig))
        if self.shild:
            screen.blit(characters['shild'], (self.x * cwid, self.y * chig))


    def update(self):
        self.rect = self.image.get_rect(center = (self.x * cwid + (cwid / 2), self.y * chig + (chig / 2)))

        if self.lastShot > 0:
            self.lastShot -= 1

        if pygame.sprite.groupcollide(enemyBulletGroupe, playerGroupe, True, False):
            if self.shild:
                self.shild = False
            else:
                game.scen = 'lose'


    def move(self, dir):
        match dir:
            case 'up':
                if game.room[self.y - 1][self.x]  == 3:
                    self.y -= 1
        
            case 'down':
                if game.room[self.y + 1][self.x]  == 3:
                    self.y += 1

            case 'right':
                if game.room[self.y][self.x + 1]  == 3:
                    self.x += 1

            case 'left':
                if game.room[self.y][self.x - 1]  == 3:
                    self.x -= 1

    def shot(self):
        if self.lastShot == 0:
            self.lastShot += self.shootSpeed
            bulletGroupe.add(Bullet(self.x, self.y,'player'))

    

player = Player()

playerGroupe = pygame.sprite.Group()
enemyGroupe = pygame.sprite.Group()
bulletGroupe = pygame.sprite.Group()
enemyBulletGroupe = pygame.sprite.Group()

playerGroupe.add(player)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, owner):
        super().__init__()
        self.x = x
        self.realX = x
        self.y = y 
        self.realY = y
        self.speed = 1 
        self.image = pygame.Surface((cwid, chig))
        self.image.blit(asset['bullet'], (0,0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(center = (-10, -10))
        self.owner = owner

        # bulet dir
        # owner: player
        if self.owner == 'player':
            mouse = pygame.mouse.get_pos()
            mid = [player.x * cwid + 25, player.y * chig + 25]

            angle = atan2(mouse[0] - mid[0], mouse[1] - mid[1])
            angle = int(degrees(angle))
            if angle < 0: 
                angle += 360

        # owner: enemy
        else:
            target = player.x, player.y
            me = self.x, self.y
            angle = atan2(target[0] - me[0], target[1] - me[1])
            angle = int(degrees(angle))
            angle += randint(-50,50)

            if angle < 0: 
                angle += 360

        
        # down
        if 337.5 < angle < 360 or 0 < angle < 22.5:
            self.dir = 'down'
            self.image = pygame.transform.rotate(self.image, -90)

        # down right
        elif 22.5 < angle < 67.5:  
            self.dir = 'down right'
            self.image = pygame.transform.rotate(self.image, -45)

        # right
        elif 67.5 < angle < 112.5:
            self.dir = 'right'

        # up right
        elif 112.5 < angle < 157.5:
            self.dir = 'up right'
            self.image = pygame.transform.rotate(self.image, 45)

        # up
        elif 157.5 < angle < 202.5:
            self.dir = 'up'
            self.image = pygame.transform.rotate(self.image, 90)

        # up left
        elif 202.5 < angle < 247.5:
            self.dir = 'up left'
            self.image = pygame.transform.rotate(self.image, 45)
            self.image = pygame.transform.flip(self.image, True, False)
            

        # left
        elif 247.5 < angle < 292.5:
            self.dir = 'left'
            self.image = pygame.transform.flip(self.image, True, False)

        # down left
        elif 292.5 < angle < 337.5:
            self.dir = 'down left'
            self.image = pygame.transform.rotate(self.image, -45)
            self.image = pygame.transform.flip(self.image, True, False)




    def update(self):
        try:    
            match self.dir:
                case 'right':
                    self.x += 0.2
                    self.realX += 1 / speed
                    self.rect = self.image.get_rect(center = ((self.x  * cwid + (cwid / 2), self.y * chig + (chig / 2))))
                
                case 'left':
                    self.x -= 0.2
                    self.realX -= 1 / speed
                    self.rect = self.image.get_rect(center = ((self.x  * cwid + (cwid / 2), self.y * chig + (chig / 2))))

                case 'up':
                    self.y -= 0.2
                    self.realY -= 1 / speed
                    self.rect = self.image.get_rect(center = ((self.x  * cwid + (cwid / 2), self.y * chig + (chig / 2))))

                case 'down':
                    self.y += 0.2
                    self.realY += 1 / speed
                    self.rect = self.image.get_rect(center = ((self.x  * cwid + (cwid / 2), self.y * chig + (chig / 2))))


                case 'up right':
                    self.y -= 0.1
                    self.x += 0.1
                    self.realY -= 0.5 / speed
                    self.realX += 0.5 / speed
                    self.rect = self.image.get_rect(center = ((self.x  * cwid + (cwid / 2), self.y * chig + (chig / 2))))

                case 'down right':
                    self.y += 0.1
                    self.x += 0.1
                    self.realY += 0.5 / speed
                    self.realX += 0.5 / speed
                    self.rect = self.image.get_rect(center = ((self.x  * cwid + (cwid / 2), self.y * chig + (chig / 2))))
        
                case 'up left':
                    self.y -= 0.1
                    self.x -= 0.1
                    self.realY -= 0.5 / speed
                    self.realX -= 0.5 / speed
                    self.rect = self.image.get_rect(center = ((self.x  * cwid + (cwid / 2), self.y * chig + (chig / 2))))

                case 'down left':
                    self.y += 0.1
                    self.x -= 0.1
                    self.realY += 0.5 / speed
                    self.realX -= 0.5 / speed
                    self.rect = self.image.get_rect(center = ((self.x  * cwid + (cwid / 2), self.y * chig + (chig / 2))))
            
        except:
            pass


        # self kill 
        if 0 >= self.x or self.x >  14:
            self.kill()
        
        if 0 >= self.y or self.y > 10:
            self.kill()

        if game.room[int(self.y)][int(self.x)] != 3 and  game.room[int(self.y)][int(self.x)] != 7:
            self.kill()



def button(x, y, wid, hig, text,size, textx = 0, color = BLUE):
    mouse = pygame.mouse.get_pos()
    mouse = pygame.Rect(mouse[0],mouse[1],1,1) 

    button = pygame.Rect(x,y,wid,hig)
    if button.colliderect(mouse) and color != BLACK:
        pygame.draw.rect(screen, color, pygame.Rect(x-5,y-5,wid+10,hig+10), 5)

    pygame.draw.rect(screen, BLACK, button, 5)
    font = pygame.font.Font(f"{phat}font\\Anton\\Anton-Regular.ttf", size)
    text = font.render(text, True, BLACK)
    screen.blit(text,(x+30-textx,y-4))

    press = False
    if button.colliderect(mouse) and pygame.mouse.get_pressed()[0]:
        press = True

    return press


class Game():
    def __init__(self):
        self.scen = 'menu'
        self.enemyNum = 0
        self.lvl = 1
        self.new = True
        self.rooms = []
        
        global reloadMapp
        def reloadMapp():
            self.rooms.clear()
            for i in range(6):
                self.rooms.append(load(phat + f'mapp\\room{i}.txt'))

            self.room = self.rooms[0]

        reloadMapp()
        


    def menu(self):
        global run
        #display
        screen.fill(WHITE)

        for i in range(len(menu_bg)):
            for j in range(len(menu_bg[i])):
                screen.blit(asset[items[menu_bg[i][j]]], (j * cwid, i * chig))


        player.y = 8
        player.x = 11
        player.draw()

        
        # play    
        if button(100,100,250,150,'PLAY',105):
            player.money = 0
            player.shootSpeed = 30
            player.shild = False
            
            player.x = 1
            player.y = 6
            game.scen = 'game'

            self.new = True
            self.lvl = 1


        if button(100,300,250,50,'GITHUB',38):
            webbrowser.open('https://github.com/MateGames/MyEpamGame2')
        
        if button(100,400,250,50,'QUIT',38):
            run = False

        # skin change
        if button(450,400,50,50,'<',38,10) and player.left:
            player.skin -= 1
            if player.skin < 0:
                player.skin = 0
            player.left = False

        if not button(450,400,50,50,'<',38,10):
            player.left = True
        
        if button(650,400,50,50,'>',38,10) and player.right:
            player.skin += 1
            if player.skin > 4:
                player.skin = 4
            player.right = False
        
        if not button(650,400,50,50,'>',38,10):
            player.right = True


    def game(self, frame):
        #reset/next room shuffle
        if self.new:
            reloadMapp()
            self.room = self.rooms[randint(0,len(self.rooms)-1)]
            bulletGroupe.empty()
            enemyBulletGroupe.empty()

            player.x = 1
            player.y = 6

            # new enemy
            random = [randint(9,14), randint(2,9)] # x,y
            while game.room[random[1]][random[0]] != 3:
                random = [randint(7,14), randint(1,10)]
                print('relocate enemy')
            
            hp = self.lvl
            if hp > 10:
                self.hp = 10
            enemyGroupe.add(Enemy(random[0], random[1], randint(hp - randint(0, int(hp / 4)), hp)))
            self.new = False



        key = pygame.key.get_pressed()
        # save
        #not working
        if key[pygame.K_s] and key[pygame.K_LCTRL] and False:
            save(mapp, phat + 'mapp\\save.txt')


        # shoot
        if key[pygame.K_SPACE]:
            player.shot()


        # player move
        if (key[pygame.K_w] or key[pygame.K_UP]) and (frame / speed) % 1 == 0:
            player.move('up')
        
        if (key[pygame.K_s] or key[pygame.K_DOWN]) and (frame / speed) % 1 == 0:
            player.move('down')

        if (key[pygame.K_a] or key[pygame.K_LEFT]) and (frame / speed) % 1 == 0:
            player.move('left')

        if (key[pygame.K_d] or key[pygame.K_RIGHT]) and (frame / speed) % 1 == 0:
            player.move('right')



        if key[pygame.K_k] and (frame / speed) % 1 == 0:
            if player.skin > 0:
                player.skin -= 1
        if key[pygame.K_l] and (frame / speed) % 1 == 0:
                if player.skin < 4:
                    player.skin += 1


        #display
        screen.fill(WHITE)

        for i in range(len(self.room)):
            for j in range(len(self.room[i])):
                screen.blit(asset[items[self.room[i][j]]], (j * cwid, i * chig))
        
        bulletGroupe.draw(screen)
        bulletGroupe.update()

        enemyBulletGroupe.draw(screen)
        enemyBulletGroupe.update()

        enemyGroupe.draw(screen)
        enemyGroupe.update()

        player.draw()
        player.update()
        

        # line and number
        if False:
            for i in range(len(self.room[0])):
                pygame.draw.line(screen, PURPLE, (i * cwid, 0), (i * cwid, hig), 1)
            for i in range(len(self.room)):
                pygame.draw.line(screen, PURPLE, (0, i * chig), (wid, i * chig), 1)


            font = pygame.font.Font(f"{phat}font\\Anton\\Anton-Regular.ttf", 15)

            for i in range(len(self.room)):
                for j in range(len(self.room[i])):
                    text = font.render(str(self.room[i][j]), True, BLACK)
                    screen.blit(text,(j*50 + 20, i*50))
                    text = font.render(str(items[self.room[i][j]]), True, BLACK)
                    screen.blit(text,(j*50 + 10, i*50 + 20))
            

        #mouse
        mouse =  pygame.mouse.get_pos()
        j = mouse[0] // (cwid)
        i = mouse[1] // (chig)

        pygame.draw.rect(screen, WHITE, (j * cwid, i * chig, cwid, chig), 2)

        if (player.x == 14 and player.y == 6) and self.enemyNum == 0:
            game.scen = 'next'


    def next(self):
        screen.fill(BLACK)

        # genrate bg
        for i in range(len(menu_bg)):
            for j in range(len(menu_bg[i])):
                screen.blit(asset[items[menu_bg[i][j]]], (j * cwid, i * chig))


        # congrat text
        text = f'Congratulations you finished room{self.lvl}!'
        button(100,100,600,50,text,38,0,BLACK)


        # next
        if button(550,450,150,50,'NEXT>',38):
            self.lvl += 1
            self.new = True
            self.scen = 'game'


        # room -> room
        text = f'ROOM{self.lvl} >>> ROOM{self.lvl + 1}'
        button(150,200,300,50,text,38,0,BLACK)


        # coin
        text = f'{player.money} COIN'
        button(500,200,150,50,text,38,5,BLACK)


        # shotspeed lvl up
        num = [4,3,2,1]
        text = f'Faster shot | 10 COIN | LVL {num[int(player.shootSpeed / 10)]}'
        if player.shootSpeed != 10:
            if player.money >= 10:
                if button(100,350,450,50,text,38,0,GREEN):
                    player.money -= 10
                    player.shootSpeed -= 10
            else:
                button(100,350,450,50,text,38,0,RED)
        
        else:
            text = 'Faster shot | LVL 3 (MAX)'
            button(100,350,450,50,text,38,0,BLACK)


        # buy shild
        text = f'Shild | 10 COIN'
        if not player.shild:
            if player.money >= 10:
                if button(100,450,250,50,text,38,0,GREEN):
                    player.money -= 10
                    player.shild = True
            else:
                button(100,450,250,50,text,38,0,RED)
        
        else:
            text = f'You have a shield!'
            button(100,450,350,50,text,38,0,BLACK)


    def lose(self):
        screen.fill(BLACK)

        # genrate bg
        for i in range(len(menu_bg)):
            for j in range(len(menu_bg[i])):
                screen.blit(asset[items[menu_bg[i][j]]], (j * cwid, i * chig))

        
        # congrat text
        text = f'You lost!'
        button(250,100,300,100,text,70,0,BLACK)


        # roomX
        text = f'ROOM{game.lvl}'
        button(200,250,150,50,text,38,0,BLACK)


        # roomX
        text = f'{(game.lvl-1)*5} COIN'
        button(450,250,150,50,text,38,5,BLACK)


        # back to menu
        text = f'MENU'
        if button(300,450,200,50,text,38,-30):
            enemyGroupe.update()
            game.scen = 'menu'
        


game = Game()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, hp):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface((cwid, chig))
        self.image.blit(characters['enemy'], (0,0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(center = (self.x * cwid + (cwid / 2), self.y * chig + (chig / 2)))
        self.hp = hp
        if self.hp > 10:
            self.hp = 10
        self.target = None
        self.fps = None
        game.enemyNum += 1
 

    def update(self):
        self.rect = self.image.get_rect(center = (self.x * cwid + (cwid / 2), self.y * chig + (chig / 2)))

        # get hit
        if pygame.sprite.groupcollide(bulletGroupe, enemyGroupe, True, False):
            self.hp -= 1
            if self.hp <= 0:
                game.room[self.y][self.x] = 3
                game.enemyNum -= 1
                player.money += 5
                self.kill()


        if game.scen == 'lose':
            game.room[self.y][self.x] = 3
            game.enemyNum -= 1
            self.kill()


        # move
        if self.target == None:
            self.fps = 1
            self.target = []

        else:
            self.fps += 1
            if self.fps == 60:
                self.target = []
                if game.room[self.y + 1][self.x] == 3:
                    self.target.append(0)
                if game.room[self.y][self.x + 1] == 3:
                    self.target.append(1)
                if game.room[self.y - 1][self.x] == 3:
                    self.target.append(2)
                if game.room[self.y][self.x - 1] == 3:
                    self.target.append(3)
                # print(self.x,self.y,self.target)

                self.target = self.target[randint(0,(len(self.target)-1))] 
                # print(self.target)

                game.room[self.y][self.x] = 3
                match self.target:
                    case 0:
                        self.y += 1 
                    case 1: 
                        self.x += 1
                    case 2:
                        self.y -= 1
                    case 3:
                        self.x -= 1
                game.room[self.y][self.x] = 7


                self.target = None
        

        # HP
        try:
            screen.blit(hp_bar[str(self.hp)], (self.x  * cwid + (cwid / 2) - 25, self.y * chig + (chig / 2) - 75))
        except:
            pass


        # shoot
        if (self.fps % 60) == 0:
            enemyBulletGroupe.add(Bullet(self.x,self.y, 'enemy'))




# dev settings
frame = 0
speed = 7

key = pygame.key.get_pressed()
def main(screen, frame):
    clock = pygame.time.Clock()
    global run

    run = True        
    while run:
        clock.tick(FPS)
        frame += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
            #click
            click = True
            if event.type == pygame.MOUSEBUTTONDOWN and False:
                if click:
                    mapp = paint(mapp)
                click = False

            if event.type == pygame.MOUSEBUTTONUP:
                click = True


        # key events
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            run = False
            break

        match game.scen:
            case 'game':
                game.game(frame)
            case 'menu':
                game.menu()
            case 'next':
                game.next()
            case 'lose':
                game.lose()


        if frame == 60:
            frame = 0

        #pygame.display.flip()
        pygame.display.update()

if __name__ == '__main__':
    main(screen,frame)




# info
'''
Block:
    img: 50px * 50px
    pixlert: 10px * 10px

'''


# generate mapp
'''
mapp = []
for i in range(9):
    mapp.append([])
    for j in range(12):
        mapp[i].append(0)
'''


# display mapp
'''
for i in range(len(mapp)):
    print(mapp[i])

'''
