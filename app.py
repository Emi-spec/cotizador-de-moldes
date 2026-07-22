from PySide6.QtWidgets import (QApplication) 

from ventana_cotizador import Ventana

def main():
    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    app = QApplication([])


    # Create a Qt widget, which will be our window.
    window = Ventana()
    #window.resize(1050, 650)
    window.showMaximized()  # IMPORTANT!!!!! Windows are hidden by default.
    window.cargar_ventana()

    # Start the event loop.
    app.exec()

    # Your application won't reach here until you exit and the event
    # loop has stopped.


if __name__ == "__main__":
    main()