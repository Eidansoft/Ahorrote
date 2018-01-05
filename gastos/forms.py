from django import forms


class TagsForm(forms.Form):
    tags = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'tag-selector', 'data-role': 'tagsinput'}
        )
    )
    spending_ids = forms.CharField(widget=forms.HiddenInput())


class SpendingConceptRegexSearchForm(forms.Form):
    regex = forms.CharField()
