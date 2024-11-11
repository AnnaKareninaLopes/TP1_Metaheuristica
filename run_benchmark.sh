#!/bin/bash


function run_benchmark(){
    output_dir=$1
    instances_dir=$2
    start_node=$3

    # Create output directory
    mkdir -p $output_dir

    for file in $(ls $instances_dir); do
        echo "Running to instance $file"
        echo "running now agm heuristic"
        instance_directory="$output_dir/$(echo $file | egrep '\..+$')"
        mkdir -p $instance_directory
        python3 main.py $instances_dir/$file $instance_directory/result.$file.agm.txt agm $start_node > /dev/null 2>&1
        echo "running now nn heuristic"
        python3 main.py $instances_dir/$file $instance_directory/result.$file.nn.txt nn $start_node > /dev/null 2>&1
        echo "running now ci heuristic"
        python3 main.py $instances_dir/$file $instance_directory/result.$file.ci.txt ci $start_node > /dev/null 2>&1
    done

}

function run_benchmark_and_storage_output_by_instance_file(){
    output_dir=$1
    instances_dir=$2
    start_node=$3

    agm_output_dir="$output_dir/agm"
    nn_output_dir="$output_dir/nn"
    ci_output_dir="$output_dir/ci"
    # Create output directory
    mkdir -p $agm_output_dir
    mkdir -p $nn_output_dir
    mkdir -p $ci_output_dir

    for file in $(ls $instances_dir); do
        echo "Running to instance $file"
        echo "running now agm heuristic"
        python3 main.py $instances_dir/$file $agm_output_dir/result.$file.txt agm $start_node > /dev/null 2>&1
        echo "running now nn heuristic"
        python3 main.py $instances_dir/$file $agm_output_dir/result.$file.txt nn $start_node > /dev/null 2>&1
        echo "running now ci heuristic"
        python3 main.py $instances_dir/$file $agm_output_dir/result.$file.txt ci $start_node > /dev/null 2>&1
    done

}

function help(){
    echo "Usage: $0 <output_dir> <instances_dir> <start_node>"
    echo "output_dir: directory to save the results"
    echo "instances_dir: directory with the instances"
    echo "start_node: initial node that each heuristic will start"
    exit $1
}

function main(){

    if [ $1 == "-h" ]; then
        help 0
    elif [ $# -ne 3 ]; then
        help 1
    fi


    output_dir=$1
    instances_dir=$2
    start_node=$3

    run_benchmark_and_storage_output_by_instance_file $output_dir $instances_dir $start_node

}

main $@
