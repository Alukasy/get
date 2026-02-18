def number_to_dac(number):
    return [int(bit) for bit in bin(int(number))[2:].zfill(8)]
print(number_to_dac(input()))