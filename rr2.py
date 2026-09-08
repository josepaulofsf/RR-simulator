import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk


class RoundRobinApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Escalonamento Round Robin")
        self.root.geometry("520x550")

        self.list_process = []
        self.process_id_counter = 0
        self.is_running = False
        self.exec_thread = None

        self._setup_ui()

    def _setup_ui(self):
        # Configuração do Time Slice
        frame_config = tk.LabelFrame(
            self.root, text="Configuração", padx=10, pady=10
        )
        frame_config.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_config, text="Time Slice (s):").grid(
            row=0, column=0, sticky="w"
        )
        self.ent_slice = tk.Entry(frame_config, width=10)
        self.ent_slice.insert(0, "2")
        self.ent_slice.grid(row=0, column=1, padx=5)

        # Adição de Processos
        frame_add = tk.LabelFrame(
            self.root, text="Adicionar Processo", padx=10, pady=10
        )
        frame_add.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_add, text="Tempo do Processo (s):").grid(
            row=0, column=0, sticky="w"
        )
        self.ent_tempo = tk.Entry(frame_add, width=10)
        self.ent_tempo.grid(row=0, column=1, padx=5)

        btn_add = tk.Button(
            frame_add, text="+ Adicionar", command=self.add_process
        )
        btn_add.grid(row=0, column=2, padx=5)

        # Controles de Execução
        frame_controls = tk.Frame(self.root, pady=5)
        frame_controls.pack(fill="x", padx=10)

        self.btn_run = tk.Button(
            frame_controls,
            text="▶ Iniciar Execução",
            bg="#4CAF50",
            fg="white",
            command=self.start_execution,
        )
        self.btn_run.pack(side="left", fill="x", expand=True, padx=2)

        self.btn_stop = tk.Button(
            frame_controls,
            text="⏹ Interromper",
            bg="#f44336",
            fg="white",
            state="disabled",
            command=self.stop_execution,
        )
        self.btn_stop.pack(side="left", fill="x", expand=True, padx=2)

        # Status e Tabela de Processos
        self.lbl_status = tk.Label(
            self.root, text="Status: Aguardando...", font=("Arial", 10, "bold")
        )
        self.lbl_status.pack(pady=5)

        self.tree = ttk.Treeview(
            self.root,
            columns=("ID", "Tempo Restante"),
            show="headings",
            height=10,
        )
        self.tree.heading("ID", text="ID do Processo")
        self.tree.heading("Tempo Restante", text="Tempo Restante (s)")
        self.tree.column("ID", anchor="center")
        self.tree.column("Tempo Restante", anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

    def add_process(self):
        try:
            tempo = int(self.ent_tempo.get())
            if tempo <= 0:
                raise ValueError
            process = {"id": self.process_id_counter, "tempo": tempo}
            self.list_process.append(process)
            self.process_id_counter += 1
            self.ent_tempo.delete(0, tk.END)
            self.update_table()
        except ValueError:
            messagebox.showerror(
                "Erro", "Informe um tempo válido (inteiro positivo)."
            )

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in self.list_process:
            self.tree.insert("", tk.END, values=(f"Processo {p['id']}", f"{p['tempo']}s"))

    def start_execution(self):
        if not self.list_process:
            messagebox.showwarning("Aviso", "Nenhum processo na fila!")
            return

        try:
            self.time_slice = int(self.ent_slice.get())
        except ValueError:
            messagebox.showerror("Erro", "Time Slice inválido.")
            return

        self.is_running = True
        self.btn_run.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.ent_slice.config(state="disabled")

        self.exec_thread = threading.Thread(
            target=self.run_scheduler, daemon=True
        )
        self.exec_thread.start()

    def stop_execution(self):
        self.is_running = False
        self.lbl_status.config(text="Status: Execução interrompida!")
        self.btn_run.config(state="normal")
        self.btn_stop.config(state="disabled")
        self.ent_slice.config(state="normal")

    def run_scheduler(self):
        i = 0
        while self.is_running and len(self.list_process) > 0:
            if i >= len(self.list_process):
                i = 0

            process = self.list_process[i]
            self.lbl_status.config(
                text=f"Executando Processo {process['id']}..."
            )

            # Executa o quantum segundo a segundo
            tempo_executado = 0
            while tempo_executado < self.time_slice and process["tempo"] > 0:
                if not self.is_running:
                    return

                time.sleep(1)
                process["tempo"] -= 1
                tempo_executado += 1
                self.root.after(0, self.update_table)

            if process["tempo"] <= 0:
                self.list_process.pop(i)
                self.root.after(0, self.update_table)
            else:
                i += 1

        if len(self.list_process) == 0:
            self.lbl_status.config(text="Status: Todos os processos finalizados!")

        self.is_running = False
        self.root.after(0, lambda: self.btn_run.config(state="normal"))
        self.root.after(0, lambda: self.btn_stop.config(state="disabled"))
        self.root.after(0, lambda: self.ent_slice.config(state="normal"))


if __name__ == "__main__":
    root = tk.Tk()
    app = RoundRobinApp(root)
    root.mainloop()
