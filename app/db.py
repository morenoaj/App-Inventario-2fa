import json, os

# Obtén la ruta del directorio actual
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construye la ruta relativa al archivo users.json
users_json_path = os.path.join(current_directory, 'users.json')
inv_json_path = os.path.join(current_directory, 'inv.json')
auth_json_path = os.path.join(current_directory, 'auth.json')

# Funciones para users.json
def get_all_users():
    with open(users_json_path, 'r') as file:
        users = json.load(file)
    return users

def insert_user(user_data):
    users = get_all_users()  # Obtener la lista actual de usuarios
    if users:
        last_id = users[-1].get("id", 0)  # Obtener el último ID utilizado
        new_id = last_id + 1  # Asignar un nuevo ID sumando 1 al último ID
    else:
        new_id = 1  # Si no hay usuarios, asignar 1 como el ID del nuevo usuario

    user_data["id"] = new_id  # Asignar el nuevo ID al nuevo usuario
    user_data["role"] = "manager"  # Asignar el nuevo ID al nuevo usuario
    users.append(user_data)  # Agregar el nuevo usuario a la lista
    with open(users_json_path, 'w') as file:
        json.dump(users, file, indent=4)  # Escribir la lista actualizada en el archivo
    
def update_user(index, user_data):
    users = get_all_users()
    if index > 0 and index <= len(users):
        users[index - 1] = user_data
        with open(users_json_path, 'w') as file:
            json.dump(users, file, indent=4)

def delete_user(user_id):
    users = get_all_users()
    updated_users = [user for user in users if user.get("id") != user_id]
    with open(users_json_path, 'w') as file:
        json.dump(updated_users, file, indent=4)

# Funciones para inv.json
def get_all_inventory():
    with open(inv_json_path, 'r') as file:
        inventory = json.load(file)
    return inventory

def insert_inventory(inventory_data):
    items = get_all_inventory()  # Obtener la lista actual de inventario
    if items:
        last_id = items[-1].get("id", 0)  # Obtener el último ID utilizado
        new_id = last_id + 1  # Asignar un nuevo ID sumando 1 al último ID
    else:
        new_id = 1  # Si no hay elementos, asignar 1 como el ID del nuevo elemento

    inventory_data["id"] = new_id  # Asignar el nuevo ID al nuevo elemento
    items.append(inventory_data)  # Agregar el nuevo elemento a la lista

    with open(inv_json_path, 'w') as file:
        json.dump(items, file, indent=4)  # Escribir la lista actualizada en el archivo

def get_inventory_by_user_id(user_id):
    inventory = get_all_inventory()
    user_inventory = [item for item in inventory if str(item.get('userid')) == str(user_id)]
    return user_inventory

def update_inventory(index, inventory_data):
    items = get_all_inventory()
    if index > 0 and index <= len(items):
        items[index - 1] = inventory_data
        with open(inv_json_path, 'w') as file:
            json.dump(items, file, indent=4)

def delete_inventory(id):
    items = get_all_inventory()
    updated_items = [item for item in items if item.get("id") != id]
    with open(inv_json_path, 'w') as file:
        json.dump(updated_items, file, indent=4)

