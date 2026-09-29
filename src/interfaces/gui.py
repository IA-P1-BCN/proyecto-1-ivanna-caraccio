import tkinter as tk

from application.change_race_status import ChangeRaceStatus
from application.finish_race import FinishRace
from application.get_today_history import GetTodayHistory
from application.race_session import RaceSession
from application.start_race import StartRace
from domain.race_status import RaceStatus
from infrastructure.logging_config import get_logger

from .formatting import format_amount, format_duration, format_history_table
from .theme import (
    ACCENT,
    ACCENT_DIM,
    BG,
    BUTTON_ACTIVE,
    BUTTON_BG,
    DANGER,
    ENTRY_BG,
    FOREGROUND,
    SURFACE,
    apply_theme,
    button_kwargs,
)

logger = get_logger(__name__)

WINDOW_TITLE = "TAXITECH"
LOGIN_TITLE = "ACCESO A TAXITECH"
HISTORY_TITLE = "CARRERAS DE HOY"
SUMMARY_TITLE = "CARRERA FINALIZADA"
ERROR_TITLE = "ERROR"
TEXT_FONT = ("Consolas", 12)
INPUT_FONT = ("Segoe UI", 14)
AMOUNT_FONT = ("Segoe UI", 32, "bold")
STATUS_FONT = ("Segoe UI", 14, "bold")
BUTTON_FONT = ("Segoe UI", 16, "bold")
BUTTON_PADY = 18
REFRESH_MS = 1000
MIN_WIDTH = 480
MIN_HEIGHT = 640
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
        self.history_button = None

    def run(self):
        logger.info("GUI started")
        self.root = self._create_root()
        self.root.withdraw()

        if not self._login():
            self.root.destroy()
            logger.info("GUI closed")
            return

        self.root.deiconify()
        self._build_window()
        self._center(self.root)
        self.root.protocol("WM_DELETE_WINDOW", self._close)
        self._schedule_refresh()
        self.root.mainloop()
        logger.info("GUI closed")

    @staticmethod
    def _create_root():
        root = tk.Tk()
        apply_theme(root)
        root.title(WINDOW_TITLE)
        root.minsize(MIN_WIDTH, MIN_HEIGHT)
        root.geometry(f"{MIN_WIDTH}x{MIN_HEIGHT}")
        return root

    def _login(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(LOGIN_TITLE)
        dialog.configure(bg=BG)
        dialog.resizable(False, False)
        dialog.grab_set()

        tk.Label(dialog, text="Introduce la contraseña:",
                 font=STATUS_FONT, bg=BG, fg=FOREGROUND).pack(
            padx=40, pady=(26, 8)
        )

        password_entry = tk.Entry(
            dialog,
            show="*",
            font=INPUT_FONT,
            width=22,
            bg=ENTRY_BG,
            fg=FOREGROUND,
            insertbackground=FOREGROUND,
            relief="flat",
        )
        password_entry.pack(padx=40, pady=4)

        error_label = tk.Label(dialog, text="", bg=BG, fg=DANGER,
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

        buttons = tk.Frame(dialog, bg=BG)
        buttons.pack(padx=40, pady=(0, 24), fill="x")
        tk.Button(buttons, text="ENTRAR", font=BUTTON_FONT,
                  command=submit, **button_kwargs()).pack(
            side="left", expand=True, fill="x"
        )
        tk.Button(buttons, text="SALIR", font=BUTTON_FONT,
                  command=cancel, **button_kwargs()).pack(
            side="left", expand=True, fill="x", padx=(10, 0)
        )

        dialog.bind("<Return>", submit)
        dialog.protocol("WM_DELETE_WINDOW", cancel)
        password_entry.focus_set()
        self._center(dialog)
        dialog.wait_window()

        return result["granted"]

    def _open_dialog(self, title):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.configure(bg=BG)
        dialog.grab_set()
        return dialog

    def _show_error(self, message):
        dialog = self._open_dialog(ERROR_TITLE)
        dialog.resizable(False, False)

        tk.Label(dialog, text=message, bg=BG, fg=FOREGROUND,
                 font=STATUS_FONT, justify="left", wraplength=360).pack(
            padx=30, pady=(24, 16)
        )
        tk.Button(dialog, text="ACEPTAR", font=BUTTON_FONT,
                  command=dialog.destroy, **button_kwargs()).pack(
            padx=30, pady=(0, 24), fill="x"
        )
        self._center(dialog)
        dialog.wait_window()

    def _ask_yes_no(self, message, title):
        dialog = self._open_dialog(title)
        dialog.resizable(False, False)
        result = {"answer": False}

        def close(answer):
            result["answer"] = answer
            dialog.destroy()

        tk.Label(dialog, text=message, bg=BG, fg=FOREGROUND,
                 font=STATUS_FONT, justify="left", wraplength=360).pack(
            padx=30, pady=(24, 16)
        )

        buttons = tk.Frame(dialog, bg=BG)
        buttons.pack(padx=30, pady=(0, 24), fill="x")
        tk.Button(buttons, text="SÍ", font=BUTTON_FONT,
                  command=lambda: close(True), **button_kwargs()).pack(
            side="left", expand=True, fill="x"
        )
        tk.Button(buttons, text="NO", font=BUTTON_FONT,
                  command=lambda: close(False), **button_kwargs()).pack(
            side="left", expand=True, fill="x", padx=(10, 0)
        )

        dialog.protocol("WM_DELETE_WINDOW", lambda: close(False))
        self._center(dialog)
        dialog.wait_window()
        return result["answer"]

    def _build_window(self):
        self.root.columnconfigure(0, weight=1, uniform="main")
        self.root.columnconfigure(1, weight=1, uniform="main")
        for row in range(1, 6):
            self.root.rowconfigure(row, weight=1)

        status_frame = tk.Frame(self.root, pady=12, bg=SURFACE)
        status_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.status_label = tk.Label(
            status_frame,
            text=f"Estado: {NO_RACE_STATUS}",
            font=STATUS_FONT,
            bg=SURFACE,
            fg=FOREGROUND,
        )
        self.status_label.pack()

        self.amount_label = tk.Label(
            status_frame,
            text=format_amount(0),
            font=AMOUNT_FONT,
            bg=SURFACE,
            fg=ACCENT,
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
        self.history_button = self._make_button(
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
            **button_kwargs(),
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

    def _show_summary(self, race):
        dialog = self._open_dialog(SUMMARY_TITLE)
        dialog.resizable(False, False)

        details = tk.Frame(dialog, bg=SURFACE)
        details.pack(padx=24, pady=(24, 6), fill="x")
        for line in (
            f"Inicio:    {race.start_time:%H:%M:%S}",
            f"Fin:       {race.end_time:%H:%M:%S}",
            f"Duración:  {format_duration(race.get_duration_seconds())}",
        ):
            tk.Label(details, text=line, bg=SURFACE, fg=FOREGROUND,
                     font=STATUS_FONT, justify="left").pack(
                padx=18, pady=5, anchor="w"
            )

        tk.Label(dialog, bg=BG, fg=ACCENT, font=AMOUNT_FONT,
                 text=f"TOTAL  "
                      f"{format_amount(race.get_current_amount())}").pack(
            padx=24, pady=(10, 14)
        )
        tk.Button(dialog, text="CERRAR", font=BUTTON_FONT,
                  command=dialog.destroy, **button_kwargs()).pack(
            padx=24, pady=(0, 24), fill="x"
        )
        self._center(dialog)
        dialog.wait_window()

    def _show_history(self):
        try:
            records, total = self.get_today_history.execute()
        except ValueError as error:
            self._show_error(f"No se puede leer el historial: {error}")
            return

        window = tk.Toplevel(self.root)
        window.title(HISTORY_TITLE)
        window.configure(bg=BG)

        body = self._history_body(records, total)
        text = tk.Text(window, font=TEXT_FONT, padx=14, pady=14,
                       width=46, height=min(len(records) + 6, 20),
                       bg=ENTRY_BG, fg=FOREGROUND,
                       insertbackground=FOREGROUND,
                       selectbackground=ACCENT, selectforeground=BG,
                       relief="flat")
        text.insert("end", body)
        text.configure(state="disabled")
        text.pack(fill="both", expand=True)

        tk.Button(window, text="CERRAR", font=BUTTON_FONT,
                  command=window.destroy, **button_kwargs()).pack(
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

    def _safe(self, action):
        try:
            return action()
        except Exception:
            logger.exception("Unexpected error while running %s",
                             action.__name__)
            self._show_error(
                "Se ha producido un error. "
                "Consulta el fichero de log para más detalles."
            )
            return None

    def _close(self):
        if self.session.active_race is not None:
            keep_going = self._ask_yes_no(
                "Hay una carrera en curso. ¿Finalizarla, guardarla en el "
                "histórico y salir?",
                WINDOW_TITLE,
            )
            if not keep_going:
                return

            self._safe(self.finish_race.execute)

        logger.info("Exit option chosen by the user")
        self.root.destroy()

    def _schedule_refresh(self):
        self._refresh()
        self.root.after(REFRESH_MS, self._schedule_refresh)

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
        self._set_enabled(self.history_button, not active)

        self._style_status_button(self.stopped_button, RaceStatus.STOPPED,
                                  race)
        self._style_status_button(self.moving_button, RaceStatus.MOVING,
                                  race)

    def _style_status_button(self, button, status, race):
        is_current = race is not None and race.status == status
        button.configure(text=self._status_text(status, race))

        if is_current:
            button.configure(bg=ACCENT_DIM, fg=ACCENT,
                             activebackground=ACCENT_DIM)
        else:
            button.configure(bg=BUTTON_BG, fg=FOREGROUND,
                             activebackground=BUTTON_ACTIVE)

    @staticmethod
    def _set_enabled(button, enabled):
        button.configure(state="normal" if enabled else "disabled")

    @staticmethod
    def _status_text(status, race):
        is_current = race is not None and race.status == status
        marker = ACTIVE_MARKER if is_current else " " * len(ACTIVE_MARKER)
        return marker + status.value.upper()
