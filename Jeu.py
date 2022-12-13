import random
from pygame import Rect
import core
from pygame.math import Vector2
import time
from win32api import GetSystemMetrics

largeur = GetSystemMetrics(0)
hauteur = GetSystemMetrics(1)


def fond():
    core.memory("fond", core.Texture("./FOND.jpg", (1, 1), 0, (largeur, hauteur)))
    if not core.memory("fond").ready:
        core.memory("fond").load()
    core.memory("fond").show()


def level(nbasteroid, niveau):
    """
    la fonction détermine si on a détruit tous les astéroïdes pour changer de niveaux, en fonction des niveaux,
    elle génère des astéroïdes pour le niveau suivant
    """
    if nbasteroid < 1 or niveau == 0:
        niveau = niveau + 1
        if niveau > 1:
            core.memory("temps_niveau", time.time())
            core.memory("message", "Passage au niveau " + str(niveau))
        for i in range(1, 3 + 2 * niveau):
            creationtarget(niveau)
    return niveau


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
    if game_over:
        core.memory("life", 2)
        core.memory("points", 0)
        core.memory("level", 0)
        core.memory("target").clear()


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
        core.memory("debris").append(d)


def creationtarget(bonus_speed):
    Px = random.randint(50, largeur - 50)
    Py = random.randint(50, hauteur - 50)
    Vx = random.randint(-1 * bonus_speed, 1 * bonus_speed)
    Vy = random.randint(-1 * bonus_speed, 1 * bonus_speed)
    l = random.randint(50, 100)
    h = random.randint(50, 100)
    c = (random.randint(10, 250), random.randint(10, 250), random.randint(10, 250))
    targ = {"Px": Px, "Py": Py, "Vx": Vx, "Vy": Vy, "couleur": c, "largeur": l, "hauteur": h}
    core.memory("target").append(targ)


def creationpetittarget(Px, Py, l, h):
    Vx = random.randint(-1, 1)
    Vy = random.randint(-1, 1)
    c = (random.randint(10, 250), random.randint(10, 250), random.randint(10, 250))
    targ = {"Px": Px, "Py": Py, "Vx": Vx, "Vy": Vy, "couleur": c, "largeur": l, "hauteur": h}
    core.memory("target").append(targ)


def setup():
    core.fps = 60
    core.WINDOW_SIZE = [largeur, hauteur]
    core.memory("Position", Vector2(500, 500))
    core.memory("Speed", Vector2(2, 0))
    core.memory("Direction", Vector2(1, 0))
    core.memory("projectile", [])
    core.memory("level", 0)
    core.memory("points", 0)
    core.memory("Start", 1)
    core.memory("life", 2)
    core.memory("collision_time", 0)
    core.memory("cadence_de_tir", 0.2)
    core.memory("target", [])
    core.memory("debris", [])
    core.memory("tir", core.Sound("Tir.mp3"))
    core.memory("son_tir", 0)
    core.memory("message", "")
    core.memory("temps_niveau", 0)


def run():
    core.cleanScreen()

    fond()

    if time.time() - core.memory("collision_time") < 2:
        for proj in core.memory("debris"):
            proj["position"] = proj["position"] + proj["speed"]
            core.Draw.circle(proj["color"], proj["position"], proj["radius"])
            if time.time() > proj["end time"]:
                core.memory("debris").remove(proj)

    elif core.memory("Start") == 0:

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
            if time.time() - core.memory("son_tir") > 0.2:
                core.memory("son_tir", time.time())
                core.memory("tir").playin()
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

        # gestion des collisions avec les tirs

        for proj in core.memory("projectile"):
            for t in core.memory("target"):
                tr = Rect(t["Px"], t["Py"], t["largeur"], t["hauteur"])
                if tr.collidepoint(proj["position"].x, proj["position"].y):
                    if t["largeur"] / 2 > 26 or t["hauteur"] / 2 > 26:
                        creationpetittarget(t["Px"], t["Py"], t["largeur"] / 2, t["hauteur"] / 2)
                        creationpetittarget(t["Px"], t["Py"], t["largeur"] / 2, t["hauteur"] / 2)
                    core.memory("target").remove(t)
                    core.memory("projectile").clear()
                    core.memory("points", core.memory("points") + 1)

        # Gestion des colisions avec astéroides

        for t in core.memory("target"):
            tr = Rect(t["Px"], t["Py"], t["largeur"], t["hauteur"])
            if (tr.collidepoint(P2.x, P2.y) or tr.collidepoint(P1.x, P1.y) or tr.collidepoint(P3.x,
                                                                                              P3.y)) and core.memory(
                "Start") == 0:
                core.memory("collision_time", time.time())
                explosion()
                core.memory("target").remove(t)
                core.memory("life", core.memory("life") - 1)
                core.memory("Position", Vector2(largeur / 2, hauteur / 2))

            if core.memory("life") < 1:
                core.memory("Start", 3)

        # mouvement des astéroïdes

        for targ in core.memory("target"):
            targ["Px"] = targ["Px"] + targ["Vx"]
            targ["Py"] = targ["Py"] + targ["Vy"]

        # nombre de target
        core.memory("level", level(len(core.memory("target")), core.memory("level")))

        # Affichage changement de niveaux

        if time.time() - core.memory("temps_niveau") < 2:
            core.Draw.text((255, 255, 255), core.memory("message"), (largeur / 2, hauteur / 2))

        # bordure fenetre target
        for targ in core.memory("target"):
            if targ["Px"] > largeur:
                targ["Px"] = 0

        for targ in core.memory("target"):
            if targ["Px"] < 0:
                targ["Px"] = largeur

        for targ in core.memory("target"):
            if targ["Py"] > hauteur:
                targ["Py"] = 0

        for targ in core.memory("target"):
            if targ["Py"] < 0:
                targ["Py"] = hauteur

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

            # Draw

            core.Draw.polygon((255, 0, 0), (P1, P2, P3))
            core.Draw.text((255, 255, 255), "Points : " + str(core.memory("points")), (50, 50))
            core.Draw.text((255, 255, 255), "Nombre de vies : " + str(core.memory("life")), (largeur - 400, 50))
            core.Draw.text((255, 255, 255), "Level : " + str(core.memory("level")), (50, 100))
            for targ in core.memory("target"):
                core.Draw.rect(targ["couleur"], (targ["Px"], targ["Py"], targ["largeur"], targ["hauteur"]))

    else:

        # Initialisation

        if core.memory("Start") == 1:
            core.Draw.text((255, 255, 255), "Appuyez sur une touche",
                           (largeur / 2 - 150, hauteur / 2))

        # Restart

        elif core.memory("Start") == 3:
            core.Draw.text((255, 255, 255), "GAME OVER", (largeur / 2, hauteur / 3))
            core.Draw.text((255, 255, 255), "Appuyez sur ECHAP pour quitter", (largeur / 2, 100))
            core.Draw.text((255, 255, 255), "Appuyez sur R pour Relancer", (largeur / 2, 150))
            core.Draw.text((255, 255, 255), "Score : " + str(core.memory("points")), (largeur - 2500, 50))

            if core.getKeyPressList("ESCAPE"):
                exit()
            if core.getKeyPressList("r"):
                restart(True)

        if (core.getKeyPressList("RETURN") and core.memory("Start") == 2) or (
                core.getkeyPress() and core.memory("Start") == 1):
            restart(False)


core.main(setup, run)
