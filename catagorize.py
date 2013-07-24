def catagorize(actors):
    """Attempt to guess what raid the given group is from"""

    # print actors
    guilds = {
        'Space Goats': [
            'Fatset',
            'Thenmal',
            'Vataro',
            'Chrysothemis',
            'Neokarasu',
            'Nastaera',
            'Donut',
            'Caelestea',
            'Leftenant',
            'Electrufu',
            'Amitriptylin',
        ],
        'Physics': [
            'Piggyslasher',
            'Banard',
            'Worgenesis',
            'Roor',
            'Masozally',
            'Mognet',
            'Manaitix',
            'Leare',
            'Aset',
        ]
    }
    results = {guild: 0 for guild in guilds}

    for player in actors:
        for guild in guilds:
            for member in guilds[guild]:
                if player == member:
                    results[guild] += 1
                    
    # sort the results
    return sorted(results, key=results.get, reverse=True)[0]


