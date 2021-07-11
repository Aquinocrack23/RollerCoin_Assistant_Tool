__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2021/7/11 10:32'

import datetime
import os
import time
import cv2
import keyboard
import pyautogui
import rc_bots.global_var as gl
from PIL import ImageGrab
from MTM import matchTemplates

from rc_bots.string_util import genRandomStr

num = 3


def mouse_click(x, y, wait=0.05):
    pyautogui.click(x, y)
    time.sleep(wait)


def screen_grab():
    im = ImageGrab.grab()
    img_name = os.getcwd() + "\\imgs\\full_snap__" + str(int(time.time())) + ".png"
    im.save(img_name, "PNG")
    return img_name


def wrapper_pos(pos):
    return (pos[0], pos[1], pos[2] + pos[0], pos[3] + pos[1])


def grab_img_by_rect(position, save_file=False):
    img = ImageGrab.grab(bbox=position)
    # save to file
    if save_file:
        imgName = os.getcwd() + "\\" + genRandomStr() + ".png"
        img.save(imgName, "PNG")
        print("saved a png file whose name is: ", imgName)
    return img


def cropImgByRect(img, position, save_file=False):
    cropped = img.crop(position)
    if save_file:
        imgName = genRandomStr() + ".png"
        cropped.save(imgName)
        print("saved a png file whose name is: ", imgName)
    return cropped


def find_image(image_path, root_image_path):
    matches = matchTemplates(
        [("img", cv2.imread(image_path))],
        cv2.imread(root_image_path),
        N_object=10,
        score_threshold=0.9,
        # maxOverlap=0.25,
        searchBox=None)
    if len(matches["BBox"]) == 0:
        return None, None
    else:
        box = matches["BBox"][0]
        return box[0], box[1]


def check_image(img):
    b, _ = find_image(img, screen_grab())
    return True if b is not None else False


def click_image(img):
    time.sleep(0.05)
    x, y = find_image(img, screen_grab())
    if x is None or y is None:
        return

    im = cv2.imread(img)
    t_cols, t_rows, _ = im.shape
    mouse_click(x + t_rows * (3 / 5), y + t_cols * (2 / 3))


def start_game(game_block_img_path):
    click_image(game_block_img_path)
    flag = False
    while not flag:
        flag = check_image("rc_items/utils/start_game.png")
        time.sleep(0.2)
    sx, sy = find_image("rc_items/utils/start_game.png", screen_grab())
    mouse_click(sx + 2, sy + 2, wait=0.05)
    print("begin to count down ...")
    time.sleep(3)


def print_log_msg(name):
    game_num = gl.get_value("GAME_NUM")
    print("Starting Game #{!s}: '{}'@{!s}".format(game_num, name, datetime.datetime.now().time()))
    gl.set_value('GAME_NUM', game_num + 1)


def end_game():
    if check_image("rc_items/utils/gain_power.png"):
        print("gain_power")
        click_image("rc_items/utils/gain_power.png")

    if check_image("rc_items/utils/gameover.png"):
        print("gameover")
        click_image("rc_items/utils/restart.png")

    if check_image("rc_items/utils/start_game.png"):
        print("start_game")
        click_image("rc_items/utils/start_game.png")

    keyboard.press_and_release("page up")
    if check_image("rc_items/utils/recaptha.png"):
        print("recaptha---")
        keyboard.press_and_release("f5")

    if check_image("rc_items/utils/error2.png"):
        keyboard.press_and_release("f5")

    if check_image("rc_items/utils/choose_game.png"):
        print("choose game")
        click_image("rc_items/utils/choose_game.png")

    if check_image("rc_items/utils/collect_pc.png"):
        print("collect pc")
        click_image("rc_items/utils/collect_pc.png")

    while not check_image("rc_items/games/coinflip_gameimg.png"):
        global num
        print("end game---")
        if num == 0:
            keyboard.press_and_release("alt+left")
        num -= 1
        return end_game()


def find_a_dissimilar(pos0, pos1, pos2):
    var1 = sum(list(map(lambda x: abs(x[0] - x[1]), zip(pos0, pos1))))
    var2 = sum(list(map(lambda x: abs(x[0] - x[1]), zip(pos0, pos2))))
    return pos1 if var1 > var2 else pos2


def variance(data, ddof=0):
    n = len(data)
    mean = sum(data) / n
    return sum((x - mean) ** 2 for x in data) / (n - ddof)

