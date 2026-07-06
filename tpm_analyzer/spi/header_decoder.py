"""
header_decoder.py

TPM SPI Header Decoder.

This file decodes only the SPI transport header.

It does NOT:
- Decode TPM registers
- Decode FIFO data
- Decode TPM commands

TPM SPI transaction format:

Byte 0:
    Operation + Transfer Size

Byte 1-3:
    TPM Register Address


Example:

    80 D4 00 24

    80:
        Write operation

    D40024:
        Locality 0
        Register offset 0024h


Address format:

    D4 L R R

    D4:
        TPM base address

    L:
        Locality nibble

    RRR:
        Register offset

Example:

    D4 20 18

    Locality:
        2

    Register:
        018h
"""


from tpm_analyzer.utils.byte_utils import (
    hex_to_bytes
)


# =========================================================
# SPI HEADER DECODER
# =========================================================


def decode_spi_header(data):

    """
    Decode TPM SPI header.

    Input:

        Hex string:
            "80 D4 00 24"

        OR

        Byte list:
            [0x80,0xD4,0x00,0x24]


    Output:

        Dictionary containing:
            operation
            transfer size
            address
            locality
            register offset
            remaining bytes
    """


    # -----------------------------------------------------
    # Input conversion
    # -----------------------------------------------------


    if isinstance(data, str):

        data = hex_to_bytes(data)



    if len(data) < 4:

        raise ValueError(
            "TPM SPI header requires at least 4 bytes"
        )



    # -----------------------------------------------------
    # Split SPI header
    # -----------------------------------------------------


    header_byte = data[0]


    address_bytes = data[1:4]



    # -----------------------------------------------------
    # Decode operation
    #
    # bit 7:
    #
    # 0 = write
    # 1 = read
    #
    # -----------------------------------------------------


    if header_byte & 0x80:

        operation = "READ"

    else:

        operation = "WRITE"



    # -----------------------------------------------------
    # Decode transfer size
    #
    # bits 5:0
    #
    # stored value = size - 1
    #
    # -----------------------------------------------------


    transfer_size = (
        header_byte & 0x3F
    ) + 1



    # -----------------------------------------------------
    # Decode 24-bit TPM address
    # -----------------------------------------------------


    address = (
        (address_bytes[0] << 16)
        |
        (address_bytes[1] << 8)
        |
        address_bytes[2]
    )



    # -----------------------------------------------------
    # Decode locality and register offset
    #
    # Address:
    #
    # D4 L R R
    #
    # Example:
    #
    # D4 30 18
    #
    # locality = 3
    #
    # register = 018h
    #
    # -----------------------------------------------------


    address_without_base = (
        address & 0xFFFF
    )


    locality = (
        address_without_base >> 12
    ) & 0xF


    register_offset = (
        address_without_base & 0x0FFF
    )



    # -----------------------------------------------------
    # Return decoded data
    # -----------------------------------------------------


    return {

        "operation":
            operation,


        "transfer_size":
            transfer_size,


        "raw_address":
            f"{address:06X}",


        "locality":
            locality,


        "register_offset":
            f"{register_offset:04X}",


        "payload":
            data[4:]

    }



# =========================================================
# OUTPUT FORMATTER
# =========================================================


def format_spi_header(decoded):

    """
    Create readable SPI header output.

    Input:
        decoded dictionary

    Output:
        formatted string
    """


    output = []


    output.append(
        "TPM SPI HEADER"
    )


    output.append(
        "------------------------------"
    )


    output.append(
        f"Operation       : {decoded['operation']}"
    )


    output.append(
        f"Transfer Size   : {decoded['transfer_size']} bytes"
    )


    output.append(
        f"Raw Address     : {decoded['raw_address']}"
    )


    output.append(
        f"Locality        : {decoded['locality']}"
    )


    output.append(
        f"Register Offset : {decoded['register_offset']}h"
    )


    return "\n".join(output)



# =========================================================
# SELF TEST
# =========================================================


if __name__ == "__main__":


    test_packets = [

        "80 D4 00 18",

        "80 D4 10 18",

        "80 D4 40 24"

    ]



    for packet in test_packets:


        decoded = decode_spi_header(
            packet
        )


        print(
            format_spi_header(decoded)
        )


        print()