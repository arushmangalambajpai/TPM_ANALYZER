"""
fifo.py

TPM FIFO Data Handler.

This file understands TPM command and response
byte streams transported through FIFO registers.

It does NOT:
- Decode SPI headers
- Decode registers
- Decode TPM structures


TPM Command:

TAG          2 bytes
SIZE         4 bytes
COMMAND CODE 4 bytes


TPM Response:

TAG           2 bytes
SIZE          4 bytes
RESPONSE CODE 4 bytes
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
# BASIC CHECKS
# =========================================================


def is_fifo_stream(data):

    """
    Check if bytes look like TPM FIFO data.
    """


    if len(data) < 2:

        return False


    tag = read_uint16(
        data,
        0
    )


    return tag in [

        TPM_ST_NO_SESSIONS,

        TPM_ST_SESSIONS

    ]



def get_tag(data):

    """
    Return TPM structure tag.
    """


    return read_uint16(
        data,
        0
    )



def get_size(data):

    """
    Return TPM command/response size.
    """


    if len(data) < 6:

        return None


    return read_uint32(
        data,
        2
    )



def is_complete(data):

    """
    Check if complete TPM packet exists.
    """


    size = get_size(
        data
    )


    if size is None:

        return False


    return len(data) >= size



# =========================================================
# COMMAND / RESPONSE DETECTION
# =========================================================


def get_code(data):

    """
    TPM commandCode or responseCode.

    Both exist at byte offset 6.
    """


    if len(data) < 10:

        return None


    return read_uint32(
        data,
        6
    )



def detect_fifo_type(data):

    """
    Identify TPM FIFO payload.

    Returns:

        COMMAND
        RESPONSE
        UNKNOWN
    """


    if not is_fifo_stream(data):

        return "UNKNOWN"



    code = get_code(
        data
    )



    if code is None:

        return "UNKNOWN"



    # TPM command codes are generally:
    #
    # 0x000001xx
    # 0x000002xx


    if (
        0x00000100
        <= code
        <= 0x000002FF
    ):

        return "COMMAND"



    # TPM_RC_SUCCESS = 0


    return "RESPONSE"



# =========================================================
# DESCRIPTION
# =========================================================


def describe_fifo(data):


    output=[]


    if not is_fifo_stream(data):

        return "Not a TPM FIFO stream"



    tag=get_tag(data)

    size=get_size(data)

    code=get_code(data)



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
        bytes_to_hex(data)
    )


    return "\n".join(output)



# =========================================================
# SELF TEST
# =========================================================


if __name__ == "__main__":


    sample_command = [

        0x80,0x02,

        0x00,0x00,0x00,0x0A,

        0x00,0x00,0x01,0x82

    ]



    print(
        describe_fifo(
            sample_command
        )
    )