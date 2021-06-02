import os
import glob
import pprint


h_pass    = '0/h'
h0_pass   = '0/h0'
hTot_pass = '0/hTotal'


def load_file(file_path):
    with open(file_path, 'r') as f_in:
        l = [s.strip() for s in f_in.readlines()]
        
        return l

def obtain_initial_value(file_path):
    l = load_file(h0_pass)
    #pprint.pprint(l)

    load_flag_pre = 0
    load_flag     = 0
    initial_value_list = []

    for s in l:
        if load_flag == 1 and ')' in s:      load_flag = 0

        if load_flag == 1:
            initial_value_list.append(s)

        if 'internalField' in s:        load_flag_pre = 1
        if load_flag_pre == 1 and '(' in s:  load_flag = 1

    #initial_value_list = [float(initial_valie) for initial_valie in initial_value_list]
    #pprint.pprint(initial_value_list)
    #print("length of the field is", len(initial_value_list))

    return initial_value_list

def add_initial_values(h_list, h0_list):
        
    return [float(h) + float(h0) for h, h0 in zip(h_list, h0_list)]


def insert_initial_value_list(target_path, initial_value_list):
    with open(target_path, 'r') as f_in:
        l = f_in.readlines()
    pprint.pprint(l)
    pos_to_insert = 0
    for s in l:
        pos_to_insert += 1
        if 'internalField' in s: break
    print('position to insert: ', pos_to_insert)

    pos_to_insert -= 1
    l.pop(pos_to_insert)
        
    for i_ins, initial_value in enumerate(initial_value_list):
        l.insert(pos_to_insert + i_ins, str(initial_value_list[i_ins])+'\n')    
    
    pprint.pprint(l)
    

    with open(target_path, 'w') as f_out:
        f_out.writelines(l)

def make_list_to_insesrt(initial_value_list):
    list_to_insert=['internalField   nonuniform List<scalar>', len(initial_value_list), '(']
    list_to_insert.extend(initial_value_list)
    list_to_insert.extend(');')
    
    #pprint.pprint(list_to_insert)

    return list_to_insert


if __name__ == '__main__':
    h0_list = obtain_initial_value(h0_pass)    
    h_list  = obtain_initial_value(h_pass)    
    hTotal_list = add_initial_values(h_list, h0_list)
    hTotal_to_insert = make_list_to_insesrt(hTotal_list)

    #pprint.pprint(hTotal_to_insert)

    insert_initial_value_list(hTot_pass, hTotal_to_insert)