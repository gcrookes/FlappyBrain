import pygame
import random
import os
import sys
import time
from GameSprites import Player, Obstacle
from Backgrounds import TextColumns

from pygame.locals import K_SPACE, K_ESCAPE, KEYDOWN

# Set a fixed window size with global variables
SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 650

def resource_path(relative_path):
    """
    Function to add the path to the file directory onto another relative path.
    The _MEIPASS is a temp folder python makes and is used for compiling the file

    Input Parameters
    ----------------
    relative_path: The path to the file relative to where the python file is located
    
    Returns
    -------
    The full system path to the relative path
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
        
    return os.path.join(base_path, relative_path)


def game():

    # Load all the images to be used for the game.
    player_image = pygame.image.load(resource_path("res\Brain.png"))
    obstacle_image = pygame.image.load(resource_path("res\Pipe.png"))
    floor_image = pygame.image.load(resource_path("res\Floor.png"))
    
    # Initialize game variables
    running = True                                              # If the game loop is running
    columns = 60                                                # The number of text columns in the background
    obstacle_speed = 5                                          # Speed obstacles move across the screen at
    obstacle_gap = 175                                          # Pixel gap between different pipes
    floor_offset = 0                                            # A pixel tracker for the floor
    score = 0                                                   # The players score
    clock = pygame.time.Clock()                                 # Create a game clock to manage frame rate
    score_font = pygame.font.SysFont('matrix', 60)              # Font to dispaly the score in
    floored_width = SCREEN_WIDTH + floor_image.get_width() * 2  # The total width to render floor/ceiling onto
    floor_width = floor_image.get_width()                       # Width of individual floor section

    # Create a screen to display graphics on and change the title and icon
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("NatHacks Flappy Brain")
    pygame.display.set_icon(player_image)

    # Create a custom event to make new obstacles on a timed bases
    ADDOBSTACLE = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDOBSTACLE, 2500)
    
    # Create a list of text columns that span across the screen
    text_columns = [TextColumns(SCREEN_WIDTH / columns * col, random.randint(130,250), SCREEN_HEIGHT) for col in range(columns)]

    # Create two sprite groups, one for just obstacles and one for all sprites which will include the player
    obstacles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    # Create a new player object and add to the sprite group
    player = Player(player_image, SCREEN_HEIGHT)
    all_sprites.add(player)

    # Game loop plays the game    
    while running:
        #################################################################################################################################
        ## Check all the game events for user input
        #################################################################################################################################
        for event in pygame.event.get():
            # If quit is pressed close the game
            if event.type == pygame.QUIT:
                return score_string, False

            # If the escape key is pressed close the game
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return score_string, False

            # If an ADDOBSTACLE event was triggered create a new obstacle and add it to both sprite groups
            if event.type == ADDOBSTACLE:
                new_obstacle = Obstacle(obstacle_image, obstacle_speed, obstacle_gap, SCREEN_HEIGHT, SCREEN_WIDTH)
                obstacles.add(new_obstacle.get_sprites())
                all_sprites.add(new_obstacle.get_sprites())

        #################################################################################################################################
        ## Update the game logic for the loop
        #################################################################################################################################
        
        # Update the player and obstacles and check if it has died 
        player_died = player.update(pygame.key.get_pressed())
        obstacles.update()
        
        # Check if the player has dies and if has kill it and stop running the game
        if pygame.sprite.spritecollideany(player, obstacles) or player_died:
            player.kill() 
            running = False

        # Move over the floor in sync with the obstacles. When it has moved over one full block reset the offset
        floor_offset += obstacle_speed
        if floor_offset == floor_image.get_width(): 
            floor_offset = 0

        # Increment the interager score, divide the score by 15 so it moves up at a rate of about 2 per second.
        score += 1
        score_string = str(score // 15)

        #################################################################################################################################
        ## Render the images onto the screen
        #################################################################################################################################

        # Fill the background black, and then blit all the text onto the screen 
        screen.fill('black')

        # Blit the background text onto the screen
        for tc in text_columns:
            tc.blit_numbers(screen)
        
        # Render floor and ceiling onto the screen
        for x in range(0, floored_width, floor_width):
            screen.blit(floor_image, (x - floor_offset, SCREEN_HEIGHT - floor_image.get_height()))
            screen.blit(pygame.transform.flip(floor_image, False, True), (x - floor_offset, 0))

        # Render all the sprites (player and obstacles)
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        # Render the text that shows the score onto the top of the screen
        score_text = score_font.render(score_string, True, "green")
        score_text_rect = score_text.get_rect(center = (SCREEN_WIDTH/2, 30))
        screen.blit(score_text, score_text_rect)
        
        # Display the graphics on the screen
        pygame.display.flip()

        # Limit clock to 30 fps frame rate
        clock.tick(30)
    
    # When the game ends return the score and true to bring up the menu
    return score_string, True

def menu(score):
    """
    Function to make a menu that shows the last score and allow the player to choose to play again

    Input Parameters
    ----------------
    score: the score to display

    Returns
    -------
    A boolean that is true if the game should play again
    """

    # Create the display and fill it with black
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    screen.fill('black')
    running = True

    # Create a font for the text, and a different one for the score
    font = pygame.font.SysFont('matrix', 60)
    score_font = pygame.font.SysFont('matrix', 120)

    # Display a title text to the screen
    title_text = font.render("Your Score!", False, "green")
    title_rect = title_text.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5))
    screen.blit(title_text, title_rect)

    # Display the score below the title
    score_text = score_font.render(str(score), False, "green")
    score_rect = score_text.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
    screen.blit(score_text, score_rect)

    # Display a prompt to play again 
    cont_text = font.render("Press Space to Play Again", False, "green")
    cont_rect = cont_text.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 // 3))
    screen.blit(cont_text, cont_rect)

    # Show the display
    pygame.display.flip()

    # Game loop waits until there is an input
    while running:

        # For each event if it is quit or escape return false (don't play again). If it is space return true (play again)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return False

            if event.type == KEYDOWN and event.key == K_SPACE:
                return True

if __name__ == "__main__":
    """
    Main function runs the game until the user quits
    """    

    pygame.init()

    # Run the game initially
    score, play_again = game()

    # Bring up the menu and if the player presses space to play again run the game again. Otherwise break the while loop
    while play_again: 
        play_again = menu(score)
        if play_again:
            score, play_again = game()

    pygame.quit()