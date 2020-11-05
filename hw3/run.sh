#/bin/sh
hdfs dfs -rm -r -f /output_dir

hadoop jar /opt//hadoop/share/hadoop/tools/lib/hadoop-streaming-3.1.2.jar \
    -file "mapper.py" \
    -file "reducer.py" \
    -mapper "python mapper.py" \
    -reducer "python reducer.py" \
    -input "/input_dir/access_log.txt" \
    -output "/output_dir" 