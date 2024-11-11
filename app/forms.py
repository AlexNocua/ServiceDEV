from django import forms
from .models import ModelProductos, ModelUsuarios
from django.contrib.auth.forms import UserChangeForm


class ModelProductosForm(forms.ModelForm):
    imagen_file = forms.ImageField(required=False)  # Campo para cargar la imagen

    class Meta:
        model = ModelProductos
        exclude = ["imagen"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data["imagen_file"]:
            instance.imagen = self.cleaned_data["imagen_file"].read()
        if commit:
            instance.save()
        return instance


class UsuarioEditForm(UserChangeForm):
    class Meta:
        model = ModelUsuarios
        fields = ["nombre_completo", "correo"]

    password = forms.CharField(
        widget=forms.PasswordInput(), required=False, help_text="Contraseña opcional"
    )
