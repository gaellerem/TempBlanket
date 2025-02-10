import view.resources_rc
import pandas as pd
from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsEllipseItem, QGraphicsPolygonItem, QSpinBox, QMessageBox, QWidget
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
        self.setFixedSize(1200, 800)
        self.load_data()

    def draw_hexagons(self, hex_radius=25, cols=22, rows=18):
        # Calculer les décalages des hexagones
        self.scene.clear()
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

                # Marquer les jours faits
                if self.df["Made"].iloc[index]:
                    green_circle = QGraphicsEllipseItem(-hex_radius * 1, -hex_radius * 1,
                                                      hex_radius * 2, hex_radius * 2)
                    green_circle.setBrush(QBrush(Qt.green))
                    green_circle.setPen(QPen(Qt.transparent))
                    green_circle.setOpacity(0.9)
                    green_circle.setPos(x_center, y_center)
                    self.scene.addItem(green_circle)

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

                # Marquer le premier jour du mois
                if self.df["Date"].iloc[index].day == 1:

                    red_circle = QGraphicsEllipseItem(-hex_radius * 0.1, -hex_radius * 0.1,
                                                      hex_radius * 0.2, hex_radius * 0.2)
                    red_circle.setBrush(QBrush(Qt.red))
                    red_circle.setPen(QPen(Qt.transparent))
                    red_circle.setOpacity(0.9)
                    red_circle.setPos(x_center, y_center)
                    self.scene.addItem(red_circle)

                index += 1

    def load_data(self):
        # Charger les données
        self.df = pd.read_csv("datas/data.csv", sep=';', names=['Date', 'TempMin', 'TempMax', 'ColorMin', 'ColorMax', 'Made'], skiprows=1)
        self.df['Date'] = pd.to_datetime(self.df["Date"], format='%Y-%m-%d')
        self.color_pairs = pd.read_csv('datas/color_pairs.csv', sep=';', header=0)
        self.total_needed = self.color_pairs["Count"].sum()

        # Recréer les noms des QSpinBox
        self.color_pairs['SpinBoxName'] = self.color_pairs.apply(
            lambda row: f'{row["ColorMin"]}_{row["ColorMax"]}_spin', axis=1
        )

        self.draw_hexagons()

        self.pairs_done = 0
        # Remplir les QSpinBox avec les données
        for index, row in self.color_pairs.iterrows():
            spin = getattr(self.ui, row['SpinBoxName'], None)
            widget = getattr(self.ui, row['SpinBoxName'].replace('_spin', ''), None)
            if spin:
                spin.setProperty("index", index)  # Stocke l'index dans l'objet
                spin.setValue(row["Made"])
                spin.valueChanged.connect(self.update_total_count)
                if row["Made"] == row["Count"]:
                    widget.hide()
                    self.pairs_done += 1

        self.display_total_count()

    def update_total_count(self):
        sender = self.sender()
        index = sender.property("index")  # Récupère l'index directement

        if index is not None:
            new_value = sender.value()
            old_value = self.color_pairs.at[index, "Made"]

            if new_value == old_value:  # Pas de changement réel
                return

            self.color_pairs.at[index, "Made"] = new_value

            # Récupérer les couleurs associées
            color_min = self.color_pairs.at[index, "ColorMin"]
            color_max = self.color_pairs.at[index, "ColorMax"]

            if new_value > old_value:  # Incrémentation : Marquer une nouvelle case "Made"
                mask = (self.df["ColorMin"] == color_min) & (self.df["ColorMax"] == color_max) & (~self.df["Made"])
                first_index = self.df.index[mask].min()  # Premier index non marqué

                if not pd.isna(first_index):
                    self.df.at[first_index, "Made"] = True

            else:  # Décrémentation : Trouver la dernière occurrence mise à True et l'annuler
                mask = (self.df["ColorMin"] == color_min) & (self.df["ColorMax"] == color_max) & (self.df["Made"])
                last_index = self.df.index[mask].max()  # Dernière occurrence marquée

                if not pd.isna(last_index):
                    self.df.at[last_index, "Made"] = False

            # Vérifier si la paire est terminée ou non
            if new_value == self.color_pairs.at[index, "Count"]:
                self.pairs_done += 1
                getattr(self.ui, sender.objectName().replace('_spin', '')).hide()


        self.display_total_count()
        self.draw_hexagons()

    def display_total_count(self):
        total_made = self.color_pairs["Made"].sum()
        self.ui.total_count.setText(f"Total : {total_made}/{self.total_needed}\nPaires terminées: {self.pairs_done}")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Quit", "Would you like to save?",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.color_pairs.drop(columns=["SpinBoxName"]).to_csv('datas/color_pairs.csv', sep=';', index=False)
            self.df.to_csv('datas/data.csv', sep=';', index=False)

        event.accept()