import json
import os

SAVE_FILE = "data/save.json"

def save_game(inventory, rooms_data):
    """
    Sauvegarde :
    - inventory : liste des artefacts collectés
    - rooms_data : dict {room_id: {"puzzles": [bool,...], "artifacts": [bool,...]}}
    """
    data = {
        "inventory": inventory,
        "rooms": rooms_data
    }
    os.makedirs("data", exist_ok=True)
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
    print("Partie sauvegardée !")

def load_game():
    """
    Charge le jeu :
    Retourne : inventory, rooms_data
    """
    if not os.path.exists(SAVE_FILE):
        return [], {}
    with open(SAVE_FILE, "r") as f:
        data = json.load(f)
    return data.get("inventory", []), data.get("rooms", {})
