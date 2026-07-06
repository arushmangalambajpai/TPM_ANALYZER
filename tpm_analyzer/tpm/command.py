"""
command.py

TPM Command Decoder Layer.

This file provides TPM Analyzer's
internal command decoding interface.

It uses:

    tpmstream_wrapper.py

but never directly imports tpmstream.


This file does NOT:
- Decode SPI
- Decode registers
- Decode FIFO
"""


from tpm_analyzer.tpm.tpmstream_wrapper import (
    decode_command
)


from tpm_analyzer.utils.byte_utils import (
    read_uint32
)



# =========================================================
# COMMAND CODE EXTRACTION
# =========================================================


def get_command_code(command_bytes):

    """
    Extract TPM_CC from command.

    TPM command format:

    bytes 0-1:
        tag

    bytes 2-5:
        size

    bytes 6-9:
        commandCode
    """


    if len(command_bytes) < 10:

        return None


    return read_uint32(
        command_bytes,
        6
    )



# =========================================================
# TPM COMMAND DECODER
# =========================================================


def decode_tpm_command(command_bytes):

    """
    Decode complete TPM command.

    Input:

        TPM FIFO command bytes


    Output:

        Dictionary:

        {
            command_code,
            decoded_text
        }
    """


    command_code = get_command_code(
        command_bytes
    )



    decoded = decode_command(
        command_bytes
    )



    return {

        "command_code":

            command_code,


        "decoded":

            decoded

    }



# =========================================================
# SELF TEST
# =========================================================


if __name__ == "__main__":


    startup_command = [

        0x80,0x01,

        0x00,0x00,0x00,0x0C,

        0x00,0x00,0x01,0x44,

        0x00,0x00

    ]



    result = decode_tpm_command(
        startup_command
    )



    print(
        "COMMAND CODE:",
        hex(result["command_code"])
    )


    print()


    print(
        result["decoded"]
    )