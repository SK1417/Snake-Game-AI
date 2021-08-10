import pygame
import random
disp_length = 800
disp_width = 600
gameDisplay = pygame.display.set_mode((disp_length,disp_width))
pygame.display.set_caption('Slither.io')
clock = pygame.time.Clock()

food_length = 25
food_width = 25
snake_length = 25
snake_width = 25

def draw_rect(snake_body, snake_length, snake_width, food_x, food_y):
      gameDisplay.fill(pygame.Color('white'))
      pygame.draw.rect(gameDisplay, pygame.Color('black'), [food_x, food_y, food_length, food_width])
      for item in snake_body:
            pygame.draw.rect(gameDisplay, pygame.Color('red'), [item[0], item[1], snake_length, snake_width])
      pygame.display.update()
      clock.tick(10)
      
def collision(snake_body):
      if(snake_body[0] in snake_body[1:]):
            return True
      else:
            return False

lead_x = 300
lead_y = 300
gameExit = False

food_x = random.randint(50, disp_length - food_length)
food_y = random.randint(50, disp_width - food_length)

snake_body = []
snake_len = 1

gameDisplay.fill(pygame.Color('white'))
pygame.draw.rect(gameDisplay, pygame.Color('black'), [food_x, food_y, food_length, food_width])

key_state = 0
while(not gameExit):
      for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                  gameExit = True
            elif(event.type == pygame.KEYDOWN):
                  if(event.key == pygame.K_UP):
                        key_state = 1
                  elif(event.key == pygame.K_DOWN):
                        key_state = 2
                  elif(event.key == pygame.K_LEFT):
                        key_state = 3
                  elif(event.key == pygame.K_RIGHT):
                        key_state = 4
      if(key_state == 1):
            lead_y = lead_y - snake_width if(lead_y > 25) else disp_width - snake_width
      elif(key_state == 2):
            lead_y = lead_y + snake_width if(lead_y < disp_width - snake_width) else 25
      if(key_state == 3):
            lead_x = lead_x - snake_length if(lead_x > 25) else disp_length - snake_length
      if(key_state == 4):
            lead_x = lead_x + snake_length if(lead_x < disp_length - snake_length) else 25

      snake_head = [lead_x, lead_y]
      snake_body.append(snake_head)
      if(len(snake_body)>snake_len):
            del(snake_body[0])
      
      if(collision(snake_body)):
            print('GAME OVER')
            pygame.quit()
            quit()

      if(lead_x in range(food_x - food_length, food_x+food_length) and lead_y in range(food_y-food_width, food_y+food_width)):
            food_x = random.randint(50, disp_length - food_length)
            food_y = random.randint(50, disp_width - food_length)
            snake_len += 1
      draw_rect(snake_body, snake_length, snake_width, food_x, food_y)
      eaten = False

pygame.quit()
quit()
