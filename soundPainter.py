import pygame
import sys
import numpy as np
import pyaudio
import random
import colorsys

# PyAudio 초기화
p = pyaudio.PyAudio()

# Pygame 초기화
pygame.init()

# 화면 크기 및 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sound Drawing")

# 색상 및 굵기 초기값
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

def draw_line(start, end, color):
    pygame.draw.line(screen, color, start, end, thickness)

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

    # 랜덤한 HSV 색상 생성 (H: 0.0 - 1.0, S: 0.2 - 0.8, V: 1.0)
    h = random.random()
    s = random.uniform(0.1, 0.3)
    v = 0.7

    # HSV를 RGB로 변환
    rgb_color = tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

    # 소리의 주파수에 따라 원을 그림
    frequency = int(np.abs(np.mean(np.fft.fft(array_data))))
    pygame.draw.circle(screen, rgb_color, (width // 2, height // 2), frequency // 10, thickness)

    pygame.display.flip()

# 종료
pygame.quit()
stream.stop_stream()
stream.close()
p.terminate()
sys.exit()