# launch


from bfsearch.qt import mainwindow
from bfsearch import translate

if __name__ == "__main__":
    translate.loadLangFiles()
    mainwindow.launch()
