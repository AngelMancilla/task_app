if __name__ == "__main__":
    tm = TaskManager()


    task = tm.add_task("Estudiar Python", "Repasar dataclasses y json", priority=1)
    print("Tarea agregada:", task.to_dict())

  
    print("Todas las tareas:", tm.get_tasks())

  
    print("Buscar 'python':", tm.search_by_title_or_description("python"))

   
    updated = tm.update_task(task.id, status=Status.COMPLETADA)
    print("Tarea actualizada:", updated)

   
    print("Filtrar completadas:", tm.filter_by_status(Status.COMPLETADA))

   
    if tm.delete_task(task.id):
        print("Tarea eliminada con éxito.")
    else:
        print("No se encontró tarea para eliminar.")

    print("Tareas después de eliminar:", tm.get_tasks())
