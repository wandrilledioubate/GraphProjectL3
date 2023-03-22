import numpy as np
from collections import deque

def lire_contraintes(fichier):
    with open(fichier, 'r') as f:
        contraintes = [list(map(int, ligne.split())) for ligne in f.readlines()]
    return contraintes

def creer_matrice(contraintes):
    N = len(contraintes)
    matrice = np.zeros((N + 2, N + 2), dtype=int)

    for c in contraintes:
        tache, duree, *predecesseurs = c
        if not predecesseurs:
            matrice[0, tache] = duree
        for pred in predecesseurs:
            matrice[pred, tache] = duree

    for i in range(1, N + 1):
        if not np.any(matrice[i, :]):
            matrice[i, -1] = contraintes[i - 1][1]

    return matrice

def afficher_graphe_triplets(matrice):
    print("Création du graphe d'ordonnancement :")
    print(f"{len(matrice)} sommets")
    print(f"{sum(sum(1 for c in row if c != 0) for row in matrice)} arcs")

    for i, row in enumerate(matrice):
        for j, valeur in enumerate(row):
            if valeur != 0:
                print(f"{i} -> {j} = {valeur}")

def afficher_matrice_formattee(matrice):
    print("Matrice des valeurs")
    print(" " * 4, end="")
    for i in range(len(matrice)):
        print(f"{i:>3}", end=" ")
    print()

    for i, row in enumerate(matrice):
        print(f"{i:>3}", end="  ")
        for cell in row:
            if cell == 0:
                print(" * ", end=" ")
            else:
                print(f"{cell:>3}", end=" ")
        print()

def verifier_proprietes(matrice):
    # Vérifier qu'il n'y a pas de valeurs négatives
    if np.any(matrice < 0):
        return False

    # Vérifier qu'il n'y a pas de circuit
    N = len(matrice)
    etats = [0] * N
    q = deque([0])

    while q:
        u = q.popleft()
        etats[u] = 1
        for v in range(N):
            if matrice[u, v] != 0:
                if etats[v] == 1:
                    return False
                if etats[v] == 0:
                    q.append(v)
                    etats[v] = 1
        etats[u] = 2

    return True

def calculer_rangs(matrice):
    N = len(matrice)
    rangs = [0] * N
    q = deque([0])

    while q:
        u = q.popleft()
        for v in range(N):
            if matrice[u, v] != 0:
                rangs[v] = max(rangs[v], rangs[u] + 1)
                q.append(v)

    return rangs


def calculer_calendriers(matrice, rangs):
    N = len(matrice)
    au_plus_tot = [0] * N
    au_plus_tard = [0] * N
    marges = [0] * N

    q = deque([0])
    while q:
        u = q.popleft()
        for v in range(N):
            if matrice[u, v] != 0:
                au_plus_tot[v] = max(au_plus_tot[v], au_plus_tot[u] + matrice[u, v])
                q.append(v)

    au_plus_tard[-1] = au_plus_tot[-1]
    q = deque([N - 1])
    while q:
        u = q.popleft()
        for v in range(N):
            if matrice[v, u] != 0:
                au_plus_tard[v] = min(au_plus_tard[v] or au_plus_tard[u], au_plus_tard[u] - matrice[v, u])
                q.append(v)

    for i in range(N):
        marges[i] = au_plus_tard[i] - au_plus_tot[i]

    return au_plus_tot, au_plus_tard, marges


def chemins_critiques(matrice, marges):
    N = len(matrice)
    chemins = []

    def dfs(u, chemin):
        if u == N - 1:
            chemins.append(chemin)
        for v in range(N):
            if matrice[u, v] != 0 and marges[v] == 0:
                dfs(v, chemin + [(u, v)])

    dfs(0, [])
    return chemins


def afficher_resultats(matrice, rangs, au_plus_tot, au_plus_tard, marges, chemins_critiques):
    print("Matrice:")
    print(matrice)
    print("\nRangs des sommets:")
    print(rangs)
    print("\nCalendrier au plus tôt:")
    print(au_plus_tot)
    print("\nCalendrier au plus tard:")
    print(au_plus_tard)
    print("\nMarges:")
    print(marges)
    print("\nChemins critiques:")
    for chemin in chemins_critiques:
        print(" -> ".join(str(u) for u, _ in chemin))

def main():
    while True:
        fichier = input("Entrez le nom du fichier contenant le tableau de contraintes (.txt) ou 'q' pour quitter: ")
        if fichier == 'q':
            break

        contraintes = lire_contraintes(fichier)
        matrice = creer_matrice(contraintes)


        afficher_graphe_triplets(matrice)
        print()
        afficher_matrice_formattee(matrice)
        print()

        if verifier_proprietes(matrice):
            rangs = calculer_rangs(matrice)
            au_plus_tot, au_plus_tard, marges = calculer_calendriers(matrice, rangs)
            chemins_crit = chemins_critiques(matrice, marges)
            afficher_resultats(matrice, rangs, au_plus_tot, au_plus_tard, marges, chemins_crit)
        else:
            print("Le graphe ne possède pas toutes les propriétés nécessaires pour être un graphe d'ordonnancement.")

if __name__ == "__main__":
    main()
