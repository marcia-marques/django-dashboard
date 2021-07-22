from django import forms


def DataRawFormFunction(path):

    class DataRawForm(forms.Form):
        files_name = forms.FilePathField(widget=forms.Select(
            attrs={'class': 'form-select form-select-sm'}),
            recursive=True, path=path)

    return DataRawForm


class DateInput(forms.DateInput):
    input_type = 'date'


def DateRangeFormFunction(var_choices, min_date, max_date):

    class DateRangeForm(forms.Form):
        start_date = forms.DateField(widget=DateInput(
            attrs={'class': 'form-control form-control-sm'}),
        )
        end_date = forms.DateField(widget=DateInput(
            attrs={'class': 'form-control form-control-sm'}),
        )
        var1 = forms.ChoiceField(widget=forms.Select(
            attrs={'class': 'form-select form-select-sm'}),
            choices=var_choices)
        var2 = forms.ChoiceField(widget=forms.Select(
            attrs={'class': 'form-select form-select-sm'}),
            choices=var_choices)

        def clean(self):
            cleaned_data = super().clean()
            start_date = cleaned_data.get("start_date")
            end_date = cleaned_data.get("end_date")
            if start_date and end_date:
                if start_date >= end_date:
                    raise forms.ValidationError(
                        "Initial date must be less than end date")
                if start_date < min_date:
                    raise forms.ValidationError(
                        "Data starts at " + str(min_date))
                if end_date > max_date:
                    raise forms.ValidationError(
                        "Data starts at " + str(max_date))

    return DateRangeForm
