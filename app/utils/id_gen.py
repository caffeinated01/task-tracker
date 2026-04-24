# Simple implementation of a Linear-feedback shift register to generate pseudo-
# random numbers. We have a 31-bit number which we cram into 6 base-36 digits
# (since 6 log_2 36 ~= 31) and use as a unique identifier.

# Values for shift register bits sourced from here:
# https://www.physics.otago.ac.nz/reports/electronics/ETR2012-1.pdf

import math

lfsr_seed = 0b0110111110100110001011110010011
lfsr = lfsr_seed


def get_next_id():
    global lfsr

    # taps: 31, 30, 29, 28
    bit = (lfsr ^ (lfsr >> 1) ^ (lfsr >> 2) ^ (lfsr >> 3)) & 1
    lfsr = lfsr >> 1 | bit << 30
    return lfsr


def conv_id_to_b36(x):
    b36_str = ""
    for i in range(math.ceil(math.log(x, 36))):
        b36_str = "0123456789abcdefghijklmnopqrstuvwxyz"[
            (x // 36**i) % 36] + b36_str
    return b36_str.zfill(6)


def get_next_b36_id():
    return conv_id_to_b36(get_next_id())


# prove it cycles through all
if __name__ == "__main__":
    from tqdm import tqdm

    for cycles in tqdm(range(1, 2**31)):
        get_next_id()
    print(cycles)
