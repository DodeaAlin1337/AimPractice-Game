import math
import random
import time
import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))  #The window that we are playing on.
pygame.display.set_caption('Aim Trainer')

TARGET_INCREMENT = 450 #(miliseconds) Larger = easier, Smaller = harder.And is the delay we want till we create another target
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30 #How many pixels i want this to be off the edge of the screen.(spacing around the edge)

BG_COLOR = (0, 25, 40)
LIVES = 3
TOP_BAR_HEIGHT = 50

#When we want to draw a text in pygame, we need to create a font object and then render an instance of that font.
LABEL_FONT = pygame.font.SysFont('comicsans', 24)

class Target:
   MAX_SIZE = 35
   GROWTH_RATE = 0.35
   COLOR = 'green'
   SECOND_COLOR = 'purple'
   
   def __init__(self, x, y):
      self.x = x
      self.y = y
      self.size = 0
      self.grow = True
      
   def update(self): #Function for the target to increase in size by grow rate to it's max size value
      if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
         self.grow = False
      
      if self.grow:
         self.size += self.GROWTH_RATE  #Target is growing
      else:
         self.size -= self.GROWTH_RATE  #Target is shrinking
         
   def draw(self, win): #Function for drawing.
      pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)  #Create a tuple that contains the X, Y positions of the center of the target + the size of it.
      pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8) #For the size we need to do it with a multiplication factor to have it
      pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6) #based on our current size our circle is because it's gonna grow and shrink
      pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)
      
   def collide(self, x, y): #This will be the mouse position to see if we collide with the circle
      dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
      return dis <= self.size
      

def draw(win, targets): #The order in which we draw things is important, if we draw something over a top of something else it's gonna overlap it
   win.fill(BG_COLOR) #With this function we will clear the screen every single time we draw.(frame by frame rendering)
   
   for target in targets:
      target.draw(win)
      
   pygame.display.update()

def format_time(secs):
   milli = math.floor(int(secs * 1000 % 1000) / 100)
   seconds = int(round(secs % 60, 1))
   minutes = int(secs // 60)
   
   return f'{minutes:02d}:{seconds:02d}:{milli}'

def draw_top_bar(win, elapsed_time, targets_pressed, misses):
   pygame.draw.rect(win,"grey",(0, 0, WIDTH, TOP_BAR_HEIGHT)) #Top left hand corner(0, 0).
   time_label = LABEL_FONT.render(f'Time: {format_time(elapsed_time)}',1,'black')
   
   speed = round(targets_pressed / elapsed_time, 1)
   speed_label = LABEL_FONT.render(f'Speed: {speed} t/s', 1, 'black')
   
   hits_label = LABEL_FONT.render(f'Hits: {targets_pressed}', 1, 'black')
   
   lives_label = LABEL_FONT.render(f'Lives: {LIVES - misses}', 1, 'black')
   
   win.blit(time_label, (5, 5))
   win.blit(speed_label, (200, 5))
   win.blit(hits_label, (450, 5))
   win.blit(lives_label, (650, 5))

def end_screen(win, elapsed_time, targets_pressed, clicks):
   win.fill(BG_COLOR)
   time_label = LABEL_FONT.render(f'Time: {format_time(elapsed_time)}',1,'white')
   
   speed = round(targets_pressed / elapsed_time, 1)
   speed_label = LABEL_FONT.render(f'Speed: {speed} t/s', 1, 'white')
   
   hits_label = LABEL_FONT.render(f'Hits: {targets_pressed}', 1, 'white')
   
   accuracy = round(targets_pressed / clicks * 100, 1)
   accuracy_label = LABEL_FONT.render(f'Accuracy: {accuracy}', 1, 'white')
   
   win.blit(time_label, (get_middle(time_label), 100))
   win.blit(speed_label, (get_middle(speed_label), 200))
   win.blit(hits_label, (get_middle(hits_label), 300))
   win.blit(accuracy_label, (get_middle(accuracy_label), 400))
   
   pygame.display.update()
   
   run = True
   while run:
      for event in pygame.event.get():
         if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            quit()

         
   
def get_middle(surface):
   return WIDTH / 2 - surface.get_width()/2

   
def main():
   run = True
   targets = [] #We are crerating a custom event at a random position
   clock = pygame.time.Clock()
   
   targets_pressed = 0 #Parameters to make the game functional and competitive :D.
   clicks = 0
   misses = 0
   start_time = time.time()
   
   pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT) #Trigger the 'event' every '350 ms'
   
   while run:
      clock.tick(60) #We want to run this while loop at 60 fps
      click = False
      mouse_pos = pygame.mouse.get_pos() #It give us the x, y coordinates of the mouse in pygame
      elapsed_time = time.time() - start_time #Gives us the nr of seconds that have elapsed
      
      
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            run = False
            break
         
         if event.type == TARGET_EVENT:
            x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
            y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
            target = Target(x, y) #Initializing a new instance of a target class
            targets.append(target) #This will push this new target obj into the 'target = []' list so we can use it and loop through it.
            
         if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
            clicks += 1
      
      for target in targets: #We need to make sure that we update all of our targets.
         target.update() #We want to update it first before removing because it starts out on a 0 size
         
         if target.size <= 0:      #If the target reaches(shrinks) to 0 pixels we will remove the target from the list 
            targets.remove(target) #that was stored in to not slow our program down with to much operations and data.
            misses += 1
            
         if click and target.collide(*mouse_pos): # "*mouse" -> Breaks down the tuple into its individiual component(splat operator)
            targets.remove(target)
            targets_pressed += 1
      
      if misses >= LIVES:
         end_screen(WIN, elapsed_time, targets_pressed, clicks)
            
      draw(WIN, targets)
      draw_top_bar(WIN, elapsed_time, targets_pressed, misses)
      pygame.display.update()
         
   pygame.quit()
   
if __name__ == "__main__":
   main()