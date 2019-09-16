'''
The purpose of the Skycast class was to find the minimum number of clicks needed to surf through
the list of all the channels provided, given also a list of blocked channels that will be skipped
and the low and high channel numbers, which should be the range that the channels to surf through should be between.
'''
def Skycast():

    '''
    The purpose of the main was to read the input from the Skycast_input txt file. Since the text
    file will have each input structured in a 3-line format, i will have every first line as the 
    saved for the low and high variables, every second line will be the list of blocked channels 
    and every third will be the list of channels to surf through. After saving all the low_high_range,
    blocked channels and channels to surf through into the appropriate variables, these variables will 
    be given through into the calc_clicks, which is given all the low_high values, blocked channel lists
    and channels to surf through for all the inputs, rather than just 1 test case input.
    '''
    def main():
        fileInput = open("Skycast_input.txt","r")

        # check made to make sure that the file is not empty
        if fileInput is '':
            raise FileNotFoundError

        allLines = fileInput.readlines()        
        fileInput.close()

        line_counter = 0
        factor = 0
        all_channels_lists = []
        blocked_list = []
        low_high_list = []
        
        # loop to go through all the lines in the input, and every first line of the input is chosen as 
        #the line for the low and high setter, and every 2nd line is the blocked channel and the last is 
        #the actual channels to surf through.
        for line in allLines:
            if(line_counter % 3 == 0):
                num_range = line.strip().split()
                if(int(num_range[0]) < 0 or int(num_range[0]) > 10000):
                    raise RuntimeError("Cannot compute! Invalid lowest channel value!")
                elif(int(num_range[1]) < int(num_range[0]) or int(num_range[1]) > 100000):
                    raise RuntimeError("Cannot compute! Invalid highest channel value!") 
                low_high_list.append(num_range)
            elif(factor*3 + 1 == line_counter):
                blocked = line.strip().split()
                # gets rid of the first line that just gives the total number of channels
                blocked.remove(blocked[0])
                factor += 1
                if(len(blocked) > 40):
                    raise RuntimeError("Cannot block more than 40 channels!")
                blocked_list.append(blocked)
            else:
                current_line = line.strip().split()
                # gets rid of the first line that just gives the total number of channels
                current_line.remove(current_line[0])
                all_channels_lists.append(current_line)

            line_counter += 1

        calc_clicks(low_high_list,blocked_list,all_channels_lists)


    '''
    The purpose of this method was to go through each individual input given, where each input consists 
    of 3 lines, 1 set of low and high, blocked channels and channels to surf through. For each of the low, 
    and high, there is a check made to make sure the number is valid. Then, the values are converted to type
    integer and saved into the variables. Then, a check is made to make sure each value in the blocked list 
    is not the low or high and then, each value is saved into the newly converted integer type array for blocked
    channels. Then, same thing is done for the list of channels to surf through, but if the value is invalid, then
    a RunTimeError is raised. Then, when the low_high, blocked list, and the channels list is converted to int, 
    these values will be passed into the calc_score method, which will go through all the channels given. There 
    is a for loop that loops through the total number of test cases, where each one has a set of low and high, 
    blocked channels and channels to surf through.
    '''
    def calc_clicks(low_high_list,blocked_list,all_channels_lists):
        list_counter = 0
        test_case_number = 1
        for each_list in all_channels_lists:
            low, high = int(low_high_list[list_counter][0]) , int(low_high_list[list_counter][1]) 
            
            int_blocked_list = []
            for num in blocked_list[list_counter]:
                if(int(num) < low or int(num) > high):
                    raise RuntimeError("Blocked Channels cannot be smaller than the lowest or bigger than the highest!")
                else:
                    int_blocked_list.append(int(num))
                
            
            int_channel_list = []
            for each in each_list:
                if(int(each) < low or int(each) > high):
                    raise RuntimeError("Channels cannot be smaller than the lowest or bigger than the highest!")
                else:
                    int_channel_list.append(int(each))

            calc_score(int_channel_list,int_blocked_list,low,high,test_case_number)    
                        
            list_counter += 1
            test_case_number += 1


    '''
    This method had the purpose of going through all the channels that we are assigned to surf through. 
    First, we check how many clicks are required for the very first channels. Then, we make sure the length 
    of the channels list is more than 1, and if so, then we have a while loop that will go through all the 
    channels in the list, and inside the loop, there is a condition that if the counter is 0, then it means 
    that its the first number. For the best_solution method that will calculate the clicks, but it takes the
    previous channel, current channel and the next channel, and also the blocked list and low and high. If the
    counter is 0, this means that there is no previou channel, so that will be 0, then the current will be the
    current channel and follow will be the next channel. Then, the else means there was a previous, so the 
    counter-1 will be the previous, in the array, counter will be current and counter+1 will be the next. 
    Counter variable will also get incremented at the end of the loop to go through all the channels. Clicks gets
    incremented by the number of clicks gotten from the best_solution method, which calculates based on given prev, 
    current and following channel. Then, the output with the clicks will be printed.
    '''
    def calc_score(nums_list,blocked_list,low,high,test_case_number):
        clicks = 0
        first_num = nums_list[0]
        while(first_num > 0):
            first_num = first_num // 10
            clicks += 1
        
        counter = 0
        if(len(nums_list) == 1):
            pass
        else:
            while(not(counter == len(nums_list)-1)):
                if(counter == 0):
                    clicks += best_solution(0,nums_list[counter],nums_list[counter+1],blocked_list,low,high)
                else:
                    clicks += best_solution(nums_list[counter-1],nums_list[counter],nums_list[counter+1],blocked_list,low,high)
                counter += 1
        print("Output for Test Case #{}: {}".format(test_case_number,clicks))

    
    '''
    The purpose of the method below was to use the prev, current and next channels taken through the parameter,
    and calculate the total clicks for using the up button, down button, using the number pad, and finally the back
    button to go back to the last channel. if the current channel is equal to the next channel, then 0 will be returned
    since no clicks are made. Then, if there was no previous, then we cannot use the back channel, so that will be 
    skipped, but if there is a previous, then a local_current variable, temporary variable representing the current channel,
    is set to the previous channel, and then total clicks are calculated in order for the previous channel to reach 
    the follow channel. Then, there is a number pad clicks variable, which will bascially increment the clicks for each
    number pressed on the number pad. Then, there is a if/elif for if the current channel is smaller than the following, 
    then the up clicks will get incremented and the local variable is incremented and the loop will go on until the current
    equals the following channel. Then, the elif is executed if the current is bigger than the follow, and if the high 
    variable value is between the local current value and local_current + (number_clicks - 1), then the current will be
    set equal to the low, and the up_clicks will be incremented, and rest of the lines will be skipped by the "continue"
    in the if loop. Then, there is a tuple where the number of clicks for the up, down, back button and number pad will be
    saved in it. Then, I return the min of all of these values, with the condition that the minimum is not 0.
    '''
    def best_solution(prev,current,follow,blocked_list,low,high):
        local_current = current

        back_clicks = 0
        up_clicks = 0
        down_clicks = 0
        number_clicks = 0

        if(current == follow):
            return 0
        
        if(not(prev == 0)):
            local_current = prev
            while(not(local_current == follow)):
                if(prev > follow):
                    local_current -= 1
                    if(local_current in blocked_list):
                        pass
                    else:
                        back_clicks += 1
                else:
                    local_current += 1
                    if(local_current in blocked_list):
                        pass
                    else:
                        back_clicks += 1
            back_clicks += 1
        local_current = current

        local_follow = follow
        while(local_follow > 0):
            local_follow = local_follow // 10
            number_clicks += 1
        
        while(not(local_current == follow)):            
            if(current < follow):
                if(local_current in blocked_list):
                    pass
                else:
                    up_clicks += 1
                local_current += 1
            elif(current > follow):
                if(local_current in blocked_list):
                    pass
                elif(high > local_current and high < local_current+(number_clicks-1)):
                    if(local_current == high):
                        local_current = low
                        up_clicks += 1
                        continue
                else:
                    down_clicks += 1
                local_current -= 1
    
        tup = (back_clicks,up_clicks,down_clicks,number_clicks)
        return min([x for x in tup if x != 0])

    
    if __name__ == "__main__":
        main()

Skycast()
