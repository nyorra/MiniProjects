import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import math


def fmt(value):
    return ("{:.2f}".format(value)).rstrip("0").rstrip(".")


class InputDialog(tk.Toplevel):
    def __init__(self, parent, title, prompt, is_int=False, default=None):
        super().__init__(parent)
        self.result = None
        self.is_int = is_int

        # --- Цветовая схема Graphite Pro ---
        bg_main = "#1E1E1E"
        fg_text = "#E0E0E0"
        fg_button = "white"
        accent = "#0A84FF"
        error_color = "#EF4444"

        self.title(title)
        self.configure(bg=bg_main)
        self.resizable(False, False)
        self.grab_set()

        self.update_idletasks()
        w, h = 420, 160
        x = parent.winfo_x() + (parent.winfo_width() // 2 - w // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2 - h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

        lbl = tk.Label(self, text=prompt, bg=bg_main, fg=fg_text,
                       font=("Segoe UI", 11, "bold"), wraplength=380)
        lbl.pack(pady=12)

        self.entry = tk.Entry(self, font=("Segoe UI", 12), justify="center",
                              bg="#252526", fg=fg_text, insertbackground=fg_text)
        self.entry.pack(pady=5, ipadx=4, ipady=3)
        if default is not None:
            self.entry.insert(0, str(default))
        self.entry.focus_set()

        btn_frame = tk.Frame(self, bg=bg_main)
        btn_frame.pack(pady=10)

        style_btn = {"font": ("Segoe UI", 11, "bold"), "width": 12}
        tk.Button(btn_frame, text="✅ ОК", command=self.on_ok,
                  bg=accent, fg=fg_button, **style_btn).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="❌ Отмена", command=self.on_cancel,
                  bg=error_color, fg=fg_button, **style_btn).grid(row=0, column=1, padx=6)

        self.bind("<Return>", lambda e: self.on_ok())
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.wait_window(self)

    def on_ok(self):
        try:
            val = self.entry.get()
            self.result = int(val) if self.is_int else float(val)
            self.destroy()
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректное значение")

    def on_cancel(self):
        self.result = None
        self.destroy()


class GraphApp:
    def __init__(self, root):
        # --- Цветовая схема Graphite Pro ---
        self.bg_main = "#1E1E1E"
        self.bg_panel = "#252526"
        self.fg_text = "#E0E0E0"
        self.fg_subtext = "#9CA3AF"
        self.accent = "#0A84FF"
        self.fg_success = "#10B981"
        self.fg_error = "#EF4444"

        self.root = root
        self.root.title("График функции")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.bg_main)

        # --- Вкладки ---
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.main_tab = tk.Frame(self.notebook, bg=self.bg_main)
        self.notebook.add(self.main_tab, text="📈 График функции")

        self.info_tab = tk.Frame(self.notebook, bg=self.bg_panel)
        self.notebook.add(self.info_tab, text="ℹ️ Сведения")

        self.build_main_tab()
        self.build_info_tab()

    def build_main_tab(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        font=("Segoe UI", 11),
                        rowheight=28,
                        background=self.bg_panel,
                        fieldbackground=self.bg_panel,
                        foreground=self.fg_text)
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 12, "bold"),
                        background=self.accent,
                        foreground="white")

        main_frame = tk.Frame(self.main_tab, bg=self.bg_main)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Верхняя часть - формула и описание
        top_frame = tk.Frame(main_frame, bg=self.bg_main)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(top_frame, text="Формула функции:",
                 font=("Segoe UI", 12, "bold"),
                 bg=self.bg_main, fg=self.fg_text).pack(anchor="w", pady=(0, 5))

        formula_text_frame = tk.Frame(top_frame, bg=self.bg_main)
        formula_text_frame.pack(fill=tk.X)

        formula_left_frame = tk.Frame(formula_text_frame, bg=self.bg_main)
        formula_left_frame.pack(side=tk.LEFT, padx=(0, 20))

        self.formula_image_frame = tk.Frame(formula_left_frame, bg=self.bg_panel, relief="sunken", bd=1)
        self.formula_image_frame.pack(pady=5)
        self.load_formula_image("formula.png")

        text_right_frame = tk.Frame(formula_text_frame, bg=self.bg_main)
        text_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        description_text = (
            "Вычислить N значений параметрической функции Y=f(x,a) для аргумента x, "
            "изменяющегося от начального значения x₁ с шагом dx.\n\n"
            "где:\n"
            "• a – параметр функции, положительное число;\n"
            "• k – коэффициент выбора вида функции;\n"
            "• x₁ – начальное значение аргумента функции;\n"
            "• N – количество значений функции;\n"
            "• dx – шаг изменения аргумента;"
        )
        desc_label = tk.Label(text_right_frame, text=description_text,
                              font=("Segoe UI", 11),
                              bg=self.bg_main, fg=self.fg_subtext,
                              justify=tk.LEFT, anchor="w",
                              wraplength=400)
        desc_label.pack(fill=tk.BOTH, expand=True)

        # Параметры и таблица
        content_frame = tk.Frame(main_frame, bg=self.bg_main)
        content_frame.pack(fill=tk.BOTH, expand=True)
        left_frame = tk.Frame(content_frame, bg=self.bg_main)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        params_frame = tk.LabelFrame(left_frame, text="Параметры",
                                     font=("Segoe UI", 13, "bold"),
                                     bg=self.bg_panel, fg=self.fg_text, padx=10, pady=10)
        params_frame.pack(fill=tk.X)

        self.params_labels = {}
        for param in ["a", "N", "kd", "k1", "k", "x1", "dx"]:
            row = tk.Frame(params_frame, bg=self.bg_panel)
            row.pack(anchor="w", pady=3)
            tk.Label(row, text=f"{param}:",
                     bg=self.bg_panel, fg=self.fg_text,
                     font=("Segoe UI", 11), width=5, anchor="w").pack(side=tk.LEFT)
            lbl_val = tk.Label(row, text="—", bg=self.bg_panel,
                               fg=self.accent, font=("Segoe UI", 11, "bold"))
            lbl_val.pack(side=tk.LEFT)
            self.params_labels[param] = lbl_val

        tk.Button(params_frame, text="📊 Построить график",
                  font=("Segoe UI", 12, "bold"),
                  bg=self.accent, fg="white",
                  command=self.ask_parameters).pack(pady=10, fill=tk.X)

        table_frame = tk.LabelFrame(left_frame, text="Вычисленные значения",
                                    font=("Segoe UI", 13, "bold"),
                                    bg=self.bg_panel, fg=self.fg_text, padx=5, pady=5)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        self.table = ttk.Treeview(table_frame, columns=("N", "X", "Y"), show="headings")
        self.table.heading("N", text="Номер точки")
        self.table.heading("X", text="Значение аргумента")
        self.table.heading("Y", text="Значение функции")
        self.table.column("N", width=120, anchor="center")
        self.table.column("X", width=200, anchor="center")
        self.table.column("Y", width=200, anchor="center")
        self.table.pack(fill=tk.BOTH, expand=True)

        self.graph_frame = tk.LabelFrame(content_frame, text="График",
                                         font=("Segoe UI", 13, "bold"),
                                         bg=self.bg_panel, fg=self.fg_text)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def build_info_tab(self):
        info_frame = tk.Frame(self.info_tab, bg=self.bg_panel)
        info_frame.pack(expand=True)

        tk.Label(info_frame, text="Сведения о разработчике",
                 font=("Segoe UI", 16, "bold"),
                 bg=self.bg_panel, fg=self.accent).pack(pady=20)

        info = [
            ("Фамилия:", "Пышкин"),
            ("Имя:", "Владислав"),
            ("Отчество:", "Андреевич"),
            ("Группа:", "3бИТС3"),
            ("Университет:", "МАДИ")
        ]

        for label, value in info:
            row = tk.Frame(info_frame, bg=self.bg_panel)
            row.pack(anchor="center", pady=8)
            tk.Label(row, text=label, font=("Segoe UI", 12, "bold"),
                     bg=self.bg_panel, fg=self.fg_text, width=14, anchor="e").pack(side=tk.LEFT)
            tk.Label(row, text=value, font=("Segoe UI", 12),
                     bg=self.bg_panel, fg=self.fg_success, width=25, anchor="w").pack(side=tk.LEFT)

    def load_formula_image(self, image_path):
        try:
            for widget in self.formula_image_frame.winfo_children():
                widget.destroy()
            image = Image.open(image_path)
            width = 400
            ratio = width / image.width
            height = int(image.height * ratio)
            image = image.resize((width, height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            label = tk.Label(self.formula_image_frame, image=photo, bg=self.bg_panel)
            label.image = photo
            label.pack(pady=5)
        except Exception:
            tk.Label(self.formula_image_frame,
                     text=f"Файл формулы не найден: {image_path}",
                     font=("Segoe UI", 10),
                     bg=self.bg_panel, fg=self.fg_error).pack(pady=10)

    def ask_parameters(self):
        try:
            while True:
                a = InputDialog(self.root, "Параметр a", "Введите положительное значение a:").result
                if a is None: return
                if a > 0:
                    self.params_labels["a"].config(text=fmt(a)); break
                messagebox.showerror("Ошибка", "a должно быть > 0")

            while True:
                N = InputDialog(self.root, "Параметр N", "Введите положительное N:", is_int=True).result
                if N is None: return
                if N > 1:
                    self.params_labels["N"].config(text=str(N)); break
                messagebox.showerror("Ошибка", "N должно быть > 1")

            while True:
                kd = InputDialog(self.root, "Параметр kd", "Введите положительное kd:").result
                if kd is None: return
                if kd > 0:
                    self.params_labels["kd"].config(text=fmt(kd)); break
                messagebox.showerror("Ошибка", "kd должно быть > 0")

            k1 = InputDialog(self.root, "Параметр k1", "Введите k1:").result
            if k1 is None: return
            self.params_labels["k1"].config(text=fmt(k1))

            while True:
                k = InputDialog(self.root, "Параметр k", f"Введите k > {k1}:").result
                if k is None: return
                if k > k1:
                    self.params_labels["k"].config(text=fmt(k)); break
                messagebox.showerror("Ошибка", f"k должно быть больше {k1}")

            x1, dx = k1 * a, kd * a
            self.params_labels["x1"].config(text=fmt(x1))
            self.params_labels["dx"].config(text=fmt(dx))

            self.table.delete(*self.table.get_children())
            xs, ys, i, counter = [], [], x1, 0

            while counter < N:
                x = i
                if x >= a:
                    y = a * math.sin((x**2 + 1)/ a)
                else:
                    y = math.cos(x + 1/a)
                xs.append(x)
                ys.append(y)
                self.table.insert("", "end", values=(counter + 1, fmt(x), fmt(y)))
                counter += 1
                i += dx

            for w in self.graph_frame.winfo_children():
                w.destroy()
            fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=110)
            ax.plot(xs, ys, marker="o", color=self.accent, linewidth=2, markersize=5)
            ax.set_facecolor(self.bg_panel)
            ax.spines['bottom'].set_color(self.fg_text)
            ax.spines['left'].set_color(self.fg_text)
            ax.xaxis.label.set_color(self.fg_text)
            ax.yaxis.label.set_color(self.fg_text)
            ax.tick_params(axis='x', colors=self.fg_text)
            ax.tick_params(axis='y', colors=self.fg_text)
            ax.set_title(f"График функции при A = {fmt(a)}",
                         fontsize=13, fontweight="bold", color=self.fg_text)
            ax.grid(True, linestyle="--", alpha=0.3, color=self.fg_subtext)
            ax.set_xlabel("Значение аргумента", color=self.fg_text)
            ax.set_ylabel("Значение функции", color=self.fg_text)
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
