import os
import base64
import datetime
import requests

from PIL import Image, ImageFont, ImageDraw

def encode_image(image_path):
    try:
        image = open(image_path,'rb')
        base_encoded = base64.b64encode(image.read())
        image.close()
        return base_encoded.decode()
    except:
        print("[-] Failed to encode image")
        return None

def download_image(url, image_path):
    response = requests.get(url, stream=True)
    if not response.ok:
        print("[-] Failed to download image")
        return 0

    f = open(image_path,'wb+')
    for block in response.iter_content(1024):
        if not block:
            break
        f.write(block)
    f.close()
    return 1

def resize_image(image_path, target_size):
    image = Image.open(image_path).convert("RGBA")
    width = min(image.size[0], image.size[1])
    image = image.crop((0,0,width,width))
    return image.resize(target_size, Image.LANCZOS)


def paste_images(self, base_image, pasted_image, pasted_box):
    image = Image.new("RGBA", base_image.size, (0,0,0,0))
    image.paste(pasted_image, pasted_box)
    image.paste(base_image,(0,0),base_image)
    return image

def customFont(font_path, size):
    return ImageFont.truetype(font_path, size)

def draw_content(self, image, base_img_width, side_space, text_start_y, content, contentFont):
    '''
    return image after written(draw)

    image: Image object
    base_img_width: width of the base image
    side_space: padding on two sides of x 
    text_start_y: y postion of the first line
    contentFont: text font 
    content: content to write(draw)

    '''
    draw = ImageDraw.Draw(image)
    content_width = base_img_width - side_space * 2

    contents_to_draw = contents_lines(content, content_width)
    next_line_y = text_start_y
    for line in contents_to_draw:
        next_line_y = draw_text(draw, base_img_width, (side_space, next_line_y), side_space, 20, "#000000", contentFont, line)
    return image

def contents_lines(content, content_width):
    '''
    sperate content to lines
    '''
    contents_to_draw = []
    next_character_idx = 0
    finished = False

    while not finished:
        current_line = content[next_character_idx]
        while True:
            width, height = draw.textsize(current_line, font=contentFont)
            if width > content_width:
                current_line = current_line[:-1]
                break
            next_character_idx += 1
            if next_character_idx >= len(content): 
                finished = True
                break
            current_line += content[next_character_idx]
        contents_to_draw += [current_line]
    return contents_to_draw

def draw_text(draw, base_img_width, top_left, side_space, padding, color, font, content, align="left"):
    '''
    return the y position of next line
    
    draw:ImageDraw object 
    base_img_width: width of the base image 
    top_left: the corridinate of x and y for the first letter
    side_space: padding on two sides of x 
    padding: padding on two sides of y
    color: text color 
    font: text font 
    content: content to write(draw) 

    align:default is left
    '''
    if align == "right":
        width,height = draw.textsize(content, font=font)
        top_left = (base_img_width - width - side_space, top_left[1])

    draw.text(top_left, content, font=font, fill=color)
    _, height = draw.textsize(content, font=font)
    return top_left[1] + height + padding






   
 