from .ObjClass import *

class PhysEngin(object):
    def __init__(self, obj_list):
        self.PhysObjects = obj_list

    def step(self):
        while self.collision_check() is not False:
            obj_a, obj_b = self.collision_check()
            obj_a.collide(obj_b)
            self.PhysObjects.remove(obj_b)
        for obj in self.PhysObjects:
            obj.velocity_delta([obj_b for obj_b in self.PhysObjects if obj != obj_b])
        for obj in self.PhysObjects:
            obj.move_to()

    def collision_check(self):
        for obj_a in self.PhysObjects:
            for objs in [obj for obj in self.PhysObjects if obj != obj_a]:
                if sum([obj_a.mass, objs.mass]) >= int(sum(obj_a.distance_to(objs.cord)) * -1):
                    return obj_a, objs
        return False

    def get_draw_args(self, obj_index):
        if self.PhysObjects:
            if obj_index >= len(self.PhysObjects):
                return False
            else:
                return self.PhysObjects[obj_index].draw()
        else:
            self.PhysObjects = []
            return False
