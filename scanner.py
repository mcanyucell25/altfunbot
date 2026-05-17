import time
import config

def scan(callback):
    while True:
        # Alt.fun scanner ileride entegre edilecek
        time.sleep(config.SCAN_INTERVAL)
