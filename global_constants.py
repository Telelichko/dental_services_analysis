import sys
from pathlib import Path

ROOT_DIR = Path(sys.executable).resolve().parents[2]
FILES_DIR = f'{ROOT_DIR}\\Data'

URL_SITE_PRODOCTOROV = 'https://prodoctorov.ru/'
URL_SITE_32TOP = 'https://tomsk.32top.ru/'

URL_PART_DENTAL_SERVICES = 'uslugi/stomatologiya/'
URL_PART_DENTISTRY = 'top/chastnaya-stomatologiya/'