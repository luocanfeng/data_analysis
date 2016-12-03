hdfs_test.py 是读取hdfs文件的测试代码，已调通，不过不建议这样做，文件很大，需要下载很久；

interests_cleaning.py 是联通兴趣数据初步处理（group）的代码，运行需要40-60分钟，不建议运行，可以直接从百度网盘下载处理好的数据，路径在“全部文件>unioncomm_data>analysis”

merge_csv_files.py 上述步骤（interests_cleaning.py）处理完以后是65个分割好的小文件，需要通过这个脚本合并文件；文件已上传到百度网盘“全部文件>unioncomm_data>analysis”，那个csv文件就是

interests_analysis.py 对于初步处理后的文件进行分析，这个脚本文件还在不断调试、优化
