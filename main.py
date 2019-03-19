import pygame
import time

import numpy as np
# 此模块包含游戏所需的常量
from pygame.locals import *

# 设置棋盘的长宽
BOARDWIDTH = 48
BOARDHEIGHT = 28
# 分数
score = 0
# 背景
grass = pygame.image.load('grass.png')
over = pygame.image.load('gameover.png')
# 食物
class Food(object):
    def __init__(self):
        self.item = (4, 5)

    # 画出食物
    def _draw(self, screen, i, j):
        color = 255, 0, 255
        radius = 10
        width = 10
        # i:1---34   j:1---25
        position = 10 + 20 * i, 10 + 20 * j
        # 画出半径为 10 的粉色实心圆
        pygame.draw.circle(screen, color, position, radius, width)

    # 随机产生食物
    def update(self, screen, enlarge, snake):
        if enlarge:
            self.item = np.random.randint(1, BOARDWIDTH - 2), np.random.randint(1, BOARDHEIGHT - 2)
            while self.item in snake.item:
                self.item = np.random.randint(1, BOARDWIDTH - 2), np.random.randint(1, BOARDHEIGHT - 2)
        self._draw(screen, self.item[0], self.item[1])


# 贪吃蛇
class Snake(object):
    def __init__(self):
        # self.item = [(3, 25), (2, 25), (1, 25), (1,24), (1,23),
        # (1,22), (1,21), (1,20), (1,19), (1,18), (1,17), (1,16)]
        # x 水平方向 y 竖直方向
        # 初始方向竖直向上
        self.item = [(3, 25), (2, 25), (1, 25), (1, 24), ]
        self.x = 0
        self.y = -1

    def move(self, enlarge):
        # enlarge 标记贪吃蛇有没有吃到食物
        if not enlarge:
            # 没吃到食物删除尾部元素
            self.item.pop()
        # 新蛇头的坐标为旧蛇头坐标加上移动方向的位移
        head = (self.item[0][0] + self.x, self.item[0][1] + self.y)
        # 将新的蛇头坐标插入在 list 最前面
        self.item.insert(0, head)

    def eat_food(self, food):
        global score
        # snake_x,snake_y 蛇头坐标
        # food_x, food_y 食物坐标
        snake_x, snake_y = self.item[0]
        food_x, food_y = food.item
        # 比较蛇头坐标与食物坐标
        if (food_x == snake_x) and (food_y == snake_y):
            score += 100
            return 1
        else:
            return 0

    def toward(self, x, y):
        # 改变蛇头朝向
        if self.x * x >= 0 and self.y * y >= 0:
            self.x = x
            self.y = y

    def get_head(self):
        # 获取蛇头坐标
        return self.item[0]

    def draw(self, screen):
        # 画出贪吃蛇
        # 蛇头为半径为 15 的红色实心圆
        radius = 15
        width = 15
        # i:1---34   j:1---25
        color = 255, 0, 0
        # position 为图形的坐标
        position = 10 + 20 * self.item[0][0], 10 + 20 * self.item[0][1]
        pygame.draw.circle(screen, color, position, radius, width)
        # 蛇身为半径为 10 的黄色实心圆
        radius = 10
        width = 10
        color = 255, 255, 0
        for i, j in self.item[1:]:
            position = 10 + 20 * i, 10 + 20 * j
            pygame.draw.circle(screen, color, position, radius, width)


# 初始界面
def init_board(screen):
    board_width = BOARDWIDTH
    board_height = BOARDHEIGHT

    #显示草地图片，设置图片坐标
    if board_width % grass.get_width() != 0: #草地横向复制
        grass_w = board_width // grass.get_width() + 1
    if board_height % grass.get_height()!=0: #草地纵向复制
        grass_h = board_height // grass.get_height() + 1
    for j in range(6):
        for i in range(10):
            screen.blit(grass,(i * grass.get_width(),j * grass.get_height()))
    #color = 10, 255, 255
    #width = 0
    # width:x, height:y
    # 左右边框占用了 X: 0 35*20
    # for i in range(board_width):
    #     pos = i * 20, 0, 20, 20
    #     pygame.draw.rect(screen, color, pos, width)
    #     pos = i * 20, (board_height - 1) * 20, 20, 20
    #     pygame.draw.rect(screen, color, pos, width)
    # # 上下边框占用了 Y: 0 26*20
    # for i in range(board_height - 1):
    #     pos = 0, 20 + i * 20, 20, 20
    #     pygame.draw.rect(screen, color, pos, width)
    #     pos = (board_width - 1) * 20, 20 + i * 20, 20, 20
    #     pygame.draw.rect(screen, color, pos, width)


# 游戏失败
def game_over(snake):
    broad_x, broad_y = snake.get_head()
    flag = 0
    old = len(snake.item)
    new = len(set(snake.item))
    # 游戏失败的两种可能
    # 咬到自身
    if new < old:
        flag = 1
    # 撞到边框
    if broad_x == 0 or broad_x == BOARDWIDTH - 1:
        flag = 1
    if broad_y == 0 or broad_y == BOARDHEIGHT - 1:
        flag = 1

    if flag:
        return True
    else:
        return False


# 打印字符
def print_text(screen, font, x, y, text, color=(255, 0, 0)):
    # 在屏幕上打印字符
    # text是需要打印的文本，color为字体颜色
    # (x,y)是文本在屏幕上的位置
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x, y))



# 按键
def press(keys, snake):
    global score
    # K_w 为 pygame.locals 中的常量
    # keys[K_w] 返回 True or False
    # 上移
    if keys[K_w] or keys[K_UP]:
        snake.toward(0, -1)
    # 下移
    elif keys[K_s] or keys[K_DOWN]:
        snake.toward(0, 1)
    # 左移
    elif keys[K_a] or keys[K_LEFT]:
        snake.toward(-1, 0)
    # 右移
    elif keys[K_d] or keys[K_RIGHT]:
        snake.toward(1, 0)
    # 重置游戏
    elif keys[K_r]:
        score = 0
        main()
    # 退出游戏
    elif keys[K_ESCAPE]:
        exit()


# 游戏初始化
def game_init():
    # pygame 初始化
    pygame.init()
    # 设置游戏界面大小
    screen = pygame.display.set_mode((BOARDWIDTH * 20, BOARDHEIGHT * 20))
    # 设置游戏标题
    pygame.display.set_caption('贪吃蛇')
    pygame.mixer.music.load('./bgm.mp3')
    pygame.mixer.music.set_volume(10)
    pygame.mixer.music.play(-1, 0.0)

    return screen


# 开始游戏
def game(screen):
    snake = Snake()
    food = Food()
    # 设置中文字体和大小
    font = pygame.font.Font('./FZSJ-XLLJW.TTF', 40)
    is_fail = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        # 填充屏幕
        screen.fill((0, 0, 100))
        init_board(screen=screen)
        # 获得用户按键命令
        keys = pygame.key.get_pressed()
        press(keys, snake)
        # 游戏失败打印提示
        if is_fail:
            print_text(screen, font, 400, 400, text)
            screen.blit(over, (150,30))
            screen.blit(time_image, (430, 450))
        # 游戏主进程
        if not is_fail:
            enlarge = snake.eat_food(food)
            text = "分数: {}".format(score)
            # 倒计时
            total_time = 0  # 分钟
            taken_time = pygame.time.get_ticks()  # 毫秒
            left_time = total_time * 60000 + taken_time  # 毫秒
            time_min = left_time // 60000
            time_sec = left_time % 60000 // 1000
            time_text = str(time_min).zfill(2) + ':' + str(time_sec).zfill(2)
            time_font = pygame.font.Font('./FZSJ-XLLJW.TTF', 44)
            time_image = time_font.render(time_text, True, (0, 0, 0))
            screen.blit(time_image, (800, 10))

            print_text(screen, font, 0, 0, text)
            food.update(screen, enlarge, snake)
            snake.move(enlarge)
            is_fail = game_over(snake=snake)
            snake.draw(screen)
        # 游戏刷新
        pygame.display.update()
        time.sleep(0.1)


# 主程序
def main():
    screen = game_init()
    game(screen)


if __name__ == '__main__':
    main()