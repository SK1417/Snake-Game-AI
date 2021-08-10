import pygame
import random

disp_length = 800
disp_width = 600
clock = pygame.time.Clock()



def collision(snake_body):
      if(snake_body[0] in snake_body[1:]):
            return True
      else:
            return False

def gameloop(board_obj, snake_obj):
      snake_obj.snake_head = [board_obj.lead_x, board_obj.lead_y]
      snake_obj.snake_body.append(snake_obj.snake_head)

      if(len(snake_obj.snake_body)>snake_obj.snake_len):
            del(snake_obj.snake_body[0])
      
      if(collision(snake_obj.snake_body)):
            print('GAME OVER')
            pygame.quit()
            quit()
      if(board_obj.lead_x in range(board_obj.food_x - board_obj.food_length, board_obj.food_x + board_obj.food_length)
       and board_obj.lead_y in range(board_obj.food_y - board_obj.food_width, board_obj.food_y + board_obj.food_width)):
            board_obj.food_x = random.randint(50, disp_length - board_obj.food_length)
            board_obj.food_y = random.randint(50, disp_width - board_obj.food_length)
            snake_obj.snake_len += 1
      
      board_obj.draw_rect(snake_obj)

class board:
      gameDisplay = pygame.display.set_mode((disp_length, disp_width))
      food_length = 25
      food_width = 25
      food_x = 0
      food_y = 0
      lead_x = 300
      lead_y = 300
      gameExit = False
      
      def __init__(self):
            gameDisplay = pygame.display.set_mode((disp_length, disp_width))
            pygame.display.set_caption('Slither.io')
            gameDisplay.fill(pygame.Color('white'))
            gameExit = False

      def get_snake(self, snake_obj):
            self.lead_x = snake_obj.lead_x
            self.lead_y = snake_obj.lead_y
      
      def move_up(self, snake_obj):
            self.lead_y = self.lead_y - snake_obj.snake_width if(self.lead_y > 25) else disp_width - snake_obj.snake_width
            gameloop(self, snake_obj)

      def move_down(self, snake_obj):
            self.lead_y = self.lead_y + snake_obj.snake_width if(self.lead_y < disp_width - snake_obj.snake_width) else 25
            gameloop(self, snake_obj)

      def move_left(self, snake_obj):
            self.lead_x = self.lead_x - snake_obj.snake_length if(self.lead_x > 25) else disp_length - snake_obj.snake_length
            gameloop(self, snake_obj)

      def move_right(self, snake_obj):
            self.lead_x = self.lead_x + snake_obj.snake_length if(self.lead_x < disp_length - snake_obj.snake_length) else 25
            gameloop(self, snake_obj)

      def draw_rect(self, snake_obj):
            self.gameDisplay.fill(pygame.Color('white'))
            pygame.draw.rect(self.gameDisplay, pygame.Color('black'), [self.food_x, self.food_y, self.food_length, self.food_width])
            for item in snake_obj.snake_body:
                  pygame.draw.rect(self.gameDisplay, pygame.Color('red'), [item[0], item[1], snake_obj.snake_length, snake_obj.snake_width])
            if(collision(snake_obj.snake_body)):
                  print('GAME OVER')
                  pygame.quit()
                  quit()
            if(len(snake_obj.snake_body)>snake_obj.snake_len):
                  del(snake_obj.snake_body[0])
            pygame.display.update()
            clock.tick(10)
      

class snake:
      lead_x = 300
      lead_y = 300
      snake_length = 25
      snake_width = 25
      snake_body = []
      snake_len = 1
      snake_head = []

      def __init__(self):
            self.lead_x = 300
            self.lead_y = 300
            self.snake_length = 25
            self.snake_width = 25
            self.snake_head = [self.lead_x, self.lead_y]
            self.snake_body.append(self.snake_head)


gameloop()