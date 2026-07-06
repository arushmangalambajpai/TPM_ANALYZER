"""
register_decoder.py

TPM FIFO Register Content Decoder.

This file converts register values into
human-readable descriptions.

It does NOT:
- Decode SPI headers
- Decode TPM commands
- Decode TPM responses


Main API:

decode_register(
    register_name,
    operation,
    data
)


Example:

decode_register(
    "TPM_ACCESS",
    "READ",
    [0xA0]
)

"""


from tpm_analyzer.utils.byte_utils import (
    get_bit,
    bytes_to_hex
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================


def bytes_to_value(data):

    """
    Convert TPM register bytes into integer.

    byte[0] = lowest address byte
    """

    value = 0


    for index, byte in enumerate(data):

        value |= (
            byte << (8 * index)
        )


    return value



def get_field(value, start, end):

    """
    Extract bit field.

    Example:

    bits 7:4

    start = 4
    end = 7
    """

    size = (
        end - start + 1
    )


    mask = (
        1 << size
    ) - 1


    return (
        value >> start
    ) & mask



def add_bit(output, value, bit, name, meanings):

    bit_value = get_bit(
        value,
        bit
    )


    output.append(
        f"Bit [{bit}] {name} = {bit_value} :"
    )


    output.append(
        meanings[bit_value]
    )


    output.append("")



def add_write_action(output, value, bit, name, description):

    if get_bit(value, bit):

        output.append(
            f"Bit [{bit}] {name} = 1 :"
        )


        output.append(
            description
        )


        output.append("")



def add_field(output, value, high, low, name, description):

    field = get_field(
        value,
        low,
        high
    )


    output.append(
        f"Bits [{high}:{low}] {name} = {field} :"
    )


    output.append(
        description
    )


    output.append("")



# =========================================================
# TPM_ACCESS
# =========================================================


def decode_access(operation, data):

    value = bytes_to_value(data)


    output = [
        "TPM_ACCESS Register:",
        "",
        f"Operation : {operation}",
        ""
    ]


    if operation == "READ":


        add_bit(
            output,value,7,
            "tpmRegValidSts",
            {
            0:"All the bits of this register are not VALID",
            1:"All the bits of this register are VALID"
            }
        )


        add_bit(
            output,value,5,
            "activeLocality",
            {
            0:"This locality is NOT ACTIVE",
            1:"This locality is ACTIVE and has control of TPM"
            }
        )


        add_bit(
            output,value,4,
            "beenSeized",
            {
            0:"Locality operates normally or is not active",
            1:"TPM control has been taken from this locality by a higher locality"
            }
        )


        add_bit(
            output,value,2,
            "pendingRequest",
            {
            0:"No other locality is requesting TPM usage",
            1:"Another locality is requesting TPM usage"
            }
        )


        add_bit(
            output,value,1,
            "requestUse",
            {
            0:"This locality is not requesting TPM or already owns TPM",
            1:"This locality is requesting TPM usage"
            }
        )


        add_bit(
            output,value,0,
            "tpmEstablishment",
            {
            0:"Dynamic OS has previously been established",
            1:"Dynamic OS has NOT previously been established"
            }
        )


    else:


        add_write_action(
            output,value,5,
            "activeLocality",
            "Relinquish control of this locality"
        )


        add_write_action(
            output,value,4,
            "beenSeized",
            "Clear beenSeized bit"
        )


        add_write_action(
            output,value,3,
            "seize",
            "Request TPM to give control to this locality"
        )


        add_write_action(
            output,value,1,
            "requestUse",
            "Request that this locality becomes active"
        )


    return "\n".join(output)



# =========================================================
# TPM_STS
# =========================================================


def decode_sts(operation, data):

    value = bytes_to_value(data)


    output = [
        "TPM_STS Register:",
        "",
        f"Operation : {operation}",
        ""
    ]


    if operation == "READ":


        add_field(
            output,value,27,26,
            "tpmFamily",
            "TPM family identifier"
        )


        add_field(
            output,value,23,8,
            "burstCount",
            "Number of bytes TPM can transfer without wait states"
        )


        add_bit(
            output,value,7,
            "stsValid",
            {
            0:"TPM_STS register fields are invalid",
            1:"TPM_STS register fields are valid"
            }
        )


        add_bit(
            output,value,6,
            "commandReady",
            {
            0:"TPM is not ready for command",
            1:"TPM is ready for command"
            }
        )


        add_bit(
            output,value,4,
            "dataAvail",
            {
            0:"TPM response data unavailable",
            1:"TPM response data available in FIFO"
            }
        )


        add_bit(
            output,value,3,
            "expect",
            {
            0:"TPM is not expecting more command bytes",
            1:"TPM expects more command bytes"
            }
        )


        add_bit(
            output,value,2,
            "selfTestDone",
            {
            0:"TPM self test is not complete",
            1:"TPM self test completed"
            }
        )


    else:


        actions = [

            (25,"resetEstablishmentBit",
             "Reset TPM establishment flag"),

            (24,"commandCancel",
             "Cancel current TPM command execution"),

            (6,"commandReady",
             "Transition TPM to command ready state"),

            (5,"tpmGo",
             "Execute command present inside FIFO"),

            (1,"responseRetry",
             "Request TPM to resend last response")

        ]


        for bit,name,msg in actions:

            add_write_action(
                output,value,bit,name,msg
            )


    return "\n".join(output)

# =========================================================
# INTERRUPT REGISTERS
# =========================================================


def decode_int_enable(operation, data):

    value = bytes_to_value(data)


    output = [
        "TPM_INT_ENABLE Register:",
        "",
        f"Operation : {operation}",
        ""
    ]


    fields = [

        (
            31,
            "globalIntEnable",
            {
            0:"TPM interrupts are globally disabled",
            1:"TPM interrupts are globally enabled"
            }
        ),


        (
            3,
            "commandReadyIntEnable",
            {
            0:"commandReady interrupt is disabled",
            1:"commandReady interrupt is enabled"
            }
        ),


        (
            2,
            "localityChangeIntEnable",
            {
            0:"Locality change interrupt is disabled",
            1:"Locality change interrupt is enabled"
            }
        ),


        (
            1,
            "stsValidIntEnable",
            {
            0:"Status valid interrupt is disabled",
            1:"Status valid interrupt is enabled"
            }
        ),


        (
            0,
            "dataAvailIntEnable",
            {
            0:"Data available interrupt is disabled",
            1:"Data available interrupt is enabled"
            }
        )

    ]


    for bit,name,meaning in fields:

        add_bit(
            output,
            value,
            bit,
            name,
            meaning
        )


    return "\n".join(output)




def decode_int_status(operation, data):

    value = bytes_to_value(data)


    output = [
        "TPM_INT_STATUS Register:",
        "",
        f"Operation : {operation}",
        ""
    ]


    if operation == "READ":


        fields = [

            (
                7,
                "commandReadyIntOccurred",
                {
                0:"Command ready interrupt has not occurred",
                1:"TPM_STS commandReady transitioned from 0 to 1"
                }
            ),


            (
                2,
                "localityChangeIntOccurred",
                {
                0:"Locality change interrupt has not occurred",
                1:"Locality change interrupt occurred"
                }
            ),


            (
                1,
                "stsValidIntOccurred",
                {
                0:"Status valid interrupt has not occurred",
                1:"TPM_STS stsValid transitioned from 0 to 1"
                }
            ),


            (
                0,
                "dataAvailIntOccurred",
                {
                0:"Data available interrupt has not occurred",
                1:"TPM_STS dataAvail transitioned from 0 to 1"
                }
            )

        ]


        for bit,name,meaning in fields:

            add_bit(
                output,
                value,
                bit,
                name,
                meaning
            )


    else:


        actions = [

            (
            7,
            "commandReadyIntOccurred",
            "Clear command ready interrupt"
            ),


            (
            2,
            "localityChangeIntOccurred",
            "Clear locality change interrupt"
            ),


            (
            1,
            "stsValidIntOccurred",
            "Clear status valid interrupt"
            ),


            (
            0,
            "dataAvailIntOccurred",
            "Clear data available interrupt"
            )

        ]


        for bit,name,msg in actions:

            add_write_action(
                output,
                value,
                bit,
                name,
                msg
            )


    return "\n".join(output)




def decode_int_vector(operation, data):

    value = bytes_to_value(data)


    return (
        "TPM_INT_VECTOR Register:\n\n"
        f"Operation : {operation}\n\n"
        f"Bits [7:0] SIRQVector = {value & 0xFF} :\n"
        "Interrupt vector number used by TPM"
    )


# =========================================================
# INTERFACE CAPABILITY
# =========================================================


def decode_intf_capability(operation, data):

    value = bytes_to_value(data)


    output = [
        "TPM_INTF_CAPABILITY Register:",
        "",
        f"Operation : {operation}",
        ""
    ]


    if operation == "WRITE":

        output.append(
            "WARNING: No writable fields"
        )



    add_field(
        output,value,30,28,
        "InterfaceVersion",
        "FIFO interface supported"
    )


    add_field(
        output,value,10,9,
        "DataTransferSizeSupport",
        "Maximum transfer size capability"
    )


    single_bits = [

        (8,"BurstCountStatic"),
        (7,"CommandReadyIntSupport"),
        (6,"InterruptEdgeFalling"),
        (5,"InterruptEdgeRising"),
        (4,"InterruptLevelLow"),
        (3,"InterruptLevelHigh"),
        (2,"LocalityChangeIntSupport"),
        (1,"StsValidIntSupport"),
        (0,"DataAvailIntSupport")

    ]


    for bit,name in single_bits:


        add_bit(
            output,
            value,
            bit,
            name,
            {
            0:"Not supported / disabled",
            1:"Supported / enabled"
            }
        )


    return "\n".join(output)



# =========================================================
# FIFO REGISTERS
# =========================================================


def decode_fifo(register_name, operation, data):

    return (
        f"{register_name} Register:\n\n"
        f"Operation : {operation}\n\n"
        "THIS IS TPM COMMAND REGISTER.\n"
        "DECODE FURTHER TO UNDERSTAND THIS.\n\n"
        "Raw Data:\n"
        f"{bytes_to_hex(data)}"
    )



# =========================================================
# OTHER REGISTERS
# =========================================================


def decode_did_vid(operation, data):

    value = bytes_to_value(data)


    vid = value & 0xFFFF


    did = (
        value >> 16
    ) & 0xFFFF


    return (
        "TPM_DID_VID Register:\n\n"
        f"Operation : {operation}\n\n"
        f"VID = {vid:04X}h :\n"
        "TPM Vendor ID assigned by TCG\n\n"
        f"DID = {did:04X}h :\n"
        "TPM Device ID assigned by vendor"
    )




def decode_rid(operation, data):

    value = bytes_to_value(data)


    return (
        "TPM_RID Register:\n\n"
        f"Operation : {operation}\n\n"
        f"RID = {value & 0xFF:02X}h :\n"
        "TPM Revision ID"
    )




def decode_data_csum(operation, data):

    value = bytes_to_value(data)


    return (
        "TPM_DATA_CSUM Register:\n\n"
        f"Operation : {operation}\n\n"
        f"dataChecksum = {value & 0xFFFF:04X}h :\n"
        "Checksum of command or response data"
    )




def decode_data_csum_enable(operation, data):

    value = bytes_to_value(data)


    output=[]


    output.append(
        "TPM_DATA_CSUM_ENABLE Register:\n"
    )


    output.append(
        f"Operation : {operation}\n"
    )


    add_bit(
        output,
        value,
        0,
        "dataCsumEnable",
        {
        0:"Checksum calculation on command and response data is disabled",
        1:"Checksum calculation on command and response data is enabled"
        }
    )


    return "\n".join(output)



# =========================================================
# MAIN DISPATCHER
# =========================================================


def decode_register(register_name, operation, data):


    operation = operation.upper()


    decoders = {


        "TPM_ACCESS":
            decode_access,


        "TPM_STS":
            decode_sts,


        "TPM_INT_ENABLE":
            decode_int_enable,


        "TPM_INT_STATUS":
            decode_int_status,


        "TPM_INT_VECTOR":
            decode_int_vector,


        "TPM_INTF_CAPABILITY":
            decode_intf_capability,


        "TPM_DID_VID":
            decode_did_vid,


        "TPM_RID":
            decode_rid,


        "TPM_DATA_CSUM":
            decode_data_csum,


        "TPM_DATA_CSUM_ENABLE":
            decode_data_csum_enable

    }



    if register_name in [

        "TPM_DATA_FIFO",

        "TPM_X_DATA_FIFO"

    ]:


        return decode_fifo(
            register_name,
            operation,
            data
        )



    if register_name in decoders:


        return decoders[register_name](
            operation,
            data
        )



    return (
        f"{register_name} Register:\n\n"
        "No decoder available"
    )



# =========================================================
# SELF TEST
# =========================================================


if __name__ == "__main__":


    print(
        decode_register(
            "TPM_ACCESS",
            "READ",
            [0xA0]
        )
    )


    print(
        "\n----------------------\n"
    )


    print(
        decode_register(
            "TPM_DATA_FIFO",
            "WRITE",
            [
                0x80,
                0x02,
                0x00,
                0x00
            ]
        )
    )