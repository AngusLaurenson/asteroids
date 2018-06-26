''' first pygame '''
import pygame as pg
import scipy as sp

# initiate the pygame
pg.init()

# initiate the game window
width, height = 500, 500
window = pg.display.set_mode((500,500))
pg.display.set_caption("Asteroids.py")

''' CLASS HIERARCHY '''
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

    def draw_rect(self):
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
        self.dangle = 0.5 # radians
        self.acceleration = 1 # pixel per loop ** 2
        self.draw_rect()

    def user_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.angle -= self.dangle

        if keys[pg.K_RIGHT]:
            self.angle += self.dangle

        if keys[pg.K_UP]:
            self.velocity += self.acceleration * sp.array([sp.cos(self.angle), sp.sin(self.angle)])

        if keys[pg.K_SPACE]:
            # shoots
            self.shoot()

    def shoot(self):
        # create an instance of the bullet class
        bodies.append(bullet(self.position,self.angle,self.velocity))

    def draw_arrow(self):
        # code for drawing line to show orientation
        pg.draw.line(window, (255,255,255), self.position + 5, self.position + 5 + (10*sp.cos(self.angle),10*sp.sin(self.angle)))

class bullet(thing):
    """docstring for bullet."""
    def __init__(self, position, ship_angle, ship_velocity):
        super(bullet, self).__init__(size=2, position=position+5)
        self.color = (255,255,255)
        self.velocity = 20 * sp.array([sp.cos(ship_angle),sp.sin(ship_angle)]) + ship_velocity
        self.draw_rect()
        self.lifetime = 0

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

    # update position of all bodies
    for body1 in bodies:
        # capture user input
        if type(body1) == player:
            body1.user_input()
            body1.draw_arrow()

        # bullets time out
        if type(body1) == bullet:
            body1.lifetime += 1
            if body1.lifetime == 10:
                bodies.remove(body1)

        # update positions
        body1.draw_rect()
        body1.update_position()

    # check collisions for all body pairs
    for body1 in bodies:
        for body2 in [i for i in bodies if i != body1]:
            if body1.image.colliderect(body2.image):

                # if bullet hits asteroid delete both
                if (type(body1) == bullet and type(body2) == asteroid):
                    bodies.remove(body1)
                    bodies.remove(body2)

                # if player hits asteroid change color
                elif type(body1) == player and type(body2) == asteroid:
                    body1.color = (255,255,255)

    # updates the position
    pg.display.update()

    # check for endgame conditions
    # if len([i for i in bodies if type(i) == asteroid]) == 0:
    #     pg.quit()

pg.quit()
