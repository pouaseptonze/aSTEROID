import random

import pygame.image
from pygame import Rect
import core
from pygame.math import Vector2
import time
from win32api import GetSystemMetrics

largeur = 1600
hauteur = 800


def tir(canon, distance):
    """
    la variable canon contient la position du canon
    """
    angle = core.memory("Speed").angle_to(core.memory("Direction"))
    p = Vector2(canon.x, canon.y)
    v = Vector2(core.memory("Speed").x, core.memory("Speed").y)
    v.scale_to_length(core.memory("Speed").length() + 10)
    v = v.rotate(angle)
    r = 7
    c = (255, 255, 255)
    et = time.time() + distance
    st = time.time()
    d = {"position": p, "speed": v, "radius": r, "start time": st, "color": c, "end time": et}
    core.memory("projectile").append(d)


def restart(game_over):
    """
    La fonction sert à redémarrer quand on a perdu
    """
    core.memory("Start", 0)
    core.memory("target").append(asteroide())
    if game_over:
        core.memory("life", 2)
        core.memory("points", 0)


def asteroide():
    """
    la fonction retourne un carré qui représente l'astéroide à une position aléatoire
    """
    l = 50
    h = 50
    x = random.randint(0, largeur - l)
    y = random.randint(0, hauteur - l)
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
        et = time.time() + random.randint(1, 2)
        d = {"position": p, "speed": v, "radius": r, "start time": st, "color": c, "end time": et}
        core.memory("projectile").append(d)


def setup():
    core.fps = 60
    core.WINDOW_SIZE = [largeur, hauteur]
    core.memory("Position", Vector2(500, 500))
    core.memory("Speed", Vector2(5, 0))
    core.memory("Direction", Vector2(1, 0))
    core.memory("projectile", [])
    core.memory("target", [])
    #core.memory("target").append(asteroide())
    #core.memory("target").append(asteroide())
    core.memory("points", 0)
    core.memory("Start", 1)
    core.memory("life", 2)
    core.memory("collision_time", 0)
    core.memory("cadence_de_tir", 0.2)
    #core.memory("vie_des_projectiles", 2)


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
                if time.time() - core.memory("projectile")[-1]["start time"] > core.memory("cadence_de_tir"):
                    if core.memory("points") < 20:
                        tir(P2, 0.5)
                    else:
                        tir(P1, 1)
                        tir(P3, 2)

            else:
                tir(P2, 0.5)

        for proj in core.memory("projectile"):
            proj["position"] = proj["position"] + proj["speed"]
            core.Draw.circle(proj["color"], proj["position"], proj["radius"])
            if time.time() > proj["end time"]:
                core.memory("projectile").remove(proj)

        # gestion des astéroïdes

        for proj in core.memory("projectile"):
            for t in core.memory("target"):
                if t.collidepoint(proj["position"].x, proj["position"].y):
                    core.memory("target").append(asteroide())
                    core.memory("target").remove(t)
                    core.memory("points", core.memory("points") + 1)

        # Gestion des colisions
        for t in core.memory("target"):
            if (t.collidepoint(P2.x, P2.y) or t.collidepoint(P1.x, P1.y) or t.collidepoint(P3.x, P3.y)) and core.memory("Start") == 0:
                core.memory("collision_time", time.time())
                explosion()
                core.memory("target").remove(t)
                core.memory("life", core.memory("life") - 1)
                core.memory("Position", Vector2(largeur/2, hauteur/2))
                core.memory("target").append(asteroide())

                if core.memory("life") == 0:
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

            if core.memory("Position").x > largeur:
                core.memory("Position").x = 0
            elif core.memory("Position").x < 0:
                core.memory("Position").x = largeur

            if core.memory("Position").y > hauteur:
                core.memory("Position").y = 0
            elif core.memory("Position").y < 0:
                core.memory("Position").y = hauteur

            # core.Draw.line((255, 255, 0), (core.memory("Position").x, core.memory("Position").y), (
            #     core.memory("Position").x + core.memory("Speed").x * 50,
            #     core.memory("Position").y + core.memory("Speed").y * 50))

            # Draw

            core.Draw.polygon((255, 0, 0), (P1, P2, P3))
            core.Draw.text((255, 255, 255), "Points : " + str(core.memory("points")), (50, 50))
            core.Draw.text((255, 255, 255), "Nombres de vie : " + str(core.memory("life")), (largeur - 400, 50))
            for t in core.memory("target"):
                core.Draw.rect((255, 0, 255), t)

    else:

        # Initiation

        if core.memory("Start") == 1:
            core.Draw.text((255, 255, 255), "Appuyez sur une touche",
                           (largeur / 2, hauteur / 2))

        # Restart

        elif core.memory("Start") == 3:
            core.Draw.text((255, 255, 255), "GAME OVER", (largeur / 2, hauteur / 3))
            core.Draw.text((255, 255, 255), "Appuyez sur ECHAP pour quitter",(largeur / 2, hauteur / 4))
            core.Draw.text((255, 255, 255), "Appuyez sur R pour Relancer",(largeur*3 / 4, hauteur / 4))
            core.Draw.text((255, 255, 255), "Score : " + str(core.memory("points")), (largeur - 2500, 50))

            if core.getKeyPressList("ESCAPE"):
                exit()
            if core.getKeyPressList("r"):
                restart(True)

        if (core.getKeyPressList("RETURN") and core.memory("Start") == 2) or (core.getkeyPress() and core.memory("Start") == 1):
            restart(False)


core.main(setup, run)
