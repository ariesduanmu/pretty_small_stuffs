# -*- coding: utf-8 -*-
# @Author: Li Qin
# @Date:   2018-05-07 15:32:43
# @Last Modified by:   Li Qin
# @Last Modified time: 2018-05-09 17:54:19
import os
from PIL import Image, ImageDraw, ImageFont  

def chinese_dateform(date):
    date = date.split(' ')[0]
    time = date.split("-")
    return time[0] + "年" + time[1] + "月" + time[2] + "日"

def single_line_text_size(draw, content, font):
    return draw.textsize(content, font=font)

def text_size(draw, content, font, spacing):
    return draw.multiline_textsize(content, font=font, spacing=spacing)

def customfont(size):
    return ImageFont.truetype('pingfang.ttf',size)

def draw_text(draw, top_left, content, font, color, align="left", padding = 20):
    draw.text(top_left, content, font=font, fill=color)
    _,height = single_line_text_size(draw, content, font)
    return top_left[1] + height + padding

def draw_inscribe(draw, content, inscribeFont, y, color, side_space = 48):
    width,height = single_line_text_size(draw, content, inscribeFont)
    inscribe_x = 750 - width - side_space
    return draw_text(draw,(inscribe_x, y), content, inscribeFont, color, align = "right")

def draw_last_constant_text(draw, community_name, experience_timestamp, y, contentFont,inscribeFont, color, left_space):
    encourage = "特此证明，以兹鼓励！"
    next_line_y = draw_text(draw, (left_space, y), encourage, contentFont, color)
    next_line_y = draw_inscribe(draw, community_name, inscribeFont, next_line_y, color)
    _ = draw_inscribe(draw, experience_timestamp, inscribeFont, next_line_y, color)

def draw_content(draw, content, community_name, experience_timestamp, contentFont,inscribeFont, color="#000000", left_space=98, init_y=640, side_space=48):
    flwidth = 750 - left_space - side_space
    lwidth = 750 - side_space * 2

    next_character_idx = 0
    isfirstline = True
    finished = False
    while 1:
        target_width = flwidth if isfirstline else lwidth
        current_line = content[next_character_idx]
        while 1:
            width, height = single_line_text_size(draw, current_line,contentFont)
            if width > target_width:
                current_line = current_line[:-1]
                break
            next_character_idx += 1
            if next_character_idx >= len(content): 
                finished = True
                break
            current_line += content[next_character_idx]
            
        if isfirstline:
            next_line_y = draw_text(draw, (left_space,init_y), current_line, contentFont, color)
            isfirstline = False
        else:
            next_line_y = draw_text(draw, (side_space, next_line_y), current_line, contentFont, color)

        if finished:
            draw_last_constant_text(draw, community_name, experience_timestamp, next_line_y, contentFont,inscribeFont, color, left_space)
            break

def paste_images(baseimg, headimg, headimg_box):
    base_img = Image.open(baseimg)
    target = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    
    region = Image.open(headimg)
    region = region.convert("RGBA")
    target.paste(region,headimg_box)
    target.paste(base_img,(0,0),base_img) 
    return target


def generate_award(baseimg, headimg, userinfo):
    contentFont = customfont(32)
    inscribeFont = customfont(24)
    left_space = 98
    init_y = 640
    side_space = 48
    headimg_box = (310, 372, 442, 504)
    experience_timestamp = chinese_dateform(userinfo["experience_timestamp"])

    image = paste_images(baseimg, headimg, headimg_box)
    draw = ImageDraw.Draw(image)
    content = f'{userinfo["name"]}，{userinfo["sex"]}，于{experience_timestamp}以{userinfo["score"]}分的成绩通过{userinfo["project"]}知识考评。'
    draw_content(draw, content, userinfo["community_name"], experience_timestamp, contentFont,inscribeFont)
    image.save("user.png")


if __name__ == "__main__":
    userinfo = {"name":"吴尊","sex":"男","experience_timestamp":"2018-05-09 17:19:06","score":"80","project":"消防科普","community_name":"湖滨街道消防中心"}
    generate_award("honor.png","headimg.jpg",userinfo)


