#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Geography Crosswalks Module

This module contains geographic data structures, crosswalks, and utilities
for the timber assets analysis. It handles state/county mappings, FIPS codes,
and other geographic reference data.
"""

import pandas as pd
import os
from pathlib import Path
from src.config import STATE_FIPS # Import STATE_FIPS from config

# Path constants - kept here to avoid circular imports
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
INPUT_DIR = DATA_DIR / 'input'
CROSSWALKS_DIR = DATA_DIR / 'crosswalks'
PROCESSED_DIR = DATA_DIR / 'processed'
REPORTS_DIR = DATA_DIR / 'reports'

# Region definitions
SOUTH_STATES = ['AL', 'AR', 'FL', 'GA', 'LA', 'MS', 'NC', 'SC', 'TN', 'TX', 'VA']
GREAT_LAKES_STATES = ['MI', 'MN', 'WI']

def format_unit_code(df, unit_col='unitcd'):
    """Format unit codes with leading zeros.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing unit codes
    unit_col : str
        Column name containing unit codes
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with properly formatted unit codes
    """
    df_copy = df.copy()
    
    if unit_col in df_copy.columns:
        df_copy[unit_col] = df_copy[unit_col].fillna(0).astype(int)
        df_copy[unit_col] = df_copy[unit_col].astype(str).str.zfill(2)
        
    return df_copy

def get_state_abbr_from_fips(fips_code):
    """Get state abbreviation from FIPS code.
    
    Parameters:
    -----------
    fips_code : str
        FIPS code (first 2 digits are state code)
        
    Returns:
    --------
    str
        State abbreviation
    """
    state_code = str(fips_code)[:2]
    return {v: k for k, v in STATE_FIPS.items()}.get(state_code)

def load_georef():
    """Load geographic reference data"""
    return pd.read_csv(CROSSWALKS_DIR / 'georef.csv')

def load_crosswalk_micromarket_county():
    """Load micromarket to county mapping"""
    return pd.read_csv(CROSSWALKS_DIR / 'crosswalk_micromarket_county.csv')

def get_price_regions(region=None):
    """
    Get price regions data directly instead of loading from CSV.
    
    Parameters:
    -----------
    region : str, optional
        Filter for specific region ('south' or 'gl'), if None returns all
        
    Returns:
    --------
    pandas.DataFrame
        Price regions data
    """
    # Define price regions data directly
    data = {
        'statecd': [],
        'countycd': [],
        'unitcd': [],
        'priceRegion': []
    }
    
    # South region price regions
    for state in SOUTH_STATES:
        state_fips = STATE_FIPS[state]
        # Add some example price regions for each state
        # In a real implementation, this would have more detailed data
        for i in range(1, 4):
            data['statecd'].append(state_fips)
            data['countycd'].append(f"{i:03d}")
            data['unitcd'].append(f"{i:02d}")
            data['priceRegion'].append(f"{i:02d}")
    
    # Great Lakes region price regions
    for state in GREAT_LAKES_STATES:
        state_fips = STATE_FIPS[state]
        # Add some example price regions for each state
        for i in range(1, 4):
            data['statecd'].append(state_fips)
            data['countycd'].append(f"{i:03d}")
            data['unitcd'].append(f"{i:02d}")
            data['priceRegion'].append(f"{i:02d}")
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Filter by region if specified
    if region == 'south':
        south_state_fips = [STATE_FIPS[state] for state in SOUTH_STATES]
        df = df[df['statecd'].isin(south_state_fips)]
    elif region == 'gl':
        gl_state_fips = [STATE_FIPS[state] for state in GREAT_LAKES_STATES]
        df = df[df['statecd'].isin(gl_state_fips)]
    
    return df

def load_crosswalk_price_regions():
    """Load price region mappings (backward compatibility)"""
    print("Warning: Using in-memory price regions instead of loading from file")
    return get_price_regions()

def load_crosswalk_tms_counties():
    """Load TMS counties mapping"""
    return pd.read_csv(CROSSWALKS_DIR / 'crosswalk_tmsCounties.csv') 