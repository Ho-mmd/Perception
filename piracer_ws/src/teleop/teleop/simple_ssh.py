import time 

import pygame
from piracer.vehicles import PiRacerStandard


pygame.init()

pygame.display.set_mode((300, 200))
pygame.display.set_caption("Controller (w, a, s, d)")

piracer = PiRacerStandard()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and keys[pygame.K_d]:
        piracer.set_steering_percent(0.0)
    elif keys[pygame.K_a]:
        piracer.set_steering_percent(1.0)
    elif keys[pygame.K_d]:
        piracer.set_steering_percent(-1.0)
    else:
        piracer.set_steering_percent(0.0)

    if keys[pygame.K_w] and keys[pygame.K_s]:
        piracer.set_throttle_percent(0.0)
    elif keys[pygame.K_w]:
        piracer.set_throttle_percent(5.0)
    elif keys[pygame.K_s]:
        piracer.set_throttle_percent(-5.0)
    else:
        piracer.set_throttle_percent(0.0)

    time.sleep(0.1)

pygame.quit()
