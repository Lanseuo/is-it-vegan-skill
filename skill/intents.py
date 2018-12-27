from . import db
from .analyze import check
from .helpers import answer, question, dialog_delegate


def launch(request, session):
    return question("Du möchtest wissen, ob eine Zutat oder ein Produkt vegan ist? Dann frage mich danach.")


def lookup(request, session):
    if request["dialogState"] == "STARTED":
        return dialog_delegate()
    elif request["dialogState"] == "IN_PROGRESS":
        return dialog_delegate()

    item_name = request["intent"]["slots"]["Item"]["value"]
    result = check(item_name)

    if result:
        if result["status"] == "vegan":
            if result["number"] == "singular":
                speech_text = f"Ja, {result['name']} ist eigentlich immer vegan."
            else:
                speech_text = f"Ja, {result['name']} sind eigentlich immer vegan."

        if result["status"] == "non_vegan":
            if result["number"] == "singular":
                speech_text = f"Nein, {result['name']} ist nicht vegan."
            else:
                speech_text = f"Nein, {result['name']} sind nicht vegan."

        if result["status"] == "can_be_vegan":
            if result["number"] == "singular":
                speech_text = (
                    f"Bei {result['name']} bin ich mir nicht sicher. Manchmal ist es vegan, "
                    "manchmal aber auch nicht.")
            else:
                speech_text = (
                    f"Bei {result['name']} bin ich mir nicht sicher. Manchmal sind sie vegan, "
                    "manchmal aber auch nicht.")

        if result.get("explanation"):
            speech_text += f" {result['explanation']}"

    else:
        speech_text = (
            f"Leider weiß ich nicht, ob {item_name} vegan ist. "
            f"Jedoch habe ich {item_name} als Vorschlag abgespeichert. "
            f"Bald werde ich Dir darüber Auskunft geben können, ob {item_name} vegan ist.")
        db.add_recommendation(item_name, session["user"]["userId"])

    speech_text += " Möchtest Du noch etwas wissen?"

    return question(speech_text)


def stop(request, session):
    return answer("Bis bald.")


def yes(request, session):
    return question("Los geht's.")


def help(request, session):
    return question("Du kannst mich zum Beispiel fragen: Sind Bananen vegan?")
