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

    ls2opt="$output_dir/ls2opt"
    vndtsr="$output_dir/vndtsr"
    vndtrs="$output_dir/vndtrs"
    vndstr="$output_dir/vndstr"
    vndsrt="$output_dir/vndsrt"
    vndrts="$output_dir/vndrts"
    vndrst="$output_dir/vndrst"
    cstsr="$output_dir/cstsr"
    # Create output directory
    mkdir -p $ls2opt
    mkdir -p $vndtsr
    mkdir -p $vndtrs
    mkdir -p $vndstr
    mkdir -p $vndsrt
    mkdir -p $vndrts
    mkdir -p $vndrst
    mkdir -p $cstsr

    for file in $(ls $instances_dir); do
        echo "Running to instance $file"
        echo "running now ls2opt local-search"
        python3 main.py $instances_dir/$file $ls2opt/results.txt $start_node --local-search ls2opt > /dev/null 2>&1
        echo "running now vndtsr local-search"
        python3 main.py $instances_dir/$file $vndtsr/results.txt $start_node --local-search vndtsr > /dev/null 2>&1
        echo "running now vndtrs local-search"
        python3 main.py $instances_dir/$file $vndtrs/results.txt $start_node --local-search vndtrs > /dev/null 2>&1
        echo "running now vndstr local-search"
        python3 main.py $instances_dir/$file $vndstr/results.txt $start_node --local-search vndstr > /dev/null 2>&1
        echo "running now vndsrt local-search"
        python3 main.py $instances_dir/$file $vndsrt/results.txt $start_node --local-search vndsrt > /dev/null 2>&1
        echo "running now vndrts local-search"
        python3 main.py $instances_dir/$file $vndrts/results.txt $start_node --local-search vndrts > /dev/null 2>&1
        echo "running now vndrst local-search"
        python3 main.py $instances_dir/$file $vndrst/results.txt $start_node --local-search vndrst > /dev/null 2>&1
        echo "running now cstsr local-search"
        python3 main.py $instances_dir/$file $cstsr/results.txt $start_node --local-search cstsr > /dev/null 2>&1
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
