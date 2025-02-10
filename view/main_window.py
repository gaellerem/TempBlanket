import view.resources_rc
import pandas as pd
from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsEllipseItem, QGraphicsPolygonItem, QSpinBox, QMessageBox
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPolygonF, QColor, QBrush, QPen
from view.utilitaires import load_ui, extract_data


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = load_ui("main")
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Temperature blanket")
        self.ui.graphicsView.setScene(QGraphicsScene())
        self.scene = self.ui.graphicsView.scene()
        self.setFixedSize(1050, 700)
        self.load_data()

    def draw_hexagons(self, hex_radius=20, cols=22, rows=18):
        # Calculer les décalages des hexagones
        offset_x = hex_radius * (3 ** 0.5)
        offset_y = hex_radius * 1.5

        index = 0
        for y in range(rows):
            for x in range(cols):
                if index >= len(self.df): break
                x_center = x * offset_x
                y_center = y * offset_y
                if y % 2 == 1:
                    if x == cols - 1:
                        continue
                    x_center += offset_x / 2

                # Marquer le premier jour du mois
                if self.df["Date"].iloc[index].day == 1:

                    red_circle = QGraphicsEllipseItem(-hex_radius * 1, -hex_radius * 1,
                                                      hex_radius * 2, hex_radius * 2)
                    red_circle.setBrush(QBrush(Qt.red))
                    red_circle.setPen(QPen(Qt.transparent))
                    red_circle.setOpacity(0.9)
                    red_circle.setPos(x_center, y_center)
                    self.scene.addItem(red_circle)

                # Créer un hexagone
                hexagon = QPolygonF([
                    QPointF(0, -hex_radius),
                    QPointF(hex_radius * (3 ** 0.5) / 2, -hex_radius / 2),
                    QPointF(hex_radius * (3 ** 0.5) / 2, hex_radius / 2),
                    QPointF(0, hex_radius),
                    QPointF(-hex_radius * (3 ** 0.5) / 2, hex_radius / 2),
                    QPointF(-hex_radius * (3 ** 0.5) / 2, -hex_radius / 2),
                ])

                # Ajouter l'hexagone à la scène
                hexagon_item = QGraphicsPolygonItem(hexagon)
                hexagon_item.setPos(x_center, y_center)
                hexagon_item.setPen(QPen(QColor(Qt.black)))
                hexagon_item.setBrush(Qt.transparent)
                self.scene.addItem(hexagon_item)

                # Cercles de couleurs
                # Couleur max
                max_circle = QGraphicsEllipseItem(-hex_radius * 0.75, -hex_radius * 0.75,
                                                  hex_radius * 1.5, hex_radius * 1.5)
                max_circle.setBrush(QBrush(QColor(self.df["ColorMax"].iloc[index])))
                max_circle.setPen(QPen(Qt.transparent))
                max_circle.setPos(x_center, y_center)
                self.scene.addItem(max_circle)

                # Couleur min
                min_circle = QGraphicsEllipseItem(-hex_radius * 0.3, -hex_radius * 0.3,
                                                  hex_radius * 0.6, hex_radius * 0.6)
                min_circle.setBrush(QBrush(QColor(self.df["ColorMin"].iloc[index])))
                min_circle.setPen(QPen(Qt.transparent))
                min_circle.setPos(x_center, y_center)
                self.scene.addItem(min_circle)

                index += 1

    def load_data(self):
        self.df = extract_data("datas/temperatures.csv")
        self.color_pairs = pd.read_csv('datas/color_pairs.csv', sep=';', header=0)

        self.color_pairs['SpinBoxName'] = self.color_pairs.apply(
            lambda row: f'{row["ColorMin"]}_{row["ColorMax"]}_spin', axis=1
        )

        self.scene.clear()
        self.draw_hexagons()

        # Remplir les QSpinBox avec les données
        for index, row in self.color_pairs.iterrows():
            spin = self.ui.findChild(QSpinBox, row['SpinBoxName'])
            if spin:
                spin.setValue(row["Made"])

        total_made = self.color_pairs["Made"].sum()
        total_needed = self.color_pairs["Count"].sum()
        self.ui.total_count.setText(f"{total_made}/{total_needed}")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Quit", "Would you like to save?",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for index, row in self.color_pairs.iterrows():
                spin = self.ui.findChild(QSpinBox, row['SpinBoxName'])
                if spin:
                    self.color_pairs.loc[index,"Made"] = spin.value()
            del self.color_pairs['SpinBoxName']
            self.color_pairs.to_csv('datas/color_pairs.csv', sep=';', index=False)

        event.accept()