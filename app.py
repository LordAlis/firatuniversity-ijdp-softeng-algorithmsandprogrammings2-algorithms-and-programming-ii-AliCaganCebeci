"""
Edit Distance (Levenshtein Distance) Visualization
Streamlit Web Application

Author: ALİ ÇAĞAN CEBECİ
Course: Algorithms and Programming II - Semester Capstone Project
University: Fırat University - Software Engineering Department
"""

import streamlit as st
import pandas as pd
import time
from algorithm import edit_distance, get_alignment_path, apply_operations
from utils import (
    create_dp_table_heatmap, 
    create_string_comparison_visual,
    create_complexity_chart,
    format_step_description,
    get_sample_string_pairs,
    calculate_edit_operations_cost
)
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Edit Distance Visualizer",
    page_icon="🔤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🔤 Edit Distance (Levenshtein Distance) Visualizer")
st.markdown("""
**Dynamic Programming Visualization for String Transformation**

This interactive tool demonstrates how the Edit Distance algorithm calculates the minimum number of operations 
(insertions, deletions, substitutions) needed to transform one string into another.

*Developed by ALİ ÇAĞAN CEBECİ for Algorithms and Programming II - Semester Capstone Project*
""")

# Sidebar for input and controls
with st.sidebar:
    st.header("🎛️ Controls")
    
    # String input section
    st.subheader("String Input")
    
    # Sample pairs dropdown
    sample_pairs = get_sample_string_pairs()
    sample_options = [f"{pair[0]} → {pair[1]} ({pair[2]})" for pair in sample_pairs]
    sample_options.insert(0, "Custom input")
    
    selected_sample = st.selectbox("Choose sample or custom:", sample_options)
    
    if selected_sample != "Custom input":
        sample_idx = sample_options.index(selected_sample) - 1
        default_str1 = sample_pairs[sample_idx][0]
        default_str2 = sample_pairs[sample_idx][1]
    else:
        default_str1 = "kitten"
        default_str2 = "sitting"
    
    str1 = st.text_input("String 1 (source):", value=default_str1, max_chars=20)
    str2 = st.text_input("String 2 (target):", value=default_str2, max_chars=20)
    
    # Validation
    if len(str1) > 20 or len(str2) > 20:
        st.warning("⚠️ Please keep strings under 20 characters for optimal visualization")
    
    # Visualization options
    st.subheader("Visualization Options")
    show_steps = st.checkbox("Show step-by-step execution", value=True)
    show_heatmap = st.checkbox("Show DP table heatmap", value=True)
    show_alignment = st.checkbox("Show string alignment", value=True)
    auto_play = st.checkbox("Auto-play steps", value=False)
    
    if auto_play:
        play_speed = st.slider("Auto-play speed (seconds)", 0.5, 3.0, 1.0, 0.5)

# Main content area
if str1 and str2:
    # Calculate edit distance with steps
    edit_dist, dp_table, steps = edit_distance(str1, str2, return_steps=True)
    
    # Basic information
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Edit Distance", edit_dist)
    with col2:
        st.metric("String 1 Length", len(str1))
    with col3:
        st.metric("String 2 Length", len(str2))
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Visualization", "🔍 Step-by-Step", "📈 Analysis", "ℹ️ Algorithm Info"])
    
    with tab1:
        st.subheader("Algorithm Visualization")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if show_heatmap:
                st.subheader("Dynamic Programming Table")
                heatmap_fig = create_dp_table_heatmap(dp_table, str1, str2)
                st.plotly_chart(heatmap_fig, use_container_width=True)
        
        with col2:
            if show_alignment:
                st.subheader("String Comparison")
                operations = get_alignment_path(str1, str2, dp_table)
                comparison_html = create_string_comparison_visual(str1, str2, operations)
                st.markdown(comparison_html, unsafe_allow_html=True)
                
                # Operations breakdown
                st.subheader("Operations Summary")
                costs = calculate_edit_operations_cost(operations)
                
                ops_df = pd.DataFrame([
                    {"Operation": "Matches", "Count": len([op for op in operations if op['operation'] == 'match']), "Cost": 0},
                    {"Operation": "Substitutions", "Count": costs['replace'], "Cost": costs['replace']},
                    {"Operation": "Insertions", "Count": costs['insert'], "Cost": costs['insert']},
                    {"Operation": "Deletions", "Count": costs['delete'], "Cost": costs['delete']},
                    {"Operation": "Total Cost", "Count": "-", "Cost": edit_dist}
                ])
                st.table(ops_df)
    
    with tab2:
        st.subheader("Step-by-Step Execution")
        
        if show_steps and steps:
            # Step navigation
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                step_number = st.number_input("Step", 0, len(steps)-1, 0)
            
            with col2:
                if auto_play:
                    if st.button("▶️ Auto Play"):
                        step_placeholder = st.empty()
                        heatmap_placeholder = st.empty()
                        
                        for i in range(len(steps)):
                            current_step = steps[i]
                            
                            with step_placeholder.container():
                                st.write(f"**Step {i+1}/{len(steps)}**")
                                st.write(format_step_description(current_step))
                            
                            with heatmap_placeholder.container():
                                if current_step['i'] >= 0 and current_step['j'] >= 0:
                                    fig = create_dp_table_heatmap(
                                        current_step['dp_table'], 
                                        str1, str2, 
                                        current_step['i'], 
                                        current_step['j']
                                    )
                                else:
                                    fig = create_dp_table_heatmap(current_step['dp_table'], str1, str2)
                                st.plotly_chart(fig, use_container_width=True)
                            
                            time.sleep(play_speed)
            
            with col3:
                st.write(f"Progress: {step_number+1}/{len(steps)}")
                progress = (step_number + 1) / len(steps)
                st.progress(progress)
            
            # Current step display
            if not auto_play:
                current_step = steps[step_number]
                
                # Step description
                st.write("### Current Step")
                st.write(format_step_description(current_step))
                
                # DP table with current position highlighted
                if current_step['i'] >= 0 and current_step['j'] >= 0:
                    fig = create_dp_table_heatmap(
                        current_step['dp_table'], 
                        str1, str2, 
                        current_step['i'], 
                        current_step['j']
                    )
                else:
                    fig = create_dp_table_heatmap(current_step['dp_table'], str1, str2)
                st.plotly_chart(fig, use_container_width=True)
                
                # Current DP table values
                st.write("### DP Table State")
                df = pd.DataFrame(current_step['dp_table'])
                # Create unique column and row labels to avoid duplicates with repeated characters
                row_labels = ['ε'] + [f"{str1[i]}({i+1})" for i in range(len(str1))]
                col_labels = ['ε'] + [f"{str2[i]}({i+1})" for i in range(len(str2))]
                df.index = row_labels
                df.columns = col_labels
                st.dataframe(df, use_container_width=True)
    
    with tab3:
        st.subheader("Complexity Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Time Complexity")
            st.latex(r"O(m \times n)")
            st.write("Where m and n are the lengths of the two strings.")
            
            st.write("### Space Complexity")
            st.latex(r"O(m \times n)")
            st.write("For storing the DP table.")
            
            st.write("### Current Problem Size")
            st.write(f"- String 1 length (m): {len(str1)}")
            st.write(f"- String 2 length (n): {len(str2)}")
            st.write(f"- Operations performed: {len(str1) * len(str2)}")
        
        with col2:
            st.write("### Complexity Comparison")
            complexity_fig = create_complexity_chart()
            st.plotly_chart(complexity_fig, use_container_width=True)
    
    with tab4:
        st.subheader("Algorithm Information")
        
        st.write("""
        ### What is Edit Distance?
        
        The **Edit Distance** (also known as **Levenshtein Distance**) between two strings is the minimum number of 
        single-character edits (insertions, deletions, or substitutions) required to change one string into another.
        
        ### Algorithm Overview
        
        This implementation uses **Dynamic Programming** to solve the problem efficiently:
        
        1. **Initialization**: Create a (m+1) × (n+1) table where m and n are string lengths
        2. **Base Cases**: Fill first row and column with incremental values
        3. **Recurrence Relation**: For each cell (i,j):
           - If characters match: `dp[i][j] = dp[i-1][j-1]`
           - If different: `dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`
        4. **Result**: The value at `dp[m][n]` is the edit distance
        
        ### Applications
        
        - **Spell Checkers**: Finding similar words
        - **DNA Sequencing**: Comparing genetic sequences  
        - **Plagiarism Detection**: Measuring text similarity
        - **Version Control**: Computing file differences
        - **Natural Language Processing**: Text comparison and analysis
        
        ### Operations
        
        - **Match**: Characters are the same (cost: 0)
        - **Substitution**: Replace one character with another (cost: 1)
        - **Insertion**: Add a character (cost: 1)  
        - **Deletion**: Remove a character (cost: 1)
        """)

else:
    st.info("👆 Please enter two strings in the sidebar to begin the visualization!")

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: gray;'>
    <small>
    Edit Distance Visualizer | ALİ ÇAĞAN CEBECİ | Fırat University Software Engineering<br>
    Algorithms and Programming II - Semester Capstone Project | 2025<br>
    Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </small>
</div>
""", unsafe_allow_html=True)
