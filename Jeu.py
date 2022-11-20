import random

import pygame.image
from pygame import Rect
import core
from pygame.math import Vector2
import time
from win32api import GetSystemMetrics


def tir(canon):
    """
    la variable canon contient la position du canon
    """
    angle = core.memory("Speed").angle_to(core.memory("Direction"))
    p = Vector2(canon.x, canon.y)
    v = Vector2(core.memory("Speed").x, core.memory("Speed").y)
    v.scale_to_length(core.memory("Speed").length() + 10)
    v = v.rotate(angle)
    if core.memory("points") < 30:
        r = 5
    if core.memory("points") >= 30:
        r = 10
    c = (255, 255, 255)
    st = time.time()
    d = {"position": p, "speed": v, "radius": r, "start time": st, "color": c}
    core.memory("projectile").append(d)


def restart(game_over):
    """
    La fonction sert à redémarrer quand on a perdu
    """
    core.memory("Start", 0)
    core.memory("target", asteroide())
    if game_over:
        core.memory("life", 2)
        core.memory("points", 0)


def asteroide():
    """
    la fonction retourne un carré qui représente l'astéroide à une position aléatoire
    """
    l = 50
    h = 50
    x = random.randint(0, GetSystemMetrics(0) - l)
    y = random.randint(0, GetSystemMetrics(1) - l)
    return Rect(x, y, l, h)



def explosion():
    for i in range(50):
        p = Vector2(core.memory("Position").x, core.memory("Position").y)
        v = Vector2(core.memory("Speed").x, core.memory("Speed").y)
        v.scale_to_length(random.randint(10, 20))
        v = v.rotate(random.randint(0, 360))
        r = 10
        c = (random.randint(50, 255), 0, 0)
        st = time.time()
        d = {"position": p, "speed": v, "radius": r, "start time": st, "color": c}
        core.memory("projectile").append(d)


def setup():
    core.fps = 60
    core.WINDOW_SIZE = [GetSystemMetrics(0), GetSystemMetrics(1)]
    core.memory("Position", Vector2(500, 500))
    core.memory("Speed", Vector2(5, 0))
    core.memory("Direction", Vector2(1, 0))
    core.memory("projectile", [])
    core.memory("target", asteroide())
    core.memory("points", 0)
    core.memory("Start", 1)
    core.memory("life", 2)
    core.memory("collision_time", 0)


def run():
    if core.memory("Start") == 0:

        core.cleanScreen()

        # DEF points du vaisseau
        P1Bis = core.memory("Direction").rotate(90)
        P1Bis.scale_to_length(20)
        P1 = core.memory("Position") + P1Bis

        # Ici on calcule P2 qui est le nez du vaisseau et qu'on utilisera pour le départ des tirs

        P2Bis = core.memory("Direction").rotate(0)
        P2Bis.scale_to_length(50)
        P2 = core.memory("Position") + P2Bis

        P3Bis = core.memory("Direction").rotate(-90)
        P3Bis.scale_to_length(20)
        P3 = core.memory("Position") + P3Bis

        # gestion des projectiles

        if core.getKeyPressList("SPACE"):
            if len(core.memory("projectile")) > 0:
                if time.time() - core.memory("projectile")[-1]["start time"] > 0.2:
                    if core.memory("points") < 10:
                        tir(P2)
                    if 10 <= core.memory("points") < 20:
                        tir(P1)
                        tir(P3)
                    if core.memory("points") >= 20:
                        tir(P1)
                        tir(P2)
                        tir(P3)

            else:
                if core.memory("points") < 10:
                    tir(P2)
                if 10 <= core.memory("points") < 20:
                    tir(P1)
                    tir(P3)

        for proj in core.memory("projectile"):
            proj["position"] = proj["position"] + proj["speed"]
            core.Draw.circle(proj["color"], proj["position"], proj["radius"])
            if time.time() - proj["start time"] > 10:
                core.memory("projectile").remove(proj)

        # gestion des astéroïdes

        for proj in core.memory("projectile"):
            if core.memory("target").collidepoint(proj["position"].x, proj["position"].y):
                core.memory("target", asteroide())
                core.memory("points", core.memory("points") + 1)

        # Gestion des colisions

        if (core.memory("target").collidepoint(P2.x, P2.y) or core.memory("target").collidepoint(P1.x,P1.y) or core.memory("target").collidepoint(P3.x, P3.y)) and core.memory("Start") == 0:
            core.memory("collision_time", time.time())
            explosion()
            core.memory("life", core.memory("life") - 1)
            core.memory("Position", Vector2(GetSystemMetrics(0)/2, GetSystemMetrics(1)/2))
            core.memory("target", asteroide())

            if core.memory("life") == 0:
                core.memory("target", Rect(-100, -100, 50, 50))
                core.memory("Start", 3)

        # Movement

        if core.memory("collision_time") == 0 or time.time() - core.memory("collision_time") > 1.5:
            core.memory("collision_time", 0)
            core.memory("Position", core.memory("Position") + core.memory("Speed"))

            if core.getKeyPressList("d"):
                core.memory("Direction", core.memory("Direction").rotate(2))

            if core.getKeyPressList("q"):
                core.memory("Direction", core.memory("Direction").rotate(-2))

            if core.getKeyPressList("z"):
                # on double la vitesse quand on appuie sur Z
                core.memory("Position", core.memory("Position") + core.memory("Speed"))
                # on calcule les angles pour la rotation entre vitesse et direction
                a = core.memory("Speed").angle_to(core.memory("Direction"))
                b = core.memory("Direction").cross(core.memory("Speed"))
                if abs(a) > 1:

                    if b > 0:
                        core.memory("Speed", core.memory("Speed").rotate(-3))

                    else:
                        core.memory("Speed", core.memory("Speed").rotate(3))

            if core.getKeyPressList("s"):
                core.memory("Position", core.memory("Position") - 0.5 * core.memory("Speed"))

            if core.getKeyPressList("ESCAPE"):
                exit()

            # Screen

            if core.memory("Position").x > GetSystemMetrics(0):
                core.memory("Position").x = 0
            elif core.memory("Position").x < 0:
                core.memory("Position").x = GetSystemMetrics(0)

            if core.memory("Position").y > GetSystemMetrics(1):
                core.memory("Position").y = 0
            elif core.memory("Position").y < 0:
                core.memory("Position").y = GetSystemMetrics(1)

            # core.Draw.line((255, 255, 0), (core.memory("Position").x, core.memory("Position").y), (
            #     core.memory("Position").x + core.memory("Speed").x * 50,
            #     core.memory("Position").y + core.memory("Speed").y * 50))

            # Draw

            core.Draw.polygon((255, 0, 0), (P1, P2, P3))
            core.Draw.text((255, 255, 255), "Points : " + str(core.memory("points")), (50, 50))
            core.Draw.text((255, 255, 255), "Nombres de vie : " + str(core.memory("life")), (GetSystemMetrics(0) - 400, 50))
            core.Draw.rect((255, 0, 255), (core.memory("target").x, core.memory("target").y, 50, 50))

    else:

        # Initiation

        if core.memory("Start") == 1:
            core.Draw.text((255, 255, 255), "Appuyez sur une touche",
                           (GetSystemMetrics(0) / 2, GetSystemMetrics(1) / 2))

        # Restart

        elif core.memory("Start") == 3:
            core.Draw.text((255, 255, 255), "GAME OVER", (GetSystemMetrics(0) / 2, GetSystemMetrics(1) / 3))
            core.Draw.text((255, 255, 255), "Appuyez sur ECHAP pour quitter",(GetSystemMetrics(0) / 2, GetSystemMetrics(1) / 4))
            core.Draw.text((255, 255, 255), "Appuyez sur R pour Relancer",(GetSystemMetrics(0)*3 / 4, GetSystemMetrics(1) / 4))
            core.Draw.text((255, 255, 255), "Score : " + str(core.memory("points")), (GetSystemMetrics(0) - 2500, 50))

            if core.getKeyPressList("ESCAPE"):
                exit()
            if core.getKeyPressList("r"):
                restart(True)

        if (core.getKeyPressList("RETURN") and core.memory("Start") == 2) or (core.getkeyPress() and core.memory("Start") == 1):
            restart(False)


core.main(setup, run)
