# from django.forms import ModelForm
# from . import models
#
#
class ModelNameForm(ModelForm):
    class Meta:
        model = models.ModelName
        exclude = ["id", ]  # Add fields that you don't want to edit fron web

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
