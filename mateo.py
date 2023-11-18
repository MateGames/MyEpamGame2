import pygame
phat = __file__[0:len(__file__)-8]

def save(mapp, phat):
    with open(phat, 'w') as f:
        for i in range(len(mapp)):
            world = ''
            for j in range(len(mapp[i])):
                world += str(mapp[i][j])
            world += '\n'
            f.write(world)



def load(phat):
    mapp = []
    with open(phat, 'r') as f:
        for line in f:
            mapp.append([])
            for i in range(len(line)-1):
                mapp[len(mapp)-1].append(int(line[i]))

    return mapp



def loadImg(sheet, imgs, line):
    asset = {}
    sheet = pygame.image.load(f'{phat}\\img\\{sheet}').convert_alpha()
    sheet = pygame.transform.scale(sheet, (500, 150))

    def getImg(sheet, wid, hig, frame, line):
        img = pygame.Surface((wid, hig)).convert_alpha()
        img.blit(sheet, (0, 0), ((frame * wid), (line * hig), wid, hig))
        img.set_colorkey((0,0,0))
        return img

    for i in range(len(imgs)):
        asset.update({imgs[i] : getImg(sheet, 50, 50, i, line)})

    return asset





'''
save(mapp, 'save.txt')


mapp = load('save.txt')
for i in range(len(mapp)):
    print(mapp[i])
'''