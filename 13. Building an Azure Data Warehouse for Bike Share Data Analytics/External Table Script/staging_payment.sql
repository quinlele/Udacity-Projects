IF NOT EXISTS (SELECT * FROM sys.external_file_formats WHERE name = 'SynapseDelimitedTextFormat') 
	CREATE EXTERNAL FILE FORMAT [SynapseDelimitedTextFormat] 
	WITH ( FORMAT_TYPE = DELIMITEDTEXT ,
	       FORMAT_OPTIONS (
			 FIELD_TERMINATOR = ',',
			 USE_TYPE_DEFAULT = FALSE
			))
GO

IF NOT EXISTS (SELECT * FROM sys.external_data_sources WHERE name = 'udacity-project2_lele_dfs_core_windows_net') 
	CREATE EXTERNAL DATA SOURCE [udacity-project2_lele_dfs_core_windows_net] 
	WITH (
		LOCATION = 'abfss://udacity-project2@lele.dfs.core.windows.net' 
	)
GO

CREATE EXTERNAL TABLE [dbo].[staging_payment] (
	[payment_id] BIGINT,
	[date] VARCHAR(50),
	[amount] FLOAT,
	[rider_id] BIGINT
	)
	WITH (
	LOCATION = 'publicpayment.csv',
	DATA_SOURCE = [udacity-project2_lele_dfs_core_windows_net],
	FILE_FORMAT = [SynapseDelimitedTextFormat]
	)
GO


SELECT TOP 100 * FROM [dbo].[staging_payment]
GO
