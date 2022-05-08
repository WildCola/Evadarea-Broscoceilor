import math

import pygame
import sys
from math import *
from copy import *
import itertools
import time
import os

def calc_dist(x, y):
    return sqrt(pow(x[0] - y[0], 2) + pow(x[1] - y[1], 2))

def punct_mal(x, y, r):
    rad = atan(y/x)
    if x < 0:
        rad += math.pi
    return r*cos(rad), r*sin(rad)


class Broasca:
    def __init__(self, nume, g, idfrunza):
        self.nume = nume
        self.idfrunza = idfrunza
        self.g = g
        self.afara = False

class Frunza:
    def __init__(self, id, x, y, nrInsecte, g):
        self.id = id
        self.x = x
        self.y = y
        self.poz = (x, y)
        self.nrInsecte = nrInsecte
        self.g = g

class Stare:
    def __init__(self, frunza, broasca, insecteMancate):
        self.frunza = frunza
        self.broasca = broasca
        self.insecteMancate = insecteMancate
        self.finala = False

class ParcurgeNod:
    def __init__(self, id, broaste, frunze, stari, tata, cost=0, h=0):
        self.id = id
        self.broaste = broaste
        self.frunze = frunze
        self.stari = stari
        self.tata = tata
        self.cost = cost
        self.h = h
        self.f = self.cost + self.h

    def obtineDrum(self):
        nod = self
        drum = [nod]
        while nod.tata:
            drum.insert(0, nod.tata)
            nod = nod.tata
        return drum

    def afisDrum(self):
        drum = self.obtineDrum()
        afis = ""
        for i in range(0, len(drum)):
            afis += f'{i + 1})\n'
            if i == 0:
                for s in drum[0].stari:
                    afis += f'{s.broasca.nume} se afla pe frunza initiala {s.frunza.id}{s.frunza.poz}. Greutate broscuta: {s.broasca.g}\n'
            else:
                for s in drum[i].stari:
                    afis += f'{s.broasca.nume} a mancat {s.insecteMancate} insecte. {s.broasca.nume} a sarit de la '
                    for staretata in drum[i - 1].stari:
                        if staretata.broasca.nume == s.broasca.nume:
                            if s.finala == False:
                                afis += f'{staretata.frunza.id}{staretata.frunza.poz} la {s.frunza.id}{s.frunza.poz}. Greutate broscuta: {s.broasca.g + s.insecteMancate - 1}\n'
                                break
                            else:
                                afis += f'{staretata.frunza.id}{staretata.frunza.poz} la mal. Greutate broscuta: {s.broasca.g + s.insecteMancate - 1}\n'
                                break
            afis += f'Stare frunze: '
            for f in drum[i].frunze:
                afis += f'{f.id}({f.nrInsecte},{f.g})'
                if f != drum[i].frunze[-1]:
                    afis += f', '
            afis += f'\n'

        return afis

    def cautaInsecteMancate(self, nod):
        insecte = 0
        nodCurent = self
        while nodCurent:
            if nodCurent.stare.nod.pozitie == nod.pozitie:
                insecte += nodCurent.stare.insecteMancate
            nodCurent = nodCurent.tata

    def __repr__(self):
        drum = self.obtineDrum()
        afis = ""
        for i in range(0, len(drum)):
            afis += f'{i + 1})\n'
            if i == 0:
                for s in drum[0].stari:
                    afis += f'{s.broasca.nume} se afla pe frunza initiala {s.frunza.id}{s.frunza.poz}. Greutate broscuta: {s.broasca.g}\n'
            else:
                for s in drum[i].stari:
                    afis += f'{s.broasca.nume} a mancat {s.insecteMancate} insecte. {s.broasca.nume} a sarit de la '
                    for staretata in drum[i-1].stari:
                        if staretata.broasca.nume == s.broasca.nume:
                            if s.finala == False:
                                afis += f'{staretata.frunza.id}{staretata.frunza.poz} la {s.frunza.id}{s.frunza.poz}. Greutate broscuta: {s.broasca.g + s.insecteMancate - 1}\n'
                                break
                            else:
                                afis += f'{staretata.frunza.id}{staretata.frunza.poz} la mal. Greutate broscuta: {s.broasca.g + s.insecteMancate - 1}\n'
                                break
            afis += f'Stare frunze: '
            for f in drum[i].frunze:
                afis += f'{f.id}({f.nrInsecte},{f.g})'
                if f != drum[i].frunze[-1]:
                    afis += f', '
            afis += f'\n'

        return afis



class Graph:
    def __init__(self, numeFisier, euristica = "banala"):
        self.euristica = euristica

        f = open(numeFisier, 'r')
        self.raza = int(f.readline())
        l = f.readline().split()

        self.broaste = []
        for i in range(0, len(l), 3):
            b = Broasca(l[i], int(l[i+1]), l[i+2])
            self.broaste.append(b)

        self.frunze = []
        l = f.readline().split()

        while l:
            frunze = Frunza(l[0], int(l[1]), int(l[2]), int(l[3]), int(l[4]))
            self.frunze.append(frunze)
            l = f.readline().split()

        #print(self.broaste[0].nume)
        #print(self.frunze[0].poz)

    def testeazaScop(self, stare: Stare):
        dist = self.raza - calc_dist(stare.frunza.poz, (0,0))

        if dist <= ((stare.broasca.g + stare.insecteMancate)/ 3) and stare.broasca.g + stare.insecteMancate > 1:
            return True
        else:
            return False

    def testeazaFinal(self, nod: ParcurgeNod):
        ok = True
        for stare in nod.stari:
            if stare.finala == False:
                ok = False
        return ok

    def genereazaSuccesori(self, tata: ParcurgeNod):

        def can_continue(nod):
            if self.testeazaFinal(nod):
                return True
            for stare in nod.stari:
                if stare.broasca.g + stare.frunza.nrInsecte <= 1:
                    return False
                frunza_mal = stare.frunza # caut cea mai apropiata frunza de mal
                for frunza in nod.frunze:
                    if calc_dist(frunza.poz, (0,0)) > calc_dist(frunza_mal.poz, (0,0)):
                        frunza_mal = frunza
                dist = self.raza - calc_dist(frunza_mal.poz, (0,0))
                gMax = max([frunza.g for frunza in nod.frunze])
                sumInsecte = sum([frunza.nrInsecte for frunza in nod.frunze]) + stare.broasca.g
                gMaxReala = min(gMax, sumInsecte)
                if dist > gMaxReala / 3:
                    return False
            return True


        succesori = []
        produsCartezian = []

        if not can_continue(tata): # Verificare daca din starile curente se poate ajunge in stari finale
            return []

        for b in tata.broaste:
            for f in deepcopy(tata.frunze):
                if b.idfrunza == f.id and b.afara == False:
                    stari = []
                    for i in range(0, f.nrInsecte+1):
                        stare = Stare(f, b, i)
                        stare.finala = self.testeazaScop(stare)
                        stari.append(stare)
                    produsCartezian.append(stari)
                    produsCartezian.append(tata.frunze)
                    break

        produsCartezian = list(itertools.product(*produsCartezian))

        elimMananca = []
        dictMuste = {}
        dictGreutate = {}
        for elem in produsCartezian:
            dictMuste.clear()
            dictGreutate.clear()
            for i in range(0, len(elem), 2):
                stare = elem[i]
                frunza = elem[i+1]
                #print(dictFrunze)
                if stare.finala == False:
                    if stare.frunza.id == frunza.id:
                        elimMananca.append(elem)
                        break
                    if stare.frunza.id in dictMuste.keys():
                        #print(dictMuste[stare.frunza.id])
                        dictMuste[stare.frunza.id] = dictMuste[stare.frunza.id] + stare.insecteMancate
                        #print(dictMuste[stare.frunza.id])
                    else:
                        dictMuste[stare.frunza.id] = stare.insecteMancate
                    #print(dictMuste)
                    #print()
                    if dictMuste[stare.frunza.id] > stare.frunza.nrInsecte:
                        #print(stare.frunza.nrInsecte)
                        elimMananca.append(elem)
                        break

                    if frunza.id in dictGreutate.keys():
                        dictGreutate[frunza.id] = dictGreutate[frunza.id] + stare.broasca.g + stare.insecteMancate - 1
                    else:
                        dictGreutate[frunza.id] = stare.broasca.g + stare.insecteMancate - 1
                    if dictGreutate[frunza.id] > frunza.g:
                        elimMananca.append(elem)
                        break

                    if (stare.broasca.g + stare.insecteMancate)/3 < calc_dist(stare.frunza.poz, frunza.poz):
                        elimMananca.append(elem)
                        break

                else:
                    if stare.frunza.id != frunza.id:
                        elimMananca.append(elem)
                        break

                if stare.broasca.g + stare.insecteMancate <= 1:
                    elimMananca.append(elem)
                    break

        # for elem in produsCartezian:
        #     for i in range(0, len(elem), 2):
        #         stare = elem[i]
        #         frunza = elem[i + 1]
        #         print(stare.broasca.nume, stare.insecteMancate, frunza.id)
        # print (len(produsCartezian))
        # print(len(elimMananca))

        for elem in elimMananca:
            produsCartezian.remove(elem)

        for elem in produsCartezian:
            cost = 0
            starisucc = []
            frunzesucc = deepcopy(tata.frunze)
            broastesucc = deepcopy(tata.broaste)
            for i in range(0, len(elem), 2):
                stare = elem[i]
                frunza = elem[i + 1]
                cost += calc_dist(stare.frunza.poz, frunza.poz)
                #print(stare.frunza.id, frunza.id, cost)
                # print(stare.broasca.nume + " " + stare.frunza.id + " " + str(stare.insecteMancate) + " " + frunza.id)
                for j in range(len(frunzesucc)):
                    if frunzesucc[j].id == stare.frunza.id:
                        #print(frunzesucc[j].nrInsecte)
                        frunzesucc[j].nrInsecte -= stare.insecteMancate
                        #print(frunzesucc[j].nrInsecte)
                        break
                for j in range(len(broastesucc)):
                    if broastesucc[j].nume == stare.broasca.nume:
                        broastesucc[j].idfrunza = frunza.id
                        broastesucc[j].g += stare.insecteMancate - 1
                        if stare.finala == True:
                            broastesucc[j].afara = True
                        break

                cpystare = deepcopy(stare)
                cpystare.frunza = frunza
                # print(cpystare.frunza.id)
                starisucc.append(cpystare)
                # else:
                #     broastesucc.remove(stare.broasca)

            if len(starisucc) == 0:
                return []
            h = self.calculeaza_h(starisucc)
            nodnou = ParcurgeNod(tata.id + 1, broastesucc, frunzesucc, starisucc, tata, tata.cost + cost, h)
            # if self.testeazaFinal(nodnou):
            #     for s in nodnou.stari:
            #         s.finala = True
            #     for b in nodnou.broaste:
            #         b.afara = True
            #     succesori = [nodnou]
            #     return succesori
            succesori.append(nodnou)
            # print()
            # for s in starisucc:
            #     print(s.frunza.id)
            # print()

        return succesori

        # for elem in produsCartezian:
        #     for i in range(0, len(elem), 2):
        #         stare = elem[i]
        #         frunza = elem[i+1]
        #         print(stare.insecteMancate, frunza.id)
        # print(len(produsCartezian))


    def calculeaza_h(self, stari):
        if self.euristica == "banala":
            for s in stari:
                if self.testeazaScop(s):
                    return 0
            return 1
        elif self.euristica == "admisibila_1":
            dist = sys.maxsize
            def frunzeVecine(frunzaCurenta, salt: float):
                distCurenta = calc_dist(frunzaCurenta.poz, (0, 0))
                frunze = []
                for frunza in self.frunze:
                    dist = calc_dist(frunza.poz, (0, 0))
                    dif = calc_dist(frunza.poz, frunzaCurenta.poz)
                    if dif <= salt and dist > distCurenta:
                        frunze.append((frunza, dif))
                return frunze

            def bf(frunzaStart, gmax: float):
                lfrunze = [(frunzaStart, 0)]
                while len(lfrunze) > 0:
                    frunzaCurenta = lfrunze.pop(0)
                    b = Broasca("Aux", gmax, frunzaCurenta[0].id)
                    if self.testeazaScop(Stare(frunzaCurenta[0], b, 0)):
                        return frunzaCurenta[1]
                    frunzeUrm = frunzeVecine(frunzaCurenta[0], gmax/3)
                    for frunza in frunzeUrm:
                        if frunza not in lfrunze:
                            lfrunze.append((frunza[0], frunza[1] + frunzaCurenta[1]))
                return sys.maxsize

            for s in stari:
                gTotala = sum([frunza.nrInsecte for frunza in self.frunze]) # suma insectelor ce pot fi mancate
                gMaxima = max([frunza.g for frunza in self.frunze]) # greutatea maxima ce poate fi sustinuta de o frunza
                gMaxReala = min(gTotala, gMaxima)
                dist = min(bf(s.frunza, gMaxReala), dist)

            return dist

        elif self.euristica == "admisibila_2":
            dist = 0
            for s in stari:
                dist = max(self.raza - calc_dist(s.frunza.poz, (0,0)), dist)
            return dist

        elif self.euristica == "neadmisibila":
            h = 0
            for s in stari:
                dist = calc_dist(s.frunza.poz, self.frunze[0].poz)
                for i in range(1, len(self.frunze)):
                    if self.frunze[i].id != s.frunza.id and calc_dist(s.frunza.poz, (0,0)) > calc_dist(self.frunze[i].poz, (0,0)) :
                        dist += calc_dist(self.frunze[i-1].poz, self.frunze[i].poz)
                    h += dist
            return h






def breadth_first(g, timeout, nrSol=1):
    tstart = time.time()

    global lmaxSuc, lmaxCoada, lTimpi, sol, maxSuc, maxCoada
    sol = []
    lmaxCoada = []
    lmaxSuc = []
    lTimpi = []
    maxSuc = 0
    maxCoada = 0

    stari = []
    for b in g.broaste:
        for f in g.frunze:
            if b.idfrunza == f.id:
                stare = Stare(f, b, 0)
                stari.append(stare)
    q = [ParcurgeNod(1, g.broaste, g.frunze, stari, 0, g.calculeaza_h(stari))]
    while len(q) > 0:
        tcurent = time.time()
        if tcurent - tstart > timeout:
            print("Timp depasit!")
            return "timp_depasit"

        maxCoada = max(len(q), maxCoada)
        nodCurent = q.pop(0)
        #print(nodCurent)
        if g.testeazaFinal(nodCurent) == True:
            sol.append(nodCurent)
            lmaxCoada.append(maxCoada)
            lmaxSuc.append(maxSuc)
            timp = time.time()
            lTimpi.append(timp - tstart)

            print()
            print("Solutie: ")
            print(nodCurent)
            print("\n----------------\n")
            nrSol-=1
            if nrSol == 0:
                return sol

        lsuccesori = g.genereazaSuccesori(nodCurent)
        maxSuc = max(maxSuc, len(lsuccesori))
        q.extend(lsuccesori)
        #print(len(q))

def depth_first(g, timeout, nrSol=1):
    tstart = time.time()

    global sol, lmaxSuc, lmaxCoada, lTimpi, maxSuc, maxCoada
    sol = []
    lmaxSuc = []
    lmaxCoada = []
    lTimpi = []
    maxSuc = 0
    maxCoada = 0

    stari = []
    for b in g.broaste:
        for f in g.frunze:
            if b.idfrunza == f.id:
                stare = Stare(f, b, 0)
                stari.append(stare)
    nod = ParcurgeNod(1, g.broaste, g.frunze, stari, 0, g.calculeaza_h(stari))
    df(nod, nrSol, timeout, tstart)
    return sol

def df(nodCurent, nrSol, timeout, tstart):
    tcurent = time.time()
    if tcurent - tstart > timeout:
        print("Timp depasit!")
        return "timp_depasit"

    global maxSuc, maxCoada

    if nrSol <= 0:
        return nrSol
    if g.testeazaFinal(nodCurent) == True:
        global sol, lmaxSuc, lmaxCoada, lTimpi
        sol.append(nodCurent)
        lmaxCoada.append(maxCoada)
        lmaxSuc.append(maxSuc)
        timp = time.time()
        lTimpi.append(timp - tstart)

        print("Solutie: ")
        print(nodCurent)
        print("\n----------------\n")
        nrSol -= 1
        if nrSol == 0:
            return nrSol

    lsuccesori = g.genereazaSuccesori(nodCurent)
    maxSuc = max(maxSuc, len(lsuccesori))
    maxCoada += len(lsuccesori)
    for sc in lsuccesori:
        if nrSol != 0:
            nrSol = df(sc, nrSol, timeout, tstart)

    return nrSol

def depth_first_iterativ(g, timeout, nrSol=1):
    tstart = time.time()

    global lmaxSuc, lmaxCoada, lTimpi, sol, maxSuc, maxCoada
    sol = []
    lmaxCoada = []
    lmaxSuc = []
    lTimpi = []
    maxSuc = 0
    maxCoada = 0

    stari = []
    for b in g.broaste:
        for f in g.frunze:
            if b.idfrunza == f.id:
                stare = Stare(f, b, 0)
                stari.append(stare)
    nod = ParcurgeNod(1, g.broaste, g.frunze, stari, 0, g.calculeaza_h(stari))
    for i in range(5000):
        if nrSol == 0:
            return sol
        #print("**********\nAdnacime maxima :", i)
        nrSol = dfi(nod, i, nrSol, timeout, tstart)
    return sol

def dfi(nodCurent, adancime, nrSol, timeout, tstart):
    tcurent = time.time()
    if tcurent - tstart > timeout:
        print("Timp depasit!")
        return "timp_depasit"

    global maxSuc, maxCoada

    if adancime == 1 and g.testeazaFinal(nodCurent):
        global sol, lmaxSuc, lmaxCoada, lTimpi
        sol.append(nodCurent)
        lmaxCoada.append(maxCoada)
        lmaxSuc.append(maxSuc)
        timp = time.time()
        lTimpi.append(timp - tstart)

        print("Solutie: ")
        print(nodCurent)
        print("\n----------------\n")
        nrSol -= 1
        if nrSol == 0:
            return nrSol
    if adancime > 1:
        lsuccesori = g.genereazaSuccesori(nodCurent)
        maxSuc = max(maxSuc, len(lsuccesori))
        maxCoada += len(lsuccesori)
        for sc in lsuccesori:
            if nrSol != 0:
                nrSol = dfi(sc, adancime-1, nrSol, timeout, tstart)
    return nrSol


def a_star(g, timeout, nrSol=1):
    tstart = time.time()

    global lmaxSuc, lmaxCoada, lTimpi, sol
    sol = []
    lmaxCoada = []
    lmaxSuc = []
    lTimpi = []
    maxSuc = 0
    maxCoada = 0

    stari = []
    for b in g.broaste:
        for f in g.frunze:
            if b.idfrunza == f.id:
                stare = Stare(f, b, 0)
                stari.append(stare)
    q = [ParcurgeNod(1, g.broaste, g.frunze, stari, 0, g.calculeaza_h(stari))]
    while len(q) > 0:
        tcurent = time.time()
        if tcurent - tstart > timeout:
            print("Timp depasit!")
            return "timp_depasit"

        maxCoada = max(maxCoada, len(q))
        nodCurent = q.pop(0)
        if g.testeazaFinal(nodCurent):
            timp = time.time()
            sol.append(nodCurent)
            lmaxCoada.append(maxCoada)
            lmaxSuc.append(maxSuc)
            lTimpi.append(timp - tstart)
            print("Solutie: ")
            print(nodCurent)
            print("\n----------------\n")
            nrSol -= 1
            if nrSol == 0:
                return sol
        lsuccesori = g.genereazaSuccesori(nodCurent)
        maxSuc = max(maxSuc, len(lsuccesori))
        for s in lsuccesori:
            #print(s.f)
            i = 0
            gasit_loc = False
            for i in range(len(q)):
                if q[i].f >= s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                q.insert(i, s)
            else:
                q.append(s)

def a_star_optim(g, timeout):
    tstart = time.time()

    global lmaxSuc, lmaxCoada, lTimpi
    lmaxCoada = []
    lmaxSuc = []
    lTimpi = []
    maxSuc = 0
    maxCoada = 0

    stari = []
    for b in g.broaste:
        for f in g.frunze:
            if b.idfrunza == f.id:
                stare = Stare(f, b, 0)
                stari.append(stare)
    l_open = [ParcurgeNod(1, g.broaste, g.frunze, stari, 0, g.calculeaza_h(stari))]
    l_closed = []
    while len(l_open) > 0:
        tcurent = time.time()
        if tcurent - tstart > timeout:
            print("Timp depasit!")
            return "timp_depasit"

        maxCoada = max(len(l_open), maxCoada)

        nodCurent = l_open.pop(0)
        l_closed.append(nodCurent)
        if g.testeazaFinal(nodCurent):
            lmaxCoada.append(maxCoada)
            lmaxSuc.append(maxSuc)
            timp = time.time()
            lTimpi.append(timp - tstart)
            print("Solutie: ")
            print(nodCurent)
            return nodCurent
        lsuccesori = g.genereazaSuccesori(nodCurent)
        maxSuc = max(maxSuc, len(lsuccesori))
        for s in lsuccesori:
            gasitC = False
            for nodC in l_open:
                if s.stari == nodC.stari:
                    gasitC = True
                    if s.f >= nodC.f:
                        lsuccesori.remove(s)
                    else:
                        l_open.remove(nodC)
                    break
                if not gasitC:
                    for nodC in l_closed:
                        if s.stari == nodC.stari:
                            if s.f >= nodC.f:
                                lsuccesori.remove(s)
                            else:
                                l_closed.remove(nodC)
                            break

        for s in lsuccesori:
            i=0
            gasit_loc = False
            for i in range(len(l_open)):
                if l_open[i].f > s.f or (l_open[i].f == s.f and l_open[i].cost <= s.cost):
                    gasit_loc = True
                    break
            if gasit_loc:
                l_open.insert(i,s)
            else:
                l_open.append(s)

def ida_star(g, timeout, nrSol=1):
    tstart = time.time()

    global sol, lmaxSuc, lmaxCoada, lTimpi, maxSuc, maxCoada
    sol = []
    lmaxSuc = []
    lmaxCoada = []
    lTimpi = []
    maxSuc = 0
    maxCoada = 0

    stari = []
    for b in g.broaste:
        for f in g.frunze:
            if b.idfrunza == f.id:
                stare = Stare(f, b, 0)
                stari.append(stare)
    nod = ParcurgeNod(1, g.broaste, g.frunze, stari, 0, g.calculeaza_h(stari))
    limita = nod.f
    while True:
        nrSol, rez = construieste_drum(g, nod, limita, nrSol, timeout, tstart)
        if rez == "gata":
            break
        if rez == float('inf'):
            print("Nu mai exista solutii")
            break
        limita = rez
    return sol

def construieste_drum(g, nodCurent, limita, nrSol, timeout, tstart):
    global maxSuc, maxCoada, sol
    tcurent = time.time()
    if tcurent - tstart > timeout:
        print("Timp depasit!")
        #sol = "timp_depasit"
        return 0, "gata"
    if nodCurent.f > limita:
        return nrSol, nodCurent.f
    if g.testeazaFinal(nodCurent):
        global lmaxSuc, lmaxCoada, lTimpi
        lmaxCoada.append(maxCoada)
        lmaxSuc.append(maxSuc)
        timp = time.time()
        lTimpi.append(timp - tstart)
        sol.append(nodCurent)
        print("Solutie: ")
        print(nodCurent)
        #print(limita)
        print("\n----------------\n")
        nrSol -= 1
        if nrSol == 0:
            return 0, "gata"
    lsuccesori = g.genereazaSuccesori(nodCurent)
    maxSuc = max(maxSuc, len(lsuccesori))
    maxCoada += len(lsuccesori)
    minim = float('inf')
    for s in lsuccesori:
        nrSol, rez = construieste_drum(g, s, limita, nrSol, timeout, tstart)
        if rez == "gata":
            return 0, "gata"
        if rez < minim:
            minim = rez
    return nrSol, minim

def verifica_fisier(nume):
    def isfloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False
    def isint(num):
        try:
            int(num)
            return True
        except ValueError:
            return False
    f = open(nume, "r")
    l1 = f.readline().split()
    if len(l1) != 1 or isfloat(l1[0]) == False: # Verific sa am un singur element de tip float (raza lac) pe prima linie
        print("Linia 1 invalida!")
        False
    l2 = f.readline().split()
    if len(l2) % 3 != 0: # Verific ca linia doi sa aiba un multiplu de 3 elemente (nume, greutate, frunza)
        print("Linia 2 invalida!")
        return False
    for i in range(0, len(l2), 3):
        if isint(l2[i+1]) == False: # Verific ca greutatea broastei sa fie de tip int
            print("Greutate invalida")
            return False

    lista = f.readlines()
    if len(lista) == 0: # Verific sa am cel putin o frunza
        print("Nu exista frunze!")
        return False
    for linie in lista:
        linie = linie.split()
        if len(linie) != 5: # Verific sa am fix 5 elemente pe fiecare linie (id, x, y, nr insecte, greutate maxima)
            print("Numar invalid de elemente")
            return False
        if isfloat(linie[1]) == False or isfloat(linie[2]) == False or isint(linie[3]) == False or isint(linie[4]) == False:
            print("Tip invalid de elemente")
            return False # Verific ca coordonatele x,y sa fie float, iar nr insecte si greutatea sa fie int
        if calc_dist((int(linie[1]), int(linie[2])), (0, 0)) >= int(l1[0]):
            return False # Verific ca frunzele sa nu fie in afara lacului

    return True



fisiereInput = os.listdir(sys.argv[1])
fisiereOutput = os.listdir(sys.argv[2])
nrSol = int(sys.argv[3])
timeout = int(sys.argv[4])



while True:

    euristici = ["banala", "admisibila_1", "admisibila_2", "neadmisibila"]
    print("1. BFS")
    print("2. DFS")
    print("3. DFI")
    print("4. A STAR")
    print("5. A STAR OPTIMIZAT")
    print("6. IDA STAR")
    print("0. IESI\n")
    opt = int(input())

    if opt == 1:
        print((", ").join(fisiereInput))
        optInput = input("Alege fisier de intrare: ")
        if optInput in fisiereInput:
            caleInput = "folder_input/" + optInput
            if verifica_fisier(caleInput):
                g = Graph(caleInput)

                tstart = time.time()
                sol = breadth_first(g, timeout, nrSol)
                tstop = time.time()
                print("Durata de rulare: " + str(tstop - tstart))
                f = open("folder_output/output_" + optInput, "w")
                if sol == "timp_depasit":
                    f.write("Algoritmul a depasit limita de timp!")
                else:
                    i = 0
                    if sol != None:
                        for solutie in sol:
                            f.write(solutie.afisDrum())
                            f.write("\nLungimea drumului: " + str(len(solutie.obtineDrum()) - 1))
                            f.write("\nCostul drumului: " + str(solutie.cost))
                            f.write("\nTimp de gasire al solutiei: " + str(lTimpi[i]))
                            f.write("\nNumarul maxim de noduri: " + str(lmaxSuc[i]))
                            f.write("\nNumarul total de noduri: " + str(lmaxCoada[i]))
                            f.write("\n\n--------------------\n\n")
                            i += 1

                            anim = input("Vizioneaza animatie (y/n): ")
                            if anim == "y":
                                pygame.init()
                                screen = pygame.display.set_mode((g.raza * 100 + 50, g.raza * 100 + 50))
                                pygame.display.set_caption("Evadarea broscoceilor")
                                drum = solutie.obtineDrum()
                                for nod in drum:
                                    screen.fill((10, 200, 10))
                                    pygame.draw.circle(screen, (0, 0, 150), (g.raza * 50 + 25, g.raza * 50 + 25),
                                                       g.raza * 50)
                                    for frunza in g.frunze:
                                        pygame.draw.circle(screen, (10, 240, 15),
                                                           ((g.raza + frunza.x) * 50 + 25,
                                                            (g.raza - frunza.y) * 50 + 25),
                                                           10)
                                    for stare in nod.stari:
                                        if stare.finala:
                                            if stare.frunza.x == 0:
                                                if stare.frunza.y > 0:
                                                    ymal = g.raza
                                                else:
                                                    ymal = g.raza * -1
                                                pygame.draw.circle(screen, (0, 0, 0),
                                                                   ((g.raza + 0) * 50 + 25, (g.raza - ymal) * 50 + 25),
                                                                   5)
                                            else:
                                                xmal, ymal = punct_mal(stare.frunza.x, stare.frunza.y, g.raza)
                                                pygame.draw.circle(screen, (0,0,0),
                                                                   ((g.raza + xmal) * 50 + 25, (g.raza - ymal) * 50 + 25),
                                                                    5)
                                        else:
                                            pygame.draw.circle(screen, (0,0,0),
                                                               ((g.raza + stare.frunza.x) * 50 + 25, (g.raza - stare.frunza.y) * 50 + 25),
                                                               5)
                                    pygame.display.update()
                                    run = True
                                    while run:
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                run = False
                                                pygame.quit()
                                            if event.type == pygame.MOUSEBUTTONUP:
                                                run = False
                                pygame.quit()

                    else:
                        f.write("Nu exista solutie!")
                f.close()

            else:
                print("Date de intrare invalide!")
        else:
            print("Fisier de intrare invalid!")

    elif opt == 2:
        print((", ").join(fisiereInput))
        optInput = input("Alege fisier de intrare: ")
        if optInput in fisiereInput:
            caleInput = "folder_input/" + optInput
            if verifica_fisier(caleInput):
                g = Graph(caleInput)
                tstart = time.time()
                sol = depth_first(g, timeout, nrSol)
                tstop = time.time()
                print("Durata de rulare: " + str(tstop - tstart))
                f = open("folder_output/output_" + optInput, "w")
                if tstop - tstart > timeout:
                    f.write("Algoritmul a depasit limita de timp!")
                elif sol == []:
                    f.write("Nu exista solutie!")
                else:
                    i = 0
                    if sol != None:
                        for solutie in sol:
                            f.write(solutie.afisDrum())
                            f.write("\nLungimea drumului: " + str(len(solutie.obtineDrum()) - 1))
                            f.write("\nCostul drumului: " + str(solutie.cost))
                            f.write("\nTimp de gasire al solutiei: " + str(lTimpi[i]))
                            f.write("\nNumarul maxim de noduri: " + str(lmaxSuc[i]))
                            f.write("\nNumarul total de noduri: " + str(lmaxCoada[i]))
                            f.write("\n\n--------------------\n\n")
                            i += 1

                            anim = input("Vizioneaza animatie (y/n): ")
                            if anim == "y":
                                pygame.init()
                                screen = pygame.display.set_mode((g.raza * 100 + 50, g.raza * 100 + 50))
                                pygame.display.set_caption("Evadarea broscoceilor")
                                drum = solutie.obtineDrum()
                                for nod in drum:
                                    screen.fill((10, 200, 10))
                                    pygame.draw.circle(screen, (0, 0, 150), (g.raza * 50 + 25, g.raza * 50 + 25),
                                                       g.raza * 50)
                                    for frunza in g.frunze:
                                        pygame.draw.circle(screen, (10, 240, 15),
                                                           ((g.raza + frunza.x) * 50 + 25,
                                                            (g.raza - frunza.y) * 50 + 25),
                                                           10)
                                    for stare in nod.stari:
                                        if stare.finala:
                                            if stare.frunza.x == 0:
                                                if stare.frunza.y > 0:
                                                    ymal = g.raza
                                                else:
                                                    ymal = g.raza * -1
                                                pygame.draw.circle(screen, (0, 0, 0),
                                                                   ((g.raza + 0) * 50 + 25, (g.raza - ymal) * 50 + 25),
                                                                   5)
                                            else:
                                                xmal, ymal = punct_mal(stare.frunza.x, stare.frunza.y, g.raza)
                                                pygame.draw.circle(screen, (0, 0, 0),
                                                                   ((g.raza + xmal) * 50 + 25,
                                                                    (g.raza - ymal) * 50 + 25),
                                                                   5)
                                        else:
                                            pygame.draw.circle(screen, (0, 0, 0),
                                                               ((g.raza + stare.frunza.x) * 50 + 25,
                                                                (g.raza - stare.frunza.y) * 50 + 25),
                                                               5)
                                    pygame.display.update()
                                    run = True
                                    while run:
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                run = False
                                                pygame.quit()
                                            if event.type == pygame.MOUSEBUTTONUP:
                                                run = False
                                pygame.quit()

                    else:
                        f.write("Nu exista solutie!")
                f.close()

            else:
                print("Date de intrare invalide!")
        else:
            print("Fisier de intrare invalid!")

    elif opt == 3:
        print((", ").join(fisiereInput))
        optInput = input("Alege fisier de intrare: ")
        if optInput in fisiereInput:
            caleInput = "folder_input/" + optInput
            if verifica_fisier(caleInput):
                g = Graph(caleInput)
                tstart = time.time()
                sol = depth_first_iterativ(g, timeout, nrSol)
                tstop = time.time()
                print("Durata de rulare: " + str(tstop - tstart))
                f = open("folder_output/output_" + optInput, "w")
                if tstop - tstart > timeout:
                    f.write("Algoritmul a depasit limita de timp!")
                elif sol == []:
                    f.write("Nu exista solutie!")
                else:
                    i = 0
                    if sol != None:
                        for solutie in sol:
                            f.write(solutie.afisDrum())
                            f.write("\nLungimea drumului: " + str(len(solutie.obtineDrum()) - 1))
                            f.write("\nCostul drumului: " + str(solutie.cost))
                            f.write("\nTimp de gasire al solutiei: " + str(lTimpi[i]))
                            f.write("\nNumarul maxim de noduri: " + str(lmaxSuc[i]))
                            f.write("\nNumarul total de noduri: " + str(lmaxCoada[i]))
                            f.write("\n\n--------------------\n\n")
                            i += 1

                            anim = input("Vizioneaza animatie (y/n): ")
                            if anim == "y":
                                pygame.init()
                                screen = pygame.display.set_mode((g.raza * 100 + 50, g.raza * 100 + 50))
                                pygame.display.set_caption("Evadarea broscoceilor")
                                drum = solutie.obtineDrum()
                                for nod in drum:
                                    screen.fill((10, 200, 10))
                                    pygame.draw.circle(screen, (0, 0, 150), (g.raza * 50 + 25, g.raza * 50 + 25),
                                                       g.raza * 50)
                                    for frunza in g.frunze:
                                        pygame.draw.circle(screen, (10, 240, 15),
                                                           ((g.raza + frunza.x) * 50 + 25,
                                                            (g.raza - frunza.y) * 50 + 25),
                                                           10)
                                    for stare in nod.stari:
                                        if stare.finala:
                                            if stare.frunza.x == 0:
                                                if stare.frunza.y > 0:
                                                    ymal = g.raza
                                                else:
                                                    ymal = g.raza * -1
                                                pygame.draw.circle(screen, (0, 0, 0),
                                                                   ((g.raza + 0) * 50 + 25, (g.raza - ymal) * 50 + 25),
                                                                   5)
                                            else:
                                                xmal, ymal = punct_mal(stare.frunza.x, stare.frunza.y, g.raza)
                                                pygame.draw.circle(screen, (0, 0, 0),
                                                                   ((g.raza + xmal) * 50 + 25,
                                                                    (g.raza - ymal) * 50 + 25),
                                                                   5)
                                        else:
                                            pygame.draw.circle(screen, (0, 0, 0),
                                                               ((g.raza + stare.frunza.x) * 50 + 25,
                                                                (g.raza - stare.frunza.y) * 50 + 25),
                                                               5)
                                    pygame.display.update()
                                    run = True
                                    while run:
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                run = False
                                                pygame.quit()
                                            if event.type == pygame.MOUSEBUTTONUP:
                                                run = False
                                pygame.quit()
                    else:
                        f.write("Nu exista solutie!")
                f.close()

            else:
                print("Date de intrare invalide!")
        else:
            print("Fisier de intrare invalid!")

    elif opt == 4:
        print((", ").join(fisiereInput))
        optInput = input("Alege fisier de intrare: ")
        if optInput in fisiereInput:
            caleInput = "folder_input/" + optInput
            if verifica_fisier(caleInput):
                print((", ").join(euristici))
                eur = input("Alege euristica: ")
                if eur in euristici:
                    g = Graph(caleInput, eur)
                    tstart = time.time()
                    sol = a_star(g, timeout, nrSol)
                    tstop = time.time()
                    print("Durata de rulare: " + str(tstop - tstart))
                    f = open("folder_output/output_" + optInput, "w")
                    if sol == "timp_depasit":
                        f.write("Algoritmul a depasit limita de timp!")
                    else:
                        i = 0
                        if sol != None:
                            for solutie in sol:
                                f.write(solutie.afisDrum())
                                f.write("\nLungimea drumului: " + str(len(solutie.obtineDrum()) - 1))
                                f.write("\nCostul drumului: " + str(solutie.cost))
                                f.write("\nTimp de gasire al solutiei: " + str(lTimpi[i]))
                                f.write("\nNumarul maxim de noduri: " + str(lmaxSuc[i]))
                                f.write("\nNumarul total de noduri: " + str(lmaxCoada[i]))
                                f.write("\n\n--------------------\n\n")
                                i += 1

                                anim = input("Vizioneaza animatie (y/n): ")
                                if anim == "y":
                                    pygame.init()
                                    screen = pygame.display.set_mode((g.raza * 100 + 50, g.raza * 100 + 50))
                                    pygame.display.set_caption("Evadarea broscoceilor")
                                    drum = solutie.obtineDrum()
                                    for nod in drum:
                                        screen.fill((10, 200, 10))
                                        pygame.draw.circle(screen, (0, 0, 150), (g.raza * 50 + 25, g.raza * 50 + 25),
                                                           g.raza * 50)
                                        for frunza in g.frunze:
                                            pygame.draw.circle(screen, (10, 240, 15),
                                                               ((g.raza + frunza.x) * 50 + 25,
                                                                (g.raza - frunza.y) * 50 + 25),
                                                               10)
                                        for stare in nod.stari:
                                            if stare.finala:
                                                if stare.frunza.x == 0:
                                                    if stare.frunza.y > 0:
                                                        ymal = g.raza
                                                    else:
                                                        ymal = g.raza * -1
                                                    pygame.draw.circle(screen, (0, 0, 0),
                                                                       ((g.raza + 0) * 50 + 25,
                                                                        (g.raza - ymal) * 50 + 25),
                                                                       5)
                                                else:
                                                    xmal, ymal = punct_mal(stare.frunza.x, stare.frunza.y, g.raza)
                                                    pygame.draw.circle(screen, (0, 0, 0),
                                                                       ((g.raza + xmal) * 50 + 25,
                                                                        (g.raza - ymal) * 50 + 25),
                                                                       5)
                                            else:
                                                pygame.draw.circle(screen, (0, 0, 0),
                                                                   ((g.raza + stare.frunza.x) * 50 + 25,
                                                                    (g.raza - stare.frunza.y) * 50 + 25),
                                                                   5)
                                        pygame.display.update()
                                        run = True
                                        while run:
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:
                                                    run = False
                                                    pygame.quit()
                                                if event.type == pygame.MOUSEBUTTONUP:
                                                    run = False
                                    pygame.quit()
                        else:
                            f.write("Nu exista solutie!")
                    f.close()

                else:
                    print("Euristica invalida!")
            else:
                print("Date de intrare invalide!")
        else:
            print("Fisier de intrare invalid!")

    elif opt == 5:
        print((", ").join(fisiereInput))
        optInput = input("Alege fisier de intrare: ")
        if optInput in fisiereInput:
            caleInput = "folder_input/" + optInput
            if verifica_fisier(caleInput):
                print((", ").join(euristici))
                eur = input("Alege euristica: ")
                if eur in euristici:
                    g = Graph(caleInput, eur)
                    tstart = time.time()
                    sol = a_star_optim(g, timeout)
                    tstop = time.time()
                    print("Durata de rulare: " + str(tstop - tstart))
                    f = open("folder_output/output_" + optInput, "w")
                    if sol == "timp_depasit":
                        f.write("Algoritmul a depasit limita de timp!")
                    elif sol == None:
                        f.write("Nu exista solutie!")
                    else:
                        f.write(sol.afisDrum())
                        f.write("\nLungimea drumului: " + str(len(sol.obtineDrum()) - 1))
                        f.write("\nCostul drumului: " + str(sol.cost))
                        f.write("\nTimp de gasire al solutiei: " + str(lTimpi[0]))
                        f.write("\nNumarul maxim de noduri: " + str(lmaxSuc[0]))
                        f.write("\nNumarul total de noduri: " + str(lmaxCoada[0]))
                        f.write("\n\n--------------------\n\n")

                        anim = input("Vizioneaza animatie (y/n): ")
                        if anim == "y":
                            pygame.init()
                            screen = pygame.display.set_mode((g.raza * 100 + 50, g.raza * 100 + 50))
                            pygame.display.set_caption("Evadarea broscoceilor")
                            drum = sol.obtineDrum()
                            for nod in drum:
                                screen.fill((10, 200, 10))
                                pygame.draw.circle(screen, (0, 0, 150), (g.raza * 50 + 25, g.raza * 50 + 25),
                                                   g.raza * 50)
                                for frunza in g.frunze:
                                    pygame.draw.circle(screen, (10, 240, 15),
                                                       ((g.raza + frunza.x) * 50 + 25,
                                                        (g.raza - frunza.y) * 50 + 25),
                                                       10)
                                for stare in nod.stari:
                                    if stare.finala:
                                        if stare.frunza.x == 0:
                                            if stare.frunza.y > 0:
                                                ymal = g.raza
                                            else:
                                                ymal = g.raza * -1
                                            pygame.draw.circle(screen, (0, 0, 0),
                                                               ((g.raza + 0) * 50 + 25, (g.raza - ymal) * 50 + 25),
                                                               5)
                                        else:
                                            xmal, ymal = punct_mal(stare.frunza.x, stare.frunza.y, g.raza)
                                            pygame.draw.circle(screen, (0, 0, 0),
                                                               ((g.raza + xmal) * 50 + 25,
                                                                (g.raza - ymal) * 50 + 25),
                                                               5)
                                    else:
                                        pygame.draw.circle(screen, (0, 0, 0),
                                                           ((g.raza + stare.frunza.x) * 50 + 25,
                                                            (g.raza - stare.frunza.y) * 50 + 25),
                                                           5)
                                pygame.display.update()
                                run = True
                                while run:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            run = False
                                            pygame.quit()
                                        if event.type == pygame.MOUSEBUTTONUP:
                                            run = False
                            pygame.quit()
                    f.close()

                else:
                    print("Euristica invalida!")
            else:
                print("Date de intrare invalide!")
        else:
            print("Fisier de intrare invalid!")

    elif opt == 6:
        print((", ").join(fisiereInput))
        optInput = input("Alege fisier de intrare: ")
        if optInput in fisiereInput:
            caleInput = "folder_input/" + optInput
            if verifica_fisier(caleInput):
                print((", ").join(euristici))
                eur = input("Alege euristica: ")
                if eur in euristici:
                    g = Graph(caleInput, eur)
                    tstart = time.time()
                    sol = ida_star(g, timeout, nrSol)
                    tstop = time.time()
                    print("Durata de rulare: " + str(tstop - tstart))
                    f = open("folder_output/output_" + optInput, "w")
                    if sol == "timp_depasit":
                        f.write("Algoritmul a depasit limita de timp!")
                    else:
                        i = 0
                        if sol != None:
                            for solutie in sol:
                                f.write(solutie.afisDrum())
                                f.write("\nLungimea drumului: " + str(len(solutie.obtineDrum()) - 1))
                                f.write("\nCostul drumului: " + str(solutie.cost))
                                f.write("\nTimp de gasire al solutiei: " + str(lTimpi[i]))
                                f.write("\nNumarul maxim de noduri: " + str(lmaxSuc[i]))
                                f.write("\nNumarul total de noduri: " + str(lmaxCoada[i]))
                                f.write("\n\n--------------------\n\n")
                                i += 1

                                anim = input("Vizioneaza animatie (y/n): ")
                                if anim == "y":
                                    pygame.init()
                                    screen = pygame.display.set_mode((g.raza * 100 + 50, g.raza * 100 + 50))
                                    pygame.display.set_caption("Evadarea broscoceilor")
                                    drum = solutie.obtineDrum()
                                    for nod in drum:
                                        screen.fill((10, 200, 10))
                                        pygame.draw.circle(screen, (0, 0, 150), (g.raza * 50 + 25, g.raza * 50 + 25),
                                                           g.raza * 50)
                                        for frunza in g.frunze:
                                            pygame.draw.circle(screen, (10, 240, 15),
                                                               ((g.raza + frunza.x) * 50 + 25,
                                                                (g.raza - frunza.y) * 50 + 25),
                                                               10)
                                        for stare in nod.stari:
                                            if stare.finala:
                                                if stare.frunza.x == 0:
                                                    if stare.frunza.y > 0:
                                                        ymal = g.raza
                                                    else:
                                                        ymal = g.raza * -1
                                                    pygame.draw.circle(screen, (0, 0, 0),
                                                                       ((g.raza + 0) * 50 + 25,
                                                                        (g.raza - ymal) * 50 + 25),
                                                                       5)
                                                else:
                                                    xmal, ymal = punct_mal(stare.frunza.x, stare.frunza.y, g.raza)
                                                    pygame.draw.circle(screen, (0, 0, 0),
                                                                       ((g.raza + xmal) * 50 + 25,
                                                                        (g.raza - ymal) * 50 + 25),
                                                                       5)
                                            else:
                                                pygame.draw.circle(screen, (0, 0, 0),
                                                                   ((g.raza + stare.frunza.x) * 50 + 25,
                                                                    (g.raza - stare.frunza.y) * 50 + 25),
                                                                   5)
                                        pygame.display.update()
                                        run = True
                                        while run:
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:
                                                    run = False
                                                    pygame.quit()
                                                if event.type == pygame.MOUSEBUTTONUP:
                                                    run = False
                                    pygame.quit()
                        else:
                            f.write("Nu exista solutie!")
                    f.close()

                else:
                    print("Euristica invalida!")
            else:
                print("Date de intrare invalide!")
        else:
            print("Fisier de intrare invalid!")

    else:
        break