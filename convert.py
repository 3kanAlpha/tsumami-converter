from pynput.mouse import Listener, Controller, Button
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Listener as KeyboardListener

import time

MOUSE_FIX_POS = (600, 600)
TSUMAMI_L_LEFT = 's'
TSUMAMI_L_RIGHT = 'a'
TSUMAMI_R_LEFT = ';'
TSUMAMI_R_RIGHT = 'l'

prev_x = -1
prev_y = -1

keyboard = KeyboardController()
mouse_controller = Controller()

# マウスイベントを処理する関数
def on_move(x, y):
    global prev_x, prev_y
    print(f'x: {x}, y: {y}')
    
    diff_x = x - prev_x
    diff_y = y - prev_y
    
    if diff_x < 0:
        keyboard.press(TSUMAMI_L_LEFT)
        keyboard.release(TSUMAMI_L_LEFT)
    elif diff_x > 0:
        keyboard.press(TSUMAMI_L_RIGHT)
        keyboard.release(TSUMAMI_L_RIGHT)
        
    if diff_y < 0:
        keyboard.press(TSUMAMI_R_LEFT)
        keyboard.release(TSUMAMI_R_LEFT)
    elif diff_y > 0:
        keyboard.press(TSUMAMI_R_RIGHT)
        keyboard.release(TSUMAMI_R_RIGHT)
    
    prev_x = x
    prev_y = y
    
    # mouse_controller.position = (x, y)

def main():
    print("waiting before start...")
    time.sleep(5)
    
    print("start mouse listener")

    # マウスリスナーを作成
    mouse_listener = Listener(on_move=on_move)
    mouse_listener.start()

    def on_press(key):
        print(f'押されたキー: {key}')
        
        # 特殊なキーが押された場合にエラーが発生するので例外処理
        try:
            # 押されたキーが q なら...
            if key.char == 'q':
                # リスナーを停止する
                mouse_listener.stop()
                return False
        except:
            pass

    # キーボードコントローラを作成
    keyboard_listener = KeyboardListener(on_press=on_press)
    keyboard_listener.start()

    # キー入力を待機する
    mouse_listener.join()
    keyboard_listener.join()

if __name__ == '__main__':
    main()