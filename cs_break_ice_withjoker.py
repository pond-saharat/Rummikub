def break_the_ice(verify_of_break_ice, handcards, boardcards):
    if verify_of_break_ice is True:
        return verify_of_break_ice
    else:
        # 判断当前条件下是否能够破冰
        if boardcards is []:
            def order_principle(card):
                color_order = {'red': 0, 'yellow': 1, 'green': 2, 'blue': 3, 'pink': 4}
                return (color_order[card[0]], card[1])

            ordered_handcards = sorted(handcards, key=order_principle)
            # step-2 将列表分成不同颜色的小列表
            red_hand_list = []
            yellow_hand_list = []
            green_hand_list = []
            blue_hand_list = []
            pink_hand_list = []
            Joker_list = []  # 鬼牌
            for i in ordered_handcards:
                if i[0] == 'red':
                    red_hand_list.append(i)
                elif i[0] == 'yellow':
                    yellow_hand_list.append(i)
                elif i[0] == 'green':
                    green_hand_list.append(i)
                elif i[0] == 'blue':
                    blue_hand_list.append(i)
                elif i[0] == 'pink':
                    pink_hand_list.append(i)
                else:
                    Joker_list.append(i)  # 鬼牌

            # step-3 生成筛选列表
            # step-3-1 筛出重复元素，并生成第二次筛选的列表
            def second_hand_list(list):
                first_hand_check_list = []
                first_hand_check_list_value = []
                second_hand_list = []

                for i in list:
                    if i not in first_hand_check_list and i[1] not in first_hand_check_list_value and i is not ['Joker', 0]:
                        first_hand_check_list.append(i)
                        first_hand_check_list_value.append(i[1])
                    else:
                        second_hand_list.append(i)

                return second_hand_list

            second_hand_red_list = second_hand_list(red_hand_list)  # 第一轮多出来的红牌
            second_hand_yellow_list = second_hand_list(yellow_hand_list)  # 第一轮多出来的黄牌
            second_hand_green_list = second_hand_list(green_hand_list)  # 第一轮多出来的绿牌
            second_hand_blue_list = second_hand_list(blue_hand_list)  # 第一轮多出来的蓝牌
            second_hand_pink_list = second_hand_list(pink_hand_list)  # 第一轮多出来的粉牌
            second_hand_joker_list = Joker_list  # 第一轮多出来的鬼牌

            # step-3-2 生成第一次筛选的列表
            def first_hand_check_list(list):  # 可改进
                first_hand_check_list = []
                first_hand_check_list_value = []
                second_hand_list = []

                for i in list:
                    if i not in first_hand_check_list and i[1] not in first_hand_check_list_value:
                        first_hand_check_list.append(i)
                        first_hand_check_list_value.append(i[1])
                    else:
                        second_hand_list.append(i)

                return first_hand_check_list

            first_hand_red_check_list = first_hand_check_list(red_hand_list)
            first_hand_yellow_check_list = first_hand_check_list(yellow_hand_list)
            first_hand_green_check_list = first_hand_check_list(green_hand_list)
            first_hand_blue_check_list = first_hand_check_list(blue_hand_list)
            first_hand_pink_check_list = first_hand_check_list(pink_hand_list)

            # step-3-3 分出奇数牌和偶数牌
            def check_odd_list(list):
                odd_list = []
                for i in list:
                    if i[1] % 2 != 0:
                        odd_list.append(i)
                return odd_list

            def check_even_list(list):
                even_list = []
                for i in list:
                    if i[1] % 2 == 0:
                        even_list.append(i)
                return even_list

            # 奇数牌组
            first_hand_red_odd_check_list = check_odd_list(first_hand_red_check_list)
            # print(first_hand_red_odd_check_list)
            first_hand_yellow_odd_check_list = check_odd_list(first_hand_yellow_check_list)
            first_hand_green_odd_check_list = check_odd_list(first_hand_green_check_list)
            first_hand_blue_odd_check_list = check_odd_list(first_hand_blue_check_list)
            first_hand_pink_odd_check_list = check_odd_list(first_hand_pink_check_list)
            # 偶数牌组
            first_hand_red_even_check_list = check_even_list(first_hand_red_check_list)
            # print(first_red_even_check_list)
            first_hand_yellow_even_check_list = check_even_list(first_hand_yellow_check_list)
            first_hand_green_even_check_list = check_even_list(first_hand_green_check_list)
            first_hand_blue_even_check_list = check_even_list(first_hand_blue_check_list)
            first_hand_pink_even_check_list = check_even_list(first_hand_pink_check_list)

            # step-4 第一轮筛选
            def first_check(list):
                first_checked_list = []
                current_list = []
                for i in list:
                    if not current_list or i[1] == current_list[-1][1] + 2:
                        current_list.append(i)
                    else:
                        first_checked_list.append(current_list)
                        current_list = [i]
                    # print(current_list)
                if current_list:
                    first_checked_list.append(current_list)
                first_checked_list = [r for r in first_checked_list if len(r) > 2]
                return first_checked_list

            # step-4-1 整理好第一轮筛选出来的元素 一个三维的列表 [[['red', 1, 0], ['red', 3, 0], ['red', 5, 1], ['red', 7, 1]]]
            first_hand_red_final_odd_list = first_check(first_hand_red_odd_check_list)
            first_hand_yellow_final_odd_list = first_check(first_hand_yellow_odd_check_list)
            first_hand_green_final_odd_list = first_check(first_hand_green_odd_check_list)
            first_hand_blue_final_odd_list = first_check(first_hand_blue_odd_check_list)
            first_hand_pink_final_odd_list = first_check(first_hand_pink_odd_check_list)

            first_hand_red_final_even_list = first_check(first_hand_red_even_check_list)
            first_hand_yellow_final_even_list = first_check(first_hand_yellow_even_check_list)
            first_hand_green_final_even_list = first_check(first_hand_green_even_check_list)
            first_hand_blue_final_even_list = first_check(first_hand_blue_even_check_list)
            first_hand_pink_final_even_list = first_check(first_hand_pink_even_check_list)

            # step-4-2 将第一轮筛选剩下的元素找出来，未来与第二轮筛选剩下的元素组成新的列表
            first_hand_total_unused_list = []

            def find_unused_element(total_list, used_odd_list, used_even_list):
                first_total_used_list = []
                for a in used_odd_list:
                    for b in a:
                        first_total_used_list.append(b)
                for a in used_even_list:
                    for b in a:
                        first_total_used_list.append(b)
                first_total_unused_list_color = [i for i in total_list if i not in first_total_used_list]

                return first_total_unused_list_color

            red_hand_first_unused_list = find_unused_element(first_hand_red_check_list, first_hand_red_final_even_list,
                                                             first_hand_red_final_odd_list)
            # print(red_first_unused_list)
            yellow_hand_first_unused_list = find_unused_element(first_hand_yellow_check_list,
                                                                first_hand_yellow_final_even_list,
                                                                first_hand_yellow_final_odd_list)
            # print(yellow_first_unused_list)
            green_hand_first_unused_list = find_unused_element(first_hand_green_check_list,
                                                               first_hand_green_final_even_list,
                                                               first_hand_green_final_odd_list)
            blue_hand_first_unused_list = find_unused_element(first_hand_blue_check_list,
                                                              first_hand_blue_final_even_list,
                                                              first_hand_blue_final_odd_list)
            pink_hand_first_unused_list = find_unused_element(first_hand_pink_check_list,
                                                              first_hand_pink_final_even_list,
                                                              first_hand_pink_final_odd_list)
            first_hand_total_unused_list = first_hand_total_unused_list + red_hand_first_unused_list + yellow_hand_first_unused_list + green_hand_first_unused_list + blue_hand_first_unused_list + pink_hand_first_unused_list
            # print(first_hand_total_unused_list)  # first_hand_total_unused_list中不含Joker

            # step-4-3 第一轮检查后合格的组
            red_hand_first_used_list = first_hand_red_final_even_list + first_hand_red_final_odd_list
            yellow_hand_first_used_list = first_hand_yellow_final_even_list + first_hand_yellow_final_odd_list
            green_hand_first_used_list = first_hand_green_final_even_list + first_hand_green_final_odd_list
            blue_hand_first_used_list = first_hand_blue_final_even_list + first_hand_blue_final_odd_list
            pink_hand_first_used_list = first_hand_pink_final_even_list + first_hand_pink_final_odd_list
            first_hand_total_used_list = red_hand_first_used_list + yellow_hand_first_used_list + green_hand_first_used_list + blue_hand_first_used_list + pink_hand_first_used_list

            # print(first_total_used_list)

            # step-5 第二轮筛查
            # step-5-1 找到第二步筛选所需要的列表（如second_hand_red_list = second_hand_red_check_list)
            second_hand_red_check_list = second_hand_red_list
            second_hand_yellow_check_list = second_hand_yellow_list
            second_hand_green_check_list = second_hand_green_list
            second_hand_blue_check_list = second_hand_blue_list
            second_hand_pink_check_list = second_hand_pink_list

            # step-5-2 分出奇数牌和偶数牌
            # 奇数牌
            second_hand_red_odd_check_list = check_odd_list(second_hand_red_check_list)
            second_hand_yellow_odd_check_list = check_odd_list(second_hand_yellow_check_list)
            second_hand_green_odd_check_list = check_odd_list(second_hand_green_check_list)
            second_hand_blue_odd_check_list = check_odd_list(second_hand_blue_check_list)
            second_hand_pink_odd_check_list = check_odd_list(second_hand_pink_check_list)
            # 偶数牌
            second_hand_red_even_check_list = check_even_list(second_hand_red_check_list)
            second_hand_yellow_even_check_list = check_even_list(second_hand_yellow_check_list)
            second_hand_green_even_check_list = check_even_list(second_hand_green_check_list)
            second_hand_blue_even_check_list = check_even_list(second_hand_blue_check_list)
            second_hand_pink_even_check_list = check_even_list(second_hand_pink_check_list)

            # step-5-3 第二轮检查
            def second_check(list):
                second_checked_list = []
                current_list = []
                for i in list:
                    if not current_list or i[1] == current_list[-1][1] + 2:
                        current_list.append(i)
                    else:
                        second_checked_list.append(current_list)
                        current_list = [i]
                    # print(current_list)
                if current_list:
                    second_checked_list.append(current_list)
                second_checked_list = [r for r in second_checked_list if len(r) > 2]
                return second_checked_list

            second_hand_red_final_odd_list = second_check(second_hand_red_odd_check_list)
            # print(second_red_final_odd_list)
            second_hand_yellow_final_odd_list = second_check(second_hand_yellow_odd_check_list)
            second_hand_green_final_odd_list = second_check(second_hand_green_odd_check_list)
            second_hand_blue_final_odd_list = second_check(second_hand_blue_odd_check_list)
            second_hand_pink_final_odd_list = second_check(second_hand_pink_odd_check_list)

            second_hand_red_final_even_list = second_check(second_hand_red_even_check_list)
            second_hand_yellow_final_even_list = second_check(second_hand_yellow_even_check_list)
            second_hand_green_final_even_list = second_check(second_hand_green_even_check_list)
            second_hand_blue_final_even_list = second_check(second_hand_blue_even_check_list)
            second_hand_pink_final_even_list = second_check(second_hand_pink_even_check_list)

            # step-5-4 将第二轮筛剩下的元素找出来
            # second_hand_total_unused_list = []

            red_hand_second_unused_list = find_unused_element(second_hand_red_check_list,
                                                              second_hand_red_final_even_list,
                                                              second_hand_red_final_odd_list)
            yellow_hand_second_unused_list = find_unused_element(second_hand_yellow_check_list,
                                                                 second_hand_yellow_final_even_list,
                                                                 second_hand_yellow_final_odd_list)
            green_hand_second_unused_list = find_unused_element(second_hand_green_check_list,
                                                                second_hand_green_final_even_list,
                                                                second_hand_green_final_odd_list)
            blue_hand_second_unused_list = find_unused_element(second_hand_blue_check_list,
                                                               second_hand_blue_final_even_list,
                                                               second_hand_blue_final_odd_list)
            pink_hand_second_unused_list = find_unused_element(second_hand_pink_check_list,
                                                               second_hand_pink_final_even_list,
                                                               second_hand_pink_final_odd_list)
            second_hand_total_unused_list = first_hand_total_unused_list + red_hand_second_unused_list + yellow_hand_second_unused_list + green_hand_second_unused_list + blue_hand_second_unused_list + pink_hand_second_unused_list
            # print(second_hand_total_unused_list)  second_hand_total_unused_list不包含Joker

            # step-5-5 第二轮检查后合格的组
            red_hand_second_used_list = second_hand_red_final_even_list + second_hand_red_final_odd_list
            yellow_hand_second_used_list = second_hand_yellow_final_even_list + second_hand_yellow_final_odd_list
            green_hand_second_used_list = second_hand_green_final_even_list + second_hand_green_final_odd_list
            blue_hand_second_used_list = second_hand_blue_final_even_list + second_hand_blue_final_odd_list
            pink_hand_second_used_list = second_hand_pink_final_even_list + second_hand_pink_final_odd_list
            second_hand_total_used_list = red_hand_second_used_list + yellow_hand_second_used_list + green_hand_second_used_list + blue_hand_second_used_list + pink_hand_second_used_list
            # print(second_total_used_list)
            # 截至第二轮筛选后，所有配对成功的组
            total_hand_used_list = first_hand_total_used_list + second_hand_total_used_list
            # print(total_hand_used_list)

            # step-6 第三步筛选（筛选剩余手牌中的可以配对的组）

            # step-6-1  剩余手牌例子：[['red', 2], ['red', 4], ['red', 8], ['red', 13], ['yellow', 13], ['green', 13], ['blue', 12], ['blue', 13], ['red', 1], ['red', 2]]
            # step-6-1 将剩余的手牌中的所有元素去重
            list1 = []
            for i in second_hand_total_unused_list:
                if i not in list1:
                    list1.append(i)

            # step-6-2 找出list中花色不同，但值相同的牌组
            # 找出牌组
            result_dict = {}
            for i in list1:
                key = i[1]
                if key in result_dict:
                    result_dict[key].append(i)
                else:
                    result_dict[key] = [i]

            handcards_group = [value for value in result_dict.values() if len(value) > 2]  # 这是一个三维列表
            while True:
                if ['Joker', 0] not in Joker_list:
                    break
                elif ['Joker', 0] in Joker_list:
                    a = 0
                    for i in Joker_list:
                        if i == ['Joker', 0]:
                            a += 1
                    if a == 1:
                        for i in handcards_group:
                            if len(i) <= 4:
                                i.append(['Joker', 0])
                                Joker_list.remove(['Joker', 0])
                                break
                    if a == 2:
                        for i in handcards_group:
                            if len(i) <= 4:
                                i.append(['Joker', 0])
                                Joker_list.remove(['Joker', 0])


            # 将手牌去除组成group的元素，生成最终的剩余手牌列表final_handcards
            # 将handcards_group拆成二维列表,因为剩余手牌是二维列表，这样才能比较
            handcards_group_elements = []
            for i in handcards_group:
                handcards_group_elements.append(i)
            # 进行去除
            final_handcards = []
            seen_set = set()
            Joker_unused_list = []
            for i in Joker_list:
                Joker_unused_list.append(i)
            second_hand_total_unused_list = second_hand_total_unused_list + Joker_unused_list
            for i in second_hand_total_unused_list:
                if i in handcards_group_elements and i not in seen_set:
                    seen_set.add(i)
                else:
                    final_handcards.append(i)
            second_hand_total_used_list = second_hand_total_used_list + handcards_group

            # step-7 判断是否破冰
            break_ice_value = 0
            for i in second_hand_total_used_list:
                for j in i:
                    break_ice_value += j[1]

            if break_ice_value >= 30:
                return True, second_hand_total_used_list, final_handcards

            else:
                return False  # handcards.append([NewCard])


        # 当桌面上有牌的情况
        else:
            def handcards_play_rule(handcards):
                def order_principle(card):
                    color_order = {'red': 0, 'yellow': 1, 'green': 2, 'blue': 3, 'pink': 4}
                    return (color_order[card[0]], card[1])

                ordered_handcards = sorted(handcards, key=order_principle)
                # step-2 将列表分成不同颜色的小列表
                red_hand_list = []
                yellow_hand_list = []
                green_hand_list = []
                blue_hand_list = []
                pink_hand_list = []
                Joker_list = []  # 鬼牌
                for i in ordered_handcards:
                    if i[0] == 'red':
                        red_hand_list.append(i)
                    elif i[0] == 'yellow':
                        yellow_hand_list.append(i)
                    elif i[0] == 'green':
                        green_hand_list.append(i)
                    elif i[0] == 'blue':
                        blue_hand_list.append(i)
                    elif i[0] == 'pink':
                        pink_hand_list.append(i)
                    else:
                        Joker_list.append(i)  # 鬼牌

                # step-3 生成筛选列表
                # step-3-1 筛出重复元素，并生成第二次筛选的列表
                def second_hand_list(list):
                    first_hand_check_list = []
                    first_hand_check_list_value = []
                    second_hand_list = []

                    for i in list:
                        if i not in first_hand_check_list and i[1] not in first_hand_check_list_value and i is not ['Joker', 0]:
                            first_hand_check_list.append(i)
                            first_hand_check_list_value.append(i[1])
                        else:
                            second_hand_list.append(i)

                    return second_hand_list

                second_hand_red_list = second_hand_list(red_hand_list)  # 第一轮多出来的红牌
                second_hand_yellow_list = second_hand_list(yellow_hand_list)  # 第一轮多出来的黄牌
                second_hand_green_list = second_hand_list(green_hand_list)  # 第一轮多出来的绿牌
                second_hand_blue_list = second_hand_list(blue_hand_list)  # 第一轮多出来的蓝牌
                second_hand_pink_list = second_hand_list(pink_hand_list)  # 第一轮多出来的粉牌
                second_hand_joker_list = Joker_list  # 第一轮多出来的鬼牌

                # step-3-2 生成第一次筛选的列表
                def first_hand_check_list(list):  # 可改进
                    first_hand_check_list = []
                    first_hand_check_list_value = []
                    second_hand_list = []

                    for i in list:
                        if i not in first_hand_check_list and i[1] not in first_hand_check_list_value:
                            first_hand_check_list.append(i)
                            first_hand_check_list_value.append(i[1])
                        else:
                            second_hand_list.append(i)

                    return first_hand_check_list

                first_hand_red_check_list = first_hand_check_list(red_hand_list)
                first_hand_yellow_check_list = first_hand_check_list(yellow_hand_list)
                first_hand_green_check_list = first_hand_check_list(green_hand_list)
                first_hand_blue_check_list = first_hand_check_list(blue_hand_list)
                first_hand_pink_check_list = first_hand_check_list(pink_hand_list)

                # step-3-3 分出奇数牌和偶数牌
                def check_odd_list(list):
                    odd_list = []
                    for i in list:
                        if i[1] % 2 != 0:
                            odd_list.append(i)
                    return odd_list

                def check_even_list(list):
                    even_list = []
                    for i in list:
                        if i[1] % 2 == 0:
                            even_list.append(i)
                    return even_list

                # 奇数牌组
                first_hand_red_odd_check_list = check_odd_list(first_hand_red_check_list)
                # print(first_hand_red_odd_check_list)
                first_hand_yellow_odd_check_list = check_odd_list(first_hand_yellow_check_list)
                first_hand_green_odd_check_list = check_odd_list(first_hand_green_check_list)
                first_hand_blue_odd_check_list = check_odd_list(first_hand_blue_check_list)
                first_hand_pink_odd_check_list = check_odd_list(first_hand_pink_check_list)
                # 偶数牌组
                first_hand_red_even_check_list = check_even_list(first_hand_red_check_list)
                # print(first_red_oven_check_list)
                first_hand_yellow_even_check_list = check_even_list(first_hand_yellow_check_list)
                first_hand_green_even_check_list = check_even_list(first_hand_green_check_list)
                first_hand_blue_even_check_list = check_even_list(first_hand_blue_check_list)
                first_hand_pink_even_check_list = check_even_list(first_hand_pink_check_list)

                # step-4 第一轮筛选
                def first_check(list):
                    first_checked_list = []
                    current_list = []
                    for i in list:
                        if not current_list or i[1] == current_list[-1][1] + 2:
                            current_list.append(i)
                        else:
                            first_checked_list.append(current_list)
                            current_list = [i]
                        # print(current_list)
                    if current_list:
                        first_checked_list.append(current_list)
                    first_checked_list = [r for r in first_checked_list if len(r) > 2]
                    return first_checked_list

                # step-4-1 整理好第一轮筛选出来的元素 一个三维的列表 [[['red', 1, 0], ['red', 3, 0], ['red', 5, 1], ['red', 7, 1]]]
                first_hand_red_final_odd_list = first_check(first_hand_red_odd_check_list)
                first_hand_yellow_final_odd_list = first_check(first_hand_yellow_odd_check_list)
                first_hand_green_final_odd_list = first_check(first_hand_green_odd_check_list)
                first_hand_blue_final_odd_list = first_check(first_hand_blue_odd_check_list)
                first_hand_pink_final_odd_list = first_check(first_hand_pink_odd_check_list)

                first_hand_red_final_even_list = first_check(first_hand_red_even_check_list)
                first_hand_yellow_final_even_list = first_check(first_hand_yellow_even_check_list)
                first_hand_green_final_even_list = first_check(first_hand_green_even_check_list)
                first_hand_blue_final_even_list = first_check(first_hand_blue_even_check_list)
                first_hand_pink_final_even_list = first_check(first_hand_pink_even_check_list)

                # step-4-2 将第一轮筛选剩下的元素找出来，未来与第二轮筛选剩下的元素组成新的列表
                first_hand_total_unused_list = []

                def find_unused_element(total_list, used_odd_list, used_even_list):
                    first_total_used_list = []
                    for a in used_odd_list:
                        for b in a:
                            first_total_used_list.append(b)
                    for a in used_even_list:
                        for b in a:
                            first_total_used_list.append(b)
                    first_total_unused_list_color = [i for i in total_list if i not in first_total_used_list]

                    return first_total_unused_list_color

                red_hand_first_unused_list = find_unused_element(first_hand_red_check_list,
                                                                 first_hand_red_final_even_list,
                                                                 first_hand_red_final_odd_list)
                # print(red_first_unused_list)
                yellow_hand_first_unused_list = find_unused_element(first_hand_yellow_check_list,
                                                                    first_hand_yellow_final_even_list,
                                                                    first_hand_yellow_final_odd_list)
                # print(yellow_first_unused_list)
                green_hand_first_unused_list = find_unused_element(first_hand_green_check_list,
                                                                   first_hand_green_final_even_list,
                                                                   first_hand_green_final_odd_list)
                blue_hand_first_unused_list = find_unused_element(first_hand_blue_check_list,
                                                                  first_hand_blue_final_even_list,
                                                                  first_hand_blue_final_odd_list)
                pink_hand_first_unused_list = find_unused_element(first_hand_pink_check_list,
                                                                  first_hand_pink_final_even_list,
                                                                  first_hand_pink_final_odd_list)
                first_hand_total_unused_list = first_hand_total_unused_list + red_hand_first_unused_list + yellow_hand_first_unused_list + green_hand_first_unused_list + blue_hand_first_unused_list + pink_hand_first_unused_list
                # print(first_hand_total_unused_list)  # first_hand_total_unused_list中不含Joker

                # step-4-3 第一轮检查后合格的组
                red_hand_first_used_list = first_hand_red_final_even_list + first_hand_red_final_odd_list
                yellow_hand_first_used_list = first_hand_yellow_final_even_list + first_hand_yellow_final_odd_list
                green_hand_first_used_list = first_hand_green_final_even_list + first_hand_green_final_odd_list
                blue_hand_first_used_list = first_hand_blue_final_even_list + first_hand_blue_final_odd_list
                pink_hand_first_used_list = first_hand_pink_final_even_list + first_hand_pink_final_odd_list
                first_hand_total_used_list = red_hand_first_used_list + yellow_hand_first_used_list + green_hand_first_used_list + blue_hand_first_used_list + pink_hand_first_used_list

                # print(first_total_used_list)

                # step-5 第二轮筛查
                # step-5-1 找到第二步筛选所需要的列表（如second_hand_red_list = second_hand_red_check_list)
                second_hand_red_check_list = second_hand_red_list
                second_hand_yellow_check_list = second_hand_yellow_list
                second_hand_green_check_list = second_hand_green_list
                second_hand_blue_check_list = second_hand_blue_list
                second_hand_pink_check_list = second_hand_pink_list

                # step-5-2 分出奇数牌和偶数牌
                # 奇数牌
                second_hand_red_odd_check_list = check_odd_list(second_hand_red_check_list)
                second_hand_yellow_odd_check_list = check_odd_list(second_hand_yellow_check_list)
                second_hand_green_odd_check_list = check_odd_list(second_hand_green_check_list)
                second_hand_blue_odd_check_list = check_odd_list(second_hand_blue_check_list)
                second_hand_pink_odd_check_list = check_odd_list(second_hand_pink_check_list)
                # 偶数牌
                second_hand_red_oven_check_list = check_even_list(second_hand_red_check_list)
                second_hand_yellow_oven_check_list = check_even_list(second_hand_yellow_check_list)
                second_hand_green_oven_check_list = check_even_list(second_hand_green_check_list)
                second_hand_blue_oven_check_list = check_even_list(second_hand_blue_check_list)
                second_hand_pink_oven_check_list = check_even_list(second_hand_pink_check_list)

                # step-5-3 第二轮检查
                def second_check(list):
                    second_checked_list = []
                    current_list = []
                    for i in list:
                        if not current_list or i[1] == current_list[-1][1] + 2:
                            current_list.append(i)
                        else:
                            second_checked_list.append(current_list)
                            current_list = [i]
                        # print(current_list)
                    if current_list:
                        second_checked_list.append(current_list)
                    second_checked_list = [r for r in second_checked_list if len(r) > 2]
                    return second_checked_list

                second_hand_red_final_odd_list = second_check(second_hand_red_odd_check_list)
                # print(second_red_final_odd_list)
                second_hand_yellow_final_odd_list = second_check(second_hand_yellow_odd_check_list)
                second_hand_green_final_odd_list = second_check(second_hand_green_odd_check_list)
                second_hand_blue_final_odd_list = second_check(second_hand_blue_odd_check_list)
                second_hand_pink_final_odd_list = second_check(second_hand_pink_odd_check_list)

                second_hand_red_final_even_list = second_check(second_hand_red_even_check_list)
                second_hand_yellow_final_even_list = second_check(second_hand_yellow_even_check_list)
                second_hand_green_final_even_list = second_check(second_hand_green_even_check_list)
                second_hand_blue_final_even_list = second_check(second_hand_blue_even_check_list)
                second_hand_pink_final_even_list = second_check(second_hand_pink_even_check_list)

                # step-5-4 将第二轮筛剩下的元素找出来
                # second_hand_total_unused_list = []

                red_hand_second_unused_list = find_unused_element(second_hand_red_check_list,
                                                                  second_hand_red_final_even_list,
                                                                  second_hand_red_final_odd_list)
                yellow_hand_second_unused_list = find_unused_element(second_hand_yellow_check_list,
                                                                     second_hand_yellow_final_even_list,
                                                                     second_hand_yellow_final_odd_list)
                green_hand_second_unused_list = find_unused_element(second_hand_green_check_list,
                                                                    second_hand_green_final_even_list,
                                                                    second_hand_green_final_odd_list)
                blue_hand_second_unused_list = find_unused_element(second_hand_blue_check_list,
                                                                   second_hand_blue_final_even_list,
                                                                   second_hand_blue_final_odd_list)
                pink_hand_second_unused_list = find_unused_element(second_hand_pink_check_list,
                                                                   second_hand_pink_final_even_list,
                                                                   second_hand_pink_final_odd_list)
                second_hand_total_unused_list = first_hand_total_unused_list + red_hand_second_unused_list + yellow_hand_second_unused_list + green_hand_second_unused_list + blue_hand_second_unused_list + pink_hand_second_unused_list
                # print(second_hand_total_unused_list)  second_hand_total_unused_list不包含Joker

                # step-5-5 第二轮检查后合格的组
                red_hand_second_used_list = second_hand_red_final_even_list + second_hand_red_final_odd_list
                yellow_hand_second_used_list = second_hand_yellow_final_even_list + second_hand_yellow_final_odd_list
                green_hand_second_used_list = second_hand_green_final_even_list + second_hand_green_final_odd_list
                blue_hand_second_used_list = second_hand_blue_final_even_list + second_hand_blue_final_odd_list
                pink_hand_second_used_list = second_hand_pink_final_even_list + second_hand_pink_final_odd_list
                second_hand_total_used_list = red_hand_second_used_list + yellow_hand_second_used_list + green_hand_second_used_list + blue_hand_second_used_list + pink_hand_second_used_list
                # print(second_total_used_list)
                # 截至第二轮筛选后，所有配对成功的组
                total_hand_used_list = first_hand_total_used_list + second_hand_total_used_list
                # print(total_hand_used_list)

                # step-6 第三步筛选（筛选剩余手牌中的可以配对的组）

                # step-6-1  剩余手牌例子：[['red', 2], ['red', 4], ['red', 8], ['red', 13], ['yellow', 13], ['green', 13], ['blue', 12], ['blue', 13], ['red', 1], ['red', 2]]
                # step-6-1 将剩余的手牌中的所有元素去重
                list1 = []
                for i in second_hand_total_unused_list:
                    if i not in list1:
                        list1.append(i)

                # step-6-2 找出list中花色不同，但值相同的牌组
                # 找出牌组
                result_dict = {}
                for i in list1:
                    key = i[1]
                    if key in result_dict:
                        result_dict[key].append(i)
                    else:
                        result_dict[key] = [i]

                handcards_group = [value for value in result_dict.values() if len(value) > 2]  # 这是一个三维列表
                while True:
                    if ['Joker', 0] not in Joker_list:
                        break
                    elif ['Joker', 0] in Joker_list:
                        a = 0
                        for i in Joker_list:
                            if i == ['Joker', 0]:
                                a += 1
                        if a == 1:
                            for i in handcards_group:
                                if len(i) <= 4:
                                    i.append(['Joker', 0])
                                    Joker_list.remove(['Joker', 0])
                                    break
                        if a == 2:
                            for i in handcards_group:
                                if len(i) <= 4:
                                    i.append(['Joker', 0])
                                    Joker_list.remove(['Joker', 0])

                # 将手牌去除组成group的元素，生成最终的剩余手牌列表final_handcards
                # 将handcards_group拆成二维列表,因为剩余手牌是二维列表，这样才能比较
                handcards_group_elements = []
                for i in handcards_group:
                    handcards_group_elements.append(i)
                # 进行去除
                final_handcards = []
                seen_set = set()
                Joker_unused_list = []
                for i in Joker_list:
                    Joker_unused_list.append(i)
                second_hand_total_unused_list = second_hand_total_unused_list + Joker_unused_list
                for i in second_hand_total_unused_list:
                    if i in handcards_group_elements and i not in seen_set:
                        seen_set.add(i)
                    else:
                        final_handcards.append(i)

                # 最终要打出的全部手牌
                second_hand_total_used_list = second_hand_total_used_list + handcards_group
                return second_hand_total_used_list, second_hand_total_unused_list

            def cs_regular_play(verify_of_break_ice, handcards, boardcards):
                if verify_of_break_ice is True:
                    # step01-找出手牌中可以自行组队的元素
                    handcards_used_list = handcards_play_rule(handcards)[0]  # 手牌单独组队后形成的新组  # 三维
                    handcards_used_elements_list = []
                    for i in handcards_used_list:
                        for j in i:
                            handcards_used_elements_list.append(j)
                    # 对其进行降维
                    handcards_unused_list = handcards_play_rule(handcards)[1]  # 手牌单独组队后剩余的手牌  # 二维
                    # step02-对board上的牌进行预处理，找出row和group的组，分别存入不同的列表中
                    boardcards_group_list = []  # 三维列表
                    boardcards_row_list = []  # 三维列表
                    # 处理boardcards中有鬼牌的情况
                    boardcards_Joker_list = []
                    for i in boardcards:
                        if ['Joker', 0] in i:
                            boardcards_Joker_list.append(i)  # 将含有Joker牌的桌牌组存入这个列表，后面不管，直接加进最终的结果
                            boardcards.remove(i)  # 要处理的桌面牌组中去除含有Joker的组

                    for i in boardcards:  # 找row
                        if i[0][0] == i[1][0]:
                            boardcards_row_list.append(i)
                    for i in boardcards:  # 找group
                        if i[0][1] == i[1][1]:
                            boardcards_group_list.append(i)
                    # step03 找出剩余手牌能否添加进boardcards的group中
                    color_list = ["red", "yellow", "green", "blue", "pink"]
                    for i in boardcards_group_list:
                        for j in handcards_unused_list:  # 一维列表，单张手牌
                            if j[1] == i[0][1] and j not in i:
                                i.append(j)  # 生成新的group
                                handcards_unused_list.remove(j)  # 去除手牌中用掉的元素
                                handcards_used_elements_list.append(j)  # 统计已经使用的手牌

                    # 如果手牌中有Joker，看Joker能否加入组中
                    while True:
                        if ['Joker', 0] not in handcards_unused_list:
                            break
                        elif ['Joker', 0] in handcards_unused_list:
                            a = 0
                            for i in handcards_unused_list:
                                if i == ['Joker', 0]:
                                    a += 1  # 统计手牌中Joker的数量
                            if a == 1:
                                for i in boardcards_group_list:
                                    if len(i) <= 4:
                                        i.append(['Joker', 0])
                                        handcards_unused_list.remove(['Joker', 0])
                                        handcards_used_elements_list.append(['Joker', 0])
                                        break
                                    if a == 2:
                                        for i in handcards_unused_list:
                                            if len(i) <= 4:
                                                i.append(['Joker', 0])
                                                handcards_unused_list.remove(['Joker', 0])
                                                handcards_used_elements_list.append(['Joker', 0])

                    # step04 找出剩余的手牌能否添加进boardcards的row中
                    # step04-01 先看每个row的前后能否加元素并添加
                    # step04-01-01 前面
                    for i in boardcards_row_list:
                        while True:
                            if i[0][1] - 2 >= 0:  # 判断第一张牌的值不为1或2
                                if [i[0][0], i[0][1] - 2] in handcards_unused_list:
                                    i.insert(0, [i[0][0], i[0][1] - 2])  # 将该张牌填入到第一位
                                    handcards_unused_list.remove([i[0][0], i[0][1] - 2])  # 去除手牌中用掉的元素
                                    handcards_used_elements_list.append([i[0][0], i[0][1] - 2])  # 统计已经使用的手牌
                                else:
                                    break

                        # step04-01-02 后面
                    for i in boardcards_row_list:
                        while True:
                            if i[-1][1] + 2 <= 15:
                                if [i[-1][0], i[-1][1] + 2] in handcards_unused_list:
                                    i.append([i[-1][0], i[-1][1] + 2])  # 将该张牌填入到最后一位
                                    handcards_unused_list.remove([i[0][0], i[0][1] + 2])  # 去除手牌中用掉的元素
                                    handcards_used_elements_list.append([i[0][0], i[0][1] + 2])  # 统计已经使用的手牌
                                else:
                                    break

                    # step04-01-02 检查手牌中是否有牌可以插入row的中间
                    #  when len(list) = 5, 在第3位i[2]中插入元素，并将该row列表分成两个
                    for i in boardcards_row_list:
                        if len(i) == 5:
                            if i[2] in handcards_unused_list:
                                i.insert(2, i[2])
                                handcards_unused_list.remove(i[2])
                                handcards_used_elements_list.append(i[2])
                                # 把一个row分成两个row
                                i1 = i[:3]
                                i2 = i[3:]
                                boardcards_row_list.remove(i)
                                boardcards_row_list.append(i1)
                                boardcards_row_list.append(i2)
                        if len(i) == 6:
                            if i[2] in handcards_unused_list:
                                i.insert(2, i[2])
                                handcards_unused_list.remove(i[2])
                                handcards_used_elements_list.append(i[2])
                                # 把一个row分成两个row
                                i1 = i[:3]
                                i2 = i[3:]
                                boardcards_row_list.remove(i)
                                boardcards_row_list.append(i1)
                                boardcards_row_list.append([i2])
                            elif i[3] in handcards_unused_list:
                                i.insert(3, i[3])
                                handcards_unused_list.remove(i[3])
                                handcards_used_elements_list.append(i[3])
                                i1 = i[:4]
                                i2 = i[4:]
                                boardcards_row_list.remove(i)
                                boardcards_row_list.append(i1)
                                boardcards_row_list.append(i2)

                        if len(i) == 7:
                            if i[2] in handcards_unused_list:
                                i.insert(2, i[2])
                                handcards_unused_list.remove(i[2])
                                handcards_used_elements_list.append(i[2])
                                # 把一个row分成两个row
                                i1 = i[:3]
                                i2 = i[3:]
                                boardcards_row_list.remove(i)
                                boardcards_row_list.append(i1)
                                boardcards_row_list.append(i2)
                            elif i[3] in handcards_unused_list:
                                i.insert(3, i[3])
                                handcards_unused_list.remove(i[3])
                                handcards_used_elements_list.append(i[3])
                                i1 = i[:4]
                                i2 = i[4:]
                                boardcards_row_list.remove(i)
                                boardcards_row_list.append(i1)
                                boardcards_row_list.append(i2)
                            elif i[4] in handcards_unused_list:
                                i.insert(4, i[4])
                                handcards_unused_list.remove(i[4])
                                handcards_used_elements_list.append(i[4])
                                i1 = i[:5]
                                i2 = i[5:]
                                boardcards_row_list.remove(i)
                                boardcards_row_list.append(i1)
                                boardcards_row_list.append(i2)

                        if len(i) == 8:
                            if i[2] in handcards_unused_list:
                                i.insert(2, i[2])
                                handcards_unused_list.remove(i[2])
                                handcards_used_elements_list.append(i[2])
                                # 把一个row分成两个row
                                i1 = i[:3]
                                i2 = i[3:]
                                boardcards_row_list.remove(i)
                                boardcards_row_list.append(i1)
                                boardcards_row_list.append(i2)
                            elif i[3] in handcards_unused_list:
                                i.insert(3, i[3])
                                handcards_unused_list.remove(i[3])
                                handcards_used_elements_list.append(i[3])
                                i1 = i[:4]
                                i2 = i[4:]
                                boardcards_row_list.remove(i)
                                boardcards_row_list.append(i1)
                                boardcards_row_list.append(i2)
                            elif i[4] in handcards_unused_list:
                                i.insert(4, i[4])
                                handcards_unused_list.remove(i[4])
                                handcards_used_elements_list.append(i[4])
                                i1 = i[:5]
                                i2 = i[5:]
                                boardcards_row_list.remove(i)
                                boardcards_row_list.append(i1)
                                boardcards_row_list.append(i2)
                            elif i[5] in handcards_unused_list:
                                i.insert(4, i[5])
                                handcards_unused_list.remove(i[5])
                                handcards_used_elements_list.append(i[5])
                                i1 = i[:6]
                                i2 = i[6:]
                                boardcards_row_list.remove(i)
                                boardcards_row_list.append(i1)
                                boardcards_row_list.append(i2)
                    boardcards = boardcards_row_list + boardcards_group_list + handcards_used_list
                    # 判断是否破冰
                    break_ice_value = 0
                    for i in handcards_used_elements_list:
                        for j in i:
                            break_ice_value += j[1]

                    if break_ice_value >= 30:
                        return boardcards, handcards_unused_list, handcards_used_elements_list
                    else:
                        pass # 要一张牌  handcards.append(new_card)





