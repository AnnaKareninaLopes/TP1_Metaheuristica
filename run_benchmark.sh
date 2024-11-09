#!/bin/bash


function exe(){
    echo "$@"
    "$@"
}


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
        exe python3 main.py $instances_dir/$file $instance_directory/result.$file.agm.txt agm $start_node
        if [ $? -ne 0 ]; then
            echo "Error running agm heuristic"
            exit 1
        fi
        echo "running now nn heuristic"
        python3 main.py $instances_dir/$file $instance_directory/result.$file.nn.txt nn $start_node
        echo "running now ci heuristic"
        python3 main.py $instances_dir/$file $instance_directory/result.$file.ci.txt ci $start_node
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

    if [ $# -ne 3 ]; then
        help 1
    elif [ $1 == "-h" ]; then
        help 0
    fi


    output_dir=$1
    instances_dir=$2
    start_node=$3

    run_benchmark $output_dir $instances_dir $start_node

}

main $@
