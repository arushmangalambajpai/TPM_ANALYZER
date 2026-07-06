"""
fifo.py

TPM FIFO Payload Handler.

This file handles byte streams AFTER a FIFO
register has already been detected.

It does NOT:
- Decode SPI headers
- Detect TPM registers
- Decode TPM structures


TPM Command:

TAG            2 bytes
SIZE           4 bytes
COMMAND CODE   4 bytes


TPM Response:

TAG            2 bytes
SIZE           4 bytes
RESPONSE CODE  4 bytes
"""


from tpm_analyzer.utils.byte_utils import (
    read_uint16,
    read_uint32,
    bytes_to_hex
)


# =========================================================
# TPM CONSTANTS
# =========================================================


TPM_ST_NO_SESSIONS = 0x8001

TPM_ST_SESSIONS = 0x8002



# =========================================================
# BASIC VALIDATION
# =========================================================


def is_fifo_stream(data):

    """
    Check if FIFO payload contains
    a valid TPM packet.
    """


    if len(data) < 10:

        return False



    tag = get_tag(
        data
    )



    if tag not in [

        TPM_ST_NO_SESSIONS,

        TPM_ST_SESSIONS

    ]:


        return False



    size = get_size(
        data
    )



    if size is None:


        return False



    if size > len(data):


        return False



    return True




def get_tag(data):


    if len(data) < 2:


        return None



    return read_uint16(
        data,
        0
    )




def get_size(data):


    if len(data) < 6:


        return None



    return read_uint32(

        data,

        2

    )




def get_code(data):

    """
    Return:

    commandCode

    OR

    responseCode
    """


    if len(data) < 10:


        return None



    return read_uint32(

        data,

        6

    )




# =========================================================
# COMMAND DETECTION
# =========================================================


def is_command(data):

    """
    Detect TPM command payload.
    """


    if not is_fifo_stream(data):


        return False



    code = get_code(
        data
    )



    if code is None:


        return False



    return (

        0x00000100

        <= code

        <= 0x000002FF

    )




def is_response(data):

    """
    Detect TPM response payload.
    """


    if not is_fifo_stream(data):


        return False



    return not is_command(
        data
    )




def detect_fifo_type(data):


    if is_command(data):


        return "COMMAND"



    if is_response(data):


        return "RESPONSE"



    return "UNKNOWN"




# =========================================================
# DESCRIPTION
# =========================================================


def describe_fifo(data):


    output = []



    if not is_fifo_stream(data):


        return "Invalid TPM FIFO packet"



    tag = get_tag(
        data
    )


    size = get_size(
        data
    )


    code = get_code(
        data
    )



    output.append(

        "TPM FIFO STREAM"

    )


    output.append(

        ""

    )



    output.append(

        f"TAG  : {tag:04X}"

    )


    output.append(

        f"SIZE : {size}"

    )


    output.append(

        f"TYPE : {detect_fifo_type(data)}"

    )


    output.append(

        f"CODE : {code:08X}"

    )


    output.append(

        ""

    )



    output.append(

        "Raw:"

    )


    output.append(

        bytes_to_hex(

            data

        )

    )



    return "\n".join(
        output
    )





# =========================================================
# SELF TEST
# =========================================================


if __name__ == "__main__":


    command = [

        0x80,0x02,

        0x00,0x00,0x00,0x0A,

        0x00,0x00,0x01,0x82

    ]



    response = [

        0x80,0x01,

        0x00,0x00,0x00,0x0A,

        0x00,0x00,0x00,0x00

    ]



    print(
        describe_fifo(command)
    )


    print()


    print(
        describe_fifo(response)
    )