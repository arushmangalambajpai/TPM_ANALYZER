"""
byte_utils.py

Generic byte manipulation utilities.

This file contains NO TPM-specific logic.

Used by:
- SPI decoder
- Register decoder
- FIFO decoder
- TPM command parser
"""


# ---------------------------------------------------------
# HEX STRING FUNCTIONS
# ---------------------------------------------------------


def clean_hex_string(hex_string):
    """
    Convert messy hex input into clean format.

    Input:
        "80 D4 00 24"
        "80:D4:00:24"
        "80-D4-00-24"

    Output:
        "80D40024"
    """

    hex_string = hex_string.strip()

    remove_chars = [
        " ",
        ":",
        "-",
        "_",
        "\n",
        "\t"
    ]

    for ch in remove_chars:
        hex_string = hex_string.replace(ch, "")

    return hex_string.upper()



def hex_to_bytes(hex_string):
    """
    Convert hex string into list of bytes.

    Input:
        "80D40024"

    Output:
        [0x80,0xD4,0x00,0x24]
    """

    hex_string = clean_hex_string(hex_string)

    if len(hex_string) % 2 != 0:
        raise ValueError(
            "Invalid hex string length"
        )

    data = []

    for i in range(0, len(hex_string), 2):

        byte = int(
            hex_string[i:i+2],
            16
        )

        data.append(byte)

    return data



def bytes_to_hex(data):
    """
    Convert byte list back to hex string.

    Input:
        [128,212,0,24]

    Output:
        "80 D4 00 18"
    """

    output = []

    for byte in data:

        output.append(
            f"{byte:02X}"
        )

    return " ".join(output)


# ---------------------------------------------------------
# INTEGER FUNCTIONS
# ---------------------------------------------------------


def read_uint16(data, index=0):
    """
    Read 2 bytes big endian.

    TPM uses network byte order.

    Example:

    80 02

    returns:

    0x8002
    """

    return (
        (data[index] << 8)
        |
        data[index+1]
    )



def read_uint32(data, index=0):
    """
    Read 4 bytes big endian.

    Example:

    00 00 01 82

    returns:

    0x182
    """

    return (
        (data[index] << 24)
        |
        (data[index+1] << 16)
        |
        (data[index+2] << 8)
        |
        data[index+3]
    )


# ---------------------------------------------------------
# BIT FUNCTIONS
# ---------------------------------------------------------


def get_bit(value, bit):
    """
    Return bit value.

    Example:

    value = 0b10000000

    bit 7 returns 1
    """

    return (
        value >> bit
    ) & 1



def is_bit_set(value, bit):
    """
    True/False check.
    """

    return get_bit(
        value,
        bit
    ) == 1



def get_bits(value, start, length):
    """
    Extract multiple bits.

    Example:

    value:

    11110000

    start=4
    length=4

    returns:

    1111
    """

    mask = (
        1 << length
    ) - 1


    return (
        value >> start
    ) & mask



# ---------------------------------------------------------
# DEBUG HELPERS
# ---------------------------------------------------------


def print_bytes(data):
    """
    Pretty print bytes.
    """

    print(
        bytes_to_hex(data)
    )



# ---------------------------------------------------------
# SELF TEST
# ---------------------------------------------------------


if __name__ == "__main__":


    test = "80 D4 00 24"


    data = hex_to_bytes(test)


    print(data)


    print(
        bytes_to_hex(data)
    )


    print(
        hex(
            read_uint16(
                [0x80,0x02]
            )
        )
    )


    print(
        hex(
            read_uint32(
                [
                    0x00,
                    0x00,
                    0x01,
                    0x82
                ]
            )
        )
    )