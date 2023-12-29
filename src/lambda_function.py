import boto3
from datetime import datetime
import json
import math

# Connect to DynamoDB table
dynamodb = boto3.resource('dynamodb')
power_table = dynamodb.Table('INSERT YOUR DYNAMODB TABLE NAME')

def calculate_power(base, exponent):
    '''
    Calculates the power of base raised to exponent and stores the result in DynamoDB.

    Args:
        base (int): The base value.
        exponent (int): The exponent value.

    Returns:
        tuple: A tuple containing the calculated power result and the DynamoDB response.
    '''
    result = math.pow(int(base), int(exponent))
    current_time = datetime.utcnow().isoformat()
    
    response = power_table.put_item(
        Item={
            'ID': str(result),
            'TimeCreated': current_time
        }
    )
    
    return result, response

def lambda_handler(event, context):
    '''
    Lambda function entry point for calculating power and storing the result.

    Args:
        event (dict): Input event containing 'base' and 'exponent'.
        context: Lambda execution context.

    Returns:
        dict: Response body with statusCode and power calculation result.
    '''
    base = event['base']
    exponent = event['exponent']
    
    evaluation, response = calculate_power(base, exponent)
    
    response_body = {
        'statusCode': 200,
        'body': json.dumps(f"{base} to the power of {exponent} is {evaluation}")
    }
    
    return response_body
