from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, BooleanProperty
from kivy.clock import Clock

from random import choice, shuffle, randint


class Plane(Image):
    pass

class Projectile(Image):
    pass

class Blanc(Widget):
    pass

class Game(Widget):
    axe_a = NumericProperty(0)
    axe_b = NumericProperty(0)
    scor = NumericProperty(0)
    bscor = NumericProperty(0)
    velocity = NumericProperty(1)
    plane = ObjectProperty(None)
    playing = BooleanProperty(False)
    a = BooleanProperty(True)

    casset = []
        
    def projectileHeat(self):
        self.scor += 1
        if self.scor > self.bscor:
            self.bscor = self.scor
            self.saveScor()
        self.velocity += 0.05

    def cassetLoad(self):
        self.casset = [
            list("----------x-------------x--x-----------xx--x-------x-----x--------x---------x-------x---------xx--x----x------x---x----x-----x"),
            list("----xx---x---------x-x----x---x-----x---------xx------------x-x-------x---x------x---------xxx------x---x--x---x-----x-x--x---"),
            list("--x---x-------xxx---------------xx-------xx-----x-----x---------x------x-----xx--------xx--------x----------x-----x-------x--x"),
        ]
        self.casset[0].reverse()
        self.casset[1].reverse()
        self.casset[2].reverse()
        print('loard')

    def shuffle(self):
        # shuffle(self.casset)
        pass
        

    def click_right(self):
        if self.plane.center_x == self.axe_a:
            self.plane.center_x = self.axe_b
        elif self.plane.center_x == self.axe_b:
            self.plane.center_x = self.axe_c

    def click_left(self):
        if self.plane.center_x == self.axe_c:
            self.plane.center_x = self.axe_b
        elif self.plane.center_x == self.axe_b:
            self.plane.center_x = self.axe_a

    def on_touch_down(self, touch):
        if touch.pos[0] > self.center_x:
            self.click_right()
        if touch.pos[0] < self.center_x:
            self.click_left()
        self.play()
        # self.generateurProjectiles()

    def update(self, *args):
        if self.playing:
            self.generateurProjectiles()
            for widget in self.children:
                if widget.type == 'projectile' or widget.type == 'blanc':
                    widget.center_y -= self.velocity
                    if widget.top < 0:
                        self.remove_widget(widget)
                        if widget.type == 'projectile':
                            self.projectileHeat()
                    elif widget.type == 'projectile' and self.plane.collide_widget(widget):
                        self.gameOver()

    def generateurProjectiles(self):
        try:
            self.addA()
            self.addB()
            self.addC()
        except:
            self.cassetLoad()

    def addA(self):
        if self.aIsFree():
            x = self.casset[0].pop()
            if x == '-':
                blanc = Blanc()
                blanc.y = self.top
                blanc.center_x = self.center_x - 100
                self.add_widget(blanc)
            elif x == 'x':
                projectile = Projectile()
                projectile.source = f'./medias/projectiles/projectile{randint(1,15)}.png'
                projectile.y = self.top
                projectile.center_x = self.center_x - 100
                self.add_widget(projectile)

    def addB(self):
        if self.bIsFree():
            x = self.casset[1].pop()
            if x == '-':
                blanc = Blanc()
                blanc.y = self.top
                blanc.center_x = self.center_x
                self.add_widget(blanc)
            elif x == 'x':
                projectile = Projectile()
                projectile.source = f'./medias/projectiles/projectile{randint(1,15)}.png'
                projectile.y = self.top
                projectile.center_x = self.center_x
                self.add_widget(projectile)

    def addC(self):
        if self.cIsFree():
            x = self.casset[2].pop()
            if x == '-':
                blanc = Blanc()
                blanc.y = self.top
                blanc.center_x = self.center_x + 100
                self.add_widget(blanc)
            elif x == 'x':
                projectile = Projectile()
                projectile.source = f'./medias/projectiles/projectile{randint(1,15)}.png'
                projectile.y = self.top
                projectile.center_x = self.center_x + 100
                self.add_widget(projectile)

    def aIsFree(self):
        out = True
        for widget in self.children:
            if widget.center_x == self.center_x - 100:
                if widget.top > self.top - 2:
                    out = False
        return out

    def bIsFree(self):
        out = True
        for widget in self.children:
            if widget.center_x == self.center_x:
                if widget.top > self.top - 2:
                    out = False
        return out

    def cIsFree(self):
        out = True
        for widget in self.children:
            if widget.center_x == self.center_x + 100:
                if widget.top > self.top - 2:
                    out = False
        return out

    def addProjectile(self):
        projectile = Projectile()
        projectile.y = self.top
        projectile.center_x = choice([self.axe_a, self.axe_b, self.axe_c])
        self.add_widget(projectile)

    def gameOver(self):
        self.playing = False
        self.velocity = 1

    def play(self):
        if not self.playing:
            self.scor = 0
            self.clean()
            self.cassetLoad()
            self.shuffle()
            self.playing = True

    def clean(self):
        while len(self.children) > 3:
            for widget in self.children:
                if widget.type == 'projectile' or widget.type == 'blanc':
                    self.remove_widget(widget)

    def saveScor(self):
        with open('./.scor','w') as f:
            f.write(str(self.bscor))

    def loardScor(self):
        try:
            with open('./.scor','r') as f:
                self.bscor = int(f.read())
        except:
            self.bscor = 0

class FlightApp(App):
    def build(self):
        game = Game()
        game.loardScor()
        Clock.schedule_interval(game.update, 0.01)
        return game


if __name__ == '__main__':
    FlightApp().run()