from django import forms


class TestForm(forms.Form):
    """Test form for """
    id = forms.IntegerField()
    