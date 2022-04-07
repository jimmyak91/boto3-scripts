import boto3

access_key = input("Enter AWS Access Key: ")
secret_key = input("Enter AWS Secret Key: ")

b = boto3.client(
    'backup',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

restore_points = []

res = b.list_recovery_points_by_backup_vault(
    BackupVaultName='sas_prd_backup_vault',
    MaxResults=1000
)
restore_points = res['RecoveryPoints']


while "NextToken" in res:
    res = b.list_recovery_points_by_backup_vault(
        BackupVaultName='sas_prd_backup_vault',
        MaxResults=1000,
        NextToken=res['NextToken']
    )
    restore_points.extend(res['RecoveryPoints'])


for point in restore_points:
    b.delete_recovery_point(
        BackupVaultName='sas_prd_backup_vault',
        RecoveryPointArn=point['RecoveryPointArn']
    )
