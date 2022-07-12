import copy
import pygame as pg
class ProcInput(object):
    def __init__(self):
        self.mouse_down = False
        self.cords = [(0, 0), (0, 0)]
        self.active_event = False
        self.edit_obj = False

    def mouse_trigger(self, event, cord, obj_list):
        self.mouse_down = event
        if self.mouse_down:
            self.cords[not event] = cord
            t_arr = []
            for obj in obj_list:
                if obj.mass >= int(sum(obj.distance_to(cord)) * -1):
                    self.edit_obj = copy.deepcopy(obj)
                    self.cords[not event] = self.edit_obj.cord
                else:
                    t_arr.append(obj)
            return t_arr
        #if obj_list:
        return obj_list
        #else:
        #    return []

    def mouse_tracker(self, cord):
        if self.mouse_down:
            self.cords[self.active_event] = cord
            self.active_event = True
        else:
            if self.active_event:
                self.cords[self.active_event] = cord
            else:
                self.cords = [(0, 0), (0, 0)]

    def _dist(self):
        dist = 0
        for a, b in zip(self.cords[0], self.cords[1]):
            if a < b:
                dist += a - b
            else:
                dist += b - a
        dist = dist if dist > 0 else dist * -1
        return dist

    def _vect(self):
        start, end = self.cords
        print(self.cords, '/', start, '/', end)
        return (end[0] - start[0]) // 10, (end[1] - start[1]) // 10

    def _event_finalized(self):
        if self.edit_obj:
            if self.mouse_down:
                return False, self.edit_obj
            elif self.active_event:
                if self.edit_obj != 'deleted':
                    self.edit_obj.velocity = self._vect()
                obj = copy.deepcopy(self.edit_obj)
                self.active_event = False
                self.edit_obj = False
                return True, obj
        else:
            if self.mouse_down:
                return True, self.cords[0], self._dist()
            elif self.active_event:
                self.active_event = False
                return True, self.cords[0], self._dist()
            else:
                return False, False, False

    def recieve_key(self, key):
        if self.edit_obj:
            if key == pg.K_s:
                self.edit_obj.solid = not self.edit_obj.solid
            if key == pg.K_f:
                self.edit_obj.fixed = not self.edit_obj.fixed
            if key == pg.K_DELETE:
                self.edit_obj = 'deleted'

    def cout(self):
        print(self.mouse_down, self.active_event)
        print(self.cords, self._dist())