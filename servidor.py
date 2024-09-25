import socket
import threading
import sqlite3

# Función para crear la base de datos SQLite y crear la tabla para las tareas
def iniciar_bd():
    conn = sqlite3.connect('tareas.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Función para crear una tarea e insertarla en la base de datos tareas.bd en la tabla tareas
def crear_tarea(descripcion):
    conn = sqlite3.connect('tareas.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tareas (descripcion) VALUES (?)", (descripcion,))
    conn.commit()
    conn.close()

# Función para verificar si una tarea existe, con el fin de poder validar la existencia de una tarea al momento de actualizarla o eliminarla
def existe_tarea(id_tarea):
    conn = sqlite3.connect('tareas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM tareas WHERE id = ?", (id_tarea,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Función para obtener la lista de todas las tareas
def listar_tareas():
    conn = sqlite3.connect('tareas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tareas")
    tareas = cursor.fetchall()
    conn.close()
    return tareas

# Función para actualizar una tarea	por el ID
def actualizar_tarea(id_tarea, nueva_descripcion):
    if existe_tarea(id_tarea):
        conn = sqlite3.connect('tareas.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE tareas SET descripcion = ?",(nueva_descripcion,)," WHERE id = ?", (id_tarea,))
        conn.commit()
        conn.close()
        return True
    else:
        return False

# Función para eliminar una tarea por el ID
def borrar_tarea(id_tarea):
    if existe_tarea(id_tarea):
        conn = sqlite3.connect('tareas.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tareas WHERE id = ?", (id_tarea,))
        conn.commit()
        conn.close()
        return True
    else:
        return False

# Función para manejar las solicitudes que vengan desde el cliente
def manejar_cliente(cliente_socket):
    while True:
        try:
            # Recibir la solicitud desde cliente
            request = cliente_socket.recv(1024).decode()
            if request.startswith("ADD"):
                # Si viene ADD desde el cliente se va a agregar una tarea
                _, descripcion = request.split(',', 1)
                crear_tarea(descripcion.strip())
                # Enviamos respuesta cuando se cree correctamente la tarea
                cliente_socket.send("Tarea creada correctamente.".encode())
            elif request == "LIST":
                # Si viene LIST desde el cliente se van a listar las tarea
                tareas = listar_tareas()
                if tareas:
                    response = "\n".join([f"ID: {t[0]} - {t[1]}" for t in tareas])
                else:
                    response = "ERROR. No hay tareas creadas en el sistema."
                cliente_socket.send(response.encode())
            elif request.startswith("UPDATE"):
                # Si viene UPDATE desde el cliente se va a actualizar una tarea
                _, id_tarea, nueva_descripcion = request.split(',', 2)
                # Verificamos que la tarea exista
                if actualizar_tarea(int(id_tarea.strip()), nueva_descripcion.strip()):
                    cliente_socket.send("Tarea actualizada correctamente.".encode())
                else:
                    cliente_socket.send("ERROR. La tarea no existe.".encode())
            elif request.startswith("DELETE"):
                # Si viene DELETE desde el cliente se va a eliminar una tarea
                _, id_tarea = request.split(',')
                # Verificamos que la tarea exista
                if borrar_tarea(int(id_tarea.strip())):
                    cliente_socket.send("Tarea eliminada correctamente.".encode())
                else:
                    cliente_socket.send("ERROR. La tarea no existe.".encode())
        except:
            cliente_socket.close()
            break

def iniciar_servidor():
    # Inicializar la base de datos
    iniciar_bd()

    # Aquí se configura el servicio
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_servidor.bind(('localhost', 12345))
    socket_servidor.listen(5)
    
    print("Servidor de tareas iniciado correctamente. Ahora está esperando conexiones...")

    while True:
        # Aceptar conexiones que vengan desde el cliente
        cliente_socket, client_address = socket_servidor.accept()
        print(f"Se estableció conexión con {client_address}")
        
        # Iniciar un hilo para manejar la conexión del cliente
        thread = threading.Thread(target=manejar_cliente, args=(cliente_socket,))
        thread.start()

if __name__ == "__main__":
    iniciar_servidor()