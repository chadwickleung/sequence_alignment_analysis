import sys
from termcolor import colored

def seqAlign():
    data = open('data.txt', 'r')
    a_Sequence = ''
    b_Sequence = ''
    identical = ''
    for line in data:
        if line[0:10] == 'A_Sequence' or line[0:10] == 'B_Sequence':
            seq_str = line.split()[2]
            if line[0:10] == 'A_Sequence':
                a_Sequence += seq_str
            else:
                b_Sequence += seq_str
            index = line.find(seq_str)
            length = len(seq_str)
        else:
            identical += line[index : index + length]
            
    colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    
    model_ans = open('model_ans.txt', 'r')
    group_num = -1
    groups = []
    color_array = []
    for line in model_ans:
        line = line.strip('\n')
        if line in colors:
            group_num += 1
            groups.append('')
            color_array.append(line)
        else:
            groups[group_num] += line


    def compareSeqs(start, end, count, mistake):
#        count = 0
#        mistake = ''
        result = ''
        remainder = 0
        for i in range(start, end):
            if identical[i] == '|':
                if count != 0:
                    result += '  (' + str(count) + ')  '
                    count = 0
                elif mistake:
                    result += '  <' + mistake + '>  '
                    mistake = ''
                result += a_Sequence[i]
            elif a_Sequence[i] == '-' or b_Sequence[i] == '-':
                if i == (end - 1) and count != 0:
                    result += '  (' + str(count) + ')  '
                
                if a_Sequence[i] == '-':
                    remainder += 1
                count += 1
            else:
                if i == (end - 1) and mistake:
                    result += '  <' + mistake + '>  '
                mistake += b_Sequence[i]
            
        if remainder > 0 and (end + remainder) <= len(a_Sequence):
            end_result, end_remainder = compareSeqs(end, end + remainder, count, mistake)
            result += end_result
            remainder += end_remainder
        return result, remainder
    
    initial = 0
    for grp_no in range(len(groups)):
        printResult = ''
        grp_length = len(groups[grp_no])
        eventual = initial + grp_length
        printResult, endcase = compareSeqs(initial, eventual, 0, '')
        
        if grp_no != (len(groups) - 1):
            print(colored(printResult, color_array[grp_no]), end='')
        else:
            print(colored(printResult, color_array[grp_no]))
        initial += grp_length + endcase
        
    
seqAlign()
