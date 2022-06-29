import pygame
import random
from pygame.locals import K_UP, K_SPACE

class Player(pygame.sprite.Sprite):
    """
    Class represents the player object for the game.

    Input Parameters
    ----------------
    image: The image to represent the player
    screen_height: The height of the window, used to calculate player limits
    """

    def __init__(self, image, screen_height):
        super(Player, self).__init__()

        # Initialize properties
        self.max_count = 5 
        self.count = 0      # Count to limit how often you can jump
        self.jumping = 0    # Count for how long you are jumping
        self.angle = 0      # Angle to render the image at

        # copy inputs into new variables
        self.image = image
        self.screen_height = screen_height

        # Create a surface for the player and move it to the starting spot of the screen
        self.surf = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(center = (120,screen_height//3))
        
        

    def update(self, pressed_keys):
        """
        Handle the update for player on each tick

        Input Parameters
        ----------------
        pressed_keys: Pygame object that has a boolean for each key and is true if it is pressed down
        """

        # Count is a running count that resets when jumping
        self.count -= 1

        # If a button is pressed and you can jump again then set the jump counter to 10 and reset the count
        if self.count <= 0 and (pressed_keys[K_UP] or pressed_keys[K_SPACE]):    
            self.jumping = 10
        
        # If you are jumping move the player up and increase the angle so the player faces up more, otherwise move the player and angle down
        if self.jumping > 0:
            self.rect.move_ip(0, -8)
            self.jumping -= 1
            self.count = self.max_count

            if self.angle <20:
                self.angle += 2
    
        else:
            self.rect.move_ip(0,4)

            if self.angle > 0:
                self.angle -= 2

        # Rotate the player image and make a rectangle for it based on the center of the surface 
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_image_rect = rotated_image.get_rect(center = self.surf.get_rect().center)

        # Fill the surface with blank pixels to clear it and then blit the rotated image
        self.surf.fill((0,0,0,0))
        self.surf.blit(rotated_image, rotated_image_rect)

        # Limit the min value of the top of the player to keep them from going through the ceiling
        self.rect.top = max(75, self.rect.top)

        # Check if the player has fallen of the bottom of the screen and return True if it has
        return self.rect.bottom >= (self.screen_height - 75)


class Obstacle(pygame.sprite.Sprite):
    """
    Class to manage a pair of pipes that are the obstacles for the game

    Input Parameters
    ----------------
    image: The image to display on the pipe
    speed: The movement speed of the obstacle along the screen
    gap: The height of the gap between two pipes
    screen_height: The height of the screen
    screen_width: The width of the screen
    """

    def __init__(self, image, speed, gap, screen_height, screen_width):
        super(Obstacle, self).__init__()

        # Calculate a random height of the bottom pipe, and calculate the height of the top. Bound by the minimum size from the top and bottom of the screen
        min_pixels = 125
        height_bottom = random.randint(min_pixels, screen_height - gap - min_pixels)
        height_top = screen_height - height_bottom - gap

        # Calculate the centers for the pipe rectangles
        x = screen_width + image.get_width() / 2
        y_bottom = screen_height - height_bottom / 2
        y_top = height_top / 2

        # Crop the image based on the heights. For the top image flip it upside down
        image_bottom = image.subsurface((0, 0, image.get_width(), height_bottom))
        image_top = pygame.transform.flip(image.subsurface((0, 0, image.get_width(), height_top)), False, True)

        # Create two pipes 
        self.pipe_bottom = Pipe((x, y_bottom), image_bottom, speed)
        self.pipe_top = Pipe((x, y_top), image_top, speed)


    def get_sprites(self):
        """
        Method to return both the pipe objects.
        """
        return self.pipe_bottom, self.pipe_top

class Pipe(pygame.sprite.Sprite):
    """
    Class to manage the pipe obstacles

    Input Parameters
    ----------------
    height: The height of the pipe
    center: The center of the rectangle for the pipe
    image: The image to display as the pipe
    speed: The speed to move the obstacle across the screen
    """
    def __init__(self, center, image, speed):
        super(Pipe, self).__init__()

        # Set the speed of the object
        self.speed = speed

        # Create a surface and blit the image onto the 
        self.surf = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        self.surf.blit(image, (0,0))
        self.rect  = self.surf.get_rect(center=center)

    def update(self):
        """
        Method to update the pipes on every tick. 
        Moves the pipe to the left based on the speed and kill it if it is off the screen
        """

        self.rect.move_ip(-self.speed, 0)

        if self.rect.right < 0:
            self.kill()