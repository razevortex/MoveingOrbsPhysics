from random import randint as rng


class GravObject(object):
    def __init__(self, mass: int, cord_pos: tuple, cord_vel: tuple, blank=False):
        self.mass = mass
        self.cord = cord_pos
        self.velocity = cord_vel
        self.color = (0, 0, 0)
        if not blank:
            self.get_color()
        self.fixed = False
        self.solid = False

    def get_color(self):
        self.color = (rng(0, 254), rng(0, 254), rng(0, 254))

    def distance_to(self, cord, vectorized=False):
        if vectorized:
            return cord[0] - self.cord[0], cord[1] - self.cord[1]
        else:
            dist_vect = []
            for a, b in zip(self.cord, cord):
                dist = 0
                if a < b:
                    dist += a - b
                else:
                    dist += b - a
                dist_vect.append(dist)
            return dist_vect

    def velocity_delta(self, obj_list):
        for obj in obj_list:
            dist = self.distance_to(obj.cord, vectorized=True)
            #force_val = int(obj.mass) / (int(sum(self.distance_to(obj.cord))) ^ 2) * 0.5

            force_val = int(self.mass * obj.mass) / (int(sum(self.distance_to(obj.cord))) ^ 2) * float(obj.mass / (self.mass + obj.mass))
            self.velocity = (force_val * (dist[0] / sum(self.distance_to(obj.cord))) + self.velocity[0],
                             force_val * (dist[1] / sum(self.distance_to(obj.cord))) + self.velocity[1])

    def collide(self, obj):
        v0 = (self.velocity[0] * self.mass, self.velocity[1] * self.mass)
        v1 = (obj.velocity[0] * obj.mass, obj.velocity[1] * obj.mass)
        self.velocity = ((v0[0] + v1[0]) / 2, (v0[1] + v1[1]) / 2)
        print('collide vs :', v0, '/', v1, '=', self.velocity)
        self.mass += obj.mass
        self.color = ((self.color[0] + obj.color[0]) // 2,
                      (self.color[1] + obj.color[1]) // 2,
                      (self.color[2] + obj.color[2]) // 2,)

    def move_to(self):
        if not self.fixed:
            self.cord = [(x + y) for x, y in zip(self.cord, self.velocity)]

    def draw(self):
        #if run:
        #    self.move_to()
        return self.color, self.cord, self.mass, {'fixed': self.fixed, 'solid': self.solid }
