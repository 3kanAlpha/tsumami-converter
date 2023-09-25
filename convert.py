from pynput.mouse import Listener, Controller, Button
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Listener as KeyboardListener

import time, threading

# 1秒に何回マウス移動の追跡を行うか
TRACK_PER_SECOND = 40
ONE_FRAME_TIME = 1 / TRACK_PER_SECOND
TSUMAMI_L_LEFT = 's'
TSUMAMI_L_RIGHT = 'a'
TSUMAMI_R_LEFT = ';'
TSUMAMI_R_RIGHT = 'l'

mouse_fix_position = (0, 0)

listener_enabled = False

keyboard = KeyboardController()
mouse_controller = Controller()

# マウスの位置を追跡して、移動量に応じてキーを押す
def track_mouse():
    while True:
        x, y = mouse_controller.position
        # print(f'x: {x}, y: {y}')
        
        prev_x, prev_y = mouse_fix_position
    
        diff_x = x - prev_x
        diff_y = y - prev_y
        
        if not listener_enabled:
            continue
        
        if diff_x < 0:
            keyboard.release(TSUMAMI_L_RIGHT)
            keyboard.press(TSUMAMI_L_LEFT)
        elif diff_x > 0:
            keyboard.release(TSUMAMI_L_LEFT)
            keyboard.press(TSUMAMI_L_RIGHT)
        else:
            keyboard.release(TSUMAMI_L_LEFT)
            keyboard.release(TSUMAMI_L_RIGHT)
            
        if diff_y < 0:
            keyboard.release(TSUMAMI_R_RIGHT)
            keyboard.press(TSUMAMI_R_LEFT)
        elif diff_y > 0:
            keyboard.release(TSUMAMI_R_LEFT)
            keyboard.press(TSUMAMI_R_RIGHT)
        else:
            keyboard.release(TSUMAMI_R_LEFT)
            keyboard.release(TSUMAMI_R_RIGHT)
        
        mouse_controller.position = mouse_fix_position
        
        time.sleep(ONE_FRAME_TIME)

mouse_tracker = threading.Thread(target=track_mouse, daemon=True)

# キー入力監視
def on_press(key):
    global listener_enabled, mouse_fix_position
    
    # 特殊なキーが押された場合にエラーが発生するので例外処理
    try:
        if key.char == 'q':
            print("exiting...")
            return False
        elif key.char == 'o':
            if listener_enabled:
                print("listener disabled")
                listener_enabled = False
            else:
                print("listener enabled")
                mouse_fix_position = mouse_controller.position
                listener_enabled = True
    except:
        pass

def main():
    print("? press q to exit")
    print("? press o to toggle mouse tracking / fixing")
    
    print("----")
    
    print("! mouse tracking rate is set to {}".format(TRACK_PER_SECOND))

    # マウス移動監視の開始
    mouse_tracker.start()

    # キー入力監視の開始
    keyboard_listener = KeyboardListener(on_press=on_press)
    keyboard_listener.start()

    # 終了の待機
    keyboard_listener.join()

if __name__ == '__main__':
    main()