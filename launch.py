# launch


import logging, datetime, os

from bfsearch.qt import mainwindow
from bfsearch import translate, settings


def main():
    # write info logs and above to standard out
    streamlog = logging.StreamHandler()
    streamlog.setLevel(logging.INFO)
    # write warning logs and above to the log file
    os.makedirs("logs", exist_ok = True)
    filelog = logging.FileHandler("logs/" + datetime.datetime.today().strftime("%Y-%m") + ".log", encoding = "UTF-8")
    filelog.setLevel(logging.WARNING)
    logging.basicConfig(format = '--- %(asctime)s : [%(levelname)s] %(message)s', level = logging.NOTSET, handlers = [streamlog, filelog])

    # settings file
    settings.load()

    # launch
    try:
        translate.loadLangFiles()
        mainwindow.launch()
    except Exception:
        logging.exception("An exception occurred that forced the application to close")
        raise

if __name__ == "__main__":
    main()
