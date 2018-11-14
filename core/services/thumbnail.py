from PIL import Image, ImageFont, ImageDraw
import constants
from urllib import request
import re
import os


def create(clip, number, destination, game, video_type, channel_logo=None):
    """
        Creates a thumbnail image from a clip and a video number.
    """
    name = remove_spaces(destination + '_' + game + '_' +
                         video_type + '_' + str(number)) + '.png'
    path = constants.THUMBNAILS_LOCATION + name

    download_image_to_location(clip.thumbnail, path)

    title = add_new_line_after_x_chars(clip.title)

    if channel_logo:
        url, file_extension = os.path.splitext(channel_logo)
        filename = channel_logo[channel_logo.rfind("/")+1:]
        logo_path = constants.LOGOS_LOCATION + clip.channel.name + file_extension

        download_image_to_location(channel_logo, logo_path)
        add_channel_logo(logo_path, path)
    else:
        add_game_icon(game, path)

    add_title(title, path)
    add_number(number, path)

    return path


def add_title(title, path):
    img = Image.open(path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(
        constants.TITLE_FONT_LOCATION, constants.TITLE_SIZE)

    x, y = 10, 10

    thickness = constants.TITLE_BORDER_THICKNESS

    # Draw a small black border around the text to make it more readable.
    draw.text((x-thickness, y-thickness), title, font=font, fill='black')
    draw.text((x+thickness, y-thickness), title, font=font, fill='black')
    draw.text((x-thickness, y+thickness), title, font=font, fill='black')
    draw.text((x+thickness, y+thickness), title, font=font, fill='black')

    # Draw the title.
    draw.text((x, y), title, constants.TITLE_FONT_COLOR, font=font)

    img.save(path)


def add_number(number, path):
    number = "#" + str(number)

    img = Image.open(path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(
        constants.NUMBER_FONT_LOCATION, constants.NUMBER_SIZE)

    x, y = 10, 220

    thickness = constants.NUMBER_BORDER_THICKNESS

    # Draw a small black border around the text to make it more readable.
    draw.text((x-thickness, y-thickness), number, font=font, fill='black')
    draw.text((x+thickness, y-thickness), number, font=font, fill='black')
    draw.text((x-thickness, y+thickness), number, font=font, fill='black')
    draw.text((x+thickness, y+thickness), number, font=font, fill='black')

    # Draw the number.
    draw.text((x, y), number, constants.NUMBER_FONT_COLOR, font=font)

    img.save(path)


def add_game_icon(game, path):
    background = Image.open(path)
    foreground = Image.open(constants.LOGOS_LOCATION + game + '.png')

    background.paste(foreground, (20, 120), foreground)
    background.save(path, format="png")


def add_channel_logo(logo_path, thumbnail_path):
    background = Image.open(thumbnail_path)
    foreground = Image.open(logo_path)
    new_width = 100
    new_height = 100
    foreground = add_corners(foreground, 70)
    foreground = foreground.resize((new_width, new_height), Image.ANTIALIAS)

    background.paste(foreground, (20, 155), foreground)
    background.save(thumbnail_path, format="png")


def download_image_to_location(url, location):
    print('Downloading image: ' + url)
    f = open(location, 'wb')
    f.write(request.urlopen(url).read())
    f.close()


def remove_spaces(string):
    return string.replace(" ", "_")


def add_new_line_after_x_chars(string):
    """
        Add a newline after 18 characters. Counted for 70pt font.
    """
    return re.sub("(.{18})", "\\1\n", string, 0, re.DOTALL)


def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im
