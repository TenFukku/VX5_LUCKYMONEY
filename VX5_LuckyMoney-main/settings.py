
import pygame

WINDOW_NAME = "Collecting Tucky Pockets"  # tên của cửa sổ trò chơi
GAME_TITLE = ""  # tiêu đề của trò chơi

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080  # kích thước của cửa sổ 1920

FPS = 90  # số frame/s mà
DRAW_FPS = True  # xác định fps được hiển thị

# sizes
BUTTONS_SIZES = (240, 90)  # kích thước các nút trò chơi
HAND_SIZE = 200  # kích thước bàn tay người chơi
HAND_HITBOX_SIZE = (60, 60)  # kích thước hitbox của tay người chơi
MOSQUITOS_SIZES = (100, 70)  # kích thước cơ bản của con muỗi

# điều chỉnh kích thước ngẫu nhiên của con muỗi
MOSQUITO_SIZE_RANDOMIZE = (1, 2)
BEE_SIZES = (100, 70)
BEE_SIZE_RANDOMIZE = (1.2, 1.5)  # kích thước ngẫu nhiên của con ong

# drawing
DRAW_HITBOX = False 
 # xác định hitbox có được vẽ lên hay không

# animation
ANIMATION_SPEED = 0.08  # tốc độ thay đổi frame của các đối tượng

# difficulty
GAME_DURATION = 60  # thời gian tổng cộng của một vòng chơi
MOSQUITOS_SPAWN_TIME = 1  # thời gian giữa mỗi lần xuất hiện của muỗi mới
# điều chỉnh tốc độ di chuyển của muỗi
MOSQUITOS_MOVE_SPEED = {"min": 20, "max": 25}
BEE_MOVE_SPEED = {"min": 35, "max": 45}
BEE_PENALITY = 10  # số điểm bị trừ khi giết một con ông

# colors
COLORS = {"title": (38, 61, 39),  # màu của tiêu đề trò chơi
          "score": (38, 61, 39),  # điểm số
          "timer": (38, 61, 39),  # thời gian
          "buttons":  # các nút
          {"default": (56, 67, 209),
           "second":  (87, 99, 255),
           "test": (128, 0, 0),
              "text": (255, 255, 255),
              "shadow": (46, 54, 163)}}  # second is the color when the mouse is on the button

# sounds / music
MUSIC_VOLUME = 0.16  # value between 0 and 1, âm lượng
SOUNDS_VOLUME = 1

# fonts
pygame.font.init()
font_path = "Assets\Roboto-Regular.ttf"
FONTS = {}
FONTS["small"] = pygame.font.Font(font_path, 20)
FONTS["medium"] = pygame.font.Font(font_path, 52)
FONTS["big"] = pygame.font.Font(font_path, 100)
