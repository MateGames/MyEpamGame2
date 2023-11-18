    mouse = pygame.mouse.get_pos()
    mouse = pygame.Rect(mouse[0],mouse[1],1,1) 

    def button(x, y, wid, hig, text,size):
        button = pygame.Rect(x,y,wid,hig)
        if button.colliderect(mouse):
            pygame.draw.rect(screen, BLUE, pygame.Rect(x-10,y-10,wid+20,hig+20), 5)

        pygame.draw.rect(screen, BLACK, button, 5)
        font = pygame.font.Font(f"{phat}font\\Anton\\Anton-Regular.ttf", size)
        text = font.render(text, True, BLACK)
        screen.blit(text,(x+30,y-4))
    
    button(100,100,250,150,'PLAY',105)
    button(100,300,250,50,'SETTINGS',38)
    button(100,400,250,50,'QUIT',38)