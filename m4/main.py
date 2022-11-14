# bleak tutorials 
# https://github.com/hbldh/bleak/blob/develop/examples/discover.py
# https://github.com/hbldh/bleak/blob/develop/examples/get_services.py
# https://github.com/hbldh/bleak/blob/develop/examples/scanner_byname.py
# multiprocessing  
# https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process
# https://stackoverflow.com/questions/54793687/python-update-variable-in-loop-and-use-it-in-another-process

from pong import play 
# trying to control w arduino 
import asyncio
import struct
import time 
from multiprocessing import Process, Manager, Value
from bleak import BleakScanner, BleakClient

DEVICE_NAME = 'Vani : Nano 33 IoT'
AX_UUID = '00002101-0000-1000-8000-00805f9b34fb' #check 
SCAN_INTERVAL_SEC = 5

async def main():
    address = None
    while True:
        print('Scanning...')
        devices = await BleakScanner.discover()
        for d in devices:
            print(f'{d.name}')
            if d.name == DEVICE_NAME:
                address = str(d.address)
                print(f'Found {DEVICE_NAME}! Address: {address}')
                break
        if address is not None:
            break
        time.sleep(SCAN_INTERVAL_SEC)

    manager = Manager()
    ax_pong = manager.Value('d', 0.0, lock=False) 
    game = Process(target=play, args=(ax_pong,))

    async with BleakClient(address) as client:
        game.start()
        while True:
            ax_bytes = await client.read_gatt_char(AX_UUID)
            ax = struct.unpack('<f', ax_bytes)[0]
            ax_pong.value = ax

    print(f'Disconnected from {address}')
    game.join()

if __name__ == '__main__':
    asyncio.run(main())