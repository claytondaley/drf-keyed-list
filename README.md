# Keyed Lists for Django REST Framework

This package supports the serialization and deserialization of a list of objects stored in a `dict` where a unique
value from the object (often a `pk`) is used as the key in the dict.  For example,


```
{
    "1": {<other fields for object with id 1>},
    "2": {<other fields for object with id 2>},
    ...
}
```

The following is a usage example:

```
class MySerializer(ModelSerializer):

    class Meta:
        list_serializer_class = KeyedListSerializer
        keyed_list_serializer_field = 'id'
```

By replacing the `list_serializer_class`, this behavior will only be enabled when the `many=True` flag is used:

```
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
serializer = MySerializer(data=instance, many=True)
# this should also work
serializer.is_valid()
serializer.save()
```

Authors
=======
2018, Clayton Daley III
