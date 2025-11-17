from mcstructure import Block, Structure



with open("../data/testing.mcstructure", "rb") as f:
    struct = Structure.load(f)

# print(type(struct))

layers = struct.get_structure()

mat_dic = {}
for layer in layers:
    for row in layer:
        for block in row:
            if block.name == 'air' or block.name == 'water' or block.name == 'structure_block':
                continue
            if block.name in mat_dic:
                mat_dic[block.name] += 1
            else:
                mat_dic[block.name] = 1

print(sorted(mat_dic))