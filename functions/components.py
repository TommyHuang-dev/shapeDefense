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


# creates some text centered on an x y coordinate
def create_text(display, location, text, centered, font, col):
    display_text = font.render(str(text), True, col)
    text_rect = display_text.get_rect()
    if centered:
        display.blit(display_text, (location[0] - text_rect[2] // 2, location[1] - text_rect[3] // 2))
    else:
        display.blit(display_text, (location[0], location[1] - text_rect[3] // 2))


# draws a semi-transparent circle and outline, radius is number of tiles
def draw_range(display, tile_loc, turret_range, valid):
    # colours
    col_range_valid = [150, 150, 150, 60]
    col_range_valid_outline = [75, 75, 75, 225]
    col_range_invalid = [200, 25, 25, 40]
    col_range_invalid_outline = [125, 0, 0, 150]
    # convert tiles to pixels
    location = [tile_loc[0] * 50 - 25, tile_loc[1] * 50 - 25]
    if valid:
        pygame.gfxdraw.aacircle(display, location[0], location[1], int(turret_range * 50), col_range_valid_outline)
        pygame.gfxdraw.filled_circle(display, location[0], location[1], int(turret_range * 50), col_range_valid)
    elif not valid:
        pygame.gfxdraw.aacircle(display, location[0], location[1], int(turret_range * 50), col_range_invalid_outline)
        pygame.gfxdraw.filled_circle(display, location[0], location[1], int(turret_range * 50), col_range_invalid)
