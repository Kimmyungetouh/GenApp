class ModelNameForm(ModelForm):
    class Meta:
        model = ModelName
        exclude = ["id", "created", "modified"]  # Add fields that you don't want to edit fron web

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
