class Television:
    """
    TV remote simulation with power, channel, and volume controls.

    Channels wrap around. Volume and channel changes are ignored while the TV is powered off.
    """

    MIN_VOLUME: int = 0
    MAX_VOLUME: int = 20
    MIN_CHANNEL: int = 1
    MAX_CHANNEL: int = 10

    def __init__(self) -> None:
        """Initialize tv with power off and all values at minimum."""
        self.__status: bool = False
        self.__muted: bool = False
        self.__volume: int = Television.MIN_VOLUME
        self.__channel: int = Television.MIN_CHANNEL

    def power(self) -> None:
        """Toggle the tv power on or off."""
        self.__status = not self.__status

    def mute(self) -> None:
        """Toggle mute on or off. Has no effect when TV is powered off."""
        if self.__status:
            self.__muted = not self.__muted

    def channel_up(self) -> None:
        """
        Increase channel by 1.
        Wraps to MIN_CHANNEL when going > MAX_CHANNEL.
        Has no effect when TV is powered off.
        """
        if self.__status:
            if self.__channel == Television.MAX_CHANNEL:
                self.__channel = Television.MIN_CHANNEL
            else:
                self.__channel += 1

    def channel_down(self) -> None:
        """
        Decrease channel by 1.
        Wraps to MAX_CHANNEL when < MIN_CHANNEL.
        Has no effect when TV is powered off.
        """
        if self.__status:
            if self.__channel == Television.MIN_CHANNEL:
                self.__channel = Television.MAX_CHANNEL
            else:
                self.__channel -= 1

    def volume_up(self) -> None:
        """
        Increase volume by 1.
        Unmutes first if currently muted.
        Has no effect when TV is powered off or volume is at max.
        """
        if self.__status:
            if self.__muted:
                self.__muted = False
            if self.__volume < Television.MAX_VOLUME:
                self.__volume += 1

    def volume_down(self) -> None:
        """
        Decrease volume by 1.
        Unmutes first if currently muted.
        Has no effect when TV is powered off or volume is at min.
        """
        if self.__status:
            if self.__muted:
                self.__muted = False
            if self.__volume > Television.MIN_VOLUME:
                self.__volume -= 1

    def set_channel(self, channel: int) -> bool:
        """
        Set channel directly to a given value.
        channel: (int) The channel number to switch to.
        return: True if the channel was set successfully, False otherwise.
        """
        if self.__status and Television.MIN_CHANNEL <= channel <= Television.MAX_CHANNEL:
            self.__channel = channel
            return True
        return False

    def is_on(self) -> bool:
        """Return True if the tv is powered on."""
        return self.__status

    def is_muted(self) -> bool:
        """Return True if the tv is currently muted."""
        return self.__muted

    def get_volume(self) -> int:
        """Return the current volume level."""
        return self.__volume

    def get_channel(self) -> int:
        """Return the current channel number."""
        return self.__channel
