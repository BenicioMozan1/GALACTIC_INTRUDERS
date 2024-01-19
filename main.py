import pygame
import random
pygame.init()

FPS = 60

BLACK = (0, 0, 0)
WHITE = (220, 220, 220)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
BLUE = (63, 72, 204)

FONT = pygame.font.Font(None, 40)

PLAYER_WIDTH, PLAYER_HEIGHT = 40, 10
BASE_WIDTH, BASE_HEIGHT = 400, 80
EXPLOSION_RADIUS = 8
EXPLOSION_MAX_RADIUS = 30
WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Intruders")

class Player():
    COLOR = WHITE
    VEL = 5

    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.explosions = []
        self.last_explosion_time = 0

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))
        for explosion in self.explosions:
            explosion.draw(win)

    def move(self, left=True):
        if left and self.x - self.VEL >= 0:  
            self.x -= self.VEL
        elif not left and self.x + self.width + self.VEL <= WIDTH: 
            self.x += self.VEL

    def move_up_down(self, up=True):
        if up and self.y - self.VEL >= 0:  
            self.y -= self.VEL
        elif not up and self.y + self.height + self.VEL <= HEIGHT - BASE_HEIGHT:  
            self.y += self.VEL
            
    def reset(self):
        self.x, self.y = self.original_x, self.original_y
        self.explosions = []

    def explode(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_explosion_time > 800:
            new_explosion = Explosion(self.x + self.width // 2, self.y + self.height // 2, EXPLOSION_RADIUS, EXPLOSION_MAX_RADIUS)
            self.explosions.append(new_explosion)
            self.last_explosion_time = current_time

class Base():
    COLOR = BLUE

    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

class Explosion():
    def __init__(self, x, y, initial_radius, max_radius):
        self.x, self.y = x, y
        self.initial_radius, self.current_radius, self.max_radius = initial_radius, initial_radius, max_radius
        self.color = RED
        self.duration = 120

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), int(self.current_radius))

    def update(self):
        if self.current_radius < self.max_radius:
            self.current_radius += (self.max_radius - self.initial_radius) / self.duration
        elif self.duration > 0:
            self.current_radius -= self.max_radius / self.duration
        self.duration -= 1

    def is_complete(self):
        return self.duration <= 0

class Missile():
    def __init__(self, x, y, cor, velocidade):
        self.x, self.y = x, y
        self.width, self.height = 10, 10 
        self.color = cor
        self.velocidade = velocidade
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def move(self, down=True):
        self.y += self.velocidade if down else 0
        self.rect.y = self.y  
   
velocidades_por_cor = {
    YELLOW: 0.7,
    GREEN: 1,
    ORANGE: 1.3,
    RED: 1.5
}     
HORDA_CONFIG = {
    1: {'cores': [GREEN, YELLOW], 'chances': [0.5, 0.5]},
    3: {'cores': [GREEN, YELLOW, ORANGE], 'chances': [0.5, 0.3, 0.2]},
    5: {'cores': [GREEN, YELLOW, ORANGE], 'chances': [0.4, 0.2, 0.4]},
    7: {'cores': [GREEN, YELLOW, ORANGE, RED], 'chances': [0.3, 0.2, 0.3, 0.2]},
    9: {'cores': [GREEN, ORANGE, RED], 'chances': [0.3, 0.3, 0.4]},
    11: {'cores': [GREEN, ORANGE, RED], 'chances': [0.2, 0.5, 0.3]},
    13: {'cores': [GREEN, ORANGE, RED], 'chances': [0.2, 0.4, 0.4]},
    15: {'cores': [GREEN, ORANGE, RED], 'chances': [0.3, 0.3, 0.4]},
    17: {'cores': [GREEN, ORANGE, RED], 'chances': [0.1, 0.4, 0.5]},
    19: {'cores': [GREEN, ORANGE, RED], 'chances': [0.1, 0.3, 0.6]},
}

def generate_horda(horda):
    missiles = []
    for _ in range(horda):
        horda_config = HORDA_CONFIG[max(k for k in HORDA_CONFIG.keys() if k <= horda)]
        cor = random.choices(horda_config['cores'], weights=horda_config['chances'], k=1)[0]
        velocidade = velocidades_por_cor[cor]
        missiles.append(Missile(random.randint(0, WIDTH), 0, cor, velocidade))
    return missiles

def generate_missile(cor):
    x = random.randint(0, WIDTH - 10)
    y = 0
    velocidade = velocidades_por_cor[cor]
    return Missile(x, y, cor, velocidade)

def draw_missiles(win, missiles):
    for missile in missiles:
        missile.draw(win)
        missile.move()

def draw_player(win, player):
    player.draw(win)

def draw_base(win, base):
    base.draw(win)
    
def draw_game_over(win):
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, (255, 255, 255))
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    font = pygame.font.Font(None, 36)
    text = font.render("Pressione R para reiniciar", True, (255, 255, 255))
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + text.get_height()))


    
def check_collision_missile_explosion(missiles, explosions):
    for missile in missiles:
        for explosion in explosions:
            dist = ((missile.x - explosion.x)**2 + (missile.y - explosion.y)**2)**0.5
            if dist <= explosion.current_radius:
                return missile
    return None

def check_collision_missile_base(missiles, base):
    for missile in missiles:
        if missile.x < base.x + base.width and missile.x + missile.width > base.x and missile.y < base.y + base.height and missile.y + missile.height > base.y:
            return True
    return False

pontos_por_cor = {
    YELLOW: 1,
    GREEN: 3,
    ORANGE: 5,
    RED: 7
}
def movement(keys, player):
    player.move(left=keys[pygame.K_a])
    player.move(left=not keys[pygame.K_d])
    player.move_up_down(up=keys[pygame.K_w])
    player.move_up_down(up=not keys[pygame.K_s])
    if keys[pygame.K_SPACE]:
        player.explode()
    
def draw_score(win, score):
    font = pygame.font.Font(None, 36)  
    text = font.render(f"Points: {score}", True, (255, 255, 255))  
    win.blit(text, (WIDTH - text.get_width() - 10, 10))  

vida = 100
dano_por_cor = {
    YELLOW: 1,
    GREEN: 2,
    ORANGE: 3,
    RED: 5
}

def draw_life(win, vida):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Vida: {vida}", True, (255, 255, 255))
    win.blit(text, (10, 10))


def main():
    game_loop = True
    clock = pygame.time.Clock()
    horda = 1
    player = Player(WIDTH // 2, HEIGHT - 125, PLAYER_WIDTH, PLAYER_HEIGHT)
    base = Base((WIDTH - BASE_WIDTH) // 2, HEIGHT - BASE_HEIGHT, BASE_WIDTH, BASE_HEIGHT)
    vida = 100
    missiles = []
    pontuacao = 0 
    ultimo_spawn = pygame.time.get_ticks()
    intervalo_spawn = 1000  

    while game_loop:
        clock.tick(FPS)

        SCREEN.fill(BLACK)
        draw_base(SCREEN, base)
        draw_player(SCREEN, player)
        draw_missiles(SCREEN, missiles)
        draw_score(SCREEN, pontuacao)
        draw_life(SCREEN, vida) 
        
        pygame.display.update()
        if vida <= 0:
            draw_game_over(SCREEN)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_loop = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main() 
                        return
        else:
            missile_colisao = check_collision_missile_explosion(missiles, player.explosions)
            if missile_colisao:
                pontuacao += pontos_por_cor[missile_colisao.color]
                missiles.remove(missile_colisao)
            
            current_time = pygame.time.get_ticks()
            if current_time - ultimo_spawn >= intervalo_spawn:
                if len(missiles) == 0 and horda <= 20:
                    horda += 1
                    print(f'Horda {horda}')
                missiles.extend(generate_horda(1))
                ultimo_spawn = current_time
                    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_loop = False

            for explosion in player.explosions:
                explosion.update()
                if explosion.is_complete():
                    player.explosions.remove(explosion)

            for missile in missiles:
                if base.rect.colliderect(missile.rect):  
                    vida -= dano_por_cor[missile.color]  
                    missiles.remove(missile)

            keys = pygame.key.get_pressed()
            movement(keys, player)

        if len(missiles) == 0 and horda <= 20:
            horda += 1
            print(f'Horda {horda}')
            
    pygame.quit()

if __name__ == '__main__':
    main()