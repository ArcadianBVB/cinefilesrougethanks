def prix_base_hd(type_, format_, saison=False, episodes=False):
    """
    Retourne un prix de base en HD (hors ajustements) selon le POV Cinéfiles.
    La base est définie pour la qualité HD.
    Pour les contenus épisodiques, si une saison complète est indiquée (saison renseignée et épisodes non renseignés),
    on renvoie le tarif de saison complète, sinon on renvoie le tarif unitaire.
    """
    format_ = format_.strip().lower()
    type_ = type_.strip().lower()

    if type_ == "film":
        return 2.0

    elif type_ == "série":
        return 4.0 if saison else 1.0

    elif type_ == "animé 3d":
        if format_ == "court métrage":
            return 4.0 if saison else 1.0
        return 2.0

    elif type_ == "novelas":
        if format_ == "court métrage":
            return 4.0 if saison else 1.0
        return 2.0

    elif type_ == "télé-réalité":
        return 4.0 if saison else 1.0

    elif type_ == "spectacle":
        if format_ == "court métrage":
            return 4.0 if saison else 0.8
        return 2.0

    elif type_ == "mangas":
        if format_ == "court métrage":
            return 4.0 if saison else 1.0
        return 2.0

    elif type_ == "dessin animé":
        if format_ == "court métrage":
            return 4.0 if saison else 0.8
        return 2.0

    elif type_ == "émissions télé":
        if format_ == "court métrage":
            return 0.8
        return 2.0

    else:
        return 0.0


def calculer_prix(type_, qualite, format_, rarete, saison, episodes):
    """
    Calcule le prix final selon le POV Cinéfiles.

    Règles :
    1. On part d'un tarif de base en HD (voir prix_base_hd) pour le type et le format.
    2. On ajuste ce tarif selon la qualité :
         - SD ou Web = base ÷ 1.5
         - Full HD = base × 2
         - 4K = base × 4
         - Cam = base × 0.5
         - BluRay = base inchangé
    3. Si rareté == "Rare", on ajoute 1 USD.
    4. Logique saison/épisodes :
         - Si ni saison ni épisodes ne sont renseignés → tarif unitaire (base calculé).
         - Si saison n'est pas renseignée mais épisodes renseignés → tarif unitaire.
         - Si saison est renseignée et épisodes ne le sont pas → on considère une saison complète (tarif unitaire × 4).
         - Si les deux sont renseignés → tarif unitaire.
    """
    # On détermine si on considère qu'il s'agit d'une saison complète
    s = saison.strip().lower() if saison and saison.strip() != "" else "none"
    e = episodes.strip().lower() if episodes and episodes.strip() != "" else "none"
    is_saison = s != "none"
    is_episode = e != "none"

    base = prix_base_hd(type_, format_, saison=is_saison, episodes=is_episode)

    qualite = qualite.strip().lower()
    if qualite in ["sd", "webrip"]:
        base /= 1.5
    elif qualite == "full hd":
        base *= 2
    elif qualite == "4k":
        base *= 4
    elif qualite == "cam":
        base *= 0.5
    # BluRay ou HD inchangé

    if rarete.strip().lower() == "rare":
        base += 1

    # Application de la logique saison/épisodes
    if s == "none" and e == "none":
        # tarif unitaire, rien à faire
        pass
    elif s != "none" and e == "none":
        # Saison complète : multiplier par 4
        base *= 4
    # Dans les autres cas, le tarif reste le tarif unitaire

    return str(round(base, 2))
