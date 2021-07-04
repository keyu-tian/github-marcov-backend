cd ..

GLOG_vmodule=MemcachedClient=-1 \
spring.submit run --gpu -n7 \
--ntasks-per-node=7 \
--cpus-per-task=2 \
--job-name "train_spider" \
python -u -m spiders.train_spider
