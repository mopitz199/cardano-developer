import requests

def get_last_epoch_number():
    response = requests.get("http://api:3000/epoch?order=id.asc")
    epochs = response.json()
    last_epoch = epochs[len(epochs) - 1]
    return last_epoch["no"]


def get_pool_hash_ids(pool_id):
    response = requests.get(f"http://api:3000/pool_hash?view=eq.{pool_id}")
    response = response.json()
    ids = []
    for pool_hash in response:
        ids.append(pool_hash["id"])
    return ids

def get_slot_leader_ids_by_pool_hash_id(pool_hash_id):
    response = requests.get(f"http://api:3000/slot_leader?pool_hash_id=eq.{pool_hash_id}")
    response = response.json()
    ids = []
    for slot_leader in response:
        ids.append(slot_leader["id"])
    return ids

def get_num_of_block_last_epoch():
    number = get_last_epoch_number()
    pool_hash_ids = get_pool_hash_ids("pool10eltx2wej46e62ulmwzm35xfu0azu47yvpjper7gwhncqe74vg6")
    total = 0
    for pool_hash_id in pool_hash_ids:
        slot_leader_ids = get_slot_leader_ids_by_pool_hash_id(pool_hash_id)
        for slot_leader_id in slot_leader_ids:
            response = requests.get(f"http://api:3000/block?and=(epoch_no.eq.{number},slot_leader_id.eq.{slot_leader_id})")
            total += len(response.json())
    return total


def get_message(last_epoch_number, num_of_block_last_epoch):
    messages_options = {
        0: f"epoch {last_epoch_number}: Llevamos {num_of_block_last_epoch} bloques firmados, pero tranquilo esto es cosa de paciencia.",
        1: f"epoch {last_epoch_number}: Ves! ya llevamos {num_of_block_last_epoch} bloques firmados y vamos por más!",
        2: f"epoch {last_epoch_number}: Eso! ya llevamos {num_of_block_last_epoch} bloques firmados",
        3: f"epoch {last_epoch_number}: Incrible! ya son {num_of_block_last_epoch} bloques firmados y esto no para!",
        4: f"epoch {last_epoch_number}: Woooow! ya van {num_of_block_last_epoch} bloques firmados, este epoch va con todo!",
        5: f"epoch {last_epoch_number}: Esto no para! ya son {num_of_block_last_epoch} bloques firmados, esto esta on fire!",
        6: f"epoch {last_epoch_number}: No me la creo... ya son {num_of_block_last_epoch} bloques firmados!",
        7: f"epoch {last_epoch_number}: Ya son {num_of_block_last_epoch} firmados!",
    }
    message = messages_options.get(num_of_block_last_epoch, None)
    if not message:
        return f"epoch {last_epoch_number}: Ya son {num_of_block_last_epoch} firmados!"
    else:
        return message