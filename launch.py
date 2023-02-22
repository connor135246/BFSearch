# launch


import sys, logging, datetime, os

from bfsearch.qt import mainwindow
from bfsearch import translate, settings


# get data file no matter if program is frozen
def df(filename):
    if getattr(sys, "frozen", False):
        return os.path.join(os.path.dirname(sys.executable), filename)
    else:
        return filename

def main():
    # write info logs and above to standard out
    streamlog = logging.StreamHandler()
    streamlog.setLevel(logging.INFO)
    # write warning logs and above to the log file
    os.makedirs(df("logs"), exist_ok = True)
    filelog = logging.FileHandler(df("logs/" + datetime.datetime.today().strftime("%Y-%m") + ".log"), encoding = "UTF-8")
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
