if __name__ == "__main__":
    tm = TaskManager()

    # Agregar tarea
    task = tm.add_task("Estudiar Python", "Repasar dataclasses y json", priority=1)
    print("Tarea agregada:", task.to_dict())

    # Listar todas
    print("Todas las tareas:", tm.get_tasks())

    # Buscar por palabra clave
    print("Buscar 'python':", tm.search_by_title_or_description("python"))

    # Actualizar tarea
    updated = tm.update_task(task.id, status=Status.COMPLETADA)
    print("Tarea actualizada:", updated)

    # Filtrar completadas
    print("Filtrar completadas:", tm.filter_by_status(Status.COMPLETADA))

    # Eliminar tarea
    if tm.delete_task(task.id):
        print("Tarea eliminada con éxito.")
    else:
        print("No se encontró tarea para eliminar.")

    # Listar todas después de eliminar
    print("Tareas después de eliminar:", tm.get_tasks())
