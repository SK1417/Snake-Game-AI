import pygame 
import random 

WIN_WIDTH = 600
WIN_HEIGHT = 600
clock = pygame.time.Clock()

# To play snake, I need a screen,
# a snake and food for the snake. The screen can be on a different class, and I can 
# ask it to randomly generate food by using a function call. The snake can be a 
# different class which interacts with the screen



class Snake:
    height = 25
    width = 25
    

    def __init__(self):
        self.leadX = 300
        self.leadY = 300
        self.length = 1
        self.body = [pygame.Rect(self.leadX, self.leadY, self.height, self.width)]
        self.direction = 1 ## 1 - right, 2 - top, 3 - left, 4 - bottom

    def move(self, direction=0):
        if(direction != 0):
            self.direction = direction 

        if self.direction == 2:
            self.leadY = self.leadY - self.width if(self.leadY > self.width) else WIN_WIDTH - self.width
        elif self.direction == 4:
            self.leadY = self.leadY + self.width if(self.leadY < WIN_WIDTH - self.width) else self.width
        elif self.direction == 3:
            self.leadX = self.leadX - self.height if(self.leadX > self.height) else WIN_HEIGHT - self.height
        elif self.direction == 1:
            self.leadX = self.leadX + self.height if(self.leadX < WIN_HEIGHT - self.height) else self.height

        self.body.append(pygame.Rect(self.leadX, self.leadY, self.height, self.width))
        if len(self.body) > self.length:
            del(self.body[0])
    
    def grow(self):
        self.length += 1

    def draw(self, win):
        for rect in self.body:
            pygame.draw.rect(win, pygame.Color('red'), rect)

    def collision(self):
        if(True in [self.body[0].colliderect(x) for x in self.body[1:]]):
            return True
        else:
            return False

class Food: 
    height = 25
    width = 25

    def __init__(self):
        self.x = 20
        self.y = 20
    
    def generate(self):
        self.x = random.randint(0, WIN_WIDTH-self.width)
        self.y = random.randint(0, WIN_HEIGHT-self.height)
    
    def draw(self, win):
        pygame.draw.rect(win, pygame.Color('black'), pygame.Rect(self.x, self.y, self.width, self.height))
    
    def eaten(self, snake):
        if snake.body[-1].colliderect(pygame.Rect(self.x, self.y, self.width, self.height)):
            return True
        else:
            return False

def draw_window(win, snake, food):
    win.fill([255,255,255])
    snake.draw(win)
    food.draw(win)
    pygame.display.update()

def main():

    score = 0
    snake = Snake()
    direction = 1
    food = Food()
    running = True
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_UP):
                    direction = 2
                elif(event.key == pygame.K_DOWN):
                    direction = 4
                elif(event.key == pygame.K_LEFT):
                    direction = 3
                elif(event.key == pygame.K_RIGHT):
                    direction = 1
        
        if snake.collision():
            print('Game Over')
            running = False

        if food.eaten(snake):
            score += 5
            print(score)
            snake.grow()
            food.generate()
            
        #direction = 
        snake.move(direction)

        draw_window(win, snake, food)

main()