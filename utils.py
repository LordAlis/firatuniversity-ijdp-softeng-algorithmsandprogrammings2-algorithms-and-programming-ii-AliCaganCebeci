"""
Utility functions for Edit Distance visualization
Author: ALİ ÇAĞAN CEBECİ
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


def create_dp_table_heatmap(dp_table, str1, str2, current_i=-1, current_j=-1):
    """
    Create a heatmap visualization of the DP table.
    
    Args:
        dp_table (list): 2D DP table
        str1 (str): First string
        str2 (str): Second string
        current_i (int): Current row being processed (for highlighting)
        current_j (int): Current column being processed (for highlighting)
    
    Returns:
        plotly.graph_objects.Figure: Heatmap figure
    """
    # Create labels for axes
    row_labels = [''] + list(str1)
    col_labels = [''] + list(str2)
    
    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=dp_table,
        x=col_labels,
        y=row_labels,
        colorscale='Blues',
        text=dp_table,
        texttemplate="%{text}",
        textfont={"size": 12},
        hoverongaps=False,
        showscale=True
    ))
    
    # Highlight current cell if specified
    if current_i >= 0 and current_j >= 0:
        fig.add_shape(
            type="rect",
            x0=current_j-0.5, y0=current_i-0.5,
            x1=current_j+0.5, y1=current_i+0.5,
            line=dict(color="red", width=3),
            fillcolor="rgba(255,0,0,0.3)"
        )
    
    fig.update_layout(
        title="Dynamic Programming Table",
        xaxis_title=f"String 2: '{str2}'",
        yaxis_title=f"String 1: '{str1}'",
        width=600,
        height=400
    )
    
    return fig


def create_string_comparison_visual(str1, str2, operations=None, current_step=0):
    """
    Create a visual comparison of two strings showing alignment.
    
    Args:
        str1 (str): First string
        str2 (str): Second string
        operations (list): List of operations from alignment
        current_step (int): Current step in transformation
    
    Returns:
        str: HTML string for display
    """
    html = "<div style='font-family: monospace; font-size: 16px; line-height: 2;'>"
    
    if operations is None:
        # Simple character-by-character comparison
        html += f"<div><b>String 1:</b> {str1}</div>"
        html += f"<div><b>String 2:</b> {str2}</div>"
        
        # Show character differences
        comparison = ""
        max_len = max(len(str1), len(str2))
        for i in range(max_len):
            char1 = str1[i] if i < len(str1) else '_'
            char2 = str2[i] if i < len(str2) else '_'
            
            if char1 == char2:
                comparison += "✓"
            else:
                comparison += "✗"
        
        html += f"<div><b>Match:  </b> {comparison}</div>"
    else:
        # Show operations-based alignment
        aligned_str1 = ""
        aligned_str2 = ""
        operations_shown = operations[:current_step] if current_step > 0 else operations
        
        for i, op in enumerate(operations_shown):
            color = "green" if op['operation'] == 'match' else "red"
            if op['operation'] == 'match':
                aligned_str1 += f"<span style='color: {color}'>{op['char1']}</span>"
                aligned_str2 += f"<span style='color: {color}'>{op['char2']}</span>"
            elif op['operation'] == 'replace':
                aligned_str1 += f"<span style='color: {color}; background-color: yellow'>{op['char1']}</span>"
                aligned_str2 += f"<span style='color: {color}; background-color: yellow'>{op['char2']}</span>"
            elif op['operation'] == 'insert':
                aligned_str1 += "<span style='color: red'>-</span>"
                aligned_str2 += f"<span style='color: red; background-color: lightgreen'>{op['char2']}</span>"
            elif op['operation'] == 'delete':
                aligned_str1 += f"<span style='color: red; background-color: lightcoral'>{op['char1']}</span>"
                aligned_str2 += "<span style='color: red'>-</span>"
        
        html += f"<div><b>String 1:</b> {aligned_str1}</div>"
        html += f"<div><b>String 2:</b> {aligned_str2}</div>"
    
    html += "</div>"
    return html


def create_complexity_chart():
    """
    Create a chart showing time complexity comparison.
    
    Returns:
        plotly.graph_objects.Figure: Complexity comparison chart
    """
    # Sample data for different string lengths
    n_values = [5, 10, 20, 50, 100, 200]
    edit_distance_ops = [n*n for n in n_values]  # O(n²)
    naive_ops = [3**n for n in n_values[:4]] + [float('inf')]*2  # O(3^n) - exponential
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=n_values,
        y=edit_distance_ops,
        mode='lines+markers',
        name='Edit Distance DP: O(n²)',
        line=dict(color='blue')
    ))
    
    fig.add_trace(go.Scatter(
        x=n_values[:4],
        y=naive_ops[:4],
        mode='lines+markers',
        name='Naive Recursive: O(3ⁿ)',
        line=dict(color='red')
    ))
    
    fig.update_layout(
        title="Time Complexity Comparison",
        xaxis_title="String Length (n)",
        yaxis_title="Number of Operations",
        yaxis_type="log",
        width=600,
        height=400
    )
    
    return fig


def format_step_description(step_data):
    """
    Format a step description for display.
    
    Args:
        step_data (dict): Step information
    
    Returns:
        str: Formatted description
    """
    if step_data['step'] == 'initialization':
        return "🔧 **Initialization**: Setting up the DP table with base cases"
    
    i, j = step_data['i'], step_data['j']
    char1 = step_data.get('char1', '')
    char2 = step_data.get('char2', '')
    operation = step_data.get('operation', '')
    
    emoji_map = {
        'match': '✅',
        'replace': '🔄',
        'insert': '➕',
        'delete': '❌'
    }
    
    emoji = emoji_map.get(operation, '🔍')
    
    if operation == 'match':
        return f"{emoji} **Step ({i},{j})**: Characters '{char1}' and '{char2}' match - no cost"
    elif operation == 'replace':
        return f"{emoji} **Step ({i},{j})**: Replace '{char1}' with '{char2}' - cost +1"
    elif operation == 'insert':
        return f"{emoji} **Step ({i},{j})**: Insert '{char2}' - cost +1"
    elif operation == 'delete':
        return f"{emoji} **Step ({i},{j})**: Delete '{char1}' - cost +1"
    
    return f"🔍 **Step ({i},{j})**: Processing..."


def get_sample_string_pairs():
    """
    Get sample string pairs for testing.
    
    Returns:
        list: List of (str1, str2, description) tuples
    """
    return [
        ("kitten", "sitting", "Classic example"),
        ("saturday", "sunday", "Day names"),
        ("algorithm", "altruistic", "Programming terms"),
        ("hello", "hallo", "Simple substitution"),
        ("abc", "def", "Complete replacement"),
        ("", "hello", "Empty to string"),
        ("world", "", "String to empty"),
        ("same", "same", "Identical strings"),
        ("a", "abc", "Single to multiple"),
        ("abcdef", "ace", "Deletions only")
    ]


def calculate_edit_operations_cost(operations):
    """
    Calculate the cost breakdown of operations.
    
    Args:
        operations (list): List of operations
    
    Returns:
        dict: Cost breakdown
    """
    costs = {
        'match': 0,
        'replace': 0,
        'insert': 0,
        'delete': 0
    }
    
    for op in operations:
        operation = op['operation']
        if operation in costs:
            if operation == 'match':
                costs[operation] += 0
            else:
                costs[operation] += 1
    
    return costs
