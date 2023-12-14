import pygame
import sys
import numpy as np
import pyaudio
import random

# PyAudio 초기화
p = pyaudio.PyAudio()

# Pygame 초기화
pygame.init()

# 화면 크기 및 설정 (전체 디스플레이 크기로 설정)
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Sound Drawing")

# 색상 및 굵기 초기값
color = (255, 255, 255)
thickness = 5

# 그리기 상태 변수
drawing = False

# 오디오 설정
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# 오디오 스트림 열기
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

def draw_circle(center, radius, color, thickness):
    pygame.draw.circle(screen, color, center, radius, thickness)

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:  # 'c' 키를 누르면 화면을 초기화
                screen.fill((0, 0, 0))

    # 오디오 데이터 읽기
    data = stream.read(CHUNK)
    array_data = np.frombuffer(data, dtype=np.int16)

    # 소리의 크기에 따라 굵기와 색상 조절
    thickness = int(np.abs(np.mean(array_data)) / 100)
    color = (int(np.abs(np.mean(array_data)) % 255),
             int(np.abs(np.mean(array_data)) % 255),
             int(np.abs(np.mean(array_data)) % 255))

    # 랜덤한 위치에 원을 그림
    center = (random.randint(0, width), random.randint(0, height))
    frequency = int(np.abs(np.mean(np.fft.fft(array_data))))
    draw_circle(center, frequency // 10, color, thickness)

    pygame.display.flip()

# 종료
pygame.quit()
stream.stop_stream()
stream.close()
p.terminate()
sys.exit()
