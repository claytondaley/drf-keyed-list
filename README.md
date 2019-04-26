# Keyed Lists for Django REST Framework

This package supports the serialization and deserialization of a list of objects stored in a `dict` where a unique
value from the object (often a `pk`) is used as the key in the dict.  For example,


```
{
    "1": {
        <other fields for object with id 1> 
    },
    "2": {
        <other fields for object with id 2>
    },
    ...
}
```

# Install

```
pip install drf-keyed-list
```

# Usage

The following is a usage example:

```python
class MySerializer(ModelSerializer):

    class Meta:
        list_serializer_class = KeyedListSerializer
        keyed_list_serializer_field = 'id'
```

By replacing the `list_serializer_class`, this behavior will only be enabled when the `many=True` flag is used:

```python
instance = {
   "id": "pk_val",
   "field1": "val1",
   "field2": "val2",
   ...
}

serializer = MySerializer(data=instance)
# this should work
serializer.is_valid()
serializer.save()

keyed_list = {
   "pk_val": {
       "field1": "val1",
       "field2": "val2",
       ...
   }
}

# many=True will trigger the keyed-list behavior
serializer = MySerializer(data=keyed_list, many=True)
# this should also work
serializer.is_valid()
serializer.save()
```

NOTE: `keyed_list_serializer_field` ***MUST*** refer to a Unique field or key collision may occur during serialization,
plus undefined deserializaiton behavior if used in combination with nested writable serializers (e.g.
[drf-writable-nested](https://github.com/beda-software/drf-writable-nested)).  At this time, the package does not
make any effort to verify that a Unique field has been selected.

## Non-String Keys (e.g. UUIDs)

Per the [JSON RFC](https://tools.ietf.org/html/rfc7159.html#section-4) the keys (a.k.a. "names") in a JSON structure 
must be strings.  The JSON Encoder in Py2 only accepts strings; in Py3, the encoder accepts some additional types (i.e. 
`int`, `float`, `bool` or `None`), but these must eventually be converted to strings.  Other types are not supported,
including common key types like UUID.

Per the discussion in issue #6, the recommended strategy for non-string keys is to use an expicit (if necessary, custom)
serializer field.  This field should implement `to_representation` and `to_internal_value` to convert the data to a 
string. For a UUID, the built-in `UUIDField` is sufficient.

Authors
=======
2018, Clayton Daley III
