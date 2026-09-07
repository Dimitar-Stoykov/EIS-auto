from django import forms


class ContactForm(forms.Form):
    first_name = forms.CharField(
        max_length=80,
        label="Име",
        widget=forms.TextInput(attrs={"placeholder": "Вашето име", "class": "ct-input"}),
    )
    last_name = forms.CharField(
        max_length=80,
        label="Фамилия",
        widget=forms.TextInput(attrs={"placeholder": "Вашата фамилия", "class": "ct-input"}),
    )
    email = forms.EmailField(
        label="Е-майл",
        widget=forms.EmailInput(attrs={"placeholder": "example@mail.com", "class": "ct-input"}),
    )
    phone = forms.CharField(
        max_length=30,
        required=False,
        label="Телефон",
        widget=forms.TextInput(attrs={"placeholder": "+359 88 …", "class": "ct-input"}),
    )
    message = forms.CharField(
        label="Съобщение",
        widget=forms.Textarea(attrs={
            "placeholder": "Опишете вашия въпрос или запитване…",
            "class": "ct-input ct-textarea",
            "rows": 5,
        }),
    )
