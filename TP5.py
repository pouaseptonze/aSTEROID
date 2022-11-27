import core

# Exercice 1 :

n = int(input("Entrez un nombre positif non nul:"))
if n > 0:
    s = 0
    for i in range(-10, n):
        s = s + i * i + 5 * i + i / n
    print(s)
else:
    print("vous n'avez pas entré un nombre positif non nul:")

# Exercice 2

n = int(input("Entrez un nombre entier:"))
s = 0
for i in range(-n, n):
    if i != 0 and i != 5:
        s = s + i + 5 / i + 3 / i
    print(s)

# Exercice 3 :

n = str(input("Quel est votre mot ?"))
if list(reversed(n)) == list(n):
    print("is")
else:
    print("isn't")

# Exercice 4 :

n = int(input("Quel est votre nombre ?"))
liste = []
for i in range(1, n):
    if n % i == 0:
        liste.append(i)
if sum(liste) == n:
    print("is")
else:
    print("isn't")

# Exercice 5 :

from pygame.math import Vector2
from pygame.mouse import get_pos


def setup():
    core.fps = 30
    core.WINDOW_SIZE = [800, 800]
    core.memory("orientation", Vector2(1, 0))
    core.memory("Position", Vector2(400, 400))


def run():
    core.cleanScreen()

    P1 = core.memory("orientation").rotate(0)
    P1.scale_to_length(20)
    P11 = core.memory("Position") + P1

    P2 = core.memory("orientation").rotate(90)
    P2.scale_to_length(20)
    P22 = core.memory("Position") + P2

    P3 = core.memory("orientation").rotate(180)
    P3.scale_to_length(20)
    P33 = core.memory("Position") + P3

    P4 = core.memory("orientation").rotate(-90)
    P4.scale_to_length(20)
    P44 = core.memory("Position") + P4

    if core.getKeyReleaseList("q"):
        core.memory("orientation", core.memory("orientation").rotate(45))

    if core.getKeyReleaseList("d"):
        core.memory("orientation", core.memory("orientation").rotate(-45))

    core.Draw.polygon((255, 0, 0), (P11, P22, P33, P44))

    if core.getMouseLeftClick():
        core.memory("Position", Vector2(get_pos()))


core.main(setup, run)
