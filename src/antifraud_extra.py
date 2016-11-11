#!/usr/bin/env python

import sys

# function for creating "check list" for input data
def get_check_list(stream_data):

    check_list = []
    prv_time = ''
    prv_id2_list = []
    # assign variables for each line
    for line in stream_data[1:]:
        
        time, id1, id2, amount, message = line.split(',',4) # some messages contain commas

        # if time is changed
        if time != prv_time:                 # if time is changed, "trusted"               
            check_list.append('trusted')
            prv_id2_list = [id2]

        # if it's the first time a user receives a payment at the current time
        elif id2 not in prv_id2_list:
            check_list.append('trusted')
            prv_id2_list.append(id2)
        
        # if a user already received a payment at the current time
        elif id2 in prv_id2_list:
            check_list.append('unverified')
        
        prv_time = time
    
    return check_list

# use sys.argv to get the input/output paths
# get check lists and outputs them into text files.
def main():

    stream_file = sys.argv[1]

    with open(stream_file, 'r') as s_f:
        stream_data = s_f.read().split('\n')
        del stream_data[-1]

    check_list = get_check_list(stream_data)
    out_text   = '\n'.join(check_list) + '\n'
    
    with open(sys.argv[2], 'w+') as out_f:
        out_f.write(out_text)

if __name__ == "__main__":

    main()
