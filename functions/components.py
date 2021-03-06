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

# rotates an image by its center
def rot_center(image, angle):
    """rotate a Surface, maintaining position."""
    loc = image.get_rect().center
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite


# creates some text centered on an x y coordinate
def create_text(display, location, text, centered, font, col):
    display_text = font.render(str(text), True, col)
    text_rect = display_text.get_rect()
    if centered:
        display.blit(display_text, (location[0] - text_rect[2] // 2, location[1] - text_rect[3] // 2))
    else:
        display.blit(display_text, (location[0], location[1] - text_rect[3] // 2))


# creates text with breakpoints every length
def create_paragraph(display, location, text, font, col, line_height, length):
    cur_text = ""
    lines = 0
    for i in text:
        new_text = cur_text + i + " "
        if len(new_text) * 20 > length:
            # render text to check length
            new_text = font.render(str(new_text), True, col)
            if new_text.get_rect()[2] > length:  
                # display old one if it goes over
                new_text = font.render(str(cur_text), True, col)
                display.blit(new_text, (location[0], location[1] + lines * line_height))
            
                lines += 1
                cur_text = ""

        cur_text += i + " "
    
    cur_text = font.render(cur_text, True, col)
    display.blit(cur_text, (location[0], location[1] + lines * line_height))


# converts xy pixel value to a grid coord
def xy_to_pos(xy):
    pos = [xy[0] // 50 + 1, xy[1] // 50 + 1]
    # make sure its not out of bounds
    if pos[0] > 20:
        pos[0] = 20
    elif pos[0] < 1:
        pos[0] = 1
    if pos[1] > 15:
        pos[1] = 15
    elif pos[1] < 1:
        pos[1] = 1

    return pos
