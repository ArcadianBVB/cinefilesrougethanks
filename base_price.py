def prix_base_hd(type_, format_, saison=False, episodes=False):
    format_ = format_.strip().lower()
    type_ = type_.strip().lower()

    if type_ == "film":
        return 2.0

    elif type_ == "série":
        return 4.0 if saison else 1.0

    elif type_ == "animé 3d":
        if format_ == "court métrage":
            return 4.0 if saison else 1.0
        return 3.0

    elif type_ == "novelas":
        if format_ == "court métrage":
            return 4.0 if saison else 1.0
        return 2.0

    elif type_ == "télé-réalité":
        return 4.0 if saison else 1.0

    elif type_ == "spectacle":
        if format_ == "court métrage":
            return 4.0 if saison else 0.8
        return 3.0

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

    elif type_ == "documentaire":
        return 3.0

    else:
        return 0.0


def calculer_prix(type_, qualite, format_, rarete, saison, episodes):
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
    # HD et BluRay : inchangé

    if rarete.strip().lower() == "rare":
        base += 1

    # Si épisodes seuls : multiplier
    if is_episode and not is_saison:
        try:
            nb_episodes = len([x for x in e.split(",") if x.strip().isdigit()])
            base *= nb_episodes
        except:
            pass

    # Si saison présente → on laisse le tarif tel quel (déjà pour saison complète)
    return str(round(base, 2))
