from dtps_http import RawData
from duckietown_messages.actuators import DifferentialPWM
from duckietown_messages.sensors import CompressedImage, Imu, Range
from duckietown_messages.simulation import (
    WorldEntityInput,
    WorldEntityOutput,
    WorldInput,
    WorldOutput,
)
from duckietown_messages.standard import Boolean, Integer


def test_native_world_input_codec_preserves_sensor_payloads() -> None:
    jpeg = b"\xff\xd8\x00\xff\xd9"
    message = WorldInput(
        session_id=7,
        entities={
            "robot": WorldEntityInput(
                compressed_image=CompressedImage(format="jpeg", data=jpeg),
                tof_ranges={"front": Range(data=None)},
                imus={
                    "body": Imu(
                        orientation_covariance=None,
                        angular_velocity_covariance=None,
                        linear_acceleration_covariance=None,
                    ),
                },
                left_encoder_ticks=Integer(data=0),
            ),
        },
    )
    native = message.to_native()
    entity = native["entities"]["robot"]
    assert "pose" not in entity
    assert entity["compressed_image"]["data"] == jpeg
    assert "data" not in entity["tof_ranges"]["front"]
    assert "angular_velocity" not in entity["imus"]["body"]
    assert entity["left_encoder_ticks"]["data"] == 0

    raw = message.to_rawdata()
    assert raw.get_as_native_object() == native
    decoded = WorldInput.from_rawdata(raw)
    assert isinstance(decoded, WorldInput)
    assert decoded == message
    assert decoded.entities is not None
    ranges = decoded.entities["robot"].tof_ranges
    assert ranges is not None
    assert ranges["front"].data is None


def test_native_world_output_codec_preserves_zero_and_false() -> None:
    message = WorldOutput(
        session_id=7,
        entities={
            "robot": WorldEntityOutput(
                differential_pwm=DifferentialPWM(left=0.0, right=0.2),
                state_reset_flag=Boolean(data=False),
            ),
        },
    )
    native = message.to_native()
    entity = native["entities"]["robot"]
    assert "car_lights" not in entity
    assert entity["differential_pwm"]["left"] == 0.0
    assert entity["state_reset_flag"]["data"] is False
    assert WorldOutput.from_rawdata(message.to_rawdata()) == message


def test_native_world_codec_supports_empty_aggregates_and_resets() -> None:
    reset = RawData.cbor_from_native_object(None)
    for message_cls in (WorldInput, WorldOutput):
        message = message_cls(entities={})
        assert message.to_native()["entities"] == {}
        assert "session_id" not in message.to_native()
        assert message_cls.from_rawdata(message.to_rawdata()) == message
        assert message_cls.from_rawdata(reset, allow_none=True) is None
    ordinary_message = Boolean(data=False)
    assert ordinary_message.to_native() == ordinary_message.model_dump()
    assert (
        ordinary_message.to_rawdata().get_as_native_object()
        == ordinary_message.model_dump()
    )
