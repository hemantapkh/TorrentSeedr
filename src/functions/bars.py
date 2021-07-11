#: Progress bar of downloading torrents
def progressBar(progress):
    bars = int(float(progress)) // 6

    return f"{'▬'*bars}{(15-bars)*'▭'} {round(float(progress), 2)}%"

#: Account space bar
def spaceBar(totalSpace, spaceUsed):
    bars = round((spaceUsed / totalSpace) * 20)

    return f"{'▣'*bars}{(20-bars)*'▢'}"