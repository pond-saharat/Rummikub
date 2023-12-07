import deck


class csPlayerRegularRule:

    # def a(self,handcards,boardcards):
    #     self.cs_regular_play(handcards,boardcards)
    # Call the function directly：cs_regular_play(self,verify_of_break_ice, handcards, boardcards):

    # step-1 Convert the card object to list
    def handcards_play_rule(self, handcards):  # handcards from grid
        handcards = [[card.colour.lower(), card.number] for card in handcards]
        for card in handcards:
            if card[0] == 'joker':
                card[1] = 0
                card[0] = 'Joker'

        def order_principle(card):
            color_order = {'red': 0, 'yellow': 1, 'green': 2, 'blue': 3, 'pink': 4, 'Joker': 5}
            return (color_order[card[0]], card[1])

        ordered_handcards = sorted(handcards, key=order_principle)
        # step-2 Divide the list into smaller lists of different colors
        red_hand_list = []
        yellow_hand_list = []
        green_hand_list = []
        blue_hand_list = []
        pink_hand_list = []
        Joker_list = []  # Joker card
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
                Joker_list.append(i)  # Joker card

        # step-3 Generate filter list
        # step-3-1 Screen out duplicate elements and generate a second filtered list
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

        second_hand_red_list = second_hand_list(red_hand_list)  # The extra red card from the first round
        second_hand_yellow_list = second_hand_list(yellow_hand_list)  # The extra yellow card from the first round
        second_hand_green_list = second_hand_list(green_hand_list)  # The extra green card from the first round
        second_hand_blue_list = second_hand_list(blue_hand_list)  # The extra blue card from the first round
        second_hand_pink_list = second_hand_list(pink_hand_list)  # The extra pink card from the first round
        second_hand_joker_list = Joker_list  # The extra Joker card from the first round

        # step-3-2 Generates a list of the first filters
        def first_hand_check_list(list):
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

        # step-3-3 Divide the odd and even cards
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

        # Odd deck
        first_hand_red_odd_check_list = check_odd_list(first_hand_red_check_list)
        # print(first_hand_red_odd_check_list)
        first_hand_yellow_odd_check_list = check_odd_list(first_hand_yellow_check_list)
        first_hand_green_odd_check_list = check_odd_list(first_hand_green_check_list)
        first_hand_blue_odd_check_list = check_odd_list(first_hand_blue_check_list)
        first_hand_pink_odd_check_list = check_odd_list(first_hand_pink_check_list)
        # Even deck
        first_hand_red_even_check_list = check_even_list(first_hand_red_check_list)
        # print(first_red_oven_check_list)
        first_hand_yellow_even_check_list = check_even_list(first_hand_yellow_check_list)
        first_hand_green_even_check_list = check_even_list(first_hand_green_check_list)
        first_hand_blue_even_check_list = check_even_list(first_hand_blue_check_list)
        first_hand_pink_even_check_list = check_even_list(first_hand_pink_check_list)

        # step-4 First screening
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

        # step-4-1 Compile a three-dimensional list of the elements selected in the first round [[['red', 1, 0], ['red', 3, 0], ['red', 5, 1], ['red', 7, 1]]]
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

        # step-4-2 The remaining elements of the first round of filtering are found and a new list is formed with the remaining elements of the second round of filtering in the future
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
        blue_hand_first_unused_list = find_unused_element(first_hand_blue_check_list, first_hand_blue_final_even_list,
                                                          first_hand_blue_final_odd_list)
        pink_hand_first_unused_list = find_unused_element(first_hand_pink_check_list, first_hand_pink_final_even_list,
                                                          first_hand_pink_final_odd_list)
        first_hand_total_unused_list = first_hand_total_unused_list + red_hand_first_unused_list + yellow_hand_first_unused_list + green_hand_first_unused_list + blue_hand_first_unused_list + pink_hand_first_unused_list
        # print(first_hand_total_unused_list)  # first_hand_total_unused_list do not include Joker

        # step-4-3 Qualified rows after the first round of inspection
        red_hand_first_used_list = first_hand_red_final_even_list + first_hand_red_final_odd_list
        yellow_hand_first_used_list = first_hand_yellow_final_even_list + first_hand_yellow_final_odd_list
        green_hand_first_used_list = first_hand_green_final_even_list + first_hand_green_final_odd_list
        blue_hand_first_used_list = first_hand_blue_final_even_list + first_hand_blue_final_odd_list
        pink_hand_first_used_list = first_hand_pink_final_even_list + first_hand_pink_final_odd_list
        first_hand_total_used_list = red_hand_first_used_list + yellow_hand_first_used_list + green_hand_first_used_list + blue_hand_first_used_list + pink_hand_first_used_list
        # All rows generated in the first round#!!!!!!!!!!
        # print(first_total_used_list)

        # step-5 Second screening
        # step-5-1 Find the list needed for second screening（eg.second_hand_red_list = second_hand_red_check_list)
        second_hand_red_check_list = second_hand_red_list
        second_hand_yellow_check_list = second_hand_yellow_list
        second_hand_green_check_list = second_hand_green_list
        second_hand_blue_check_list = second_hand_blue_list
        second_hand_pink_check_list = second_hand_pink_list

        # step-5-2 Divide the odd and even cards
        # Odd card
        second_hand_red_odd_check_list = check_odd_list(second_hand_red_check_list)
        second_hand_yellow_odd_check_list = check_odd_list(second_hand_yellow_check_list)
        second_hand_green_odd_check_list = check_odd_list(second_hand_green_check_list)
        second_hand_blue_odd_check_list = check_odd_list(second_hand_blue_check_list)
        second_hand_pink_odd_check_list = check_odd_list(second_hand_pink_check_list)
        # Even cards
        second_hand_red_even_check_list = check_even_list(second_hand_red_check_list)
        second_hand_yellow_even_check_list = check_even_list(second_hand_yellow_check_list)
        second_hand_green_even_check_list = check_even_list(second_hand_green_check_list)
        second_hand_blue_even_check_list = check_even_list(second_hand_blue_check_list)
        second_hand_pink_even_check_list = check_even_list(second_hand_pink_check_list)

        # step-5-3 Second round inspection
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

        # step-5-4 Find the remaining elements from the second round of screening
        # second_hand_total_unused_list = []

        red_hand_second_unused_list = find_unused_element(second_hand_red_check_list, second_hand_red_final_even_list,
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
        # print(second_hand_total_unused_list)  second_hand_total_unused_list do not include Joker

        # step-5-5 Qualified rows after a second round of inspection
        red_hand_second_used_list = second_hand_red_final_even_list + second_hand_red_final_odd_list
        yellow_hand_second_used_list = second_hand_yellow_final_even_list + second_hand_yellow_final_odd_list
        green_hand_second_used_list = second_hand_green_final_even_list + second_hand_green_final_odd_list
        blue_hand_second_used_list = second_hand_blue_final_even_list + second_hand_blue_final_odd_list
        pink_hand_second_used_list = second_hand_pink_final_even_list + second_hand_pink_final_odd_list
        second_hand_total_used_list = red_hand_second_used_list + yellow_hand_second_used_list + green_hand_second_used_list + blue_hand_second_used_list + pink_hand_second_used_list
        # Second generated row，！！！！！！
        # print(second_total_used_list)
        # As of the second round of screening, all matched rows were successful
        total_hand_used_list = first_hand_total_used_list + second_hand_total_used_list
        # The total rows generated in one or two rounds!!!!!!!
        # print(total_hand_used_list)

        # step-6 Step 3 Filter (Filter the remaining pairs of cards)

        # step-6-1  Examples of remaining hands：[['red', 2], ['red', 4], ['red', 8], ['red', 13], ['yellow', 13], ['green', 13], ['blue', 12], ['blue', 13], ['red', 1], ['red', 2]]
        # step-6-1 Deweight all elements in the remaining hand
        list1 = []
        list2 = []
        for i in second_hand_total_unused_list:
            if i not in list1:
                list1.append(i)
            else:
                list2.append(i)
        # list1 = [i for i in second_hand_total_unused_list if i not in list1]
        # step-6-2 Find the cards in the list that have different suits but the same value
        # Find the deck
        result_dict = {}
        for i in list1:
            key = i[1]
            if key in result_dict:
                result_dict[key].append(i)
            else:
                result_dict[key] = [i]

        handcards_group = [value for value in result_dict.values() if len(value) > 2]  # This is a three-dimensional list
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
            else:
                break

        # Removes the hand from the elements that make up the group, generating the final list of remaining hands final_handcards
        # Split handcards_group into a two-dimensional list because the remaining hands are a two-dimensional list so that you can compare them
        handcards_group_elements = []
        for i in handcards_group:
            handcards_group_elements.append(i)
        # Carry out removal
        final_handcards = []
        seen_set = set()
        Joker_unused_list = []
        # list2_elements = []
        for i in Joker_list:
            Joker_unused_list.append(i)
        # for i in list2:

        second_hand_total_unused_list = second_hand_total_unused_list + Joker_unused_list + list2
        for i in second_hand_total_unused_list:
            if i in handcards_group_elements and i not in seen_set:
                seen_set.add(i)
            else:
                final_handcards.append(i)

        # All hands to be played (rows and groups sorted)
        second_hand_total_used_list = second_hand_total_used_list + handcards_group
        return second_hand_total_used_list, second_hand_total_unused_list

    def cs_regular_play(self, handcards, boardcards):
        # if verify_of_break_ice is True:
        # deal with boardcard: translate it from grid
        # boardcards = [boardcards for boardcards in grid.value]
        # step01-Find the element of the handcards that can form a team on its own

        boardcards = [[[card.colour.lower(), card.number] for card in cell] for cell in boardcards]
        for cell in boardcards:
            for card in cell:
                if card[0] == 'joker':
                    card[1] = 0
                    card[0] = 'Joker'

        handcards_used_list = self.handcards_play_rule(handcards)[0]  # new groups formed when the hands are paired individually
        handcards_used_elements_list = []
        for i in handcards_used_list:
            for j in i:
                handcards_used_elements_list.append(j)
        handcards_unused_list = self.handcards_play_rule(handcards)[1]  # The handcards left after a single team
        # step02-Preprocess the cards on the board, find the groups of row and group, and store them in different lists
        boardcards_group_list = []  # Three-dimensional list
        boardcards_row_list = []  # Three-dimensional list
        # Handle Joker cards in the boardcards
        boardcards_Joker_list = []
        for i in boardcards:
            if ['Joker', 0] in i:
                boardcards_Joker_list.append(i)  # The board deck containing Joker cards is stored in this list, left behind, and added directly to the final result
                boardcards.remove(i)  # Remove the group containing Joker from the desktop deck to be processed

        for i in boardcards:  # find row
            if i[0][0] == i[1][0]:
                boardcards_row_list.append(i)
        for i in boardcards:  # find group
            if i[0][1] == i[1][1]:
                boardcards_group_list.append(i)
        # step03 Find out if the remaining hand can be added to the group of boardcards
        color_list = ["red", "yellow", "green", "blue", "pink"]
        for i in boardcards_group_list:
            for j in handcards_unused_list:  # One-dimensional list, single card
                if j[1] == i[0][1] and j not in i:
                    i.append(j)  # Generate a new group
                    handcards_unused_list.remove(j)  # Removes the missing element from the handcards
                    handcards_used_elements_list.append(j)  # Count the handcards that have been used

        # If there is a Joker in the hand, see if the Joker can be added to the group
        while True:
            if ['Joker', 0] not in handcards_unused_list:
                break
            elif ['Joker', 0] in handcards_unused_list:
                a = 0
                for i in handcards_unused_list:
                    if i == ['Joker', 0]:
                        a += 1  # Count the number of Jokers in handcards
                if a == 1:
                    for i in boardcards_group_list:
                        if len(i) <= 4:
                            i.append(['Joker', 0])
                            handcards_unused_list.remove(['Joker', 0])
                            break
                        if a == 2:
                            for i in handcards_unused_list:
                                if len(i) <= 4:
                                    i.append(['Joker', 0])
                                    handcards_unused_list.remove(['Joker', 0])
            else:
                break

        # step04 Find out if the remaining handcards can be added to the row of boardcards
        # step04-01 See if can add elements before and after each row and add them
        # step04-01-01 front
        handcards = [[card.colour, card.number] for card in handcards]

        for i in boardcards_row_list:
            while True:
                if i[0][1] - 2 > 0:
                    if [i[0][0], i[0][1] - 2] in handcards_unused_list:
                        i.insert(0, [i[0][0], i[0][1] - 2])  # Fill the card in first place
                        handcards_unused_list.remove([i[0][0], i[1][1] - 2])  # Remove the missing element from the handcards
                        handcards_used_elements_list.append([i[0][0], i[1][1] - 2])  # save the handcards that have been used
                    else:
                        break
                else:
                    break
            # step04-01-02 rear
        for i in boardcards_row_list:
            while True:
                if i[-1][1] + 2 <= 15:
                    if [i[-1][0], i[-1][1] + 2] in handcards_unused_list:
                        i.append([i[-1][0], i[-1][1] + 2])  # Fill the card to the last place
                        handcards_unused_list.remove([i[0][0], i[-1][1]])  # Remove the missing element from the handcards
                        handcards_used_elements_list.append([i[0][0], i[-1][1]])  # save the handcards that have been used
                    else:
                        break
                else:
                    break

        # step04-01-02 Check that whether there are cards in the hand that can be inserted into the middle of the row
        #  when len(list) = 5, Insert the element in bit i[2] and split the row list into two
        for i in boardcards_row_list:
            if len(i) == 5:
                if i[2] in handcards_unused_list:
                    i.insert(2, i[2])
                    handcards_unused_list.remove(i[2])
                    handcards_used_elements_list.append(i[2])
                    # split one row into two rows
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
                    # split one row into two rows
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

            if len(i) == 7:
                if i[2] in handcards_unused_list:
                    i.insert(2, i[2])
                    handcards_unused_list.remove(i[2])
                    handcards_used_elements_list.append(i[2])
                    # split one row into two rows
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
                    # split one row into two rows
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

        # step05 Count the final results
        # step05-01
        boardcards = boardcards_row_list + boardcards_group_list + handcards_used_list + boardcards_Joker_list
        return boardcards, handcards_unused_list  # , handcards_used_list


