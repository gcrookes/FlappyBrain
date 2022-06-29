import random
import pygame

class TextColumns:
    """
    Class to create moving columns of green numbers to use as a background.
    Creates a column of numbers that descends from the top of the screen and rests once it falls off the bottoms

    Input Parameters
    ----------------
    x:  the x position on the screen to render the column at
    numbers: The number of numbers to render in the column
    screen_height: The height of the screen to render on
    """
    def __init__(self, x, numbers, screen_height):

        # Set the class variable to the inputs
        self.num = numbers
        self.screen_height = screen_height
        self.x = x

        # Create a new font to use for the class
        self.font_size = 20
        self.font = pygame.font.SysFont('matrix', self.font_size)
        
        # Create a random speed limit so the columns decend at different speeds
        self.speed_max = random.randint(4,6)
        self.speed_min = random.randint(2,4)

        # Call the method to create a column
        self.create_column()

    def blit_numbers(self, screen):
        """
        Method to render the numbers onto the screen

        Input Parameters
        ----------------
        screen: the pygame screen to blit the numbers onto
        """

        # If the top number has fallen off the bottom of the screen then recreate the column at the top of the screen
        if self.numbers[-1][1].top >= self.screen_height:
            self.create_column()

        # Set a random speed so the columns move at different speeds
        speed = random.randint(self.speed_min,self.speed_max)

        # Loop over all the numbers, move them down, then blit them onto the screen
        for text, text_rect in self.numbers:
            text_rect.move_ip(0,speed)
            screen.blit(text, text_rect)

    def create_column(self):
        """
        Initialize the data for the column of numbers
        """

        # Create a yoffset to start the column above the screen and make an empty list of numbers
        yoffset = random.randint(-160, 0)
        self.numbers  = []

        # For the number of new numbers to make create a new text item with a random number between 0 and 9, stack them vertically and append them into the numbers list
        for i in range(self.num):  
            text = self.font.render(str(random.randint(0,9)), True, "green")
            text_rect = text.get_rect()
            text_rect.move_ip(self.x, self.font_size * (yoffset - i))
            self.numbers.append((text, text_rect))