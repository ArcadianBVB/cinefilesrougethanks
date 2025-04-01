def prix_base_hd(type_, format_):
    """
    Retourne le tarif de base en HD (hors ajustement qualité et rareté),
    correspondant au tarif unitaire 'épisode' si c'est un type épisodique,
    ou au tarif global si c'est un type non épisodique.
    """
    # Types épisodiques : Série (1$), Novelas (1.5$), Dessin animé (1$ si court, 2$ si long),
    # Animé 3D (1$ si court, 3$ si long), Télé-réalité (1$), Émissions TV étrangères (1$),
    # Mangas (1$ si court, 2$ si long)
    # Types non épisodiques : Film (2$), Documentaire (3$), Spectacle (1$ si court, 3$ si long)
    if type_ == "Film":
        return 2
    elif type_ == "Série":
        return 1
    elif type_ == "Novelas":
        return 1.5
    elif type_ == "Dessin animé":
        if format_.lower() == "court métrage":
            return 1
        else:
            return 2
    elif type_ == "Animé 3D":
        if format_.lower() == "court métrage":
            return 1
        else:
            return 3
    elif type_ == "Télé-réalité":
        return 1
    elif type_ == "Émissions TV étrangères":
        return 1
    elif type_ == "Mangas":
        if format_.lower() == "court métrage":
            return 1
        else:
            return 2
    elif type_ == "Documentaire":
        return 3
    elif type_ == "Spectacle":
        if format_.lower() == "court métrage":
            return 1
        else:
            return 3
    else:
        return 0

def calculer_prix(type_, qualite, format_, rarete, saison, episodes):
    """
    1) On part d'un tarif de base HD via prix_base_hd(type_, format_).
    2) On ajuste selon la Qualité :
       - SD => /1.5
       - Full HD => x2
       - 4K => x4
       - Cam => x0.5
       - WebRip/BluRay => inchangé
    3) On ajoute +1$ si Rareté = "Rare".
    4) On applique la logique saison/épisodes :
       - (saison=none, episodes=none) => rien
       - (saison=none, episodes!=none) => tarif unitaire épisode déjà dans base
       - (saison!=none, episodes=none) => on multiplie par 4 (saison)
       - (saison!=none, episodes!=none) => priorité épisode => rien
    """
    # 1) Tarif de base en HD
    base = prix_base_hd(type_, format_)

    # 2) Ajustement Qualité
    if qualite == "SD":
        base /= 1.5
    elif qualite == "Full HD":
        base *= 2
    elif qualite == "4K":
        base *= 4
    elif qualite == "Cam":
        base *= 0.5
    # WebRip/BluRay => inchangé

    # 3) Rareté
    if rarete == "Rare":
        base += 1

    # 4) Saison / Episodes
    s = saison.strip().lower() if saison else "none"
    e = episodes.strip().lower() if episodes else "none"

    if s == "none" and e == "none":
        # ni saison ni épisode => rien de plus
        pass
    elif s == "none" and e != "none":
        # tarif unitaire épisode => déjà dans base
        pass
    elif s != "none" and e == "none":
        # tarif "saison" => on multiplie par 4
        base *= 4
    elif s != "none" and e != "none":
        # priorité à l'épisode => on ne touche pas
        pass

    return str(round(base, 2))
