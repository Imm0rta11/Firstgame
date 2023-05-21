# import
import time
import pygame
from score import score_record

# init window
clock = pygame.time.Clock()
pygame.init()
win = pygame.display.set_mode((618, 359))
pygame.display.set_caption("First game :)")
# Variable
x = 0
y = 250
width = 0
height = 0
speed = 10
jump_count = 8
score = 0
is_jump = False

left = [
    pygame.image.load('run left/run1.png'),
    pygame.image.load('run left/run2.png'),
    pygame.image.load('run left/run3.png'),
    pygame.image.load('run left/run4.png'),
    pygame.image.load('run left/run5.png'),
    pygame.image.load('run left/run6.png')
]
right = [
    pygame.image.load(' run right/run1.png'),
    pygame.image.load(' run right/run2.png'),
    pygame.image.load(' run right/run3.png'),
    pygame.image.load(' run right/run4.png'),
    pygame.image.load(' run right/run5.png'),
    pygame.image.load(' run right/run6.png')
]
jump = [
    pygame.image.load('jump/jump1.png'),
    pygame.image.load('jump/jump2.png'),
    pygame.image.load('jump/jump3.png'),
    pygame.image.load('jump/jump4.png')
]
idle = [
    pygame.image.load('idle/idle1.png'),
    pygame.image.load('idle/idle2.png'),
    pygame.image.load('idle/idle3.png'),
    pygame.image.load('idle/idle4.png')
]
ghost = pygame.image.load('ghost.png')
bg = pygame.image.load('bg.png')
player_anim_count = 0
idle_anim_count = 0
jump_anim = 0

color_text1 = (0, 0, 0)
color_text2 = (0, 0, 0)
color_text3 = (0, 0, 0)

ghost_difficulty = 0

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, ghost_difficulty)
ghost_list_in_game = []

fonts = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 15)
lose_text = fonts.render('You lose!', False, (0, 0, 0))
retry_text = fonts.render('Press ENTER for retry', False, (0, 0, 0))

main_menu = fonts.render('MY FIRST GAME', False, (0, 0, 0))
main_text = fonts.render('Press ENTER for start', False, (0, 0, 0))
main_text1 = fonts.render('Press ESC to exit', False, (0, 0, 0))

menu_select_title = fonts.render('Select difficulty', False, (0, 0, 0))
menu_select_text_1 = fonts.render('1.Easy', False, color_text1)
menu_select_text_2 = fonts.render('2.Normal', False, color_text2)
menu_select_text_3 = fonts.render('3.Hard', False, color_text3)
menu_select_text_4 = fonts.render('Press 4 for start!', False, (0, 0, 0))

pause_text = fonts.render('Pause', False, (0, 0, 0))
pause_text1 = fonts.render('Press C for unpause', False, (0, 0, 0))

gameplay = False
menu = True
menu_select = False
pause = False
run = True
gameover = False

keys = pygame.key.get_pressed()

game_song = pygame.mixer.Sound('music/game_music.ogg')
menu_song = pygame.mixer.Sound('music/menu_music.ogg')

game_over_sound = pygame.mixer.Sound('music/game_over.ogg')
game_start_sound = pygame.mixer.Sound('music/game_start_sound.ogg')
menu_select_sound = pygame.mixer.Sound('music/menu_select.ogg')
pause_sound = pygame.mixer.Sound('music/pause_sound.ogg')

game_over_sound_played = False

# play menu song
menu_song.play(loops=-1)
# while for game
while run:
    # init game menu
    if menu:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
        if keys[pygame.K_RETURN]:
            game_start_sound.play()
            game_start_sound.set_volume(0.5)
            menu = False
            menu_select = True
        win.fill((0, 0, 255))
        win.blit(main_text1, (0, 0))
        win.blit(main_menu, (150, 120))
        win.blit(main_text, (150, 200))
        score_record_win = fonts.render('Your record:' + str(score_record), False, (0, 0, 0))
        win.blit(score_record_win, (150, 160))
    clock.tick(20)
    # Select difficulty
    if menu_select and not menu and not gameplay:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
        if keys[pygame.K_1]:
            menu_select_sound.play()
            menu_select_sound.set_volume(0.5)
            ghost_difficulty = 1000
            ghost_timer = pygame.USEREVENT + 1
            pygame.time.set_timer(ghost_timer, ghost_difficulty)
        if keys[pygame.K_2]:
            menu_select_sound.play()
            menu_select_sound.set_volume(0.5)
            ghost_difficulty = 750
            color_text2 = (255, 255, 255)
            ghost_timer = pygame.USEREVENT + 1
            pygame.time.set_timer(ghost_timer, ghost_difficulty)
        if keys[pygame.K_3]:
            menu_select_sound.play()
            menu_select_sound.set_volume(0.5)
            ghost_difficulty = 600
            color_text3 = (255, 255, 255)
            ghost_timer = pygame.USEREVENT + 1
            pygame.time.set_timer(ghost_timer, ghost_difficulty)
        if keys[pygame.K_4]:
            game_start_sound.play()
            game_start_sound.set_volume(0.5)
            time.sleep(0.5)
            gameplay = True
            menu_select = False
            menu_song.stop()
            game_song.play(loops=-1)
            ghost_list_in_game.clear()
            score = 0
        win.fill((0, 0, 255))
        win.blit(menu_select_title, (170, 100))
        win.blit(menu_select_text_1, (170, 150))
        win.blit(menu_select_text_2, (170, 180))
        win.blit(menu_select_text_3, (170, 210))
        win.blit(menu_select_text_4, (170, 280))
    # game
    if gameplay and not pause:
        ghost_timer = pygame.USEREVENT + 1
        keys = pygame.key.get_pressed()
        win.blit(bg, (0, 0))
        player_hitbox = left[0].get_rect(topleft=(x, y))
        if keys[pygame.K_p]:
            gameplay = False
            pause = True
            while_for = 1
            ghost_timer = None
            win.blit(pause_text, (250, 150))
            game_song.stop()
            pause_sound.play()
        # ghosts
        if ghost_list_in_game:
            for el in ghost_list_in_game:
                win.blit(ghost, el)
                el.x -= 10
                if el.x < -9:
                    ghost_list_in_game.remove(el)
                # hitbox entity
                if player_hitbox.colliderect(el) and not menu and not pause:
                    gameplay = False
                    gameover = True
                    pause = False
                    if not game_over_sound_played and not menu:
                        game_song.stop()
                        game_over_sound.play()
                        game_over_sound_played = True
        # tracking keys
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
        # animation left and move
        if keys[pygame.K_LEFT] and x > 0:
            win.blit(left[player_anim_count // 4], (x, y))
            if player_anim_count > 8:
                player_anim_count = 0
            player_anim_count += 1
            x -= speed
        # animation right and move
        elif keys[pygame.K_RIGHT] and x < 580:
            win.blit(right[player_anim_count // 4], (x, y))
            if player_anim_count > 8:
                player_anim_count = 0
            player_anim_count += 1
            x += speed
        # idle animations
        else:
            win.blit(idle[idle_anim_count], (x, y))
        # Jump
        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    y -= (jump_count ** 2) / 2
                else:
                    y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8
        score_blit = fonts.render('Score: ' + str(score), False, (255, 255, 255))
        win.blit(score_blit, (0, 0))
    # game over screen
    if pause and not gameover and not gameplay:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]:
            gameplay = True
            pause = False
            ghost_timer = pygame.USEREVENT + 1
            game_song.play(loops=-1)
    if gameover and not gameplay and not pause and not menu_select and not menu:
        ghost_timer = pygame.USEREVENT + 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            win.blit(exit_main, (120, 125))
            pygame.quit()
        if keys[pygame.K_RETURN]:
            score = 0
            game_over_sound_played = False
            game_song.play(loops=-1)
            gameplay = True
            x = 0
            ghost_list_in_game.clear()
        # write record to file score.py
        if score > score_record:
            score_record = score
            write_record = open('score.py', 'w')
            write_record.write(f'score_record = {score}')

        win.fill((255, 0, 0))
        win.blit(lose_text, (120, 100))
        win.blit(retry_text, (120, 250))
        score_record_win = fonts.render('Your record:' + str(score_record), False, (0, 0, 0))
        win.blit(score_record_win, (120, 150))
        score_now_win = fonts.render('Your score:' + str(score), False, (0, 0, 0))
        win.blit(score_now_win, (120, 200))
    pygame.display.update()
    # add ghost in list
    for event in pygame.event.get():
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(620, 250)))
            score += 1

pygame.quit()
