import tiles


world_dsl = """
|  |MV|LE|BA|  |
|  |RT|  |BT|  |
|  |AV|JG|AV|  |
|  |  |RU|  |  |
|TA|EN|JG|EN|SA|
|  |JG|  |JG|  |
|HU|EN|  |EN|RU|
|  |JG|JG|JG|  |
|  |  |VP|  |  |
|RU|BE|BE|BE|EN|
|  |  |ST|  |  |
"""

tile_type_dict = {"ST": tiles.StartingTile,
                  "LE": tiles.LeavingTile,
                  "VP": tiles.OldPirateTile,
                  "HU": tiles.HutOldPirateTile,
                  "JG": tiles.JungleTile,
                  "EN": tiles.EnemyTile,
                  "RU": tiles.FindRhumTile,
                  "TA": tiles.FindTalisamanTile,
                  "SA": tiles.FindSwordTile,
                  "AV": tiles.WarningTile,
                  "RT": tiles.RiverTile,
                  "BT": tiles.BridgeTile,
                  "MV": tiles.LivingDeadTile,
                  "BA": tiles.BatsTile,
                  "BE": tiles.BeachTile,
                  "NE": tiles.NeutralTile, # for dev only
                  "  ": None}

world_map = []
starting_position = None

def is_dsl_valid(dsl):
    if dsl.count("|ST|") != 1:
        return False
    if dsl.count("|LE|") == 0:
        return False
    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count("|") for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False

    return True

def create_world():
    global starting_position

    if not is_dsl_valid(world_dsl):
        raise SyntaxError("DSL is invalid!")

    dsl_lines = world_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]

    for y, dsl_row in enumerate(dsl_lines):
        row = []
        dsl_cells = dsl_row.split("|")
        dsl_cells = [c for c in dsl_cells if c]
        for x, dsl_cell in enumerate(dsl_cells):
            tile_type = tile_type_dict[dsl_cell]
            row.append(tile_type(x, y) if tile_type else None)
            if dsl_cell == 'ST':
                starting_position = (x, y)

        world_map.append(row)

def tile_at(x, y):
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None