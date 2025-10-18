import math

level_data = [
    {
        "title": "The Mesmerizer",
        "desc": "Several circles of bullets fly at you. Dodge them and don't run out of health.",
        "time": 60 * 60,
        "song": "cat.mp3"
    }
]

levels = [
    [
        {
            "type": 1,
            "pos": [480, 270],
            "velocity": 2,
            "number": 3,
            "angle": 0,
            "period": 10,
            "activate": round(60 * 8.525),
            "deactivate": round(60 * 27.134),
            "preticks": [
                1, 1
            ]
        },
        {
            "type": 0,
            "pos": [480, 270],
            "velocity": 2,
            "number": 3,
            "angle": 0,
            "period": 10,
            "activate": 0,
            "deactivate": math.inf,
            "preticks": [
                1, -1,
                10, [60 * 2, 1, "*", -1],
                10, [60 * 4, 1, "*", 0.9],
            ]
        },
        {
            "type": 4,
            "pos": [480, 270],
            "velocity": 2,
            "number": 3,
            "angle": 0,
            "period": 10,
            "activate": 30 * 60,
            "deactivate": round(60 * 34.218),
            "preticks": [
                1, 0.5,
                11, [15, "number", "*", 0],
                11, [16, "number", "+", 20]
            ]
        },
        {
            "type": 0,
            "pos": [480, 270],
            "velocity": 2,
            "number": 20,
            "angle": 0,
            "period": 1,
            "activate": round(60 * 38.511),
            "deactivate": round(60 * 38.511) + 2,
            "preticks": [
                0
            ]
        },
    ]
]