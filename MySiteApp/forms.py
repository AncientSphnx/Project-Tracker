from django import forms

class UserForm(forms.Form):
    name = forms.CharField(max_length=100, label="Full Name", widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    role = forms.ChoiceField(
        label="Role",
        choices=[('admin', 'Admin'), ('developer', 'Developer'), ('manager', 'Manager'), ('other', 'Other')],
    )
    additional_info = forms.CharField(
        label="Additional Information",
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Enter any additional information (optional)', 'rows': 4}),
    )