from django import forms

REQUIRED_MSG = "Това поле е задължително."


class ContactForm(forms.Form):
    # Required: first name, email, message (a blank message reads as spam).
    # Optional: last name, phone.
    first_name = forms.CharField(
        max_length=80,
        label="Име",
        error_messages={"required": REQUIRED_MSG},
        widget=forms.TextInput(attrs={"placeholder": "Вашето име", "class": "ct-input"}),
    )
    last_name = forms.CharField(
        max_length=80,
        required=False,
        label="Фамилия",
        widget=forms.TextInput(attrs={"placeholder": "Вашата фамилия", "class": "ct-input"}),
    )
    email = forms.EmailField(
        label="Е-майл",
        error_messages={
            "required": REQUIRED_MSG,
            "invalid": "Въведете валиден е-майл адрес.",
        },
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
        error_messages={"required": REQUIRED_MSG},
        widget=forms.Textarea(attrs={
            "placeholder": "Опишете вашия въпрос или запитване…",
            "class": "ct-input ct-textarea",
            "rows": 5,
        }),
    )

    # Honeypot — hidden from real visitors via CSS (see contacts.html/css),
    # left blank by them. Bots that auto-fill every field on a form tend to
    # fill this too. Never shown as an error to the user — ContactsView
    # checks it and silently drops the submission (pretends success) so
    # bots don't learn they were caught.
    website = forms.CharField(
        required=False,
        label="Website",
        widget=forms.TextInput(attrs={
            "autocomplete": "off",
            "tabindex": "-1",
            "class": "ct-hp-field",
        }),
    )
