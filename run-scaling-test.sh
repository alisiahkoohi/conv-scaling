#!/bin/bash -l

[ -d logs ] || mkdir logs

echo "Running Devito tests"
devito_file=logs/devito-conv.txt
rm -f $devito_file

for log_nch in `seq 1 1 4`
do
    for k in `seq 3 2 11`
    do
        for log_n in `seq 5 1 14`
        do
            echo "running test for log(nch)=$log_nch, k=$k, log(n)=$log_n"

            info=$( { /usr/bin/time --format \
                   'wall-clock time (s): %e\nmemory (kbytes): %M' \
                   python devito-conv.py $k $log_n $log_nch; } 2>&1 )

            if [ $? -eq 0 ]
            then
                echo "$info"
                run_time=$(echo "$info" | grep "wall" |& grep -oP \
                    '(?<=(s)\): ).*')
                memory=$(echo "$info" | grep "memory" |& grep -oP \
                    '(?<=(kbytes)\): ).*')

                echo "$log_nch,$k,$log_n,$run_time,$memory" >> $devito_file

            else
                echo "Failed — perhaps low memory"
                echo "$log_nch,$k,$log_n,-1,-1" >> $devito_file
            fi
        done

        echo "log(nch)=$log_nch, k=$k — uploading to dropbox"
        rclone copy --progress $devito_file GTDropbox:scaling-test/aws/

    done
done


echo "Running PyTorch CPU tests"
torch_file=logs/torch-conv.txt
rm -f $torch_file

for log_nch in `seq 1 1 4`
do
    for k in `seq 3 2 11`
    do
        for log_n in `seq 5 1 14`
        do
            echo "running test for log(nch)=$log_nch, k=$k, log(n)=$log_n"

            info=$( { /usr/bin/time --format \
                   'wall-clock time (s): %e\nmemory (kbytes): %M' \
                   python torch-conv.py $k $log_n $log_nch; } 2>&1 )

            if [ $? -eq 0 ]
            then
                echo "$info"
                run_time=$(echo "$info" | grep "wall" |& grep -oP \
                    '(?<=(s)\): ).*')
                memory=$(echo "$info" | grep "memory" |& grep -oP \
                    '(?<=(kbytes)\): ).*')

                echo "$log_nch,$k,$log_n,$run_time,$memory" >> $torch_file

            else
                echo "Failed — perhaps low memory"
                echo "$log_nch,$k,$log_n,-1,-1" >> $torch_file
            fi
        done

        echo "log(nch)=$log_nch, k=$k — uploading to dropbox"
        rclone copy --progress $torch_file GTDropbox:scaling-test/aws/

    done
done
