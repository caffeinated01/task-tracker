# We use a 38-bit representation of the current Unix timestamp (which lasts us 
# until around year 10000, good enough) with another 8 bits added to the back 
# to ensure uniqueness (this is generated using a linear-feedback shift regis-
# ter). Seed is determined using a random byte. This may lead to collisions, 
# but only if the server is rerun on the same second it is turned off.

# Values for shift register bits sourced from here:
# https://www.physics.otago.ac.nz/reports/electronics/ETR2012-1.pdf

import math
import datetime
import random

lfsr_seed = random.randint(0, 2**13 - 1)
lfsr = lfsr_seed


def get_next_lfsr():
    global lfsr
    
    # taps: 13, 12, 10, 9
    bit = (lfsr ^ (lfsr >> 1) ^ (lfsr >> 3) ^ (lfsr >> 4)) & 1
    lfsr = lfsr >> 1 | bit << 12
    return lfsr

def get_next_id():
    # make it fit within 38 bits
    curr_time = int(datetime.datetime.now().timestamp()) % 2 ** 38
    return (get_next_lfsr() << 38) + curr_time

def conv_id_to_b36(x):
    b36_str = ""
    for i in range(math.ceil(math.log(x, 36))):
        b36_str = "0123456789abcdefghijklmnopqrstuvwxyz"[(x // 36**i) % 36] + b36_str
    return b36_str.zfill(10)


def get_next_b36_id():
    return conv_id_to_b36(get_next_id())


# prove it cycles through all
if __name__ == "__main__":
    from tqdm import tqdm

    ledger = bytearray(2**13 // 8)
    for cycles in tqdm(range(2**13)):
        get_next_lfsr()
        if ledger[lfsr//8] & 1<<(lfsr%8):
            print(lfsr, cycles)
            break
        ledger[lfsr//8] |= 1<<(lfsr%8)