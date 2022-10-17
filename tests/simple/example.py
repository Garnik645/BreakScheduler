import os
import sys
ROOT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIRECTORY)
import checkresult

# RUN: %{diff} --length 5 --filter 20 --result-path %T_arguments_swapped_AND_arguments_swapped --first-module %{simple_clones_pdg}/list-arguments_swapped.list --second-module %{simple_clones_pdg}/list-arguments_swapped-copy.list

checkresult.check_result_diff("Output_arguments_swapped_AND_arguments_swapped",
                              "arguments_swapped__and__arguments_swapped.json")

# RUN: %{python} %s
