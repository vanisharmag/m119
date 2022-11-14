# What : Python Pong game implementation 
# Where : https://www.101computing.net/pong-tutorial-using-pygame-getting-started/
# Why : For M4 we neeeded to play the Pong game with our arduino as the controller
#       we were allowed to find the Pong game online and then implement the bluetooth connection part
#       this website was easy to follow along and used pygame which I have seen used before! 

# Import the pygame library and initialise the game engine
import pygame 
from paddle import Paddle
from ball import Ball

def play(ax):

    pygame.init() 

    # Define some colors
    BLACK = ( 0, 0, 0)
    WHITE = ( 255, 255, 255)

    # Open a new window
    size = (700, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pong")
    
    paddle = Paddle(WHITE, 10, 100)
    paddle.rect.x = 670
    paddle.rect.y = 200

    ball = Ball(WHITE,10,10)
    ball.rect.x = 345
    ball.rect.y = 195

    #This will be a list that will contain all the sprites we intend to use in our game.
    all_sprites_list = pygame.sprite.Group()

    # Add the paddles to the list of sprites
    all_sprites_list.add(paddle)
    all_sprites_list.add(ball)

    # The loop will carry on until the user exits the game (e.g. clicks the close button).
    carryOn = True
    
    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()

    #Initialise player scores
    score = 0
    
    # -------- Main Program Loop -----------
    while carryOn:
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                carryOn = False # Flag that we are done so we exit this loop
            elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_x: #Pressing the x Key will quit the game
                        carryOn=False  

        #Moving the paddle with arduino 
        if ax.value >= .1 : # change 
            paddle.moveDown(7) #check direction
        elif ax.value <= -.1 :
            paddle.moveUp(7)
    
        # --- Game logic should go here
        all_sprites_list.update()

        #Check if the ball is bouncing against any of the 4 walls:
        if ball.rect.x>=690:
            ball.velocity[0] = -ball.velocity[0]
            score+=1
        if ball.rect.x<=0:
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.y>490:
            ball.velocity[1] = -ball.velocity[1]
        if ball.rect.y<0:
            ball.velocity[1] = -ball.velocity[1] 

        #Detect collisions between the ball and the paddles
        if pygame.sprite.collide_mask(ball, paddle):
            ball.bounce()

        # --- Drawing code should go here
        # First, clear the screen to black. 
        screen.fill(BLACK)
        #Draw the net
        pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
        
        #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        all_sprites_list.draw(screen) 

        #Display scores:
        font = pygame.font.Font(None, 74)
        text = font.render(str(score), 1, WHITE)
        screen.blit(text, (250,10))
        text = font.render("misses", 1, WHITE)
        screen.blit(text, (420,10))
    
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        
        # --- Limit to 60 frames per second
        clock.tick(60)
    
    #Once we have exited the main program loop we can stop the game engine:
    pygame.quit()