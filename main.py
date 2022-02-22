from timeit import timeit
from tabulate import tabulate
import sys

message = '''d = {
 'PackageID' : 1539,
 'PersonID' : 33,
 'Name' : """MEGA_GAMER_2222""",
 'Inventory': dict((str(i),i) for i in iter(range(100))),
 'CurrentLocation': """
 Pentos is a large port city, more populous than Astapor on Slaver Bay,
 and may be one of the most populous of the Free Cities.
 It lies on the bay of Pentos off the narrow sea, with the Flatlands
 plains and Velvet Hills to the east.
 The city has many square brick towers, controlled by the spice traders.
 Most of the roofing is done in tiles. There is a large red temple in
 Pentos, along with the manse of Illyrio Mopatis and the Sunrise Gate
 allows the traveler to exit the city to the east,
 in the direction of the Rhoyne.
 """
}'''

avro_schema_message = """test_schema = '''
    {"namespace": "test.avro",
     "type": "record",
     "name": "User",
     "fields": [
         {"name": "PackageID", "type": "int"},
         {"name": "PersonID",  "type": "int"},
         {"name": "Name",  "type": "string"},
         {"name": "Inventory", "type": {"type": "map", "values": "int"}},
         {"name": "CurrentLocation", "type": "string"}
     ]
    }
    '''
    """

setup_pickle = '%s ; import pickle ; src = pickle.dumps(d, 2)' % message
setup_json = '%s ; import json; src = json.dumps(d)' % message
setup_XML = "%s\n" \
            "import dicttoxml, xmltodict\n" \
            "src = dicttoxml.dicttoxml(d)\n" % message
setup_protobuf = "%s\n" \
                 "import google.protobuf.json_format as format\n" \
                 "from scheme_pb2 import Player\n" \
                 "src = format.ParseDict(d, Player())" % message
setup_apacheAvro = "%s\n" \
                   "%s\n" \
                   "import io, avro.io\n" \
                   "schema = avro.schema.parse(test_schema)\n" \
                   "writer = avro.io.DatumWriter(schema)\n" \
                   "bytes_writer = io.BytesIO()\n" \
                   "encoder = avro.io.BinaryEncoder(bytes_writer)\n" \
                   "writer.write(d, encoder)\n" \
                   "src = bytes_writer.getvalue()" % (message, avro_schema_message)
setup_yaml = "%s\n" \
             "import yaml\n" \
             "src = yaml.dump(d)" % message
setup_msgpack = '%s\n' \
                'import ormsgpack\n' \
                'src = ormsgpack.packb(d)' % message

tests = [
 # (title, setup, enc_test, dec_test)
 ('pickle (native serialization)', setup_pickle, 'pickle.dumps(d, 2)', 'pickle.loads(src)'),
 ('json', setup_json, 'json.dumps(d)', 'json.loads(src)'),
 ('XML', setup_XML, 'dicttoxml.dicttoxml(d)', 'xmltodict.parse(src)'),
 ('ProtoBuf', setup_protobuf, 'format.ParseDict(d, Player())', 'format.MessageToJson(src)'),
 ('ApacheAvro', setup_apacheAvro, 'bytes_writer.getvalue()', 'reader = avro.io.DatumReader(schema);'\
                                                             'message_bytes = io.BytesIO(src);'\
                                                             'decoder = avro.io.BinaryDecoder(message_bytes);'\
                                                             'reader.read(decoder)'),
 ('YAML', setup_yaml, 'yaml.dump(d)', 'yaml.safe_load(src)'),
 ('MessagePack', setup_msgpack, 'ormsgpack.packb(d)', 'ormsgpack.unpackb(src)')
]
loops = 1000
enc_table = []
dec_table = []
print("Running tests (%d loops each)" % loops)

for title, mod, enc, dec in tests:
    print(title)
    print(" [Encode]", enc)
    result = timeit(enc, mod, number=loops)
    exec(mod)
    enc_table.append([title, result, sys.getsizeof(src)])
    print(" [Decode]", dec)
    result = timeit(dec, mod, number=loops)
    dec_table.append([title, result])

enc_table.sort(key=lambda x: x[1])
enc_table.insert(0, ['Package', 'Seconds', 'Size'])
dec_table.sort(key=lambda x: x[1])
dec_table.insert(0, ['Package', 'Seconds'])
print("\nEncoding Test (%d loops)" % loops)
print(tabulate(enc_table, headers="firstrow"))
print("\nDecoding Test (%d loops)" % loops)
print(tabulate(dec_table, headers="firstrow"))


d = {
    'PackageID': 1539,
    'PersonID': 33,
    'Name': """MEGA_GAMER_2222""",
    'Inventory': dict((str(i), i) for i in iter(range(100))),
    'CurrentLocation': """
                         Pentos is a large port city, more populous than Astapor on Slaver Bay,
                         and may be one of the most populous of the Free Cities.
                         It lies on the bay of Pentos off the narrow sea, with the Flatlands
                         plains and Velvet Hills to the east.
                         The city has many square brick towers, controlled by the spice traders.
                         Most of the roofing is done in tiles. There is a large red temple in
                         Pentos, along with the manse of Illyrio Mopatis and the Sunrise Gate
                         allows the traveler to exit the city to the east,
                         in the direction of the Rhoyne.
                         """
}
