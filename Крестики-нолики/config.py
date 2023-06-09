"""
Словарь, для рисования крестиков и ноликов в форме игрового поля.
Каждому кючу сопостовляется кнопка, в соответсвии с её номером (текстом кнопки).
В качестве значений, представлены наборы координат в кортежах: (x0, y0, x1, y1)
"""

coordinates_by_position = {
    "x":
        {
            0: [(20, 20, 180, 180), (180, 20, 20, 180)],
            1: [(220, 20, 380, 180), (380, 20, 220, 180)],
            2: [(420, 20, 580, 180), (580, 20, 420, 180)],
            3: [(20, 220, 180, 380), (180, 220, 20, 380)],
            4: [(220, 220, 380, 380), (380, 220, 220, 380)],
            5: [(420, 220, 580, 380), (580, 220, 420, 380)],
            6: [(20, 420, 180, 580), (180, 420, 20, 580)],
            7: [(220, 420, 380, 580), (380, 420, 220, 580)],
            8: [(420, 420, 580, 580), (580, 420, 420, 580)],
        },
    "o":
        {
            0: (10, 10, 190, 190),
            1: (210, 10, 390, 190),
            2: (410, 10, 590, 190),
            3: (10, 210, 190, 390),
            4: (210, 210, 390, 390),
            5: (410, 210, 590, 390),
            6: (10, 410, 190, 590),
            7: (210, 410, 390, 590),
            8: (410, 410, 590, 590),
        }
}
