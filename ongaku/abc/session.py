import abc
import typing as t
import dataclasses


@dataclasses.dataclass
class Session(abc.ABC):
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
    def as_payload(cls, payload: dict[t.Any, t.Any]):
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

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)
