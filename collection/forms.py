from django import forms
import unicodedata

from .models import Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["audio", "transcription", "dialect"]

    def clean_audio(self):
        audio = self.cleaned_data["audio"]
        if audio.size > 10 * 1024 * 1024:
            raise forms.ValidationError("Recording is too large (10 MB max).")
        if not audio.content_type.startswith("audio/"):
            raise forms.ValidationError("Please upload an audio file.")
        return audio


    def clean_transcription(self):
        text = self.cleaned_data["transcription"].strip()
        return unicodedata.normalize("NFC", text)