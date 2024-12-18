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

    twooptout="$output_dir/2opt"
    swapout="$output_dir/swap"
    reallocate="$output_dir/reallocate"
    # Create output directory
    mkdir -p $twooptout
    mkdir -p $swapout
    mkdir -p $reallocate

    for file in $(ls $instances_dir); do
        echo "Running to instance $file"
        echo "running now lsswap local-search"
        python3 main.py $instances_dir/$file $swapout/results.txt $start_node --local-search lsswap > /dev/null 2>&1
        echo "running now ls2opt local-search"
        python3 main.py $instances_dir/$file $twooptout/results.txt $start_node --local-search ls2opt > /dev/null 2>&1
        echo "running now lsreallocate local-search"
        python3 main.py $instances_dir/$file $reallocate/results.txt $start_node --local-search lsreallocate > /dev/null 2>&1
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
