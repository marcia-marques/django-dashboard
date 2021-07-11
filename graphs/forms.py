from django import forms

from data.models import Campaign


class DateInput(forms.DateInput):
    input_type = 'date'


class DateRangeModelForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['start_date', 'end_date', 'var1', 'var2']
        widgets = {
            'start_date': DateInput(attrs={'class': 'form-control'}),
            'end_date': DateInput(attrs={'class': 'form-control'}),
            'var1': forms.TextInput(attrs={'class': 'form-control'}),
            'var2': forms.TextInput(attrs={'class': 'form-control'})}


class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control form-control-sm'}),
    )
    end_date = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control form-control-sm'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError(
                    "Initial date must be less than end date")
            # if start_date < min_date:
            #     raise forms.ValidationError(
            #         "Data starts at " + str(min_date)
            # if end_date > max_date:
            #     raise forms.ValidationError(
            #         "Data starts at " + str(max_date)
