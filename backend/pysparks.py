from pyspark.sql import functions as F

grouped = (
	txp_spark.groupBy("customer_id")
	.agg(
		F.sum("amount").alias("total_amount"),
		F.avg("amount").alias("average_amount"),
		F.count("amount").alias("transaction_count"),
	)
)

grouped.show()
