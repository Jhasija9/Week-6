
import logging
import os
import yaml
import subprocess
import pandas as pd
import datetime
import gc
import re


#reading the file

def read_file(filepath):
    with open(filepath,'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)
            
# replacing the character

def replace(string, char):
    pattern=char + '{2,}'
    string= re.sub(pattern,char,string)
    return string


# standardizes columns and validates dataframe YAML against validation YAML

def col_header_valid(df, table_config):
    df.columns=df.columns.str.lower()
    df.columns = df.columns.str.replace('[^\w]', '_', regex=True)
    df.columns= list(map(lambda x: x.strip('_'), list(df.columns)))
    df.columns= list(map(lambda x: replace(x, '_'), list(df.columns)))
    expected_col= list(map(lambda x:x.lower(),table_config['columns']))
    expected_col.sort()
    df.columns = list(map(lambda x: x.lower(), list(df.columns)))
    
    if len(expected_col)==len(df.columns) and list(expected_col)==list(df.columns):
        print("Column name and column length validation passed.")
        return 1
    else:
        print("Column name and column length validation failed.")
        mismatched_columns_file=list(set(df.columns).difference(expected_col))
        print("Following file columns are not in the YAML file",mismatched_columns_file)
        missing_YAML_file = list(set(expected_col).difference(df.columns))
        print("Following YAML columns are not in the file uploaded",missing_YAML_file)
        logging.info(f'df columns: {df.columns}')
        logging.info(f'expected columns: {expected_col}')
        return 0
