import pygame
import os

def play(sound_type, volume):
    """
    指定されたエンジン音タイプに基づいてMP3ファイルを再生する関数。

    Args:
        sound_type (str): エンジンの種類 (例: "ev", "sports", "race", "back")
        volume (float): 音量（0.0-1.0）
    """
    sound_files = {
        "none": "none",
        "ev": "engine_sound/yamaha-ev.mp3",
        "sports": "engine_sound/RX-7-FD3S_large.mp3",
        "race": "engine_sound/F1_large.mp3",
        "back": "engine_sound/back_large.mp3",
    }
    
    try:
        if sound_type not in sound_files:
            print(f"Error: Unknown engine type '{sound_type}'")
            return
        
        if sound_type != "none":
            sound_file = sound_files[sound_type]
            
            if not os.path.exists(sound_file):
                print(f"Error: Sound file '{sound_file}' not found.")
                return
            
            # 既存のミキサーをクリーンアップして再初期化
            pygame.mixer.quit()
            os.environ['SDL_AUDIODRIVER'] = 'alsa'  # または 'alsa'
            pygame.mixer.init(
                frequency=60000,  # サンプリング周波数（Hz）
                size=-16,         # サンプルサイズ（ビット）
                channels=2,       # チャンネル数（1:モノラル、2:ステレオ）
                buffer=2048       # バッファサイズ（バイト）
            )
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
            
            print(f"Playing sound for engine type: {sound_type}")
            
    except pygame.error as e:
        print(f"音声の再生に失敗しました: {e}")

    # # 再生が終了するまで待機
    # while pygame.mixer.music.get_busy():
    #     pass

def stop():
    """
    音声の再生を停止する関数。
    """
    try:
        # mixerが初期化されているか確認
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
    except pygame.error as e:
        print(f"音声の停止に失敗しました: {e}")
    pass

if __name__ == "__main__":
    # テストケース
    # ev, sports, race, back
    engine_type = "ev"
    play(engine_type, 1.0)
