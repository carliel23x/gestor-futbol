import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import csv
import os
from datetime import datetime

class TeamManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Equipo de Fútbol")
        self.root.geometry("800x600")

        self.jugadores = []  
        self.partidos = []
        self.alineaciones = []

 
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)


        self.create_jugadores_tab()
        self.create_rating_tab()
        self.create_partidos_tab()
        self.create_alineaciones_tab()
        self.create_configuracion_tab()
        self.load_jugadores()
        self.load_partidos()
        self.load_alineaciones()
        self.update_time_remaining()

    def create_jugadores_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Jugadores")

        form_frame = ttk.LabelFrame(tab, text="Añadir Jugador")
        form_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=2, sticky='e')
        self.nombre_entry = ttk.Entry(form_frame)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Número:").grid(row=1, column=0, padx=5, pady=2, sticky='e')
        self.numero_entry = ttk.Entry(form_frame)
        self.numero_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Posición:").grid(row=2, column=0, padx=5, pady=2, sticky='e')
        self.posicion_combobox = ttk.Combobox(form_frame, values=["Portero", "Defensa", "Medio", "Delantero"], state="readonly")
        self.posicion_combobox.grid(row=2, column=1, padx=5, pady=2)
        self.posicion_combobox.current(0)

        ttk.Label(form_frame, text="Goles:").grid(row=3, column=0, padx=5, pady=2, sticky='e')
        self.goles_entry = ttk.Entry(form_frame)
        self.goles_entry.grid(row=3, column=1, padx=5, pady=2)
        self.goles_entry.insert(0, "0")

        ttk.Label(form_frame, text="Asistencias:").grid(row=4, column=0, padx=5, pady=2, sticky='e')
        self.asistencias_entry = ttk.Entry(form_frame)
        self.asistencias_entry.grid(row=4, column=1, padx=5, pady=2)
        self.asistencias_entry.insert(0, "0")

        self.add_jugador_button = ttk.Button(form_frame, text="Añadir Jugador", command=self.add_jugador)
        self.add_jugador_button.grid(row=5, column=0, columnspan=2, pady=5)

        cols = ("ID", "Nombre", "Número", "Posición", "Goles", "Asistencias")
        self.tree_jugadores = ttk.Treeview(tab, columns=cols, show='headings')
        for col in cols:
            self.tree_jugadores.heading(col, text=col)
            self.tree_jugadores.column(col, width=100, anchor='center')
        self.tree_jugadores.pack(fill='both', expand=True, padx=5, pady=5)

        self.tree_jugadores.bind("<Double-1>", self.on_edit_jugador)

    def create_rating_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Rating")

        cols = ("Nombre", "Goles", "Asistencias", "Total")
        self.tree_rating = ttk.Treeview(tab, columns=cols, show='headings')
        for col in cols:
            self.tree_rating.heading(col, text=col)
            self.tree_rating.column(col, width=100, anchor='center')
        self.tree_rating.pack(fill='both', expand=True, padx=5, pady=5)

    def create_partidos_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Partidos")


        form_frame = ttk.LabelFrame(tab, text="Registrar Partido")
        form_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(form_frame, text="Equipo Local:").grid(row=0, column=0, padx=5, pady=2, sticky='e')
        self.local_entry = ttk.Entry(form_frame)
        self.local_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Equipo Visitante:").grid(row=1, column=0, padx=5, pady=2, sticky='e')
        self.visitante_entry = ttk.Entry(form_frame)
        self.visitante_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Fecha:").grid(row=2, column=0, padx=5, pady=2, sticky='e')
        self.fecha_entry = DateEntry(form_frame, date_pattern='yyyy-mm-dd')
        self.fecha_entry.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Hora (HH:MM):").grid(row=3, column=0, padx=5, pady=2, sticky='e')
        self.hora_entry = ttk.Entry(form_frame)
        self.hora_entry.grid(row=3, column=1, padx=5, pady=2)

        self.add_partido_button = ttk.Button(form_frame, text="Agregar Partido", command=self.add_partido)
        self.add_partido_button.grid(row=4, column=0, columnspan=2, pady=5)

        cols = ("Local", "Visitante", "Fecha", "Hora", "Tiempo restante")
        self.tree_partidos = ttk.Treeview(tab, columns=cols, show='headings')
        for col in cols:
            self.tree_partidos.heading(col, text=col)
            self.tree_partidos.column(col, width=100, anchor='center')
        self.tree_partidos.pack(fill='both', expand=True, padx=5, pady=5)

    def create_alineaciones_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Alineaciones")

        select_frame = ttk.LabelFrame(tab, text="Seleccionar Alineaci\u00f3n")
        select_frame.pack(fill='both', padx=5, pady=5)

        self.jugadores_listbox = tk.Listbox(select_frame, selectmode=tk.MULTIPLE, width=50, height=15)
        self.jugadores_listbox.pack(side='left', padx=5, pady=5, fill='y')
        self.jugadores_scrollbar = ttk.Scrollbar(select_frame, orient='vertical', command=self.jugadores_listbox.yview)
        self.jugadores_scrollbar.pack(side='left', fill='y')
        self.jugadores_listbox.config(yscrollcommand=self.jugadores_scrollbar.set)

        ttk.Label(select_frame, text="Fecha:").pack(padx=5, pady=2)
        self.fecha_alineacion_entry = DateEntry(select_frame, date_pattern='yyyy-mm-dd')
        self.fecha_alineacion_entry.pack(padx=5, pady=2)

        self.save_alineacion_button = ttk.Button(select_frame, text="Guardar Alineaci\u00f3n", command=self.save_alineacion)
        self.save_alineacion_button.pack(padx=5, pady=5)


        cols = ("Fecha", "Jugadores")
        self.tree_alineaciones = ttk.Treeview(tab, columns=cols, show='headings')
        self.tree_alineaciones.heading("Fecha", text="Fecha")
        self.tree_alineaciones.heading("Jugadores", text="Jugadores")
        self.tree_alineaciones.column("Fecha", width=100, anchor='center')
        self.tree_alineaciones.column("Jugadores", width=600, anchor='w')
        self.tree_alineaciones.pack(fill='both', expand=True, padx=5, pady=5)

    def create_configuracion_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Configuraci\u00f3n")

        self.delete_jugadores_button = ttk.Button(tab, text="Borrar Jugadores", command=self.delete_jugadores)
        self.delete_jugadores_button.pack(pady=5)

        self.delete_partidos_button = ttk.Button(tab, text="Borrar Partidos", command=self.delete_partidos)
        self.delete_partidos_button.pack(pady=5)

        self.delete_alineaciones_button = ttk.Button(tab, text="Borrar Alineaciones", command=self.delete_alineaciones)
        self.delete_alineaciones_button.pack(pady=5)

        self.delete_all_button = ttk.Button(tab, text="Borrar Todo", command=self.delete_all)
        self.delete_all_button.pack(pady=5)

    def add_jugador(self):
        nombre = self.nombre_entry.get().strip()
        numero = self.numero_entry.get().strip()
        posicion = self.posicion_combobox.get()
        goles = self.goles_entry.get().strip()
        asistencias = self.asistencias_entry.get().strip()
        if not nombre or not numero or not posicion or goles == "" or asistencias == "":
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return
        try:
            numero = int(numero)
            goles = int(goles)
            asistencias = int(asistencias)
        except ValueError:
            messagebox.showerror("Error", "Número, Goles y Asistencias deben ser números enteros.")
            return


        new_id = 1
        if self.jugadores:
            existing_ids = [j['ID'] for j in self.jugadores]
            new_id = max(existing_ids) + 1

        jugador = {
            "ID": new_id,
            "Nombre": nombre,
            "Número": numero,
            "Posición": posicion,
            "Goles": goles,
            "Asistencias": asistencias
        }
        self.jugadores.append(jugador)


        self.tree_jugadores.insert("", "end", values=(new_id, nombre, numero, posicion, goles, asistencias))

        self.nombre_entry.delete(0, tk.END)
        self.numero_entry.delete(0, tk.END)
        self.goles_entry.delete(0, tk.END)
        self.asistencias_entry.delete(0, tk.END)
        self.numero_entry.insert(0, "")
        self.goles_entry.insert(0, "0")
        self.asistencias_entry.insert(0, "0")

        self.save_jugadores()
        self.update_rating()
        self.update_jugadores_listbox()

    def on_edit_jugador(self, event):
        item = self.tree_jugadores.selection()
        if not item:
            return
        item = item[0]
        valores = self.tree_jugadores.item(item, "values")
        id_jugador = int(valores[0])
        current_goles = int(valores[4])
        current_asistencias = int(valores[5])

        edit_win = tk.Toplevel(self.root)
        edit_win.title("Editar Goles y Asistencias")
        ttk.Label(edit_win, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(edit_win, text=valores[1]).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(edit_win, text="Goles:").grid(row=1, column=0, padx=5, pady=5)
        goles_entry = ttk.Entry(edit_win)
        goles_entry.grid(row=1, column=1, padx=5, pady=5)
        goles_entry.insert(0, str(current_goles))
        ttk.Label(edit_win, text="Asistencias:").grid(row=2, column=0, padx=5, pady=5)
        asistencias_entry = ttk.Entry(edit_win)
        asistencias_entry.grid(row=2, column=1, padx=5, pady=5)
        asistencias_entry.insert(0, str(current_asistencias))
        def save_changes():
            try:
                new_goles = int(goles_entry.get().strip())
                new_asistencias = int(asistencias_entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Goles y Asistencias deben ser enteros.")
                return
            for j in self.jugadores:
                if j["ID"] == id_jugador:
                    j["Goles"] = new_goles
                    j["Asistencias"] = new_asistencias
                    break
            self.tree_jugadores.item(item, values=(id_jugador, valores[1], valores[2], valores[3], new_goles, new_asistencias))
            edit_win.destroy()
            self.save_jugadores()
            self.update_rating()
        save_button = ttk.Button(edit_win, text="Guardar", command=save_changes)
        save_button.grid(row=3, column=0, columnspan=2, pady=5)

    def add_partido(self):
        local = self.local_entry.get().strip()
        visitante = self.visitante_entry.get().strip()
        fecha = self.fecha_entry.get()
        hora = self.hora_entry.get().strip()
        if not local or not visitante or not fecha or not hora:
            messagebox.showerror("Error", "Complete todos los campos del partido.")
            return
        try:
            datetime.strptime(hora, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "La hora debe tener el formato HH:MM (24h).")
            return
        partido = {
            "Local": local,
            "Visitante": visitante,
            "Fecha": fecha,
            "Hora": hora
        }
        self.partidos.append(partido)
        self.tree_partidos.insert("", "end", values=(local, visitante, fecha, hora, ""))
        self.local_entry.delete(0, tk.END)
        self.visitante_entry.delete(0, tk.END)
        self.hora_entry.delete(0, tk.END)

        self.save_partidos()

    def save_alineacion(self):
        selected_indices = self.jugadores_listbox.curselection()
        if len(selected_indices) != 11:
            messagebox.showerror("Error", "Debe seleccionar exactamente 11 jugadores.")
            return
        selected_players = []
        posiciones = []
        for idx in selected_indices:
            text = self.jugadores_listbox.get(idx)
            parts = text.split(" - ")
            if len(parts) < 2:
                continue
            name_pos = parts[1]
            if "(" in name_pos and ")" in name_pos:
                nombre = name_pos.split(" (")[0]
                posicion = name_pos[name_pos.find("(")+1:name_pos.find(")")]
            else:
                nombre = name_pos
                posicion = ""
            selected_players.append(nombre)
            posiciones.append(posicion)
        if "Portero" not in posiciones:
            messagebox.showerror("Error", "La alineación debe incluir al menos 1 portero.")
            return
        fecha = self.fecha_alineacion_entry.get()
        alineacion_str = ", ".join(selected_players)
        alineacion = {"Fecha": fecha, "Jugadores": alineacion_str}
        self.alineaciones.append(alineacion)
        self.tree_alineaciones.insert("", "end", values=(fecha, alineacion_str))
        self.save_alineaciones()

    def delete_jugadores(self):
        if messagebox.askyesno("Confirmar", "¿Seguro que desea borrar todos los jugadores?"):
            self.jugadores = []
            for item in self.tree_jugadores.get_children():
                self.tree_jugadores.delete(item)
            self.save_jugadores()
            self.update_rating()
            self.update_jugadores_listbox()

    def delete_partidos(self):
        if messagebox.askyesno("Confirmar", "¿Seguro que desea borrar todos los partidos?"):
            self.partidos = []
            for item in self.tree_partidos.get_children():
                self.tree_partidos.delete(item)
            self.save_partidos()

    def delete_alineaciones(self):
        if messagebox.askyesno("Confirmar", "¿Seguro que desea borrar todas las alineaciones?"):
            self.alineaciones = []
            for item in self.tree_alineaciones.get_children():
                self.tree_alineaciones.delete(item)
            self.save_alineaciones()

    def delete_all(self):
        if messagebox.askyesno("Confirmar", "¿Seguro que desea borrar todos los datos?"):
            self.delete_jugadores()
            self.delete_partidos()
            self.delete_alineaciones()

    def save_jugadores(self):
        with open("jugadores.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Nombre", "Número", "Posición", "Goles", "Asistencias"])
            for j in self.jugadores:
                writer.writerow([j["ID"], j["Nombre"], j["Número"], j["Posición"], j["Goles"], j["Asistencias"]])

    def load_jugadores(self):
        if not os.path.exists("jugadores.csv"):
            return
        with open("jugadores.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    jugador = {
                        "ID": int(row["ID"]),
                        "Nombre": row["Nombre"],
                        "Número": int(row["Número"]),
                        "Posición": row["Posición"],
                        "Goles": int(row["Goles"]),
                        "Asistencias": int(row["Asistencias"])
                    }
                except:
                    continue
                self.jugadores.append(jugador)
                self.tree_jugadores.insert("", "end", values=(jugador["ID"], jugador["Nombre"], jugador["Número"], jugador["Posición"], jugador["Goles"], jugador["Asistencias"]))
        self.update_rating()
        self.update_jugadores_listbox()

    def save_partidos(self):
        with open("partidos.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Local", "Visitante", "Fecha", "Hora"])
            for p in self.partidos:
                writer.writerow([p["Local"], p["Visitante"], p["Fecha"], p["Hora"]])

    def load_partidos(self):
        if not os.path.exists("partidos.csv"):
            return
        with open("partidos.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                partido = {"Local": row["Local"], "Visitante": row["Visitante"], "Fecha": row["Fecha"], "Hora": row["Hora"]}
                self.partidos.append(partido)
                self.tree_partidos.insert("", "end", values=(partido["Local"], partido["Visitante"], partido["Fecha"], partido["Hora"], ""))

    def save_alineaciones(self):
        with open("alineaciones.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Fecha", "Jugadores"])
            for a in self.alineaciones:
                writer.writerow([a["Fecha"], a["Jugadores"]])

    def load_alineaciones(self):
        if not os.path.exists("alineaciones.csv"):
            return
        with open("alineaciones.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                alineacion = {"Fecha": row["Fecha"], "Jugadores": row["Jugadores"]}
                self.alineaciones.append(alineacion)
                self.tree_alineaciones.insert("", "end", values=(alineacion["Fecha"], alineacion["Jugadores"]))

    def update_rating(self):
        for item in self.tree_rating.get_children():
            self.tree_rating.delete(item)
        sorted_players = sorted(self.jugadores, key=lambda x: x["Goles"] + x["Asistencias"], reverse=True)
        for j in sorted_players:
            total = j["Goles"] + j["Asistencias"]
            self.tree_rating.insert("", "end", values=(j["Nombre"], j["Goles"], j["Asistencias"], total))

    def update_jugadores_listbox(self):
        self.jugadores_listbox.delete(0, tk.END)
        for j in self.jugadores:
            text = f"{j['ID']} - {j['Nombre']} ({j['Posici\u00f3n']})"
            self.jugadores_listbox.insert(tk.END, text)

    def update_time_remaining(self):
        now = datetime.now()
        updated_partidos = []
        for item in self.tree_partidos.get_children():
            self.tree_partidos.delete(item)
        for p in self.partidos:
            dt_str = p["Fecha"] + " " + p["Hora"]
            try:
                match_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            except:
                continue
            diff = match_time - now
            if diff.total_seconds() < 0:
               
                continue
            days = diff.days
            hours, remainder = divmod(diff.seconds, 3600)
            minutes = remainder // 60
            tiempo = f"{days} días, {hours} horas, {minutes} minutos"
            updated_partidos.append(p)
            self.tree_partidos.insert("", "end", values=(p["Local"], p["Visitante"], p["Fecha"], p["Hora"], tiempo))
    
        if len(updated_partidos) != len(self.partidos):
            self.partidos = updated_partidos
            self.save_partidos()
       
      
        self.root.after(60000, self.update_time_remaining)

if __name__ == "__main__":
    root = tk.Tk()
    app = TeamManagerApp(root)
    root.mainloop()
