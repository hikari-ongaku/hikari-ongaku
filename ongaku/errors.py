class OngakuBaseException(Exception):
    """
    The base exception for all Ongaku exceptions.
    """


class BuildException(OngakuBaseException):
    """
    Raised when a model fails to build correctly.
    """


class LavalinkException(OngakuBaseException):
    """
    Raised when an error is returned on the websocket, or a rest command.
    """


class LavalinkConnectionException(LavalinkException):
    """
    Raised when any Rest action (or a websocket connection) fails to connect to the lavalink server.
    """


class SessionNotStartedException(LavalinkException):
    """
    Raised when the session id is needed, but is null.
    """

class SessionError(LavalinkException):
    """
    Raised when an error occurs with the Lavalink websocket connection.
    """


class PlayerException(OngakuBaseException):
    """
    Base player related exceptions
    """


class PlayerSettingException(PlayerException):
    """
    Raised when a setting is set wrong.
    """

class PlayerCreateException(PlayerException):
    """
    Raised when ongaku failed to build a new player, or connect to the channel.
    """

class PlayerMissingException(PlayerException):
    """
    Raised when the player does not exist.
    """


class PlayerQueueException(PlayerException):
    """
    Raised when there is a problem with the queue.
    """


class GatewayOnlyException(OngakuBaseException):
    """
    Raised when Gateway bot is not used.
    """
