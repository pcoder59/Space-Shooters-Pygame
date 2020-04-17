import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Load Assets

#Enemy Ships
RED_SPACE_SHIP = pygame.image.load("assets/pixel_ship_red_small.png")
GREEN_SPACE_SHIP = pygame.image.load("assets/pixel_ship_green_small.png")
BLUE_SPACE_SHIP = pygame.image.load("assets/pixel_ship_blue_small.png")
BLUE_2_SPACE_SHIP = pygame.image.load("assets/pixel_ship_blue_small_2.png")
PURPLE_SPACE_SHIP = pygame.image.load("assets/pixel_ship_purple_small.png")
YELLOW_2_SPACE_SHIP = pygame.image.load("assets/pixel_ship_yellow_small.png")

# Player Ships
YELLOW_PLAYER_SPACE_SHIP = pygame.image.load("assets/pixel_ship_yellow.png")
GREEN_PLAYER_SPACE_SHIP = pygame.image.load("assets/pixel_ship_green.png")

# Lasers

# Enemy Lasers
RED_LASER = pygame.image.load("assets/pixel_laser_red.png")
GREEN_LASER = pygame.image.load("assets/pixel_laser_green.png")
BLUE_LASER = pygame.image.load("assets/pixel_laser_blue.png")
DARK_BLUE_LASER = pygame.image.load("assets/pixel_laser_dark_blue.png")
DARKISH_GREEN_LASER = pygame.image.load("assets/pixel_laser_darkish_green.png")
ORANGE_LASER = pygame.image.load("assets/pixel_laser_orange.png")

# Player Lasers
YELLOW_LASER = pygame.image.load("assets/pixel_laser_yellow.png")
PINK_LASER = pygame.image.load("assets/pixel_laser_pink.png")

# Backgrounds

# Game
BG = pygame.transform.scale(pygame.image.load("assets/background-black.png"), (WIDTH, HEIGHT))

# Main Menu
BG_animated = pygame.transform.scale(pygame.image.load("assets/animated_background.gif"), (WIDTH, HEIGHT))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        
    def move(self, vel):
        self.y += vel
        
    def off_screen(self, height):
        return not(self.y < height and self.y >= 0)
    
    def collision(self, obj):
        return collide(self, obj)

class Ship:
    COOLDOWN = 6
    
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.ship_imag = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        
    def draw(self, window):
        window.blit(self.ship_imag, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
        self.healthbar(window)
        
    def movelasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
        
    def get_width(self):
        return self.ship_imag.get_width()
    
    def get_height(self):
        return self.ship_imag.get_height()
    
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        else:
            self.cool_down_counter += 1
    
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            
    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_imag.get_height() + 10, self.ship_imag.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_imag.get_height() + 10, int(self.ship_imag.get_width() * (self.health/self.max_health)), 10))
    
class Player(Ship):
    def __init__(self, x, y, player_ship, player_laser, health=100):
        super().__init__(x, y, health)
        self.ship_imag = player_ship
        self.laser_img = player_laser
        self.mask = pygame.mask.from_surface(self.ship_imag)
        self.max_health = health
        
    def movelasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        obj.health -= 100
                        if(obj.health) <= 0:
                            objs.remove(obj)

class Enemy(Ship):
    COLOR_MAP = {
        "red": (random.choice([RED_SPACE_SHIP, PURPLE_SPACE_SHIP]), random.choice([RED_LASER, ORANGE_LASER]), 200),
        "green": (random.choice([GREEN_SPACE_SHIP, YELLOW_2_SPACE_SHIP]), random.choice([GREEN_LASER, DARKISH_GREEN_LASER]), 100),
        "blue": (random.choice([BLUE_SPACE_SHIP, BLUE_2_SPACE_SHIP]), random.choice([BLUE_LASER, DARK_BLUE_LASER]), 50)    
    }
    
    def __init__(self, x, y, color, level, health=100):
        super().__init__(x, y, health)
        self.ship_imag, self.laser_img, self.health = self.COLOR_MAP[color]
        self.health = self.health * level/2
        self.max_health = self.health
        self.mask = pygame.mask.from_surface(self.ship_imag)
        
    def move(self, vel):
        self.y += vel
        
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
        
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60
    level = 0
    lives = 4
    main_font = pygame.font.SysFont("comicsans", 50, bold=False, italic=False)
    lost_font = pygame.font.SysFont("comicsans", 60, bold=True, italic=False)
    
    enemies = []
    wave_length = 5
    enemy_vel = 2
    
    player_vel = 5
    laser_vel = 10
    
    player = Player(300, 630, random.choice([YELLOW_PLAYER_SPACE_SHIP, GREEN_PLAYER_SPACE_SHIP]), random.choice([YELLOW_LASER, PINK_LASER]))
    
    clock = pygame.time.Clock()
    
    lost = False
    lost_count = 0
    
    def redraw_window():
        WIN.blit(BG, (0, 0))
        
        #draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 0, 0))
        level_label = main_font.render(f"Level: {level}", 1, (0, 255, 0))
        
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        
        for enemy in enemies:
            enemy.draw(WIN)
        
        player.draw(WIN)
        
        if lost:
            lost_label = lost_font.render("You Lost!", 1, (0, 0, 255))
            WIN.blit(lost_label, (int(WIDTH/2 - lost_label.get_width()/2), 350))
        
        pygame.display.update()
    
    while run:
        clock.tick(FPS)
        redraw_window()
        
        if lives <=0 or player.health <= 0:
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        
        if len(enemies) == 0:
            level += 1
            level_label = lost_font.render(f"Level {level}!", 1, (0, 0, 255))
            WIN.blit(level_label, (int(WIDTH/2 - level_label.get_width()/2), 350))
            pygame.display.update()
            pygame.time.wait(300)
            wave_length += 5
            player_vel += 1
            player.health += 10
            player.max_health += 10
            lives += 1
            player_vel += 1
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]), level)
                enemies.append(enemy)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0: #Left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH: #Right
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0: #Up
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 25 < HEIGHT: #Down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
            
        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.movelasers(laser_vel, player)
            
            if random.randrange(0, 2*FPS) == 1:
                enemy.shoot()
            
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
            
        player.movelasers(-laser_vel, enemies)
                
def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70, bold=True, italic=True)
    
    run = True
    while run:
        WIN.blit(BG_animated, (0, 0))
        title_label = title_font.render("Press Enter key to Begin", 1, (255, 255, 0))
        WIN.blit(title_label, (int(WIDTH/2 - title_label.get_width()/2), 350))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                main()
                
    pygame.quit()
                
main_menu()
