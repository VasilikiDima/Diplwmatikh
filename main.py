from game import *

#από εδώ χειρίζομαι την game, τα gamestates πληκτρολόγιο κλπ

#αυτά είναι για να βγει το .exe
#pyinstaller --onefile main.py
#pyinstaller --onefile --noconsole main.py

myGame = Game()

#Για playtest location στο location.txt πρέπει να είναι 399,352,961,129

location = open('location.txt', 'r')
location_x = location.readline()
location_y = location.readline()
camera_x = int(location.readline())
camera_y = int(location.readline())
character = Player((int(location_x), int(location_y)), camera_x, camera_y)
character.health = int(location.readline())
location.close()

game_state = 'stating_screen'

options_open_panel_animation = False
options_close_panel_animation = False
open = True
close = False
page = 0
i=0
dialog = ''
dialog_index = -1
index_instructions = 0
previus_game_state = 'map'
move_intro = True

while True:
    #print(character.player_pos)
    #print(character.camera_x)
    #print(character.camera_y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_state == 'code' and event.type == pygame.KEYUP:
            flag = False
            for box in myGame.active_text_boxes:
                if flag:
                    box.change_active()
                    myGame.active_text_boxes_index += 1
                    flag = False
                    break
                flag = box.handle_event(event)
            if flag:
                myGame.active_text_boxes[0].change_active()
                myGame.active_text_boxes_index = 0
                flag = False
        if game_state == 'play_instuctions' and event.type == pygame.KEYUP and myGame.code_instruction_textbox and event.key != pygame.K_SPACE:
            flag = False
            for box in myGame.code_instruction_textbox:
                print(box.text)
                if flag:
                    box.change_active()
                    myGame.code_instruction_textbox_index += 1
                    if myGame.code_instruction_textbox_index >= len(myGame.code_instruction_textbox):
                        myGame.code_instruction_textbox_index = 0
                    flag = False
                    break
                flag = box.handle_event(event)
                print(box.text)
            if flag:
                myGame.code_instruction_textbox[0].change_active()
                myGame.code_instruction_textbox_index = 0
                flag = False


    keys = pygame.key.get_pressed()
    keys_released = pygame.key.get_just_released()
    if keys[pygame.K_s] and (game_state == 'map' or game_state == 'options'):
        print('save')
        myGame.save(character)
        pygame.time.wait(1000)
    if keys[pygame.K_m] and game_state == 'map':
        game_state = 'options'
        #character.renderMap(myGame.screen)
    if game_state == 'intro':

        if (keys_released[pygame.K_RETURN] or keys_released[pygame.K_SPACE]):
            completed_intro = myGame.intro()
            if not completed_intro:
                game_state = 'map'
        if move_intro:
            completed_intro = myGame.intro()
            move_intro = False

    if game_state == 'stating_screen':
        myGame.draw_starting_screen()
        if keys_released[pygame.K_UP]:
            myGame.sound_click.play()
            myGame.start_menu.move_up()
        if keys_released[pygame.K_DOWN]:
            myGame.sound_click.play()
            myGame.start_menu.move_down()
        if keys_released[pygame.K_RETURN]:
            myGame.sound_click.play()
            if myGame.start_menu.active_button == 0:
                if myGame.my_mission.get_mission_id() == 1:
                    game_state = "intro"
                else:
                    game_state = 'map'
            elif myGame.start_menu.active_button == 1:
                game_state = 'start_menu_directions'
            elif myGame.start_menu.active_button == 2:
                game_state = 'start_menu_info'
            elif myGame.start_menu.active_button == 3:
                pygame.quit()
                sys.exit()
    elif game_state == 'start_menu_directions':
        myGame.start_menu_directions()
        if keys_released[pygame.K_RETURN]:
            game_state = 'stating_screen'
    elif game_state == 'start_menu_info':
        myGame.start_menu_info()
        if keys_released[pygame.K_RETURN]:
            game_state = 'stating_screen'

    if game_state == 'map':
        previus_game_state = 'map'
        if character.health < 0:
            myGame = Game()
            try:
                del open
            except Exception as e:
                print(f"An error occurred: {e}")
            location_file = open('location.txt', 'r')
            location_x = location_file.readline()
            location_y = location_file.readline()
            camera_x = int(location_file.readline())
            camera_y = int(location_file.readline())
            character = Player((int(location_x), int(location_y)), camera_x, camera_y)
            character.health = int(location_file.readline())

        else:
            last_move = character.update(keys,myGame.map_width,myGame.map_height,myGame.object_layer,keys_released,myGame.object_layer_collidable,myGame.get_monsters())
            if keys[pygame.K_1] and myGame.my_mission.get_mission_id() >8:
                character.attack(1)

            myGame.item_pickup(keys,character)
            if keys_released[pygame.K_u]:
                myGame.use_item(character)
            myGame.update(character.camera_x, character.camera_y,character.player_pos[0], character.player_pos[1],character,last_move[0])
            if  not myGame.my_mission.get_current_mission()["dialog_start"]:
                game_state = 'draw_dialog_start'
                dialog = myGame.my_mission.get_current_mission()["dialogs"].get("start")
                dialog_index = 0
            if  not myGame.my_mission.get_current_mission()["dialog_end"] and myGame.my_mission.get_current_mission()["code_task"].get("correct_answers") == []:
                try:
                    if myGame.my_mission.get_current_mission()["destination"][0]-100<=character.camera_x<myGame.my_mission.get_current_mission()["destination"][0]+100:
                        if myGame.my_mission.get_current_mission()["destination"][1] - 100 <= character.camera_y <myGame.my_mission.get_current_mission()["destination"][1] + 100:
                            print('destination')
                            print(myGame.stash[0].get_name())
                            print(myGame.my_mission.get_mission_id())
                            if myGame.my_mission.get_mission_id() not in [6,8,10]:
                                game_state = 'draw_dialog_end'
                                dialog = myGame.my_mission.get_current_mission()["dialogs"].get("start")
                                dialog_index = 0
                            elif myGame.my_mission.get_mission_id() == 8:
                                if myGame.stash[0].get_name() == 'κρυσταλλοσ' and myGame.stash[1].get_name() == 'κρυσταλλοσ' and myGame.stash[2].get_name() == 'κρυσταλλοσ':
                                    game_state = 'draw_dialog_end'
                                    dialog = myGame.my_mission.get_current_mission()["dialogs"].get("start")
                                    myGame.stash[0].set_item('empty')
                                    myGame.stash[1].set_item('empty')
                                    myGame.stash[2].set_item('empty')
                                    dialog_index = 0
                            elif myGame.my_mission.get_mission_id() == 10:
                                if myGame.all_diamonds():
                                    game_state = 'draw_dialog_end'
                                    dialog = myGame.my_mission.get_current_mission()["dialogs"].get("end")
                                    for s in myGame.stash:
                                        s.set_item('empty')
                                    dialog_index = 0
                            elif myGame.stash[0].get_name() == 'κρυσταλλοσ':
                                game_state = 'draw_dialog_end'
                                dialog = myGame.my_mission.get_current_mission()["dialogs"].get("start")
                                myGame.stash[0].set_item('empty')
                                dialog_index = 0
                except Exception as e: print(e)

    if keys_released[pygame.K_d] and game_state != 'stating_screen':
        myGame.select_item_right()
    if keys_released[pygame.K_a] and game_state != 'stating_screen':
        myGame.select_item_left()

    if game_state == 'draw_dialog_end':
        myGame.draw_dialog_end(dialog_index)
        if keys_released[pygame.K_SPACE] or keys_released[pygame.K_RETURN]:
            dialog_index += 1
            if dialog_index >= len(myGame.my_mission.get_current_mission()["dialogs"].get("end")):
                if previus_game_state != 'map':
                    game_state = 'options'
                    page = 3
                else:
                    game_state = 'map'
                myGame.my_mission.update_dialog_end()
                dialog_index = 0
                myGame.my_mission.next_mission()

    if game_state == 'draw_dialog_start':
        previus_game_state = 'draw_dialog_start'
        myGame.draw_dialog_start(dialog_index)
        if keys_released[pygame.K_SPACE] or keys_released[pygame.K_RETURN]:
            dialog_index += 1
            if dialog_index >= len(myGame.my_mission.get_current_mission()["dialogs"].get("start")):
                game_state = 'map'
                myGame.my_mission.update_dialog_start()
                dialog_index = 0
    if game_state == 'options':
        previus_game_state = 'options'
        if open:
            options_open_panel_animation = myGame.open_options_panel(character,last_move[0])
            page = 0
        if not options_open_panel_animation:
            open = False
            myGame.draw_options(character, page,last_move[0])
            if keys_released[pygame.K_DOWN]:
                myGame.sound_click.play()
                page += 1
                if page >5:
                    page = 0
            elif keys_released[pygame.K_UP]:
                myGame.sound_click.play()
                page -= 1
                if page < 0:
                    page = 5
            if keys_released[pygame.K_m]:
                myGame.sound_click.play()
                #myGame.reset_animation_counter()
                options_close_panel_animation = myGame.close_options_panel(character,last_move[0])
                close = True
            if (keys_released[pygame.K_SPACE] or keys_released[pygame.K_RETURN]) and page == 4 and myGame.my_mission.get_current_mission()["code_task"].get("correct_answers") !=[]:
                myGame.sound_click.play()
                myGame.active_text_boxes = []
                game_state = 'play_instuctions'
            if close:
                options_close_panel_animation = myGame.close_options_panel(character,last_move[0])
            if not options_close_panel_animation and close:
                options_open_panel_animation = False
                options_close_panel_animation = False
                open = True
                close = False
                page = 0
                myGame.reset_animation_counter()
                game_state = 'map'
    if game_state == 'code':
        previus_game_state = 'code'
        if keys_released[pygame.K_ESCAPE]:
            game_state = 'options'

        if keys_released[pygame.K_TAB] or keys_released[pygame.K_RIGHT]:
            myGame.active_text_boxes[myGame.active_text_boxes_index].change_active()
            myGame.active_text_boxes_index += 1
            if myGame.active_text_boxes_index >= len(myGame.active_text_boxes):
                myGame.active_text_boxes_index = 0
            myGame.active_text_boxes[myGame.active_text_boxes_index].change_active()
        elif (keys_released[pygame.K_BACKSPACE] and myGame.active_text_boxes[myGame.active_text_boxes_index].text=='') or keys_released[pygame.K_LEFT]:
            myGame.active_text_boxes[myGame.active_text_boxes_index].change_active()
            myGame.active_text_boxes_index -= 1
            if myGame.active_text_boxes_index < 0:
                myGame.active_text_boxes_index = len(myGame.active_text_boxes)-1
            myGame.active_text_boxes[myGame.active_text_boxes_index].change_active()
        myGame.draw_code()
        if keys_released[pygame.K_RETURN] or keys_released[pygame.K_RETURN]:
            if myGame.check_code():
                dialog_index = 0
                myGame.sound_completed.play()
                game_state = 'code_mission_completed'
        if keys_released[pygame.K_F1]:
            game_state = 'play_instuctions_completed'
            index_instructions = 0
        if keys_released[pygame.K_F2]:
            game_state = 'play_code_general'
    if game_state == 'play_code_general':
        myGame.code_general()
        if keys_released[pygame.K_SPACE] or keys_released[pygame.K_RETURN] or keys_released[pygame.K_ESCAPE]:
            game_state = 'code'
    if game_state == 'code_mission_completed':
        previus_game_state = 'code_mission_completed'
        myGame.draw_code_mission_completed()
        if keys_released[pygame.K_SPACE] or keys_released[pygame.K_RETURN]:
            game_state = 'draw_dialog_end'
    if game_state == 'play_instuctions' or game_state=='play_instuctions_completed':
        #myGame.draw_code()
        previus_game_state = 'play_instuctions'
        box = myGame.draw_code_instructions(index_instructions,game_state=='play_instuctions_completed')
        if keys_released[pygame.K_RETURN]:
            if not box:
                index_instructions += 1
                if index_instructions >= len(myGame.my_mission.get_current_mission()["code_instuctions_1"]):
                    index_instructions = 0
                    game_state = 'code'
            else:
                if myGame.check_code_instruction_answer(index_instructions):
                    index_instructions += 2
                    myGame.code_instruction_textbox.clear()
                    if index_instructions >= len(myGame.my_mission.get_current_mission()["code_instuctions_1"]):
                        index_instructions = 0
                        game_state = 'code'
        elif keys_released[pygame.K_SPACE]:
            index_instructions -= 1
            if index_instructions <= 0:
                index_instructions = 1
            if ' ' not in myGame.my_mission.get_current_mission()["code_instuctions_1"][index_instructions]:
                print(myGame.my_mission.get_current_mission()["code_instuctions_1"][index_instructions])
                index_instructions -= 2
            myGame.code_instruction_textbox.clear()

        elif keys_released[pygame.K_TAB] or keys_released[pygame.K_RIGHT]:
            myGame.code_instruction_textbox[myGame.code_instruction_textbox_index].change_active()
            myGame.code_instruction_textbox_index += 1
            if myGame.code_instruction_textbox_index >= len(myGame.code_instruction_textbox):
                myGame.code_instruction_textbox_index = 0
            myGame.code_instruction_textbox[myGame.code_instruction_textbox_index].change_active()
        elif (keys_released[pygame.K_BACKSPACE] and myGame.code_instruction_textbox[myGame.code_instruction_textbox_index].text=='') or keys_released[pygame.K_LEFT]:
            myGame.code_instruction_textbox[myGame.code_instruction_textbox_index].change_active()
            myGame.code_instruction_textbox_index -= 1
            if myGame.code_instruction_textbox_index < 0:
                myGame.code_instruction_textbox_index = len(myGame.code_instruction_textbox)-1
            myGame.code_instruction_textbox[myGame.code_instruction_textbox_index].change_active()
    pygame.display.update()
    myGame.clock.tick(60)