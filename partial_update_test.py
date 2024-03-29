#!/usr/bin/python
import os
import logging
from waveshare_epd import epd4in2_V2
from PIL import Image,ImageDraw,ImageFont

#initialize some vars
logging.basicConfig(level=logging.DEBUG)
font18 = ImageFont.truetype('Font.ttc', 11)
text = ""

def init_display():
    #initialize and clear display
    epd = epd4in2_V2.EPD()
    #logging.info("init and Clear")
    epd.init()
    epd.Clear()
    return epd 

def init_image(epd):
    #logging.info("Draw Image")
    draw_image = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    #logging.info("set image object")
    draw = ImageDraw.Draw(draw_image)
    return draw,draw_image

def partial_update_text(draw, draw_image,text, epd):
    logging.info("draw text")
    draw.rectangle((0, 0, 400, 300), fill = 255)
    draw.text((5, 5), text, font = font18, fill=0)
    epd.display_Partial(epd.getbuffer(draw_image))

def cleanup(epd):
    # Cleanup and sleep
    epd.init()
    epd.Clear()
    epd.sleep()

epd = init_display() #initialize the display one time. 
draw, draw_image = init_image(epd)

while True:
    try:
        count = 0
        while True:
            if(count < 10):
                str_count = str(count)
                text = text + " " + str_count
                partial_update_text(draw, draw_image, text, epd)
                count = count + 1
            break

    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd4in2_V2.epdconfig.module_exit(cleanup=True)
        cleanup(epd) 
        exit()