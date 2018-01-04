from django import forms


class TagsForm(forms.Form):
    tags = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'tag-selector', 'data-role': 'tagsinput'}
        )
    )
    spending_ids = forms.CharField(max_length=256, widget=forms.HiddenInput())


class SpendingConceptRegexSearchForm(forms.Form):
    regex = forms.CharField()
