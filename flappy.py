import pygame, random
from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 10 # VELOCIDADE INICIAL DO PÁSSARO. Para ele ir caindo com o tempo.
GRAVITY = 1
GAME_SPEED = 10 # GAME_SPEED = Define tanto a velocidade do 'chão' como dos 'canos'

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 200

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #Pra classe realizar operação de contrução do sprite internamente; Para inicializar

        self.images = [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
                       pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()]

        self.speed = SPEED
        
        self.current_image = 0 # a cada update vai gerar a proxima imagem do bird. Começando com a imagem 0
        
        self.image = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()  # convert_alpha = Faz o programa entender os pixels transparentes
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect() #rect = retângulo = tupla com 4 informações. as 2 primeiras dizem onde está a imagem, as outras 2 dizem o tamanho.
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

        self.speed += GRAVITY

        #Update Height
        self.rect[1] += self.speed

    def bump(self): # Para o Bird ir para cima
        self.speed = - SPEED # Para ele subir

class Pipe(pygame.sprite.Sprite):

    def __init__(self,inverted,xpos,ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/sprites/pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)

        else:
            self.rect[1] = SCREEN_HEIGHT - ysize    

        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):

    def __init__(self,xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED # rect[0] = x . GAME_SPEED = Define tanto a velocidade do 'chão' como dos 'canos'

def is_off_screen(sprite): # Para verificar se sprite está fora da tela.
    return sprite.rect[0] < - (sprite.rect[2])# Para ver se a posição x é menor que menos o tamanho dele.

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT)) # Irá tranformar o tamanho da imagem usada para background no tamanho da tela. Para que possa preencher toda a tela .

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()
while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit() 


        if event.type == KEYDOWN: #Quando apertar alguma tecla
            if event.key == K_SPACE: # Se a tecla for 'espaço'
                bird.bump() # O pássaro faz 'bump', pula...

    screen.blit(BACKGROUND, (0,0)) #Para a imagem de fundo ficar aparecendo a toda atualização. Além disso passa uma tupla (0,0) informando a posição da tela que o canto superior esquerdo da imagem vai ficar. Para ficar no início..

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])   
        pipe_group.remove(pipe_group.sprites()[0]) #cano invertido

        pipes = get_random_pipes(SCREEN_WIDTH * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen) #Desenhar todo mundo que está no grupo de bird..
    ground_group.draw(screen)
    pipe_group.draw(screen)

    pygame.display.update()

    if pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask): #collide_mask = coloca em todos os pixels do sprite que são transparente e coloca '0' e os que tem alguma cor '1' 
        #Game Over
        input()
        break
