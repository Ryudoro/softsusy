def verification_input(nom, valeurs):
    #nom de la variable, valeurs : (min, max, step)
    if not isinstance(nom, str):
        return True, 'mauvais nom'

    if isinstance(valeurs, list):
        for valeur in valeurs:
            if not isinstance(valeur, (int, float)):
                return True, f'mauvais type de valeur pour {valeur}'

        if valeurs[0]>valeurs[1]:
            return True, "valeur maximale inférieur à la variable minimale"

        if valeurs[2]>valeurs[1]-valeurs[0]:
            return True, "pas trop faible pour l'interval"

    elif not isinstance(valeurs, (int, float)):
        return True, "pas le bon type pour la valeur"

    return False, "C'est ok"
