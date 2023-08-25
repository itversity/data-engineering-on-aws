aws emr create-cluster \
  --applications Name=Hadoop Name=Spark Name=JupyterEnterpriseGateway \
  --ec2-attributes '{"KeyName":"itvlivedemos","InstanceProfile":"EMR_EC2_DefaultRole","SubnetId":"subnet-3340f619","EmrManagedSlaveSecurityGroup":"sg-a5a51ed4","EmrManagedMasterSecurityGroup":"sg-4da61d3c"}' \
  --release-label emr-6.4.0 \
  --log-uri 's3n://aws-logs-582845781536-us-east-1/elasticmapreduce/' \
  --steps '[{"Args":["spark-submit","--deploy-mode","cluster","--conf","spark.yarn.appMasterEnv.ENVIRON=PROD","\\","--conf","spark.yarn.appMasterEnv.SRC_DIR=s3://itv-github-emr/prod/landing/ghactivity/","\\","--conf","spark.yarn.appMasterEnv.SRC_FILE_FORMAT=json","\\","--conf","spark.yarn.appMasterEnv.TGT_DIR=s3://itv-github-emr/prod/raw/ghactivity/","\\","--conf","spark.yarn.appMasterEnv.TGT_FILE_FORMAT=parquet","\\","--conf","spark.yarn.appMasterEnv.SRC_FILE_PATTERN=2021-01-14","\\","--py-files","s3://itv-github-emr/app/itv-ghactivity.zip","\\","s3://itv-github-emr/app/app.py"],"Type":"CUSTOM_JAR","ActionOnFailure":"CONTINUE","Jar":"command-runner.jar","Properties":"","Name":"ITV GHActivity"},{"Args":["spark-submit","--deploy-mode","cluster","--conf","spark.yarn.appMasterEnv.ENVIRON=PROD","--conf","spark.yarn.appMasterEnv.SRC_DIR=s3://itv-github-emr/prod/landing/ghactivity/","--conf","spark.yarn.appMasterEnv.SRC_FILE_FORMAT=json","--conf","spark.yarn.appMasterEnv.TGT_DIR=s3://itv-github-emr/prod/raw/ghactivity/","--conf","spark.yarn.appMasterEnv.TGT_FILE_FORMAT=parquet","--conf","spark.yarn.appMasterEnv.SRC_FILE_PATTERN=2021-01-14","--py-files","s3://itv-github-emr/app/itv-ghactivity.zip","s3://itv-github-emr/app/app.py"],"Type":"CUSTOM_JAR","ActionOnFailure":"CONTINUE","Jar":"command-runner.jar","Properties":"","Name":"Spark application"}]' \
  --instance-groups '[{"InstanceCount":1,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"InstanceGroupType":"CORE","InstanceType":"m5.xlarge","Name":"Core - 2"},{"InstanceCount":0,"BidPrice":"OnDemandPrice","EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"InstanceGroupType":"TASK","InstanceType":"m5.xlarge","Name":"Task_m5.xlarge_SPOT_By_Managed_Scaling"},{"InstanceCount":1,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"InstanceGroupType":"MASTER","InstanceType":"m5.xlarge","Name":"Master - 1"}]' \
  --configurations '[{"Classification":"spark-hive-site","Properties":{"hive.metastore.client.factory.class":"com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"}}]' \
  --auto-scaling-role EMR_AutoScaling_DefaultRole \
  --ebs-root-volume-size 10 \
  --service-role EMR_DefaultRole \
  --enable-debugging \
  --auto-termination-policy '{"IdleTimeout":1800}' \
  --managed-scaling-policy '{"ComputeLimits":{"MaximumOnDemandCapacityUnits":1,"UnitType":"Instances","MaximumCapacityUnits":2,"MinimumCapacityUnits":1,"MaximumCoreCapacityUnits":1}}' \
  --name 'itv-github-emr' \
  --scale-down-behavior TERMINATE_AT_TASK_COMPLETION \
  --region us-east-1

aws emr add-steps \
  --cluster-id j-XXXXXXXX \
  --steps Type=CUSTOM_JAR,Name=CustomJAR,ActionOnFailure=CONTINUE,Jar=s3://mybucket/mytest.jar,Args=arg1,arg2,arg3
