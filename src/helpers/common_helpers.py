from src.business_logic import global_state

def retrieveRoomFromID(room_id):
    found = False
    room = None

    for category_name in global_state.CAT_ROOM_IDS_TO_LOBBIES:
        cat_lobbies = global_state.CAT_ROOM_IDS_TO_LOBBIES[category_name]
        if room_id in cat_lobbies:
            room = cat_lobbies[room_id]
            found = True
        if found:
            break

    return room