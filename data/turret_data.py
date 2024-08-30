TURRET_DATA = {
    "camo": {
        "bullet":[
            {
                #1
                'range': 150,
                'damage' : 1,
                'cooldown': 1500,
                'path' : 'data/assets/images/turrets/Camo/Weapons/turret_01_mk1.png',
            },
            {
                #2
                'range': 150,
                'damage' : 2,
                'cooldown': 1500,
                'path' : 'data/assets/images/turrets/Camo/Weapons/turret_01_mk2.png',
            },
            {
                #3
                'range': 250,
                'damage' : 2,
                'cooldown': 1200,
                'path' : 'data/assets/images/turrets/Camo/Weapons/turret_01_mk3.png',
                
            },
            {
                #4
                'range': 250,
                'damage' : 3,
                'cooldown': 1200,
                'path' : 'data/assets/images/turrets/Camo/Weapons/turret_01_mk4.png',
            },
        ],
        "laze":[
            {
                #1
                'range': 200,
                'damage' : 2,
                'cooldown': 1500,
                'path' : 'data/assets/images/turrets/Camo/Weapons/turret_02_mk1.png',
            },
            {
                #2
                'range': 200,
                'damage' : 2,
                'cooldown': 1200,
                'path' : 'data/assets/images/turrets/Camo/Weapons/turret_02_mk2.png',
            },
            {
                #3
                'range': 250,
                'damage' : 3,
                'cooldown': 1200,
                'path' : 'data/assets/images/turrets/Camo/Weapons/turret_02_mk3.png',
            },
            {
                #4
                'range': 250,
                'damage' : 4,
                'cooldown': 1000,
                'path' : 'data/assets/images/turrets/Camo/Weapons/turret_02_mk4.png',
            },
        ]
    }
}

TURRET_TYPE = {
    1 : {
        #ID = 1
        'name' : 'camo',
        'type' : 'bullet',
        'path' : 'data/assets/images/turrets/Camo/Weapons/weapons_1.png',
        'base_range': 150,
        'cost' : 200,
    },
    2 : {
        #2
        'name' : 'camo',
        'type' : 'laze',
        'path' : 'data/assets/images/turrets/Camo/Weapons/weapons_5.png',
        'base_range': 200,
        'cost' : 400,
    },
}