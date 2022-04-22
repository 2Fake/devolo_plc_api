"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class PairDeviceStart(google.protobuf.message.Message):
    """
    Message to trigger the pairing process
    Http POST this payload
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    MAC_ADDRESS_FIELD_NUMBER: builtins.int
    mac_address: typing.Text
    """MAC address of the targeted device"""

    def __init__(self,
        *,
        mac_address: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["mac_address",b"mac_address"]) -> None: ...
global___PairDeviceStart = PairDeviceStart

class PairDeviceResponse(google.protobuf.message.Message):
    """
    Message which will be returned upon reception of PairDeviceStarte
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class _Result:
        ValueType = typing.NewType('ValueType', builtins.int)
        V: typing_extensions.TypeAlias = ValueType
    class _ResultEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[PairDeviceResponse._Result.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        SUCCESS: PairDeviceResponse._Result.ValueType  # 0
        MACADDR_INVALID: PairDeviceResponse._Result.ValueType  # 1
        MACADDR_UNKNOWN: PairDeviceResponse._Result.ValueType  # 2
        COMMUNICATION_ERROR: PairDeviceResponse._Result.ValueType  # 254
        UNKNOWN_ERROR: PairDeviceResponse._Result.ValueType  # 255
    class Result(_Result, metaclass=_ResultEnumTypeWrapper):
        pass

    SUCCESS: PairDeviceResponse.Result.ValueType  # 0
    MACADDR_INVALID: PairDeviceResponse.Result.ValueType  # 1
    MACADDR_UNKNOWN: PairDeviceResponse.Result.ValueType  # 2
    COMMUNICATION_ERROR: PairDeviceResponse.Result.ValueType  # 254
    UNKNOWN_ERROR: PairDeviceResponse.Result.ValueType  # 255

    RESULT_FIELD_NUMBER: builtins.int
    result: global___PairDeviceResponse.Result.ValueType
    """contains the result of PairDeviceStart"""

    def __init__(self,
        *,
        result: global___PairDeviceResponse.Result.ValueType = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["result",b"result"]) -> None: ...
global___PairDeviceResponse = PairDeviceResponse
