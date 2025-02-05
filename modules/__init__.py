"""
Ce fichier __init__.py permet à Python de reconnaître le dossier "modules"
comme un package. 
Il est nécessaire pour que les imports depuis "modules" fonctionnent correctement.
Par exemple, dans un autre fichier Python, on peut écrire :
    from modules.recup_url_yt import qualif_destination

Ce fichier peut rester vide, mais on peut aussi y ajouter des imports globaux
si nécessaire pour simplifier l'accès aux modules internes.

Exemple d'import global :
    from .recup_url_yt import qualif_destination
Ce qui permet ensuite d'importer directement :
    from modules import qualif_destination
"""


# (Laisse ce fichier vide si aucun import global n'est nécessaire)
