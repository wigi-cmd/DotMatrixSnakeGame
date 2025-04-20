from machine import Pin, SPI, ADC
import time
import random

#dot matrix tanımlar
spi = SPI(0, baudrate=10000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))
cs = Pin(16, Pin.OUT)

#joystick tanımları
x_axis = ADC(Pin(26))  
y_axis = ADC(Pin(27))  
button = Pin(22, Pin.IN, Pin.PULL_UP)

#global variables
snake = [(2, 3), (2, 4)]
score = 0
direction = (1, 0)
apple = (random.randint(0, 7), random.randint(0, 7))
speed = 0.20
eaten_apples = 0

def send_data(row, value):
    cs.value(0)
    spi.write(bytearray([row + 1, value]))
    cs.value(1)
    
def clear_matrix():
    for i in range(8):
        send_data(i, 0b00000000)
        
def start():
    start_pattern = [
        0b01111110,
        0b10111101,
        0b11011011,
        0b11100111,
        0b11100111,
        0b11011011,
        0b10111101,
        0b01111110,
        ]
    for i, val in enumerate(start_pattern):
        send_data(i, val)
        
    print("PRESS THE BUTTON TO START!!!")
    while button.value() == 1:
        pass #time.sleep(0.1) gereksizmiş?
            
def draw_objects():
    pattern = [0b00000000] * 8
    for x, y in snake:
        pattern[y] |= (1 << x)
    pattern[apple[1]] |= (1 << apple[0])
    for row in range(8):
        send_data(row, pattern[row])
        
def update_snake():
    global snake, apple, score, speed, eaten_apples
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    
    #çarpma kontrolü
    if new_head in snake or not (0 <= new_head[0] < 8 and 0 <= new_head[1] < 8):
        game_over()
        return
    
    snake.insert(0, new_head)
    
    #elma yedi mi?
    if new_head == apple:
        score += 1
        eaten_apples += 1
        print(f"\rScore: {score}     ", end="")  
        
        #hız artışı
        if eaten_apples % 8 == 0 and speed < 0.3:
            speed += 0.030
            print(f"\nNew speed: {speed}")
            
        apple = (random.randint(0, 7), random.randint(0, 7))
    else:
        snake.pop()
        
def change_direction():
    global direction
    x_value = x_axis.read_u16()
    y_value = y_axis.read_u16()
    
    if x_value < 15000 and direction != (1, 0):
        direction = (-1, 0)
    elif x_value > 50000 and direction != (-1, 0):
        direction = (1, 0)
        
    if y_value > 50000 and direction != (0, 1):
        direction = (0, -1)
    elif y_value < 15000 and direction != (0, -1):
        direction = (0, 1)
        
def game_over():
    x_pattern = [
        0b10000001,
        0b01000010,
        0b00100100,
        0b00011000,
        0b00011000,
        0b00100100,
        0b01000010,
        0b10000001,
        ]
    for _ in range(3):
        for i, val in enumerate(x_pattern):
            send_data(i, val)
        time.sleep(0.3)
        clear_matrix()
        time.sleep(0.3)
    
    for i, val in enumerate(x_pattern):
        send_data(i, val)
        
    while button.value() == 1:
        pass
    restart()
    
def restart():
    restart_pattern = [
        0b00011000,
        0b00100100,
        0b01000010,
        0b10000000,
        0b10001111,
        0b01000011,
        0b00100101,
        0b00011001,
        ]
    while button.value() == 1:
        pass
    
    for i, val in enumerate(restart_pattern):
        send_data(i, val)
        
    time.sleep(0.5)
        
    print("PRESS THE BUTTON TO REPLAY!")
    while button.value == 1:
        time.sleep(0.2)
        
    reset_game()
    
def reset_game():
    global snake, direction, apple, speed, eaten_apples
    snake = [(2, 3), (2, 4)]
    score = 0
    direction = (1, 0)
    apple = (random.randint(0, 7), random.randint(0, 7))
    speed = 0.20
    eaten_apples = 0
    game_loop()
    
def game_loop():
    initialize_matrix()
    start()
    while True:
        change_direction()
        update_snake()
        draw_objects()
        time.sleep(speed)
        
def initialize_matrix():
    clear_matrix()
    print("THE GAME STARTED!!")
    

game_loop()                        