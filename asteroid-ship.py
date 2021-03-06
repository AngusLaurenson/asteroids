''' first pygame '''
import pygame as pg
import scipy as sp

# initiate the pygame
pg.init()

# initiate the game window
width, height = 500, 500
window = pg.display.set_mode((500,500))
pg.display.set_caption("Asteroids.py")

# player spaceship properties
dv = 1
# angle
da      = 0.5

class newClass(object):
    """docstring for newClass."""
    def __init__(self, arg):
        super(newClass, self).__init__()
        self.arg = arg


# base class for objects in the game
class thing():
    """docstring for thing."""
    def __init__(self, size, position='None', velocity='None'):
        self.size = size

        # if no position or velocity given,
        # generate random number
        if position != 'None':
            self.position = position
        else:
            self.position = sp.random.rand(2) * width
        if velocity != 'None':
            self.velocity = velocity
        else:
            self.velocity = sp.random.rand(2) * 5

    def update_position(self):
        self.position = (self.position + self.velocity) % width

    def draw(self):
        self.image = pg.draw.rect(window,
        self.color,
        (self.position[0],self.position[1],self.size,self.size)
        )

# Asteroids as squares
class asteroid(thing):
    """docstring for asteroid."""
    def __init__(self):
        super(asteroid, self).__init__(size=20, position='None', velocity='None')
        self.color = (255,0,0)

# create player
class player(thing):
    """docstring for player."""
    def __init__(self):
        super(player, self).__init__(size=10,
        position=sp.array([width,height])/2,
        velocity=0
        )
        self.angle = 0
        self.color = (0,0,255)

    def user_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.angle -= da

        if keys[pg.K_RIGHT]:
            self.angle += da

        if keys[pg.K_UP]:
            self.velocity += dv * sp.array([sp.cos(self.angle), sp.sin(self.angle)])

        if keys[pg.K_SPACE]:
            # shoots
            pass

    def draw_arrow(self):
        # code for drawing line to show orientation
        pg.draw.line(window, (255,255,255), self.position + 5, self.position + 5 + (10*sp.cos(self.angle),10*sp.sin(self.angle)))

# create an asteroid
asterix = asteroid()
player1 = player()
bodies = [player1,asterix]


# control loop
run = True
while run:
    pg.time.delay(100)
    pg.key.set_repeat(1,10)

    for event in pg.event.get():
        # break loop if quit button used
        if event.type == pg.QUIT:
            run = False

    # clear the screen between frames
    window.fill((0,0,0))
    for body in bodies:
        if type(body) == player:
            body.user_input()
            body.draw_arrow()
        body.draw()
        body.update_position()

    # updates the position
    pg.display.update()

pg.quit()
