#!/usr/bin/env python
import sys
import pygame
import random
import time


pygame.mixer.pre_init(44100,16,2,4096)

class Pola(pygame.sprite.Sprite):
    def __init__(self):
        super(Pola, self).__init__()
    def draw(self):
        window.blit(self.img, (self.rect.x, self.rect.y))


class TopGround(Pola):
    def __init__(self):
        super(TopGround, self).__init__()
        self.img = pygame.image.load("TopGround.png")
        self.rect = self.img.get_rect()
        self.rect.x = 0
        self.rect.y = 60
        self.mask = pygame.mask.from_surface(self.img)

class Rzeka (Pola):
    def __init__(self):
        super(Rzeka, self).__init__()
        self.img = pygame.image.load("rzeka.png")
        self.rect = self.img.get_rect()
        self.rect.x = 0
        self.rect.y = 120
        self.mask = pygame.mask.from_surface(self.img)


class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, img, direction):
        super(Car, self).__init__()
        self.speed=speed
        self.go_left = direction
        self.img = pygame.image.load(img)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self):
        if self.go_left:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

        if self.rect.x > 600:
            self.rect.x = -40
        elif self.rect.x < -180:
            self.rect.x = 600

        window.blit(self.img, (self.rect.x, self.rect.y))


class Log(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, img, direction):
        super(Log, self).__init__()
        self.speed=speed
        self.go_left = direction
        self.img = pygame.image.load(img)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self):
        if self.go_left:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

        if self.rect.x > 600:
            self.rect.x = -140
        elif self.rect.x < -200:
            self.rect.x = 600

        window.blit(self.img, (self.rect.x, self.rect.y))

class Zaba(pygame.sprite.Sprite):
    def __init__(self):
        super(Zaba, self).__init__()
        self.img_forward = pygame.image.load("zaba.png")
        self.img_forward_animation = pygame.image.load("zaba2.png")
        self.img_back = pygame.image.load("zaba_dol.png")
        self.img_back_animation = pygame.image.load("zaba_dol2.png")
        self.img_left = pygame.image.load("zaba_lewo.png")
        self.img_left_animation = pygame.image.load("zaba_lewo2.png")
        self.img_right = pygame.image.load("zaba_prawo.png")
        self.img_right_animation = pygame.image.load("zaba_prawo2.png")
        self.img_death = pygame.image.load("zaba_trup.png")
        self.img_life = pygame.image.load("zaba_zycie.png")
        self.img_win = pygame.image.load("zaba_win.png")
        self.img = self.img_forward
        self.rect = self.img.get_rect()

        with open("highscore.txt", "r") as plik:
            try:
                self.hscore= int(plik.read())
            except:
                self.hscore = 69
        self.lives = 4
        self.rect.x = 280
        self.rect.y = 560
        self.startpos= (self.img, (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.img)
        self.x_wina=0
        self.y_wina=0
        self.ilosc_winow=0
        self.tab_win=[[0 for col in range(2)] for row in range(5)]
        self.count=0

    def draw(self):
        self.mask = pygame.mask.from_surface(self.img)
        self.move()
        self.display_lives()
        self.score()
        self.highscore()
        window.blit(self.img, (self.rect.x, self.rect.y))

    def move(self):
        self.rect.move(self.rect.x, self.rect.y)
        self.rect.clamp_ip(pygame.Rect((0,80), (600, 640)))


    def left(self):
        self.img = self.img_left_animation
        self.rect.x -= 5
        self.draw()
        pygame.display.flip()
        self.img = self.img_left_animation
        self.rect.x -= 5
        self.draw()
        pygame.display.flip()
        self.img=self.img_left
        self.rect.x -=10


    def right(self):
        self.img = self.img_right_animation
        self.rect.x += 5
        self.draw()
        pygame.display.flip()
        self.img = self.img_right_animation
        self.rect.x += 5
        self.draw()
        pygame.display.flip()
        self.img=self.img_right
        self.rect.x += 10


    def forward(self):
        self.img = self.img_forward_animation
        self.rect.y -= 10
        self.draw()
        pygame.display.flip()
        self.img = self.img_forward_animation
        self.rect.y -= 10
        self.draw()
        pygame.display.flip()
        self.img = self.img_forward
        self.rect.y -= 20

    def back(self):
        self.img = self.img_back_animation
        self.rect.y += 10
        self.draw()
        pygame.display.flip()
        self.img = self.img_back_animation
        self.rect.y += 10
        self.draw()
        pygame.display.flip()
        self.img = self.img_back
        self.rect.y += 20

    def display_lives(self):
        x = 2
        y = 36
        for i in range (self.lives):
            window.blit(self.img_life, (x,y))
            x +=22
        for i in range (5):
            if not self.tab_win[i][0] == 0:
                x = self.tab_win[i][0]
                y = self.tab_win[i][1]
                window.blit(self.img_win, (x, y))

    def death(self):
        pygame.mixer.music.load("dad.mp3")
        pygame.mixer.music.play(1)
        self.lives -=1
        self.img = self.img_death
        self.draw()
        pygame.display.flip()
        pygame.time.wait(700)
        self.rect.x = 280
        self.rect.y = 560
        self.img = self.img_forward

    def win(self):
        pygame.display.flip()
        pygame.time.wait(200)
        self.rect.x = 280
        self.rect.y = 560
        self.img = self.img_forward
        self.ilosc_winow+=1
        if self.ilosc_winow > self.hscore:
            with open("highscore.txt", "w") as f:
                f.write(str(self.ilosc_winow))

    def print_win(self):
        window.blit(self.img_win, (self.rect.x, self.rect.y))
        if not self.tab_win[3][0]==0:
            pygame.mixer.music.load("ma_men.mp3")
            pygame.mixer.music.play(1)
        else:
            pygame.mixer.music.load("win.mp3")
            pygame.mixer.music.play(1)
        self.x_wina = self.rect.x
        self.y_wina = self.rect.y
        if self.tab_win[0][0]==0:
            self.tab_win[0][0]=self.x_wina
            self.tab_win[0][1]=self.y_wina
        elif self.tab_win[1][0]==0:
            self.tab_win[1][0]=self.x_wina
            self.tab_win[1][1]=self.y_wina
        elif self.tab_win[2][0]==0:
            self.tab_win[2][0]=self.x_wina
            self.tab_win[2][1]=self.y_wina
        elif self.tab_win[3][0]==0:
            self.tab_win[3][0]=self.x_wina
            self.tab_win[3][1]=self.y_wina
        elif self.tab_win[4][0]==0:
            self.tab_win[4][0]=self.x_wina
            self.tab_win[4][1]=self.y_wina


    def score(self):
        font =pygame.font.Font("emulogic.ttf", 15)
        text = font.render("Score: " + str(self.count), True, (255,255,255))
        window.blit(text,(160, 36))

    def highscore(self):
        font =pygame.font.Font("emulogic.ttf", 15)
        text = font.render("Highcore: " + str(self.hscore), True, (255,255,255))
        window.blit(text,(160, 10))

def wait_for_input():
    # Allow these keys to cancel the loop.
    valid_keys = [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key in valid_keys:
                    # Return to wherever we were called from.
                    return

def pause():
    pause_font = pygame.font.Font("emulogic.ttf", 20)
    pause_label = pause_font.render("PAUSED", 1, (255, 255, 255))
    window.blit(pause_label, (250, 300))
    pygame.display.flip()
    print ("paused")
    pygame.mixer.music.load("tiktak.mp3")
    pygame.mixer.music.play(-1)
    wait_for_input()
    pygame.mixer.music.stop()

def terminate():
    pygame.quit()
    sys.exit()

def game_over():
    gameover_font = pygame.font.Font('emulogic.ttf', 20)
    gameover_label = gameover_font.render("GAME OVER", 1, (255,255,255))
    window.blit(gameover_label, (200,300))
    pygame.display.flip()
    wait_for_input()
    terminate()

def start_screen():
    white = (255,255,255)
    start_font =pygame.font.Font('emulogic.ttf', 20)
    background=pygame.image.load("init_tlo.png")
    background_music = pygame.mixer.Sound("menu_music.ogg")
    background_music.play(-1)
    window.blit(background, (0, 0))
    label1= start_font.render("Press Enter", 1, white)
    label2= start_font.render("    to",1,white)
    label3= start_font.render(" conitinue",1,white)
    label4= start_font.render("Frogger", 1, (142,234,170))
    window.blit(label1, (200,150))
    window.blit(label2, (200,175))
    window.blit(label3, (200,200))
    window.blit(label4, (250,100))

    pygame.display.flip()
    wait_for_input()
    background_music.stop()

def create_floatables():
    floatables = pygame.sprite.Group()
    ys=[120,160,200,240,280]
    x=0
    for i in range (5):
        kloda = Log(x, ys[4], 3, "kloda1.png", True)
        floatables.add(kloda)
        x += 160
    x=40
    for i in range (3):
        kloda2 = Log(x,ys[3], 2, "kloda2.png", False)
        floatables.add(kloda2)
        x += 250
    x=60
    for i in range (2):
        kloda3 = Log(x,ys[1], 1, "kloda3.png", True)
        floatables.add(kloda3)
        x+= 360
    x=80
    for i in range (2):
        zolw1 = Log(x,ys[2], 3, "zolw3_prawa.png", False)
        floatables.add(zolw1)
        x+=350
    x=100
    for i in range (3):
        zolw2 = Log(x,ys[0], 3.5, "zolw2_lewa.png", True)
        floatables.add(zolw2)
        x+=200
    x=120

    srodek=Log(0,320,0,"srodkowabela.png", True)
    floatables.add(srodek)


    return floatables

def create_hostiles(level):
    hostiles = pygame.sprite.Group()
    ys = [520, 480, 440, 400, 360]
    x = random.randrange(200)
    speed1 = 2
    for _ in range(4):
        car = Car(x, ys[0], 2, "osobowe.png", True)
        hostiles.add(car)
        x += 150
    x = random.randrange(200)
    for _ in range(3):
        car = Car(x, ys[1], 3, "osobowe2.png", False)
        hostiles.add(car)
        x += 200
    x = random.randrange(200)
    for _ in range(2):
        car = Car(x, ys[2], 8, "racer.png", True)
        hostiles.add(car)
        x += 400
    x = random.randrange(200)
    for _ in range(3):
        car = Car(x, ys[3], 2, "osobowe_prawo.png", False)
        hostiles.add(car)
        x += 200
    x = random.randrange(200)
    for _ in range(2):
        car1 = Car(x, ys[4], 4*level+1, "truck.png", True)
        hostiles.add(car1)
        x += 400

    return hostiles

def create_deathzones():
    deathzones = pygame.sprite.Group()

    topground = TopGround()
    deathzones.add(topground)
    river = Rzeka()
    deathzones.add(river)

    return deathzones


def main():
    count=0
    level=0
    start_screen()
    clock = pygame.time.Clock()
    background = pygame.image.load("tlo.png")
    zaba=Zaba()
    hostiles=create_hostiles(level)
    floatables = create_floatables()
    deathzones = create_deathzones()
    background_music = pygame.mixer.Sound("Daab_Podzielono_swiat.ogg")
    background_music.play(-1)
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(zaba.rect.x, zaba.rect.y)
                if event.key == pygame.K_ESCAPE:
                    pause()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    pygame.mixer.music.load("pyp.mp3")
                    pygame.mixer.music.play(1)
                    zaba.left()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    pygame.mixer.music.load("pyp.mp3")
                    pygame.mixer.music.play(1)
                    zaba.right()
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    pygame.mixer.music.load("pyp.mp3")
                    pygame.mixer.music.play(1)
                    zaba.forward()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    pygame.mixer.music.load("pyp.mp3")
                    pygame.mixer.music.play(1)
                    zaba.back()

        window.blit(background, (0,0))

        font = pygame.font.Font("emulogic.ttf", 15)
        text = font.render("Zycia:", True, (255, 255, 255))
        window.blit(text, (3, 10))


        for i in deathzones:
            i.draw()

        for i in floatables:
            i.draw()

        zaba.draw()

        for i in hostiles:
            i.draw()

        if pygame.sprite.spritecollide(zaba, hostiles, False, pygame.sprite.collide_mask):
            zaba.death()

        for i in pygame.sprite.spritecollide(zaba, floatables, False):
            if i.go_left:
                zaba.rect.x -= i.speed
            else:
                zaba.rect.x += i.speed

        if zaba.rect.x<=0 and (zaba.rect.y==120 or zaba.rect.y==160 or zaba.rect.y==200 or zaba.rect.y==240 or zaba.rect.y==280):
            zaba.death()
        if zaba.rect.x>=560 and (zaba.rect.y==120 or zaba.rect.y==160 or zaba.rect.y==200 or zaba.rect.y==240 or zaba.rect.y==280):
            zaba.death()
        if (zaba.rect.y>=120 and zaba.rect.y<=280):
            if not pygame.sprite.spritecollide(zaba, floatables, False, pygame.sprite.collide_rect):
                zaba.death()
        if (zaba.rect.y==80):
            if (zaba.rect.x<28 or (zaba.rect.x>43 and zaba.rect.x<147) or (zaba.rect.x>167 and zaba.rect.x<268) or (zaba.rect.x>280 and zaba.rect.x<389) or(zaba.rect.x>400 and zaba.rect.x<510) or (zaba.rect.x>529) or (zaba.rect.x >=zaba.tab_win[0][0]-10 and zaba.rect.x <=zaba.tab_win[0][0]+10)or (zaba.rect.x >=zaba.tab_win[1][0]-10 and zaba.rect.x <=zaba.tab_win[1][0]+10)or (zaba.rect.x >=zaba.tab_win[2][0]-10 and zaba.rect.x <=zaba.tab_win[2][0]+10)or (zaba.rect.x >=zaba.tab_win[3][0]-10 and zaba.rect.x <=zaba.tab_win[3][0]+10)):
                zaba.death()

            else:
                zaba.print_win()
                zaba.win()
                zaba.count+=1
                count+=1

        if not zaba.lives:
            game_over()


        if (zaba.ilosc_winow%5==0):
            zaba.tab_win=[[0 for col in range(2)] for row in range(5)]
            level+=1


        timer=int(time.clock())
        font = pygame.font.Font("emulogic.ttf", 15)
        text = font.render("Time in game:", True, (255, 255, 255))
        window.blit(text, (400, 10))
        text=font.render(" " + str(timer), True, (255,255,255))
        window.blit(text, (400, 36))

        clock.tick(30)

        pygame.display.update()


pygame.init()
pygame.display.set_caption('Frogger')
window = pygame.display.set_mode((600, 600), 0, 32)
main()
pygame.quit()
quit()