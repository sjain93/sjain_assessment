import sjain_assess
import pytest
import json


def test_process_transactions():
    sjain_assess.process_transactions(output_file='actual_output.txt')

    exp_out = open('expected_output.txt')
    act_out = open('actual_output.txt')

    exp_out_content = exp_out.readlines()
    act_out_content = act_out.readlines()

    act_cnt = 0
    exp_cnt = 0

    while act_cnt < len(act_out_content) and exp_cnt < len(exp_out_content):
        assert json.loads(exp_out_content[exp_cnt]) == json.loads(act_out_content[act_cnt])
        act_cnt += 1
        exp_cnt += 1


    exp_out.close()
    act_out.close()
