# Sistema de Gestión de Tareas Cliente-Servidor — Ibero, Arquitectura de Software

Este proyecto implementa un sistema de gestión de tareas utilizando la arquitectura o modelo cliente-servidor en Python. El sistema permite agregar, listar, eliminar y actualizar tareas, almacenando los datos en una base de datos SQLite similar al ejemplo que se colocó en clase sobre los usuarios.

## Características

- **Agregar Tareas**: Los usuarios pueden agregar tareas proporcionando una descripción.
- **Listar Tareas**: Se listan todas las tareas con su ID y descripción.
- **Eliminar Tareas**: Los usuarios pueden eliminar una tarea existente mediante su ID.
- **Actualizar Tareas**: Los usuarios pueden modificar la descripción de una tarea existente mediante su ID.
- **Manejo de Errores**: Si se intenta eliminar o actualizar una tarea que no existe, el sistema responde con un mensaje de error.

## Requisitos

- **Python 3.x**
- **SQLite** (viene integrado ya con Python)

## Uso

### 1. Ejecutar el Servidor

El servidor se encargará de gestionar la base de datos y manejar las conexiones de los clientes. Para iniciarlo:

```bash
python servidor.py
```

### 2. Ejecutar el Cliente

El cliente permite interactuar con el servidor y realizar las operaciones de gestión de tareas. Para iniciar el cliente:

```bash
python cliente.py
```

### Estructura del Proyecto

- **cliente.py**: Lógica del cliente para interactuar con el servidor
- **servidor.py**: Lógica del servidor para gestionar las tareas y los clientes
- **tareas.db**: Base de datos SQLite (se genera automáticamente)
- **README.md**: Documentación del proyecto