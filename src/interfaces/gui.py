import tkinter as tk
from tkinter import messagebox

from application.change_race_status import ChangeRaceStatus
from application.finish_race import FinishRace
from application.get_today_history import GetTodayHistory
from application.race_session import RaceSession
from application.start_race import StartRace
from domain.race_status import RaceStatus
from infrastructure.logging_config import get_logger

from .formatting import format_amount, format_duration, format_history_table

logger = get_logger(__name__)

WINDOW_TITLE = "TAXITECH"
LOGIN_TITLE = "ACCESO A TAXITECH"
HISTORY_TITLE = "CARRERAS DE HOY"
TEXT_FONT = ("Consolas", 12)
INPUT_FONT = ("Segoe UI", 14)
AMOUNT_FONT = ("Segoe UI", 32, "bold")
STATUS_FONT = ("Segoe UI", 14, "bold")
BUTTON_FONT = ("Segoe UI", 16, "bold")
BUTTON_PADY = 18
NO_RACE_STATUS = "—"
ACTIVE_MARKER = "● "


class TaxiGui:
    def __init__(self, repository, rates=None, validate_access=None):
        self.session = RaceSession()
        self.start_race = StartRace(self.session, rates)
        self.change_race_status = ChangeRaceStatus(self.session)
        self.finish_race = FinishRace(self.session, repository)
        self.get_today_history = GetTodayHistory(repository)
        self.validate_access = validate_access

        self.root = None
        self.status_label = None
        self.amount_label = None
        self.start_button = None
        self.stopped_button = None
        self.moving_button = None
        self.finish_button = None

    def run(self):
        logger.info("GUI started")
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.withdraw()

        if not self._login():
            self.root.destroy()
            logger.info("GUI closed")
            return

        self.root.deiconify()
        self._build_window()
        self.root.mainloop()
        logger.info("GUI closed")

    def _login(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(LOGIN_TITLE)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Introduce la contraseña:",
                 font=STATUS_FONT).pack(padx=40, pady=(26, 8))

        password_entry = tk.Entry(dialog, show="*", font=INPUT_FONT, width=22)
        password_entry.pack(padx=40, pady=4)

        error_label = tk.Label(dialog, text="", fg="#c0392b",
                               font=("Segoe UI", 10, "bold"))
        error_label.pack(padx=40, pady=(4, 10))

        result = {"granted": False}

        def submit(event=None):
            password = password_entry.get()
            if not password:
                logger.info("Access cancelled by the user")
                dialog.destroy()
                return

            if self.validate_access.execute(password):
                result["granted"] = True
                dialog.destroy()
                return

            error_label.configure(text="Contraseña incorrecta. "
                                       "Acceso denegado.")
            password_entry.delete(0, tk.END)
            password_entry.focus_set()

        def cancel():
            logger.info("Access cancelled by the user")
            dialog.destroy()

        buttons = tk.Frame(dialog)
        buttons.pack(padx=40, pady=(0, 24), fill="x")
        tk.Button(buttons, text="ENTRAR", font=BUTTON_FONT,
                  command=submit).pack(side="left", expand=True, fill="x")
        tk.Button(buttons, text="SALIR", font=BUTTON_FONT,
                  command=cancel).pack(side="left", expand=True, fill="x",
                                       padx=(10, 0))

        dialog.bind("<Return>", submit)
        dialog.protocol("WM_DELETE_WINDOW", cancel)
        password_entry.focus_set()
        self._center(dialog)
        dialog.wait_window()

        return result["granted"]

    def _build_window(self):
        status_frame = tk.Frame(self.root, pady=12)
        status_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.status_label = tk.Label(
            status_frame,
            text=f"Estado: {NO_RACE_STATUS}",
            font=STATUS_FONT,
        )
        self.status_label.pack()

        self.amount_label = tk.Label(
            status_frame,
            text=format_amount(0),
            font=AMOUNT_FONT,
            fg="#1a7f37",
        )
        self.amount_label.pack()

        self.start_button = self._make_button(
            "INICIAR CARRERA", self._start, row=1, columnspan=2
        )
        self.stopped_button = self._make_button(
            "PARADO",
            lambda: self._change_status(RaceStatus.STOPPED),
            row=2,
            column=0,
        )
        self.moving_button = self._make_button(
            "EN MOVIMIENTO",
            lambda: self._change_status(RaceStatus.MOVING),
            row=2,
            column=1,
        )
        self.finish_button = self._make_button(
            "FINALIZAR CARRERA", self._finish, row=3, columnspan=2
        )
        self._make_button(
            "HISTÓRICO DE HOY", self._show_history, row=4, columnspan=2
        )
        self._make_button("SALIR", self._close, row=5, columnspan=2)

        self._refresh()

    def _make_button(self, text, command, row, column=0, columnspan=1):
        button = tk.Button(
            self.root,
            text=text,
            font=BUTTON_FONT,
            command=command,
            pady=BUTTON_PADY,
        )
        button.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            sticky="ew",
            padx=14,
            pady=7,
        )
        return button

    def _start(self):
        self._safe(self.start_race.execute)
        self._refresh()

    def _change_status(self, new_status):
        self._safe(lambda: self.change_race_status.execute(new_status))
        self._refresh()

    def _finish(self):
        race = self._safe(self.finish_race.execute)
        if race is not None:
            self._show_summary(race)
        self._refresh()

    @staticmethod
    def _show_summary(race):
        messagebox.showinfo(
            "CARRERA FINALIZADA",
            f"Inicio:    {race.start_time:%H:%M:%S}\n"
            f"Fin:       {race.end_time:%H:%M:%S}\n"
            f"Duración:  {format_duration(race.get_duration_seconds())}\n"
            f"TOTAL:     {format_amount(race.get_current_amount())}",
        )

    def _show_history(self):
        try:
            records, total = self.get_today_history.execute()
        except ValueError as error:
            messagebox.showerror(
                WINDOW_TITLE,
                f"No se puede leer el historial: {error}",
            )
            return

        window = tk.Toplevel(self.root)
        window.title(HISTORY_TITLE)

        body = self._history_body(records, total)
        text = tk.Text(window, font=TEXT_FONT, padx=14, pady=14,
                       width=46, height=min(len(records) + 6, 20))
        text.insert("end", body)
        text.configure(state="disabled")
        text.pack(fill="both", expand=True)

        tk.Button(window, text="CERRAR", font=BUTTON_FONT,
                  command=window.destroy).pack(
            padx=14, pady=12, fill="x"
        )
        self._center(window)

    @staticmethod
    def _history_body(records, total):
        if not records:
            return "Aún no hay carreras registradas.\n"

        lines = format_history_table(records)
        lines.append("")
        lines.append(f"Carreras: {len(records)}")
        lines.append(f"TOTAL ACUMULADO: {format_amount(total)}")
        return "\n".join(lines) + "\n"

    @staticmethod
    def _center(window):
        window.update_idletasks()
        x = (window.winfo_screenwidth() - window.winfo_width()) // 2
        y = (window.winfo_screenheight() - window.winfo_height()) // 2
        window.geometry(f"+{x}+{y}")

    @staticmethod
    def _safe(action):
        try:
            return action()
        except Exception:
            logger.exception("Unexpected error while running %s",
                             action.__name__)
            messagebox.showerror(
                WINDOW_TITLE,
                "Se ha producido un error. "
                "Consulta el fichero de log para más detalles.",
            )
            return None

    def _close(self):
        if self.session.active_race is not None:
            keep_going = messagebox.askyesno(
                WINDOW_TITLE,
                "Hay una carrera en curso. ¿Salir sin finalizarla?",
            )
            if not keep_going:
                return

        logger.info("Exit option chosen by the user")
        self.root.destroy()

    def _refresh(self):
        race = self.session.active_race

        if race is None:
            status = NO_RACE_STATUS
            amount = format_amount(0)
        else:
            status = race.status.value
            amount = format_amount(race.get_current_amount())

        self.status_label.configure(text=f"Estado: {status}")
        self.amount_label.configure(text=amount)
        self._update_controls(race)

    def _update_controls(self, race):
        active = race is not None
        self._set_enabled(self.start_button, not active)
        self._set_enabled(self.stopped_button, active)
        self._set_enabled(self.moving_button, active)
        self._set_enabled(self.finish_button, active)

        self.stopped_button.configure(
            text=self._status_text(RaceStatus.STOPPED, race)
        )
        self.moving_button.configure(
            text=self._status_text(RaceStatus.MOVING, race)
        )

    @staticmethod
    def _set_enabled(button, enabled):
        button.configure(state="normal" if enabled else "disabled")

    @staticmethod
    def _status_text(status, race):
        is_current = race is not None and race.status == status
        marker = ACTIVE_MARKER if is_current else " " * len(ACTIVE_MARKER)
        return marker + status.value.upper()
