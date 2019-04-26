from django.utils.translation import ugettext_lazy as _
from rest_framework.serializers import ListSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SkipField
from rest_framework.settings import api_settings


class KeyedListSerializer(ListSerializer):
    default_error_messages = {
        'not_a_dict': _('Expected a dict of items but got type "{input_type}".'),
        'empty': _('This dict may not be empty.')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        meta = getattr(self.child, 'Meta', None)
        assert hasattr(meta, 'keyed_list_serializer_field'), \
            "Must provide a field name at keyed_list_serializer_field when using KeyedListSerializer"
        self._keyed_field = meta.keyed_list_serializer_field

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            message = self.error_messages['not_a_dict'].format(
                input_type=type(data).__name__
            )
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='not_a_dict')
        if not self.allow_empty and len(data) == 0:
            if self.parent and self.partial:
                raise SkipField()

            message = self.error_messages['empty']
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='empty')
        data = [{**v, **{self._keyed_field: k}} for k, v in data.items()]
        return super().to_internal_value(data)

    def to_representation(self, data):
        response = super().to_representation(data)
        return {v.pop(self._keyed_field): v for k, v in response.items()}

    def is_valid(self, raise_exception=False):
        return super().is_valid(raise_exception)
