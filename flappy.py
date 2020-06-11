import pygame
from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 10 # VELOCIDADE INICIAL DO PÁSSARO. Para ele ir caindo com o tempo.

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #Pra classe realizar operação de contrução do sprite internamente; Para inicializar

        self.images = [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
                       pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()]

        self.current_image = 0 # a cada update vai gerar a proxima imagem do bird. Começando com a imagem 0
        
        self.image = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()  # convert_alpha = Faz o programa entender os pixels transparentes
        
        self.rect = self.image.get_rect() #rect = retângulo = tupla com 4 informações. as 2 primeiras dizem onde está a imagem, as outras 2 dizem o tamanho.
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

        #Update Height
        self.rect[1] += SPEED


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT)) # Irá tranformar o tamanho da imagem usada para background no tamanho da tela. Para que possa preencher toda a tela .

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)


clock = pygame.time.Clock()
while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit() 

    screen.blit(BACKGROUND, (0,0)) #Para a imagem de fundo ficar aparecendo a toda atualização. Além disso passa uma tupla (0,0) informando a posição da tela que o canto superior esquerdo da imagem vai ficar. Para ficar no início..

    bird_group.update()

    bird_group.draw(screen) #Desenhar todo mundo que está no grupo de bird..

    pygame.display.update()