import datetime
import os
import shutil
import rc_util.global_var as global_var

from rc_bots.BotCoinFlipBot import BotCoinFlipBot
from rc_model.ScreenSetting import TargetScreen


def setup_screen_shots_dir():
    if not os.path.exists('imgs'):
        os.mkdir('imgs')
    else:
        shutil.rmtree('imgs')
        os.mkdir('imgs')


def main(screen_obj):
    Bots = [BotCoinFlipBot]
    while True:
        for bot in Bots:
            if bot(screen_obj).can_start():
                bot(screen_obj).play()


if __name__ == "__main__":
    # check the url TODO
    global_var.init()
    setup_screen_shots_dir()
    screen_setting = TargetScreen.getInstance()
    try:
        main(screen_setting)
    except KeyboardInterrupt:
        print("Program closed by User!")

    finally:
        print("\nStatistics:\n",
              "Time running: {!s}\n".format(datetime.datetime.now() - gl.get_value('START_TIME')),
              "Played Games:  {!s}\n".format(gl.get_value('GAME_NUM'))
              )
        # remove all the images captured before
        shutil.rmtree('imgs')
