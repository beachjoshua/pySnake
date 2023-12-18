import pygame
import random

def checkAppleCoords(x, y, snakeBody, snakeHead, cell_size, width, height):
    repeat = False
    if (x==0):
        x+=1
    if (x==width/cell_size):
        x-=1
    if(y==0):
        y+=1
    if (y==height/cell_size):
        y-=1
    
    for part in snakeBody:
        if part.x == x*cell_size and part.y == y*cell_size:
            repeat = True
    if snakeHead.x == x*cell_size and snakeHead.y == y*cell_size:
        repeat = True
           
    while(repeat):
        x = random.randint(0, width/cell_size)
        y = random.randint(0, height/cell_size)
        if (x==0):
            x+=1
        if (x==width/cell_size):
            x-=1
        if(y==0):
            y+=1
        if (y==height/cell_size):
            y-=1
    
        
        repeat = False
        for part in snakeBody:
            if part.x == x*cell_size and part.y == y*cell_size:
                repeat = True
        if snakeHead.x == x*cell_size and snakeHead.y== y*cell_size:
            repeat = True
            
    return x,y

if __name__ == "__main__":
    #initializing window
    pygame.init()
    width, height = 900, 900
    screen = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()
    running = True

    #runtime vars
    fps = 30
    last_key = None
    frame_counter=0
    bufferedKeys = []

    #snake vars
    speed = 5
    cell_size = 100
    snakeHead_pos = pygame.Vector2(150, 400)
    movement = pygame.Vector2(0, 0)
    body = [pygame.Vector2(100,400), pygame.Vector2(50, 400)]
    #player_rect = pygame.Rect(player_pos.x, player_pos.y, cell_size, cell_size)

    #apple vars
    apple_pos = pygame.Vector2(700, 400)

    while running:
        clock.tick(fps)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if len(bufferedKeys)==0 or event.key != bufferedKeys[-1]:
                        bufferedKeys.append(event.key)
        
        #keys = pygame.key.get_pressed()
            
        frame_counter+=1
        if(frame_counter>=4):
        
            #for key in (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d):
                #if keys[key]:
                    #bufferedKeys.append(key)
            for part in body:
                #if collides withs body and snake is moving
                if snakeHead_rect.colliderect(pygame.Vector2(part).x, pygame.Vector2(part).y, cell_size, cell_size) and (movement.x!=0 or movement.y!=0):
                    running=False
                    
            #update the rest of the body positions
            if(movement.x!=0 or movement.y!=0):
                body.append(pygame.Vector2(snakeHead_pos))
                body.pop(0)
                
            
            if len(bufferedKeys)>0:
            #makes sure snake cant move directly in the oppisote direction snake is going
                if (bufferedKeys[0] == pygame.K_w or bufferedKeys[0] == pygame.K_UP) and movement.y != 1:
                    movement.y = -1
                    movement.x = 0
                elif (bufferedKeys[0] == pygame.K_s or bufferedKeys[0] == pygame.K_DOWN) and movement.y != -1:
                    movement.y = 1     
                    movement.x = 0 
                elif (bufferedKeys[0] == pygame.K_a or bufferedKeys[0] == pygame.K_LEFT) and movement.x != 1:
                    movement.x = -1
                    movement.y = 0 
                elif (bufferedKeys[0] == pygame.K_d or bufferedKeys[0] == pygame.K_RIGHT) and movement.x != -1:
                    movement.x = 1
                    movement.y = 0
            
                #checks heads position and ends if it is at the edge and moving off screen
            if((snakeHead_pos.x >0 and snakeHead_pos.x < width-cell_size) or ((snakeHead_pos.x<=cell_size and movement.x != -1) or (snakeHead_pos.x>= width-cell_size and movement.x != 1))):
                snakeHead_pos.x += movement.x * cell_size
                snakeHead_pos.x = int(snakeHead_pos.x / cell_size) * cell_size
            else:
                 running=False
            if((snakeHead_pos.y >0 and snakeHead_pos.y < height-cell_size) or ((snakeHead_pos.y<=cell_size and movement.y != -1) or (snakeHead_pos.y>= height-cell_size and movement.y != 1))):    
                snakeHead_pos.y += movement.y * cell_size
                snakeHead_pos.y = int(snakeHead_pos.y / cell_size) * cell_size
            else:
                running=False
                    
            #reset bufferedKeys
            if len(bufferedKeys)>0:
                bufferedKeys.pop()
            
            #reset frame_counter
            frame_counter=0
        
        screen.fill("black")
        
        #drawing grid (can delete later)
        for x in range(0, width, cell_size):
            pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, height))
        for y in range(0, height, cell_size):
            pygame.draw.line(screen, (255, 255, 255), (0, y), (width, y))
        
        #update snake rect
        snakeHead_rect = pygame.Rect(snakeHead_pos.x, snakeHead_pos.y, cell_size, cell_size)
        pygame.draw.rect(screen, "green", snakeHead_rect)
        
        #draw rectangle for each length of body
        for part in body:
            body_rect = pygame.Rect(pygame.Vector2(part).x, pygame.Vector2(part).y, cell_size, cell_size)
            pygame.draw.rect(screen, "green", body_rect)
            
        apple_rect = pygame.Rect(apple_pos.x, apple_pos.y, cell_size, cell_size)
        pygame.draw.rect(screen, "red", apple_rect)
        
        appleCollision = snakeHead_rect.colliderect(apple_rect)
        
        #if snake eats apple, grow snake
        if(appleCollision):
            body.append(pygame.Vector2(body[-1]))
            
            #make these values random and not equal to player_pos
            x = random.randint(0, width/cell_size)
            y = random.randint(0, height/cell_size)
            
            x,y = checkAppleCoords(x, y, body, snakeHead_rect, cell_size, width, height)
            
            apple_pos.x= x*cell_size
            apple_pos.y = y*cell_size
            
            apple_rect = pygame.Rect(apple_pos.x, apple_pos.y, cell_size, cell_size)
            pygame.draw.rect(screen, "red", apple_rect)
        
        pygame.display.flip()
        
        
    pygame.quit()
