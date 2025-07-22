def suggerisci_modulo(giocatori):
    esterni = [g for g in giocatori if g["position"] in ["ED", "ES"]]
    centrocampisti = [g for g in giocatori if g["position"] == "CC"]
    difensori = [g for g in giocatori if g["position"] == "DC"]

    if len(esterni) >= 2 and len(centrocampisti) >= 3:
        return "3-4-2-1"
    elif len(difensori) >= 4:
        return "4-3-3"
    else:
        return "4-4-2"
