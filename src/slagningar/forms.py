'''
Created on 22 apr. 2017

@author: hakan
'''

from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    bootfile = forms.FileField(label='Välj fil',help_text='max. 42 megabytes')
