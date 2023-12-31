import random
import math
import game_framework

from pico2d import *

import game_world

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk']

class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombie/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]

    def __init__(self):
        self.x, self.y = random.randint(1600-800, 1600), 150
        self.load_images()
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])
        self.size_x = 200
        self.size_y = 200
        self.coll_size = 60


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 1600:
            self.dir = -1
        elif self.x < 800:
            self.dir = 1
        self.x = clamp(800, self.x, 1600)
        pass


    def draw(self):
        if self.dir < 0:
            Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, self.size_x, self.size_y)
        else:
            Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, self.size_x, self.size_y)
        # 디버그용 바운딩박스 그리기
        draw_rectangle(*self.get_bb())


    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'zombie:ball':
            self.size_x /= 2
            self.size_y /= 2
            self.y -= self.size_y /2
            self.coll_size /= 2

            if self.size_y <= 50 :
                game_world.remove_object(self)

    def get_bb(self):
        return self.x -self.coll_size, self.y -self.coll_size,self.x +self.coll_size, self.y +self.coll_size
