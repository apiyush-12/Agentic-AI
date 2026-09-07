# AWS Skill — Examples

## Example 1: S3 client using credentials from environment, not hardcoded

```python
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    "s3",
    region_name=os.environ.get("AWS_REGION", "us-east-1"),
)  # boto3 picks up AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY from the environment automatically


def upload_scratch_file(bucket: str, key: str, content: bytes) -> None:
    s3.put_object(Bucket=bucket, Key=key, Body=content)


def read_scratch_file(bucket: str, key: str) -> bytes:
    response = s3.get_object(Bucket=bucket, Key=key)
    return response["Body"].read()
```

## Example 2: Least-privilege IAM policy for a single S3 prefix

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DeepAgentScratchAccess",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::my-deepagent-bucket/scratch/*"
    },
    {
      "Sid": "DeepAgentListBucket",
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::my-deepagent-bucket",
      "Condition": {
        "StringLike": { "s3:prefix": "scratch/*" }
      }
    }
  ]
}
```

Avoid the overly broad equivalent:

```json
{
  "Effect": "Allow",
  "Action": "s3:*",
  "Resource": "*"
}
```

## Example 3: Assuming a role instead of long-lived keys

```python
import boto3

sts = boto3.client("sts")
assumed = sts.assume_role(
    RoleArn="arn:aws:iam::123456789012:role/DeepAgentRole",
    RoleSessionName="deepagent-session",
)
credentials = assumed["Credentials"]

s3 = boto3.client(
    "s3",
    aws_access_key_id=credentials["AccessKeyId"],
    aws_secret_access_key=credentials["SecretAccessKey"],
    aws_session_token=credentials["SessionToken"],
)
```

## Example 4: Read-only dry-run before a mutating call

```python
import boto3

s3 = boto3.client("s3")

# Confirm the object exists and check its size before overwriting/deleting it
head = s3.head_object(Bucket="my-deepagent-bucket", Key="scratch/notes.md")
print(head["ContentLength"], head["LastModified"])

# Only after confirming with the user:
# s3.delete_object(Bucket="my-deepagent-bucket", Key="scratch/notes.md")
```

## Example 5: Bedrock as an alternative LangChain model provider

```python
import os
from dotenv import load_dotenv
from langchain_aws import ChatBedrock

load_dotenv()

llm = ChatBedrock(
    model_id="anthropic.claude-sonnet-5-v1:0",
    region_name=os.environ.get("AWS_REGION", "us-east-1"),
)

response = llm.invoke("Summarize the deepagent architecture in one sentence.")
```
