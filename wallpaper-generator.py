"""
Wallpaper Generator. See original HTML/Javascript version by roytanck (Roy Tanck)
https://github.com/roytanck/wallpaper-generator 
"""

from PIL import Image, ImageDraw
import random
import base64
import math
import os

def generateValues(width):
    # line segments (either few, or fluent lines (200))
    segments = 1 + math.floor(9 * random.random()) if random.random() < 0.5 else 200
    # wavelength
    wl = width / (5 + (15 * random.random()))

    # other random values
    random_vals_dict = {
        'segments': segments,
        'wl': wl,
        'layers': 3 + math.floor(10 * random.random()),
        'hueStart': 360 * random.random(),
        'hueIncrement': 20 - (40 * random.random()),
        'ampl': (0.1 * wl) + (0.9 * wl) * random.random(),
        'offset': width * random.random(),
        'offsetIncrement': width / 20 + (width / 10) * random.random(),
        'sat': 15 + (35 * random.random()),
        'light': 15 + (45 * random.random()),
        'lightIncrement': (2 + (4 * random.random())) if random.random() < 0.5 else -(2 + (4 * random.random()))
    }
    
    print(random_vals_dict)
    return random_vals_dict

def hsl_to_rgb(h, s, l):
    # Convert HSL to RGB
    # Code borrowed from https://www.programcreek.com/python/example/94482/colorsys.hsv_to_rgb
    h /= 360
    s /= 100
    l /= 100
    c = (1 - abs(2*l - 1)) * s
    x = c * (1 - abs((h*6) % 2 - 1))
    m = l - c/2
    c += m
    x += m
    if h < 1/6: return (c, x, m)
    elif h < 1/3: return (x, c, m)
    elif h < 1/2: return (m, c, x)
    elif h < 2/3: return (m, x, c)
    else: return (x, m, c)


def generate_filename(base_dir, base_name):
    """Returns a filename of the form 'name-{n}' and uses the next available highest number."""
    
    # Get a list of all existing files in the base directory
    files = os.listdir(base_dir)

    # Find the highest number currently in use
    highest_num = 0
    for file in files:
        if file.startswith(base_name):
            try:
                # Extract the number from the filename
                num = int(file[len(base_name):-4])  # Subtract 4 for the file extension
                highest_num = max(highest_num, num)
            except ValueError:
                pass  # Filename didn't have a number, ignore it

    # Return a filename with the highest number incremented by 1
    return f"{base_dir}/{base_name}{highest_num + 1}.png"


def draw():
    width = 3840
    height = 2160

    values = generateValues(width)
    segments = values['segments']
    layers = values['layers']
    hueStart = values['hueStart']
    hueIncrement = values['hueIncrement']
    wl = values['wl']
    ampl = values['ampl']
    offset = values['offset']
    offsetIncrement = values['offsetIncrement']
    sat = values['sat']
    light = values['light']
    lightIncrement = values['lightIncrement']

    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    # background
    r, g, b = [int(x * 255) for x in hsl_to_rgb(hueStart, sat, light)]
    draw.rectangle([(0, 0), (width, height)], fill=(r, g, b))

    # draw the layers
    for l in range(layers):
        h = hueStart + ((l+1) * hueIncrement)
        s = sat
        v = light + ((l+1) * lightIncrement)
        r, g, b = [int(x * 255) for x in hsl_to_rgb(h, s, v)]
        layerOffset = offset + (offsetIncrement * l)
        offsetY = ((l+0.5) * (height / layers))
        startY = offsetY + (ampl * math.sin(layerOffset / wl))
        coords = [(0, startY)]
        for i in range(segments+1):
            x = i * (width / segments)
            coords.append((x, startY + (ampl * math.sin((layerOffset + x) / wl))))
        coords.append((width, height))
        coords.append((0, height))
        coords.append((0, startY))
        draw.polygon(coords, fill=(r, g, b))

    image.show() # Shows the image using the default image viewer.

    # Now, you can use this function to get the next filename:
    next_filename = generate_filename('./generated-wallpapers', 'generated-')
    image.save(next_filename)


if __name__ == "__main__":
    draw()
