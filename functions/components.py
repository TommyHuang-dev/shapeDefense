import pygame
from pygame import gfxdraw

# various methods for drawing components such as grids and paths on the tower defence game

# this method draws a grid!!
# border draws a border around the grid, of the same colour as the grid itself
# offset offsets the lines drawn in the grid, negative values are recommended, default 0
def draw_grid(display, start_x, start_y, l, h, space, col, border, offset_l=0, offset_h=0, ):
    if l < 0 or h < 0 or space < 0:
        raise ValueError('draw_grid was called with less than 0 for length, height, or spacing!')

    display.lock()  # lock then unlock screen after drawing for more efficiency
    end_x = start_x + l
    end_y = start_y + h
    # vertical lines
    for i in range((l - 1 - offset_l) // space):
        pygame.draw.line(display, col, (start_x + offset_l + (i + 1) * space, start_y),
                         (start_x + offset_l + (i + 1) * space, end_y - 1))
    # horizontal lines
    for i in range((h - 1 - offset_h) // space):
        pygame.draw.line(display, col, (start_x, start_y + offset_h + (i + 1) * space),
                         (end_x - 1, start_y + offset_h + (i + 1) * space,))
    # border
    if border:
        pygame.draw.rect(display, col, (start_x, start_y, l, h), 1)
    display.unlock()


# draws the path based on a list of corners, uses lines for the path, circles to fill in corners
def draw_path(display, corner_list, col):
    display.lock()  # lock then unlock screen after drawing for more efficiency
    pygame.draw.lines(display, col, False, corner_list, 45)
    for i in range(len(corner_list)):
        pygame.gfxdraw.filled_circle(display, corner_list[i][0], corner_list[i][1], 22, col)
    display.unlock()


# creates a rectangular button object
def create_button(display, rect, text, fontsize, back_col, text_col):
    pass


# creates some text centered on an x y coordinate
def create_text(display, location, text, centered, font, col):
    display_text = font.render(str(text), True, col)
    text_rect = display_text.get_rect()
    if centered:
        display.blit(display_text, (location[0] - text_rect[2] // 2, location[1] - text_rect[3] // 2))
    else:
        display.blit(display_text, (location[0], location[1] - text_rect[3] // 2))
