from django.forms.utils import ErrorDict
from django.utils.encoding import force_text


class LabelErrorsDict(ErrorDict):
    def as_text_by_key(self):
        return {k: force_text(v) for k, v in self.items()}
