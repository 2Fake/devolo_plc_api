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

class SetUserDeviceName(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    MAC_ADDRESS_FIELD_NUMBER: builtins.int
    USER_DEVICE_NAME_FIELD_NUMBER: builtins.int
    mac_address: typing.Text
    """MAC address of the targeted device"""

    user_device_name: typing.Text
    """user provided device name, if any"""

    def __init__(self,
        *,
        mac_address: typing.Text = ...,
        user_device_name: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["mac_address",b"mac_address","user_device_name",b"user_device_name"]) -> None: ...
global___SetUserDeviceName = SetUserDeviceName

class SetUserDeviceNameResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class _Result:
        ValueType = typing.NewType('ValueType', builtins.int)
        V: typing_extensions.TypeAlias = ValueType
    class _ResultEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[SetUserDeviceNameResponse._Result.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        SUCCESS: SetUserDeviceNameResponse._Result.ValueType  # 0
        MACADDR_INVALID: SetUserDeviceNameResponse._Result.ValueType  # 1
        MACADDR_UNKNOWN: SetUserDeviceNameResponse._Result.ValueType  # 2
        DEVICE_NAME_INVALID: SetUserDeviceNameResponse._Result.ValueType  # 3
        COMMUNICATION_ERROR: SetUserDeviceNameResponse._Result.ValueType  # 254
        UNKNOWN_ERROR: SetUserDeviceNameResponse._Result.ValueType  # 255
    class Result(_Result, metaclass=_ResultEnumTypeWrapper):
        pass

    SUCCESS: SetUserDeviceNameResponse.Result.ValueType  # 0
    MACADDR_INVALID: SetUserDeviceNameResponse.Result.ValueType  # 1
    MACADDR_UNKNOWN: SetUserDeviceNameResponse.Result.ValueType  # 2
    DEVICE_NAME_INVALID: SetUserDeviceNameResponse.Result.ValueType  # 3
    COMMUNICATION_ERROR: SetUserDeviceNameResponse.Result.ValueType  # 254
    UNKNOWN_ERROR: SetUserDeviceNameResponse.Result.ValueType  # 255

    RESULT_FIELD_NUMBER: builtins.int
    result: global___SetUserDeviceNameResponse.Result.ValueType
    """contains the result of SetUserDeviceName message"""

    def __init__(self,
        *,
        result: global___SetUserDeviceNameResponse.Result.ValueType = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["result",b"result"]) -> None: ...
global___SetUserDeviceNameResponse = SetUserDeviceNameResponse
