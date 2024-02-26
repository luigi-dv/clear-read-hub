from abc import abstractmethod

from sentry_sdk import scope


class Base:
    def __init__(self):
        self._tag_name = "External Service"
        self._tag_value = None
        self._extra_name = None
        self._extra_value = None

    @property
    def tag_name(self) -> str:
        return self._tag_name

    @property
    def tag_value(self) -> str:
        return self._tag_value

    @tag_value.setter
    def tag_value(self, tv: str):
        self._tag_value = tv

    @property
    def extra_name(self) -> str:
        return self._extra_name

    @extra_name.setter
    def extra_name(self, en: str):
        self._extra_name = en

    @property
    def extra_value(self) -> str:
        return self._extra_value

    @extra_value.setter
    def extra_value(self, ev: str):
        self._extra_value = ev

    def set_sentry_tag(self, s: scope):
        s.set_tag(self.tag_name, self.tag_value)

    def set_sentry_extra(self, s: scope):
        s.set_extra(self._extra_name, self._extra_value)
