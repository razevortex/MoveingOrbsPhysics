import pygame as pg, sys
from GSimPkg.Engine import *
from GSimPkg.GetInput import *
from pygame.locals import *

pg.init()

FPS = 24    # frames per second setting
fpsClock = pg.time.Clock()

DISPLAY = pg.display.set_mode((1920, 1080), flags=pg.FULLSCREEN, depth=8)
DISPLAY.fill((127, 127, 127))

#set up the colors
black = (0,   0,   0)
white = (255, 255, 255)
red = (255,   0,   0)
green = (0, 255,   0)
blue = (0,   0, 255)

proc_in = ProcInput()
#PhyEngin = PhysEngin([GravObject(8, (50, 100), (2, 0)), GravObject(5, (600, 800), (-1, -1)), GravObject(3, (300, 450), (0, 1)) ])
PhyEngin = PhysEngin([])
run_engine = False
pg.display.update()

while True:
    if run_engine:
        PhyEngin.step()
    i = 0
    DISPLAY.fill((127, 127, 127))
    while True:
        if PhyEngin.get_draw_args(i) is not False:
            color, pos, mass, mod_dic = PhyEngin.get_draw_args(i)
            pg.draw.circle(DISPLAY, color, pos, mass, 0)
            if mod_dic['fixed']:
                pg.draw.circle(DISPLAY, black, pos, mass // 2, 0)
            if mod_dic['solid']:
                pg.draw.circle(DISPLAY, black, pos, mass, mass // 4)
            i += 1
        else:
            break
        pg.display.update()
    proc_in.mouse_tracker(pg.mouse.get_pos())
    if proc_in.edit_obj is not False:
        state, obj = proc_in._event_finalized()
        #print(state, obj.mass, obj.velocity)
        if obj != 'deleted':
            if state:
                    PhyEngin.PhysObjects.append(obj)
            else:

                color, pos, mass, mod_dic = obj.draw()
                pg.draw.circle(DISPLAY, white, pos, mass, 0)
                if mod_dic['fixed']:
                    pg.draw.circle(DISPLAY, black, pos, mass // 2, 0)
                if mod_dic['solid']:
                    pg.draw.circle(DISPLAY, black, pos, mass, mass // 4)
                pg.display.flip()
    else:
        state, cord, radius = proc_in._event_finalized()
        # proc_in.cout()
        if state:
            if proc_in.active_event:
                pg.draw.circle(DISPLAY, white, cord, radius, 0)
            else:
                PhyEngin.PhysObjects.append(GravObject(radius, cord, (0, 0)))
        pg.display.flip()
    fpsClock.tick(FPS)
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            PhyEngin.PhysObjects = proc_in.mouse_trigger(True, pg.mouse.get_pos(), PhyEngin.PhysObjects)
        if event.type == pg.MOUSEBUTTONUP:
            PhyEngin.PhysObjects = proc_in.mouse_trigger(False, pg.mouse.get_pos(), PhyEngin.PhysObjects)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                run_engine = not run_engine
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            else:
                proc_in.recieve_key(event.key)


