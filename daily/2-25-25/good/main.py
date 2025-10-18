import ldtk

with open("world.ldtk") as file:
    level = ldtk.FieldDefinition.to_dict(file.read())

print(level.keys())