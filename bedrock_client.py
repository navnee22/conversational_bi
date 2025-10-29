import boto3, json, os

bedrock = boto3.client(service_name='bedrock-runtime', region_name=os.getenv("AWS_REGION"))

PROMPT_TEMPLATE = """
You are an expert data analyst. 
Generate an ANSI SQL query for the following user request.
Use only the provided schema and table names.

Schema:
{schema}

User question:
{question}

Return only SQL, no explanation.
"""

def generate_sql_from_prompt(user_query: str, metadata: dict):
    schema_text = json.dumps(metadata, indent=2)
    prompt = PROMPT_TEMPLATE.format(schema=schema_text, question=user_query)

    response = bedrock.invoke_model(
        modelId=os.getenv("BEDROCK_MODEL_ID"),
        body=json.dumps({"prompt": prompt})
    )
    result = json.loads(response["body"].read())
    return result.get("outputs", [{}])[0].get("text", "")
