from django import template

register = template.Library()

@register.filter
def filetype(data):
    ext = data.get_ext()
    if ext == 'png' or ext == 'jpg' or ext == 'jpeg' or ext == 'gif':
        type = 'image'
    elif ext == 'zip' or ext == 'rar' or ext == '7z':
        type = 'archive'
    elif ext == 'xlsx' or ext == 'xls':
        type == 'excel'
    elif ext == 'pdf':
        type = 'pdf'
    elif ext == 'mp3':
        type = 'audio'
    elif ext == 'docx' or ext == 'dot' or ext == 'dotx':
        type = 'word'
    elif ext == 'html' or ext == 'css' or ext == 'py':
        type = 'code'
    elif ext == 'txt':
        type = 'text'
    else:
        type = 'file'
    return type