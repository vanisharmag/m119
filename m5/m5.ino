# bleak tutorials 
# https://github.com/hbldh/bleak/blob/develop/examples/discover.py
# https://github.com/hbldh/bleak/blob/develop/examples/get_services.py
# https://github.com/hbldh/bleak/blob/develop/examples/scanner_byname.py
# multiprocessing  
# https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process
# https://stackoverflow.com/questions/54793687/python-update-variable-in-loop-and-use-it-in-another-process
# multiple devices 
# https://github.com/hbldh/bleak/blob/develop/examples/two_devices.py

from pong import play 
# trying to control w arduino 
import asyncio
import struct
from multiprocessing import Process, Manager, Value
from bleak import BleakClient

DEVICE_NAME = 'Vani : Nano 33 IoT'
AZ_UUID = '00002101-0000-1000-8000-00805f9b34fb' #check 

async def connect_to_device(add, az_pong):
    print("starting", add, "loop")
    async with BleakClient(add) as client:
        while True:
            az_bytes = await client.read_gatt_char(AZ_UUID)
            az = struct.unpack('<f', az_bytes)[0]
            az_pong.value = az
def wrapper(add, az_pong):
    asyncio.run(connect_to_device(add, az_pong))

async def main(addresses):
    manager = Manager()
    az_p1 = manager.Value('d', 0.0, lock=False) 
    az_p2 = manager.Value('d', 0.0, lock=False) 
    game = Process(target=play, args=(az_p1, az_p2))
    player1 = Process(target=wrapper, args=(addresses[0], az_p1))
    player2 = Process(target=wrapper, args=(addresses[1], az_p2))
    # while (1): 
    # await asyncio.gather(
    #    wrapper(addresses[0], az_p1), 
    #    wrapper(addresses[1], az_p2),
    #    play(az_p1, az_p2),
    # )
    player1.start()
    player2.start()
    game.start()

    player2.join()
    player1.join()
    game.join()
        

if __name__ == '__main__':
    asyncio.run(main([
        "45ED2862-E09E-9A16-10F5-F6C1A7380C20", # my arduino address
        "911AED22-62E7-4A1A-CA76-D9DCC1769E5A", # someone elsese arduino addres 
    ]))
