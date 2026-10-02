import os
import sys

from PyQt6.QtCore import Qt, QEvent, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QIntValidator, QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QLineEdit, QPushButton, QButtonGroup, QGraphicsOpacityEffect,
)

from SampleSize import SampleSize


def resource_path(relative):
    """Devuelve la ruta correcta de un recurso, tanto en desarrollo como dentro del .exe de PyInstaller."""
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, relative)

# ───────────────────────────── PALETA ─────────────────────────────
BLACK = "#0B0C0E"
SURFACE = "#15171A"
SURFACE_2 = "#1C1F23"
BORDER = "#272B30"
MINT = "#A8E6CF"
MINT_HOVER = "#BDF0DC"
MINT_PRESSED = "#8FD8BB"
WHITE = "#FFFFFF"
MUTED = "#8A9099"
ERROR = "#FF8A8A"

STYLE = f"""
* {{
    font-family: 'Segoe UI', 'SF Pro Display', 'Inter', 'Helvetica Neue', sans-serif;
    color: {WHITE};
}}
QWidget#root {{ background-color: {BLACK}; }}

QLabel#title {{ font-size: 20px; font-weight: 600; letter-spacing: 0.3px; }}
QLabel#subtitle {{ font-size: 12px; color: {MUTED}; }}
QLabel#fieldLabel {{ font-size: 12px; font-weight: 500; color: {MUTED}; }}
QLabel#error {{ font-size: 11px; color: {ERROR}; }}
QLabel#suffix {{ font-size: 14px; color: {MUTED}; background: transparent; }}

/* Segmented controls */
QFrame#segment {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 14px;
}}
QPushButton#segBtn {{
    background: transparent;
    border: none;
    border-radius: 11px;
    padding: 9px 18px;
    font-size: 13px;
    font-weight: 500;
    color: {MUTED};
}}
QPushButton#segBtn:hover:!checked {{ color: {WHITE}; }}
QPushButton#segBtn:checked {{
    background-color: {MINT};
    color: {BLACK};
    font-weight: 600;
}}
QPushButton#langBtn {{
    background: transparent;
    border: none;
    border-radius: 9px;
    padding: 5px 10px;
    font-size: 11px;
    font-weight: 600;
    color: {MUTED};
}}
QPushButton#langBtn:hover:!checked {{ color: {WHITE}; }}
QPushButton#langBtn:checked {{ background-color: {SURFACE_2}; color: {MINT}; }}

/* Inputs */
QFrame#field {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
}}
QFrame#field[focused="true"] {{ border: 1px solid {MINT}; background-color: {SURFACE_2}; }}
QFrame#field[invalid="true"] {{ border: 1px solid {ERROR}; }}
QLineEdit {{
    background: transparent;
    border: none;
    padding: 12px 4px 12px 14px;
    font-size: 15px;
    selection-background-color: {MINT};
    selection-color: {BLACK};
}}

/* Botón principal */
QPushButton#primary {{
    background-color: {MINT};
    color: {BLACK};
    border: none;
    border-radius: 14px;
    padding: 14px;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.4px;
}}
QPushButton#primary:hover {{ background-color: {MINT_HOVER}; }}
QPushButton#primary:pressed {{ background-color: {MINT_PRESSED}; }}

/* Resultado */
QFrame#result {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 18px;
}}
QLabel#resultCaption {{ font-size: 11px; font-weight: 600; letter-spacing: 1.6px; color: {MUTED}; }}
QLabel#resultValue {{ font-size: 44px; font-weight: 700; color: {MINT}; }}
QLabel#resultValue[empty="true"] {{ color: {BORDER}; }}
"""

# ───────────────────────────── TEXTOS ─────────────────────────────
TEXTS = {
    "es": {
        "title": "Tamaño de Muestra",
        "subtitle": "Calcula la muestra ideal para tu estudio",
        "finite": "Finita",
        "infinite": "Infinita",
        "population": "Población",
        "trust": "Nivel de Confianza",
        "success": "Probabilidad de Éxito",
        "calculate": "Calcular",
        "result": "RESULTADO",
        "invalid_pop": "Población inválida. Ingresa un número mayor a 0.",
    },
    "en": {
        "title": "Sample Size",
        "subtitle": "Calculate the ideal sample for your study",
        "finite": "Finite",
        "infinite": "Infinite",
        "population": "Population",
        "trust": "Confidence Level",
        "success": "Success Probability",
        "calculate": "Calculate",
        "result": "RESULT",
        "invalid_pop": "Invalid population. Enter a number greater than 0.",
    },
}


# ───────────────────────────── COMPONENTES ─────────────────────────────
class Field(QWidget):
    """Campo con etiqueta, sufijo opcional y mensaje de error."""

    def __init__(self, placeholder, suffix="", max_value=2147483647):
        super().__init__()
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(6)

        self.label = QLabel()
        self.label.setObjectName("fieldLabel")
        outer.addWidget(self.label)

        self.frame = QFrame()
        self.frame.setObjectName("field")
        row = QHBoxLayout(self.frame)
        row.setContentsMargins(0, 0, 14, 0)
        row.setSpacing(0)

        self.edit = QLineEdit()
        self.edit.setPlaceholderText(placeholder)
        self.edit.setValidator(QIntValidator(0, max_value))
        self.edit.installEventFilter(self)
        row.addWidget(self.edit)

        if suffix:
            s = QLabel(suffix)
            s.setObjectName("suffix")
            row.addWidget(s)

        outer.addWidget(self.frame)

        self.error = QLabel()
        self.error.setObjectName("error")
        self.error.hide()
        outer.addWidget(self.error)

    def eventFilter(self, obj, event):
        if obj is self.edit:
            if event.type() == QEvent.Type.FocusIn:
                self._set_prop("focused", True)
            elif event.type() == QEvent.Type.FocusOut:
                self._set_prop("focused", False)
        return super().eventFilter(obj, event)

    def _set_prop(self, name, value):
        self.frame.setProperty(name, value)
        self.frame.style().unpolish(self.frame)
        self.frame.style().polish(self.frame)

    def set_error(self, message=None):
        if message:
            self.error.setText(message)
            self.error.show()
            self._set_prop("invalid", True)
        else:
            self.error.hide()
            self._set_prop("invalid", False)

    def value(self):
        text = self.edit.text().replace(" ", "").replace("-", "").replace("+", "")
        return int(text) if text else 0


def segmented(buttons):
    """Crea un control segmentado a partir de una lista de botones."""
    frame = QFrame()
    frame.setObjectName("segment")
    lay = QHBoxLayout(frame)
    lay.setContentsMargins(4, 4, 4, 4)
    lay.setSpacing(4)
    group = QButtonGroup(frame)
    group.setExclusive(True)
    for b in buttons:
        b.setCheckable(True)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        group.addButton(b)
        lay.addWidget(b)
    return frame, group


# ───────────────────────────── VENTANA ─────────────────────────────
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.sesion = SampleSize()
        self.lang = "es"
        self.finite = True
        self.last_result = None

        self.setObjectName("root")
        self.setWindowTitle("SampleSize Calculator")
        self.setWindowIcon(QIcon(resource_path("icon.ico")))
        self.setFixedSize(420, 700)
        self.setStyleSheet(STYLE)

        self._build()
        self._retranslate()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 28)
        root.setSpacing(0)

        # Encabezado: idioma
        top = QHBoxLayout()
        top.addStretch()
        self.btn_es, self.btn_en = QPushButton("ES"), QPushButton("EN")
        for b in (self.btn_es, self.btn_en):
            b.setObjectName("langBtn")
        lang_frame, lang_group = segmented([self.btn_es, self.btn_en])
        lang_frame.setStyleSheet("QFrame#segment { border-radius: 12px; }")
        self.btn_es.setChecked(True)
        self.btn_es.clicked.connect(lambda: self._set_lang("es"))
        self.btn_en.clicked.connect(lambda: self._set_lang("en"))
        self._lang_group = lang_group
        top.addWidget(lang_frame)
        root.addLayout(top)
        root.addSpacing(12)

        # Título
        self.title = QLabel()
        self.title.setObjectName("title")
        self.subtitle = QLabel()
        self.subtitle.setObjectName("subtitle")
        root.addWidget(self.title)
        root.addSpacing(2)
        root.addWidget(self.subtitle)
        root.addSpacing(22)

        # Finita / Infinita
        self.btn_finite, self.btn_infinite = QPushButton(), QPushButton()
        for b in (self.btn_finite, self.btn_infinite):
            b.setObjectName("segBtn")
        mode_frame, mode_group = segmented([self.btn_finite, self.btn_infinite])
        self.btn_finite.setChecked(True)
        self.btn_finite.clicked.connect(lambda: self._set_mode(True))
        self.btn_infinite.clicked.connect(lambda: self._set_mode(False))
        self._mode_group = mode_group
        root.addWidget(mode_frame)
        root.addSpacing(22)

        # Campos
        self.f_population = Field("0")
        self.f_trust = Field("99", "%", 100)
        self.f_success = Field("50", "%", 100)
        for f in (self.f_population, self.f_trust, self.f_success):
            f.edit.returnPressed.connect(self.get_data)

        root.addWidget(self.f_population)
        root.addSpacing(14)
        root.addWidget(self.f_trust)
        root.addSpacing(14)
        root.addWidget(self.f_success)
        root.addStretch()

        # Botón calcular
        self.btn_calc = QPushButton()
        self.btn_calc.setObjectName("primary")
        self.btn_calc.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_calc.clicked.connect(self.get_data)
        root.addWidget(self.btn_calc)
        root.addSpacing(18)

        # Resultado
        self.result_card = QFrame()
        self.result_card.setObjectName("result")
        rl = QVBoxLayout(self.result_card)
        rl.setContentsMargins(20, 18, 20, 20)
        rl.setSpacing(4)
        self.result_caption = QLabel()
        self.result_caption.setObjectName("resultCaption")
        self.result_caption.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_value = QLabel("—")
        self.result_value.setObjectName("resultValue")
        self.result_value.setProperty("empty", True)
        self.result_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rl.addWidget(self.result_caption)
        rl.addWidget(self.result_value)
        root.addWidget(self.result_card)

        # Animación de aparición del resultado
        self._fx = QGraphicsOpacityEffect(self.result_value)
        self.result_value.setGraphicsEffect(self._fx)
        self._anim = QPropertyAnimation(self._fx, b"opacity", self)
        self._anim.setDuration(350)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    # ───────── Estado ─────────
    def _set_mode(self, finite):
        self.finite = finite
        self.f_population.setVisible(finite)
        self.f_population.set_error(None)
        self._reset_result()

    def _set_lang(self, lang):
        self.lang = lang
        self._retranslate()

    def _retranslate(self):
        t = TEXTS[self.lang]
        self.title.setText(t["title"])
        self.subtitle.setText(t["subtitle"])
        self.btn_finite.setText(t["finite"])
        self.btn_infinite.setText(t["infinite"])
        self.f_population.label.setText(t["population"])
        self.f_trust.label.setText(f"{t['trust']} (%)")
        self.f_success.label.setText(f"{t['success']} (%)")
        self.btn_calc.setText(t["calculate"].upper())
        self.result_caption.setText(t["result"])
        if self.f_population.error.isVisible():
            self.f_population.error.setText(t["invalid_pop"])

    def _reset_result(self):
        self.last_result = None
        self._show_result("—", empty=True)

    def _show_result(self, text, empty=False):
        self.result_value.setText(text)
        self.result_value.setProperty("empty", empty)
        self.result_value.style().unpolish(self.result_value)
        self.result_value.style().polish(self.result_value)
        if not empty:
            self._anim.stop()
            self._anim.start()

    # ───────── Cálculo ─────────
    def get_data(self):
        trust = self.f_trust.value()
        success = self.f_success.value()

        if self.finite:
            population = self.f_population.value()
            if population <= 0:
                self.f_population.set_error(TEXTS[self.lang]["invalid_pop"])
                return
            self.f_population.set_error(None)
            result = self.sesion.finitePopulation(population, trust, success)
        else:
            result = self.sesion.infinitePopulation(trust, success)

        self.last_result = result
        self._show_result(f"{round(result, 2):,.2f}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())