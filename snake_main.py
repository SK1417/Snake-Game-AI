import pygame 
import neat 
import time 
import numpy as np 
import os 
from neat.math_util import softmax
import random 

pygame.font.init()
STAT_FONT = pygame.font.SysFont('comicsans', 50)

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
        self.idle_clock = 0
        self.length = 1
        self.body = [pygame.Rect(self.leadX, self.leadY, self.height, self.width)]
        self.direction = 1 ## 1 - right, 2 - top, 3 - left, 4 - bottom

    def move(self, direction=0):
        self.idle_clock += 1
        if(direction != 0):
            self.direction = direction 
        else:
            self.direction = random.randint(1,4)

        if self.direction == 2:
            self.leadY = self.leadY - self.width #if(self.leadY > self.width) else WIN_WIDTH - self.width
        elif self.direction == 4:
            self.leadY = self.leadY + self.width #if(self.leadY < WIN_WIDTH - self.width) else self.width
        elif self.direction == 3:
            self.leadX = self.leadX - self.height #if(self.leadX > self.height) else WIN_HEIGHT - self.height
        elif self.direction == 1:
            self.leadX = self.leadX + self.height #if(self.leadX < WIN_HEIGHT - self.height) else self.height

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
        elif(self.leadX == 0 or self.leadX == WIN_WIDTH or self.leadY == 0 or self.leadY == WIN_HEIGHT):
            return True
        else:
            return False

class Food: 
    height = 25
    width = 25

    def __init__(self):
        self.generate()
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def generate(self):
        self.x = random.randint(0, WIN_WIDTH-self.width)
        self.y = random.randint(0, WIN_HEIGHT-self.height)
    
    def draw(self, win):
        pygame.draw.rect(win, pygame.Color('black'), pygame.Rect(self.x, self.y, self.width, self.height))
    
    def eaten(self, snake):
        if snake.body[0].colliderect(pygame.Rect(self.x, self.y, self.width, self.height)):
            return True
        else:
            return False

def draw_window(win, snake, food, fitness):
    win.fill([255,255,255])
    snake.draw(win)
    food.draw(win)
    text = STAT_FONT.render('Best Fitness: ' + str(fitness), 1, (0, 0, 0))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    pygame.display.update()

def get_inputs(snake, food, win_size):

    dist_food = [0, 0, 0, 0] ## Top, down, left and right
    dist_body = [0, 0, 0, 0]
    dist_wall = [0, 0, 0, 0]

    ### Look in the right direction 
    for m in range(1, win_size+1):
        x = m*snake.width + snake.leadX
        if(x <= WIN_WIDTH):
            rect = pygame.Rect(x, snake.leadY, snake.width, snake.height)
            ##Check for food
            if(rect.colliderect(food.get_rect())):
                dist_food[3] = m
            ##Check for snake
            if(rect.collidelist(snake.body[1:]) != -1):
                dist_body[3] = m
            
            if(x == 0 or x == WIN_WIDTH):
                dist_wall[3] = m
    
    ### Look in the left direction 
    for m in range(1, win_size+1):
        x = snake.leadX - m*snake.width 
        if(x >= 0):
            rect = pygame.Rect(x, snake.leadY, snake.width, snake.height)
            ##Check for food
            if(rect.colliderect(food.get_rect())):
                dist_food[2] = m
            ##Check for snake
            if(rect.collidelist(snake.body[1:]) != -1):
                dist_body[2] = m

            if(x == 0 or x == WIN_WIDTH):
                dist_wall[2] = m
        
    ### Look in the top direction 
    for m in range(1, win_size+1):
        y = snake.leadY - m*snake.height 
        
        if y >= 0:
            rect = pygame.Rect(snake.leadX, y, snake.width, snake.height)
            ##Check for food
            if(rect.colliderect(food.get_rect())):
                dist_food[0] = m
            ##Check for snake
            if(rect.collidelist(snake.body[1:]) != -1):
                dist_body[0] = m

            if(y == 0 or y == WIN_WIDTH):
                dist_wall[0] = m

    ### Look in the bottom direction
    for m in range(1, win_size+1):
        y = snake.leadY + m*snake.height 
        
        if y <= WIN_HEIGHT:
            rect = pygame.Rect(snake.leadX, y, snake.width, snake.height)
            ##Check for food
            if(rect.colliderect(food.get_rect())):
                dist_food[1] = m
            ##Check for snake
            if(rect.collidelist(snake.body[1:]) != -1):
                dist_body[1] = m  

            if(y == 0 or y == WIN_WIDTH):
                dist_wall[1] = m

    dist_food.extend(dist_body)
    dist_food.extend(dist_wall)
    return tuple(dist_food)

def main(genomes, config):

    nets = []
    ge = []
    snakes = []
    foods = []
    win_size = 10

    for _, g in genomes:     #### Because genomes is a tuple containing the genome id and the genome
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        snakes.append(Snake())
        foods.append(Food())
        g.fitness = 0
        ge.append(g)

    #snake = Snake()
    #food = Food()
    running = True
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    while running:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
        
        if len(snakes) == 0:
            running = False
            break

        for x, snake in enumerate(snakes):

            #if snake.idle_clock == 30:
            #    ge[x].fitness -= 0.2
            
    
            input_vector = get_inputs(snake, foods[x], win_size)
            output = nets[x].activate(input_vector)
            output = softmax(output)
            direction = np.argmax(((output / np.max(output)) == 1).astype(int))
            snake.move(direction)
            #ge[x].fitness += 0.1

            if(ge[x].fitness == max([x.fitness for x in ge])):
                draw_window(win, snake, foods[x], max([x.fitness for x in ge]))

            if foods[x].eaten(snake):
                ge[x].fitness += 2
                snake.idle_clock = 0
                foods[x].generate()
                snake.grow()
            
            if snake.collision():
                ge[x].fitness -= 1
                snakes.pop(x)
                ge.pop(x)
                foods.pop(x)
                nets.pop(x)
            elif ge[x].fitness < 0 or snake.idle_clock > 200:
                snakes.pop(x)
                ge.pop(x)
                foods.pop(x)
                nets.pop(x)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)