from src.module.infrastructure.logging.services.base import Base


class AzureLogging(Base, object):

    def __init__(self, tvd: str, en: str, ev: str):
        """
        Parametric Constructor for Description and Extra
        :param tvd: Scope Tag Value Description
        :param en: Scope Tag Extra Name
        :param ev: Scope Tag Extra Value
        """
        super().__init__()
        self.tag_value = "Azure | " + tvd
        self.extra_name = en
        self.extra_value = ev
