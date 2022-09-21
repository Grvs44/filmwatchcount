from rest_framework.metadata import SimpleMetadata
class TextMetadata(SimpleMetadata):
    def get_field_info(self, field):
        field_info = super().get_field_info(field)
        if 'base_template' in field.style and field.style['base_template'] == 'textarea.html':
            field_info['long'] = True
        return field_info