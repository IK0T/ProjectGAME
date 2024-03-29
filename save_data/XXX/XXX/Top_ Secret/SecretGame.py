import pygame
from paddle import Paddle
from ball import Ball

def start():
    pygame.init()

def exit():
    pygame.quit()

def main():
    
    start()
    
    BLACK = (25, 56, 25)
    WHITE = (215, 215, 215)

    size = (700, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("ping_pong")

    paddleA = Paddle(WHITE, 10, 100)
    paddleA.rect.x = 20
    paddleA.rect.y = 200

    paddleB = Paddle(WHITE, 10, 100)
    paddleB.rect.x = 670
    paddleB.rect.y = 200

    ball = Ball(WHITE, 10, 10)
    ball.rect.x = 345
    ball.rect.y = 195

    all_sprites_list = pygame.sprite.Group()

    all_sprites_list.add(paddleA)
    all_sprites_list.add(paddleB)
    all_sprites_list.add(ball)

    clock = pygame.time.Clock()

    scoreA = 0
    scoreB = 0

    carryOn = True
    while carryOn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  carryOn = False

            elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_x:
                         carryOn=False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            paddleA.moveUp(5)

        if keys[pygame.K_s]:
            paddleA.moveDown(5)

        if keys[pygame.K_UP]:
            paddleB.moveUp(5)

        if keys[pygame.K_DOWN]:
            paddleB.moveDown(5)    
 
        all_sprites_list.update()

        if ball.rect.x>=690:
            scoreA+=1
            ball.velocity[0] = -ball.velocity[0]
        elif ball.rect.x<=0:
            scoreB+=1
            ball.velocity[0] = -ball.velocity[0]
        elif ball.rect.y>490:
            ball.velocity[1] = -ball.velocity[1]
        elif ball.rect.y<0:
            ball.velocity[1] = -ball.velocity[1]     

        if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
          ball.bounce()
          hitsound = pygame.mixer.Sound("Sound/Sound_hit.wav")
          hitsound.play()

        screen.fill(BLACK)
        pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)

        all_sprites_list.draw(screen) 

        font = pygame.font.Font(None, 74)

        text = font.render(str(scoreA), 1, WHITE)
        screen.blit(text, (250,10))

        text = font.render(str(scoreB), 1, WHITE)
        screen.blit(text, (420,10))

        pygame.display.flip()
        clock.tick(60)
        
    exit()
    
if __name__ == "__main__":
    main()
