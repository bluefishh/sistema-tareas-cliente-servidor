import socket
# Función principal que ejecuta el menú del lado del cliente y desde donde también nos conectamos al servidor
def cliente():
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Aquí nos conectamos al servidor
    cliente_socket.connect(('localhost', 12345))
    
    # Menú para interactuar con el servidor
    while True:
        print("\n--- Menú Sistema de Tareas ---")
        print("1. Crear tarea")
        print("2. Listar tareas")
        print("3. Actualizar tarea")
        print("4. Eliminar tarea")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            # Crear tareas
            descripcion = input("Descripción de la tarea: ")
            peticion = f"ADD,{descripcion}"
            cliente_socket.send(peticion.encode())
        elif opcion == '2':
            # Listar tareas
            peticion = "LIST"
            cliente_socket.send(peticion.encode())
        elif opcion == '3':
            # Actualizar tareas
            id_tarea = input("ID de la tarea a actualizar: ")
            nueva_descripcion = input("Nueva descripción de la tarea: ")
            peticion = f"UPDATE,{id_tarea},{nueva_descripcion}"
            cliente_socket.send(peticion.encode())
        elif opcion == '4':
            # Eliminar tareas
            id_tarea = input("ID de la tarea a eliminar: ")
            peticion = f"DELETE,{id_tarea}"
            cliente_socket.send(peticion.encode())
        elif opcion == '5':
            print("Saliendo del cliente...")
            break
        # Recibir la respuesta desde el servidor
        response = cliente_socket.recv(1024).decode()
        print(f"\nRespuesta del servidor:\n{response}")
    
    # Aquí se cierra la conexión del cliente
    cliente_socket.close()

if __name__ == "__main__":
    cliente()
