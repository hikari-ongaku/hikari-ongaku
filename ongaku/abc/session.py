import attrs
import typing as t
from .base import PayloadBase


@attrs.define
class Session(PayloadBase):
    """
    Session

    All of the Session information.

    Find out more [here](https://lavalink.dev/api/rest.html#update-session).

    Parameters
    ----------
    resuming : bool
        Whether resuming is enabled for this session or not
    timeout : int
        The timeout in seconds (default is 60s)
    """

    resuming: bool
    timeout: int

    @classmethod
    def from_payload(cls, payload: dict[str, t.Any]):
        """
        Session parser

        parse a payload of information, to receive a `Session` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        Session
            The Session you parsed.
        """
        resuming = payload["resuming"]
        timeout = payload["timeout"]

        return cls(resuming, timeout)
