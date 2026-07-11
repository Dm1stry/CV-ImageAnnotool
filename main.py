import os
import sys
from PyQt5.QtCore import QLibraryInfo
from PyQt5.QtWidgets import QApplication, QDialog
from widgets.segmentation_window import SegmentWindow
from widgets.dialog_window import DialogWindow
from widgets.direction_window import DirectionWindow
from widgets.detection_window import DetectionWindow

# cv2 overwrites QT_QPA_PLATFORM_PLUGIN_PATH with its own bundled (incompatible) Qt
# plugins on import, so point it back at PyQt5's plugins before creating QApplication.
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(QLibraryInfo.PluginsPath)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    dialog = DialogWindow()
    if dialog.exec_() == QDialog.Accepted:
        selected = dialog.selected_option
        if selected == 0:
            window = SegmentWindow(image_height = 928, image_width = 1600, classes=["Connector", 
                                                                                    "Capacitor", 
                                                                                    "Led", 
                                                                                    "Relay",
                                                                                    "Coil", 
                                                                                    "Varistor", 
                                                                                    "Blue-connector", 
                                                                                    "Terminal", 
                                                                                    "Red-switch",
                                                                                    "Battery",
                                                                                    "Buzzer",
                                                                                    "Antenna",
                                                                                    "Dcdc",
                                                                                    "EndCap",
                                                                                    "Plug",
                                                                                    "Buttons"])
        elif selected == 1:
            window = DetectionWindow(image_height = 480, image_width = 640, classes=["PCB"])
        elif selected == 2:
            window = DirectionWindow()
        window.show()
        sys.exit(app.exec_())  # запускаем только если диалог был успешно завершён
    else:
        print("Пользователь закрыл диалог")
        sys.exit(0)

    
    