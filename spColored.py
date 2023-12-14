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

# 초기 색상 값
main_color = pygame.Color(255, 0, 0)  # 초기 메인 색상은 붉은색
sub_color_step = 100  # 서브 색상 간격

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

def draw_circle(center, radius, color, fill=False):
    # 테두리 굵기 랜덤 설정
    thickness = random.choice([2, 4, 8])  # 원하는 굵기 값으로 수정 가능

    
    fill_probability = 80  # 원하는 확률 값으로 수정 가능
    fill = random.randint(1, 100) <= fill_probability

    pygame.draw.circle(screen, color, center, radius, thickness)  # 테두리만 그림
    if fill:
        pygame.draw.circle(screen, color, center, radius)  # 중앙을 비우지 않고 색 채움

# 메인 루프
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # 초당 60 프레임으로 제한

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:  # 'ESC' 키를 떼면 종료
                running = False
            elif event.key == pygame.K_c:  # 'c' 키를 떼면 화면을 초기화
                screen.fill((0, 0, 0))

    # 오디오 데이터 읽기
    data = stream.read(CHUNK)
    array_data = np.frombuffer(data, dtype=np.int16)

    # 메인 색상을 목소리의 높낮이에 따라 변화시킴
    main_color.hsva = (int(np.abs(np.mean(array_data)) % 255), 75, 75, 100)  # 색상은 그대로 두고 채도와 명도만 변경

    # 랜덤한 위치에 원을 그림 (소리 크기에 따라 일정 크기 이상일 때만 그리도록 변경)
    frequency = int(np.abs(np.mean(np.fft.fft(array_data))))
    if frequency > 300:  # 예시값, 조절이 필요할 수 있음
        center = (random.randint(0, width), random.randint(0, height))
        draw_circle(center, frequency // 10, main_color)

    pygame.display.flip()

# 종료
pygame.quit()
stream.stop_stream()
stream.close()
p.terminate()
sys.exit()
