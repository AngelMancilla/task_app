import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models.task_manager import TaskManager
from models.task import Status

PRIORITY_COLORS = {
    1: "#ff6961",  
    2: "#fdfd96",  
    3: "#77dd77",  
}

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("750x650")
        self.manager = TaskManager()
        self.filtered_tasks = self.manager.tasks  

        self.create_widgets()
        self.refresh_task_list()

    def create_widgets(self):
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill="x", pady=8, padx=10)

        ttk.Label(top_frame, text="Buscar:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.apply_filters())
        search_entry = ttk.Entry(top_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=5)

        ttk.Label(top_frame, text="Ordenar por:").pack(side="left", padx=(15,0))
        ttk.Button(top_frame, text="Prioridad", command=lambda: self.sort_tasks("priority")).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Fecha límite", command=lambda: self.sort_tasks("limit_date")).pack(side="left", padx=5)

        ttk.Button(top_frame, text="Nueva Tarea", command=self.open_new_task_window).pack(side="right")

        self.tasks_frame = ttk.Frame(self.root)
        self.tasks_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.tasks_frame)
        self.scrollbar = ttk.Scrollbar(self.tasks_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def apply_filters(self):
        query = self.search_var.get().lower()
 
        self.filtered_tasks = [
            t for t in self.manager.tasks if query in t.title.lower() or query in t.description.lower()
        ]
        self.refresh_task_list()

    def sort_tasks(self, by):
        if by == "priority":
            self.filtered_tasks.sort(key=lambda t: t.priority)
        elif by == "limit_date":

            self.filtered_tasks.sort(key=lambda t: t.limit_date or datetime.max)
        self.refresh_task_list()

    def open_new_task_window(self):
        self._open_task_window()

    def open_edit_task_window(self, task):
        self._open_task_window(task)

    def _open_task_window(self, task=None):
        is_edit = task is not None

        top = tk.Toplevel(self.root)
        top.title("Editar Tarea" if is_edit else "Nueva Tarea")
        top.geometry("420x350")
        top.transient(self.root)
        top.grab_set()

        title_var = tk.StringVar(value=task.title if is_edit else "")
        desc_var = tk.StringVar(value=task.description if is_edit else "")
        priority_var = tk.IntVar(value=task.priority if is_edit else 2)
        status_var = tk.StringVar(value=task.status.value if is_edit else Status.ACTIVA.value)
        limit_date_var = tk.StringVar(value=task.limit_date.strftime('%Y-%m-%d') if (is_edit and task.limit_date) else "")

        ttk.Label(top, text="Título:").grid(row=0, column=0, sticky="w", padx=10, pady=6)
        ttk.Entry(top, textvariable=title_var, width=40).grid(row=0, column=1, pady=6)

        ttk.Label(top, text="Descripción:").grid(row=1, column=0, sticky="w", padx=10, pady=6)
        ttk.Entry(top, textvariable=desc_var, width=40).grid(row=1, column=1, pady=6)

        ttk.Label(top, text="Prioridad (1-3):").grid(row=2, column=0, sticky="w", padx=10, pady=6)
        ttk.Spinbox(top, from_=1, to=3, textvariable=priority_var, width=5).grid(row=2, column=1, sticky="w", pady=6)

        ttk.Label(top, text="Estado:").grid(row=3, column=0, sticky="w", padx=10, pady=6)
        ttk.Combobox(top, textvariable=status_var, values=[s.value for s in Status], state="readonly").grid(row=3, column=1, sticky="w", pady=6)

        ttk.Label(top, text="Fecha límite (YYYY-MM-DD):").grid(row=4, column=0, sticky="w", padx=10, pady=6)
        ttk.Entry(top, textvariable=limit_date_var, width=20).grid(row=4, column=1, sticky="w", pady=6)

        def save_task():
            title = title_var.get().strip()
            description = desc_var.get().strip()
            priority = priority_var.get()
            status_str = status_var.get()
            limit_date_str = limit_date_var.get().strip()

            if not title:
                messagebox.showwarning("Error", "El título no puede estar vacío.")
                return

            try:
                limit_date = datetime.fromisoformat(limit_date_str) if limit_date_str else None
            except ValueError:
                messagebox.showwarning("Error", "Fecha límite no válida. Use formato YYYY-MM-DD.")
                return

            status = next((s for s in Status if s.value == status_str), Status.ACTIVA)

            if is_edit:
                self.manager.update_task(
                    task.id,
                    title=title,
                    description=description,
                    priority=priority,
                    status=status,
                    limit_date=limit_date
                )
            else:
                task_created = self.manager.add_task(
                    title=title,
                    description=description,
                    priority=priority,
                    limit_date=limit_date
                )
                self.manager.update_task(task_created.id, status=status)

            self.apply_filters()  
            top.destroy()

        def cancel():
            top.destroy()

        btn_frame = ttk.Frame(top)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)
        ttk.Button(btn_frame, text="Guardar", command=save_task).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancelar", command=cancel).pack(side="left", padx=10)

    def refresh_task_list(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for task in self.filtered_tasks:
            self.create_task_card(task)

    def create_task_card(self, task):
        card_bg = PRIORITY_COLORS.get(task.priority, "#ffffff")

        card = ttk.Frame(self.scrollable_frame, borderwidth=1, relief="solid")
        card.pack(fill="x", pady=6, padx=5)

        color_bar = tk.Frame(card, bg=card_bg, width=8)
        color_bar.pack(side="left", fill="y")

        content = ttk.Frame(card, padding=10)
        content.pack(side="left", fill="both", expand=True)

        ttk.Label(content, text=task.title, font=("Segoe UI", 12, "bold")).pack(anchor="w")
        ttk.Label(content, text=task.description, wraplength=500).pack(anchor="w", pady=3)

        ttk.Label(content, text=f"Prioridad: {task.priority}").pack(anchor="w")
        ttk.Label(content, text=f"Estado: {task.status.value}").pack(anchor="w")
        ttk.Label(content, text=f"Fecha límite: {task.limit_date.strftime('%Y-%m-%d') if task.limit_date else 'No definida'}").pack(anchor="w")

        btn_frame = ttk.Frame(content)
        btn_frame.pack(anchor="e", pady=6)

        if task.status != Status.COMPLETADA:
            ttk.Button(btn_frame, text="Marcar Completada",
                       command=lambda tid=task.id: self.mark_completed(tid)).pack(side="right", padx=5)

        ttk.Button(btn_frame, text="Editar", command=lambda t=task: self.open_edit_task_window(t)).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=lambda tid=task.id: self.delete_task(tid)).pack(side="right", padx=5)

    def mark_completed(self, task_id):
        self.manager.update_task(task_id, status=Status.COMPLETADA)
        self.apply_filters()

    def delete_task(self, task_id):
        self.manager.delete_task(task_id)
        self.apply_filters()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()



