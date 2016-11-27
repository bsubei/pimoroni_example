#!/usr/bin/env python

import sys
import time

import unicornhat as unicorn

class Game(object):

    GRAVITY = 0.01
    JUMP_VELOCITY = -2.1
    FRAME_RATE = 60

    def __init__(self):

        unicorn.set_layout(unicorn.AUTO)
        unicorn.rotation(0)
        unicorn.brightness(0.5)
        self.width, self.height = unicorn.get_shape()

        self.player = Player([4.0, 0.0])
        self.grounds = [Ground([1.0 * x, 7.0]) for x in range(8)]
        self.obstacles = [Obstacle([7.0, 6.0])]
        
        # How fast the game progresses (independent of the framerate).
        self.tempo = 0.1

    def draw(self):

        # Clear all pixels
        unicorn.clear()

        for o in self.obstacles:
            # Draw each obstacle.
            pos = tuple([int(round(p)) for p in o.position])
            unicorn.set_pixel(*(pos + tuple(o.color)))

        for g in self.grounds:
            # Draw the ground .
            pos = tuple([int(round(p)) for p in g.position])
            unicorn.set_pixel(*(pos + tuple(g.color)))
        
        # Draw player.
        pos = tuple([int(round(p)) for p in self.player.position])
        unicorn.set_pixel(*(pos + tuple(self.player.color)))
            
        unicorn.show()

# TODO add something to make sure all objects are within bounds
    def do_physics(self):
        # Move all the obstacles based on the tempo.
        for o in self.obstacles:
            o.position[0] -= self.tempo

        # Gravity effect on player (change velocity).
        self.player.velocity[1] += Game.GRAVITY

        # Update position of player.
        self.player.position[1] += self.player.velocity[1]

        # TODO check obstacles colliding with player
        # Check for collision and react accordingly.
        # if collided, reset velocity and position
        if self.player.position[1] >= 6.0:
            self.player.position[1] = 6.0

        player_pos = [int(round(x)) for x in self.player.position]
        for o in self.obstacles:
            obs_pos = [int(round(x)) for x in o.position]
            if (player_pos == obs_pos):
                print("BOOM")
                # TODO react correctly

        # TODO cleanup obstacles that are out of screen


    def run(self, frame_rate):

        #while True:
        #    # TODO check for user input

        #    # Update physics and redraw everything.
        #    self.do_physics()
        #    self.draw()

        #    # HACK to implement fake (soft) frame_rate
        #    time.sleep(1.0 / Game.FRAME_RATE)


        print("started...")
        for x in range(3 * Game.FRAME_RATE):
            self.do_physics()
            self.draw()
            time.sleep(1.0 / Game.FRAME_RATE)
            
        print("jumping now!")
        self.player.jump()
        for x in range(3 * Game.FRAME_RATE):
            self.do_physics()
            self.draw()
            time.sleep(1.0 / Game.FRAME_RATE)

        
        return 0


    def print_intsructions():
        print("""oh hai TODO """) 


class Thing(object):
    def __init__(self, position):
        self.position = position

class Player(Thing):
    def __init__(self, position):
        super(Player, self).__init__(position)
        self.velocity = [0.0, 0.0]
        self.color = [255, 255, 255]

    def jump(self):
        self.velocity[1] += Game.JUMP_VELOCITY

class Obstacle(Thing):
    def __init__(self, position):
        super(Obstacle, self).__init__(position)
        self.velocity = [0.0, 0.0]
        self.color = [255, 0, 0]


class Ground(Thing):
    def __init__(self, position):
        super(Ground, self).__init__(position)
        self.velocity = [0.0, 0.0]
        self.color = [0, 255, 0]


if __name__ == '__main__':
    g = Game()
    sys.exit(g.run(Game.FRAME_RATE))