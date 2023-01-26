# launch


import sys, logging, datetime

from bfsearch.qt import mainwindow
from bfsearch import translate


def main():
    # write info logs and above to standard out
    streamlog = logging.StreamHandler()
    streamlog.setLevel(logging.INFO)
    # write warning logs and above to the log file
    filelog = logging.FileHandler("logs/" + datetime.datetime.today().strftime("%Y-%m") + ".log", encoding = "UTF-8")
    filelog.setLevel(logging.WARNING)
    logging.basicConfig(format = '--- %(asctime)s : [%(levelname)s] %(message)s', level = logging.NOTSET, handlers = [streamlog, filelog])

    try:
        translate.loadLangFiles()
        mainwindow.launch()
    except Exception as e:
        logging.exception("An exception occurred that forced the application to close")
        raise

if __name__ == "__main__":
    main()
