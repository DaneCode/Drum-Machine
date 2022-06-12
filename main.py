import pygame
from pygame import mixer
pygame.init()

WIDTH = 1400
HEIGHT = 800

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)
light_gray = (170, 170, 170)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Beat Maker")
label_font = pygame.font.Font("freesansbold.ttf", 32)
medium_font = pygame.font.Font("freesansbold.ttf", 24)
fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 7
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
active_list = [1 for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 0
beat_changed = True
save_menu = False
load_menu = False
saved_beats = []
file = open("saved_beats.txt", "r")
for line in file:
    saved_beats.append(line)

beat_name = ""
typing = False
index = 100

#load in sounds
hi_hat = mixer.Sound("sounds\hi hat.WAV")
hi_hat1 = mixer.Sound("sounds\kit2\hi hat.wav")
clap = mixer.Sound("sounds\clap.wav")
clap1 = mixer.Sound("sounds\kit2\clap.wav")
crash = mixer.Sound("sounds\crash.wav")
crash1 = mixer.Sound("sounds\kit2\crash.wav")
kick = mixer.Sound("sounds\kick.WAV")
kick1 = mixer.Sound("sounds\kit2\kick.WAV")
snare = mixer.Sound("sounds\snare.WAV")
snare1 = mixer.Sound("sounds\kit2\snare.WAV")
tom = mixer.Sound("sounds\\tom.WAV")
tom1 = mixer.Sound("sounds\kit2\\tom.WAV")
snap = mixer.Sound("sounds\Snap.wav")
temp = []
pygame.mixer.set_num_channels(instruments * 3)

def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()
            if i == 6:
                snap.play()

def draw_grid(clicks, active_beat, actives):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT-200], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT-200, WIDTH, 200], 5)
    boxes = []
    colors = [gray, white, gray]
    # Text for Instruments in GUI
    hi_hat_text = label_font.render("Hi Hat", True, colors[actives[0]])
    screen.blit(hi_hat_text, (30, 30))
    snare_text = label_font.render("Snare", True, colors[actives[1]])
    screen.blit(snare_text, (30, 115))
    kick_text = label_font.render("Kick", True, colors[actives[2]])
    screen.blit(kick_text, (30, 200))
    crash_text = label_font.render("Crash", True, colors[actives[3]])
    screen.blit(crash_text, (30, 285))
    clap_text = label_font.render("Clap", True, colors[actives[4]])
    screen.blit(clap_text, (30, 370))
    floor_text = label_font.render("Floor Tom", True, colors[actives[5]])
    screen.blit(floor_text, (30, 455))
    snap_text = label_font.render("Snap", True, colors[actives[6]])
    screen.blit(snap_text, (30, 540))


    #Grid of lines between Instrument text
    for i in range(instruments):
        pygame.draw.line(screen, gray, (0, (i * 85) + 85), (200, (i * 85) + 85), 2)
    # Beat Grid Code
    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                if actives[j] == 1:
                    color = green
                else:
                    color = dark_gray
            rect = pygame.draw.rect(screen, color,
                                    [i * ((WIDTH - 200) // beats) + 205, (j * 85) + 5, (WIDTH - 200) // beats - 10,
                                     ((HEIGHT - 200) // instruments)-10], 0, 3)
            pygame.draw.rect(screen, gold,
                                    [i * ((WIDTH - 200) // beats) + 200, (j * 85), (WIDTH - 200) // beats,
                                     ((HEIGHT - 200) // instruments)], 5, 5)
            pygame.draw.rect(screen, black,
                                    [i * ((WIDTH - 200) // beats) + 200, (j * 85), (WIDTH - 200) // beats,
                                     ((HEIGHT - 200) // instruments)], 2, 5)
            boxes.append((rect, (i, j)))
        active = pygame.draw.rect(screen, blue, [active_beat * ((WIDTH - 200)//beats) + 200, 0, ((WIDTH - 200)//beats), instruments * 85], 5, 3)

    return boxes

def draw_save_menu(beat_name, typing):
    pygame.draw.rect(screen, black, [0,0, WIDTH, HEIGHT])
    menu_text = label_font.render("Save Menu: Enter a name for current beat", True, white)
    saving_btn = pygame.draw.rect(screen, gray, [WIDTH // 2 - 200, HEIGHT * 0.75, 400, 100], 0, 5)
    saving_txt = label_font.render("Save Beat", True, white)
    screen.blit(saving_txt, (WIDTH // 2 - 70, HEIGHT * 0.75 + 30))
    screen.blit(menu_text, (400, 40))
    exit_btn = pygame.draw.rect(screen, gray, [WIDTH-200, HEIGHT-100, 180,90], 0, 5)
    exit_text = label_font.render("Close", True, white)
    screen.blit(exit_text, (WIDTH-160, HEIGHT-70))
    if typing:
        entry_rect = pygame.draw.rect(screen, dark_gray, [400, 200, 600, 200], 0, 5)
    entry_rect = pygame.draw.rect(screen, gray, [400,200,600,200], 5, 5)
    entry_text = label_font.render(f'{beat_name}', True, white)
    screen.blit(entry_text, (430,250))
    return exit_btn, saving_btn, entry_rect
def draw_load_menu(index):
    loaded_clicked = []
    loaded_beats = []
    loaded_bpm = []
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render("Load Menu: Select a beat", True, white)
    loading_btn = pygame.draw.rect(screen, gray, [WIDTH // 2 - 200, HEIGHT * 0.87, 400, 100], 0, 5)
    loading_txt = label_font.render("Load Beat", True, white)
    screen.blit(loading_txt, (WIDTH // 2 - 70, HEIGHT * 0.87 + 30))
    delete_btn = pygame.draw.rect(screen, gray, [WIDTH // 2 - 493, HEIGHT * 0.87, 200, 100], 0, 5)
    delete_txt = label_font.render("Delete Beat", True, white)
    screen.blit(delete_txt, ((WIDTH // 2) - 485, HEIGHT * 0.87 + 30))
    screen.blit(menu_text, (400, 40))
    exit_btn = pygame.draw.rect(screen, gray, [WIDTH-200, HEIGHT-100, 180,90], 0, 5)
    exit_text = label_font.render("Close", True, white)
    screen.blit(exit_text, (WIDTH-160, HEIGHT-70))
    if 0 <= index < len(saved_beats):
        pygame.draw.rect(screen, light_gray, [190, 100 + index * 50, 1000, 50])
    for beat in range(len(saved_beats)):
        if beat < 10:
            beat_clicked = []
            row_text = medium_font.render(f'{beat + 1}', True, white)
            screen.blit(row_text, (200, 100 + beat * 50))
            name_index_start = saved_beats[beat].index('name: ')  + 6
            name_index_end = saved_beats[beat].index(', beats:')
            name_text = medium_font.render(saved_beats[beat][name_index_start:name_index_end], True, white)
            screen.blit(name_text, (240, 100 + beat * 50))
        if 0 <= index < len(saved_beats) and beat == index:
            beat_index_end = saved_beats[beat].index(", bpm: ")
            loaded_beats = int(saved_beats[beat][name_index_end + 8: beat_index_end])
            bpm_index_end = saved_beats[beat].index(", selected: ")
            loaded_bpm = int(saved_beats[beat][beat_index_end + 6: bpm_index_end])
            loaded_clicks_string = saved_beats[beat][bpm_index_end + 14: -3]
            loaded_clicks_rows = list(loaded_clicks_string.split("], ["))
            for row in range(len(loaded_clicks_rows)):
                loaded_clicks_row = (loaded_clicks_rows[row].split(", "))
                for item in range(len(loaded_clicks_row)):
                    if loaded_clicks_row[item] == "1" or loaded_clicks_row[item] == "-1":
                        loaded_clicks_row[item] = int(loaded_clicks_row[item])
                beat_clicked.append(loaded_clicks_row)
                loaded_clicked = beat_clicked
    loaded_info = [loaded_beats, loaded_bpm, loaded_clicked]
    entry_rect= pygame.draw.rect(screen, gray, [190, 90, 1000, 600], 5, 5)
    return exit_btn, loading_btn, delete_btn, entry_rect, loaded_info

run = True
#Gaming Loop Code
while run:
    timer.tick(fps)
    screen.fill(black)

    boxes = draw_grid(clicked, active_beat, active_list)
    #Start Pause Menu Buttons
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render("Play/Pause", True, white)
    screen.blit(play_text, (70, HEIGHT - 130))
    if playing:
        play_text2 = medium_font.render("Playing", True, dark_gray)
    else:
        play_text2 = medium_font.render("Paused", True, dark_gray)
    screen.blit(play_text2, (70, HEIGHT - 100))


    if beat_changed:
        play_notes()
        beat_changed = False

    #Beats Per Minuite Controls
    bpm_rect = pygame.draw.rect(screen, gray, [300, HEIGHT - 150, 215, 100], 5, 5)
    bpm_text = medium_font.render("Beats Per Minute", True, white)
    screen.blit(bpm_text, (308, HEIGHT - 130))
    bpm_text2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text2, (370, HEIGHT - 100))
    bpm_add_rect = pygame.draw.rect(screen, gray, [520, HEIGHT - 150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, gray, [520, HEIGHT - 100, 48,48], 0, 5)
    add_text = medium_font.render("+5", True, white)
    sub_text = medium_font.render("-5", True, white)
    screen.blit(add_text, (530, HEIGHT - 140))
    screen.blit(sub_text, (530, HEIGHT - 90))

    # Number of Beats Controls
    beats_rect = pygame.draw.rect(screen, gray, [580, HEIGHT - 150, 215, 100], 5, 5)
    beats_text = medium_font.render("Beats in Loop", True, white)
    screen.blit(beats_text, (608, HEIGHT - 130))
    beats_text2 = label_font.render(f'{beats}', True, white)
    screen.blit(beats_text2, (670, HEIGHT - 100))
    beats_add_rect = pygame.draw.rect(screen, gray, [800, HEIGHT - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [800, HEIGHT - 100, 48,48], 0, 5)
    add_text2 = medium_font.render("+1", True, white)
    sub_text2 = medium_font.render("-1", True, white)
    screen.blit(add_text2, (810, HEIGHT - 140))
    screen.blit(sub_text2, (810, HEIGHT - 90))

    # instrument rectangles
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 85), (200, 85))
        instrument_rects.append(rect)

    #Save and Load Buttons
    save_button = pygame.draw.rect(screen, gray, [900, HEIGHT - 150, 200, 48], 0, 5)
    save_text = label_font.render("Save Beat", True, white)
    screen.blit(save_text, (920, HEIGHT - 140))
    load_button = pygame.draw.rect(screen, gray, [900, HEIGHT - 100, 200, 48], 0, 5)
    load_text = label_font.render("Load Beat", True, white)
    screen.blit(load_text, (920, HEIGHT - 90))

    #Clear Board Function
    clear_button = pygame.draw.rect(screen, gray, [1150, HEIGHT - 150, 200, 100], 0, 5)
    clear_text = label_font.render("Clear Beat", True, white)
    screen.blit(clear_text, (1160, HEIGHT - 120))

    #Swap Sound Buttons
    snap_button = pygame.draw.rect(screen, gray, [1200, HEIGHT - 45, 150, 30], 0, 5)
    snap_text = medium_font.render("Swap Snap", True, white)
    screen.blit(snap_text, (1200, HEIGHT - 40))
    tom_button = pygame.draw.rect(screen, gray, [1015, HEIGHT - 45, 150, 30], 0, 5)
    tom_text = medium_font.render("Swap Tom", True, white)
    screen.blit(tom_text, (1017, HEIGHT - 40))
    clap_button = pygame.draw.rect(screen, gray, [822, HEIGHT - 45, 150, 30], 0, 5)
    clap_text = medium_font.render("Swap Clap", True, white)
    screen.blit(clap_text, (824, HEIGHT - 40))
    crash_button = pygame.draw.rect(screen, gray, [629, HEIGHT - 45, 150, 30], 0, 5)
    crash_text = medium_font.render("Swap Crash", True, white)
    screen.blit(crash_text, (631, HEIGHT - 40))
    kick_button = pygame.draw.rect(screen, gray, [436, HEIGHT - 45, 150, 30], 0, 5)
    kick_text = medium_font.render("Swap kick", True, white)
    screen.blit(kick_text, (438, HEIGHT - 40))
    snare_button = pygame.draw.rect(screen, gray, [243, HEIGHT - 45, 150, 30], 0, 5)
    snare_text = medium_font.render("Swap Snare", True, white)
    screen.blit(snare_text, (245, HEIGHT - 40))
    hi_hat_button = pygame.draw.rect(screen, gray, [50, HEIGHT - 45, 150, 30], 0, 5)
    hi_hat_text = medium_font.render("Swap Hi Hat", True, white)
    screen.blit(hi_hat_text, (50, HEIGHT - 40))

    if save_menu:
        exit_button, saving_button, entry_rect = draw_save_menu(beat_name, typing)
    if load_menu:
        exit_button, loading_button, delete_button, loaded_rect, loaded_information = draw_load_menu(index)

    #Mouse Controls for GUI
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True
            # BPM Clicking Event
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 5
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    for i in range(len(clicked)):
                        clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            elif clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
            #Swap Sound Click
            elif hi_hat_button.collidepoint(event.pos):
                hi_hat, hi_hat1 = hi_hat1, hi_hat
            elif snare_button.collidepoint(event.pos):
                snare, snare1 = snare1, snare
            elif kick_button.collidepoint(event.pos):
                kick, kick1 = kick1, kick
            elif crash_button.collidepoint(event.pos):
                crash, crash1 = crash1, crash
            elif clap_button.collidepoint(event.pos):
                clap, clap1 = clap1, clap
            elif tom_button.collidepoint(event.pos):
                tom, tom1 = tom1, tom
            elif save_button.collidepoint(event.pos):
                save_menu = True
            elif load_button.collidepoint(event.pos):
                load_menu = True
            #Clear Click
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1
        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True
                beat_name = ""
                typing = False
            elif loaded_rect.collidepoint(event.pos):
                index = (event.pos[1] - 100) // 50
            elif delete_button.collidepoint(event.pos):
                if 0 <= index <len(saved_beats):
                    saved_beats.pop(index)
            elif load_button.collidepoint(event.pos):
                if 0 <= index < len(saved_beats):
                    beats = loaded_information[0]
                    bpm = loaded_information[1]
                    clicked = loaded_information[2]
                    index = 100
                    load_menu = False

            elif saving_button.collidepoint(event.pos):
                file = open("saved_beats.txt", "w")
                saved_beats.append(f'\nname: {beat_name}, beats: {beats}, bpm: {bpm}, selected: {clicked}')
                for i in range(len(saved_beats)):
                    file.write(str(saved_beats[i]))
                file.close()
                save_menu = False
                typing = False
                beat_name = ''
        #Typing Controls
        if event.type == pygame.TEXTINPUT and typing:
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0 and typing:
                beat_name = beat_name[:-1]
    #Setting Beat based off FPS*60 and Controlling the Beat
    beat_length = 3600 // bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats -1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()

pygame.quit()