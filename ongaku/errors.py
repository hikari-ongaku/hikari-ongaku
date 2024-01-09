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


class RequiredException(OngakuBaseException):
    """
    Raised when a value is required, but is None, or missing.
    """


# MIT License

# Copyright (c) 2023 MPlatypus

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
