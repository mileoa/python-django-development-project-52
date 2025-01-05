from django.forms import ModelForm
from labels.models import Labels


class LabelsForm(ModelForm):

    class Meta:
        model = Labels
        fields = ["name"]
