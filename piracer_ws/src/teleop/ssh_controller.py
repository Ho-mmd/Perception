import time

import pygame
from piracer.vehicles import PiRacerStandard


pygame.init()

pygame.display.set_mode((300, 200))
pygame.display.set_caption("Controller (w, a, s, d)")

piracer = PiRacerStandard()

piracer.set_steering_percent(0.0)
piracer.set_throttle_percent(0.0)
time.sleep(1)

steering_data = None
throttle_data = None
pre_steering_data = None
pre_throttle_data = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and keys[pygame.K_d]:
        steering_data = 0
    elif keys[pygame.K_a]:
        steering_data = -1
    elif keys[pygame.K_d]:
        steering_data = 1
    else:
        steering_data = 0

    if keys[pygame.K_w] and keys[pygame.K_s]:
        throttle_data = 0
    elif keys[pygame.K_w]:
        throttle_data = 1
    elif keys[pygame.K_s]:
        throttle_data = -1
    else:
        throttle_data = 0

    if pre_steering_data is None or pre_steering_data != steering_data:
        pre_steering_data = steering_data
        piracer.set_steering_percent(steering_data * -1.0)

    if pre_throttle_data is None or pre_throttle_data != throttle_data:
        pre_throttle_data = throttle_data
        piracer.set_throttle_percent(throttle_data * 0.5)

    time.sleep(0.1)

pygame.quit()
