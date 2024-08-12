import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set a custom theme for the app
st.set_page_config(
    page_title="SIMPLE DATA EXPLORATION TOOL",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for dark theme and improved design
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: #E1E1E1;
        }
        .sidebar .sidebar-content {
            background: #333333;
        }
        .css-18e3th9 {
            background-color: #333333;
        }
        .css-1d391kg p {
            color: #E1E1E1;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
        }
        .stSlider .st-bg {
            background-color: #4CAF50;
        }
        .stSelectbox, .stTextInput {
            color: #E1E1E1;
        }
        .stDataFrame {
            border: 1px solid #4CAF50;
        }
        .stColorPicker input {
            background-color: #333333;
        }
    </style>
""", unsafe_allow_html=True)

# Title of the app
st.title("📊 Professional Data Analysis and Visualization Tool")

# File uploader to accept CSV files
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
        
        # Display the shape of the dataset
        st.subheader("Dataset Shape")
        st.write(f"The dataset has {df.shape[0]} rows and {df.shape[1]} columns.")
        
        # Display the data types of the columns
        st.subheader("Data Types")
        st.write(df.dtypes)
        
    except Exception as e:
        st.error(f"Error loading file: {e}")
        df = None  # Ensure df is None if the file loading fails
    if df is not None:
        # Add Reset Button
        if st.button("Reset Dataset"):
            df = pd.read_csv(uploaded_file)
            st.info("Dataset has been reset.")

        st.subheader("Data Preview")
        st.write(df.head())

        st.subheader("Data Description")
        st.write(df.describe())
        
        st.subheader("Select Columns to Display")
        columns_to_display = st.multiselect("Choose columns", df.columns.tolist(), default=df.columns.tolist())
        st.write(df[columns_to_display].head())

        st.subheader("Sort Data")
        sort_column = st.selectbox("Select column to sort by", df.columns.tolist())
        sort_order = st.radio("Sort order", ["Ascending", "Descending"])
        df = df.sort_values(by=sort_column, ascending=(sort_order == "Ascending"))
        st.write(df.head())

        st.subheader("Rename Columns")
        column_to_rename = st.selectbox("Select column to rename", df.columns.tolist())
        new_column_name = st.text_input("Enter new column name")
        if st.button("Rename Column"):
            df.rename(columns={column_to_rename: new_column_name}, inplace=True)
            st.success(f"Column '{column_to_rename}' renamed to '{new_column_name}'.")
            st.write(df.head())

        st.subheader("Sample Data")
        sample_size = st.slider("Select number of rows to sample", min_value=1, max_value=len(df), value=5)
        st.write(df.sample(sample_size))

        st.subheader("Handle Missing Data")
        missing_option = st.selectbox("Select how to handle missing data", 
                                     ["None", "Drop missing values", 
                                      "Fill missing values with specific value", 
                                      "Fill missing values with mean/median/mode"])
        
        if missing_option == "Drop missing values":
            df = df.dropna()
            st.success("Missing values dropped.")
        elif missing_option == "Fill missing values with specific value":
            fill_value = st.text_input("Enter value to fill missing data")
            try:
                df = df.fillna(float(fill_value))
                st.success(f"Missing values filled with '{fill_value}'.")
            except ValueError:
                st.error("Please enter a valid numeric value.")
        elif missing_option == "Fill missing values with mean/median/mode":
            fill_strategy = st.selectbox("Choose strategy", ["Mean", "Median", "Mode"])
            try:
                if df.select_dtypes(include='number').empty:
                    st.error("Dataframe contains no numeric columns.")
                else:
                    if fill_strategy == "Mean":
                        df = df.fillna(df.mean())
                    elif fill_strategy == "Median":
                        df = df.fillna(df.median())
                    elif fill_strategy == "Mode":
                        df = df.fillna(df.mode().iloc[0])
                    st.success(f"Missing values filled with '{fill_strategy}' strategy.")
            except Exception as e:
                st.error(f"Error filling missing values: {e}")
else:
    st.warning("Please upload a CSV file to proceed.")























































        # st.subheader("Advanced Filter Data")
        # columns = df.columns.tolist()
        # selected_column_1 = st.selectbox("Select first column to filter by", columns)
        # selected_value_1 = st.text_input(f"Enter value for {selected_column_1}")
        # selected_column_2 = st.selectbox("Select second column to filter by", columns)
        # selected_value_2 = st.text_input(f"Enter value for {selected_column_2}")
        
        # try:
        #     if selected_value_1 and selected_value_1 not in df[selected_column_1].unique():
        #         raise ValueError(f"Value '{selected_value_1}' not found in column '{selected_column_1}'.")
        #     if selected_value_2 and selected_value_2 not in df[selected_column_2].unique():
        #         raise ValueError(f"Value '{selected_value_2}' not found in column '{selected_column_2}'.")

        #     if selected_value_1 and selected_value_2:
        #         filtered_df = df[(df[selected_column_1] == selected_value_1) & (df[selected_column_2] == selected_value_2)]
        #         st.write(filtered_df)
        #     else:
        #         st.error("Please provide valid values for both filters.")
        # except ValueError as ve:
        #     st.error(ve)
        # except KeyError:
        #     st.error("Selected column or value not found in the dataset.")
        # except Exception as e:
        #     st.error(f"An unexpected error occurred: {e}")

        # st.subheader("Export Filtered Data")
        # if st.button("Download Filtered Data as CSV"):
        #     try:
        #         filtered_df.to_csv("filtered_data.csv", index=False)
        #         st.success("Filtered data downloaded.")
        #     except Exception as e:
        #         st.error(f"Error exporting data: {e}")

        # st.subheader("Plot Data")
        # x_column = st.selectbox("Select x-axis column", columns)
        # y_column = st.selectbox("Select y-axis column", columns)
        
        # plot_type = st.selectbox("Select Plot Type", 
        #                          ["Line Plot", "Bar Plot", "Scatter Plot", 
        #                           "Histogram", "Box Plot", "Pie Chart", 
        #                           "Heatmap", "Area Plot", "Violin Plot", 
        #                           "Pair Plot", "Hexbin Plot", "KDE Plot"])
        
        # color_option = st.color_picker("Pick a color for the plot", "#4CAF50")
        # line_style = st.selectbox("Select line style (for line plot)", ["-", "--", "-.", ":"], index=0)
        # grid_option = st.checkbox("Show grid lines", value=True)
        # legend_option = st.checkbox("Show legend", value=True)

        # if st.button("Generate plot"):
        #     try:
        #         fig, ax = plt.subplots(figsize=(10, 6))
                
        #         if plot_type == "Line Plot":
        #             ax.plot(df[x_column], df[y_column], marker='o', linestyle=line_style, color=color_option)
        #             ax.set_title(f'{y_column} vs {x_column} (Line Plot)')
        #         elif plot_type == "Bar Plot":
        #             ax.bar(df[x_column], df[y_column], color=color_option)
        #             ax.set_title(f'{y_column} vs {x_column} (Bar Plot)')
        #         elif plot_type == "Scatter Plot":
        #             ax.scatter(df[x_column], df[y_column], color=color_option)
        #             ax.set_title(f'{y_column} vs {x_column} (Scatter Plot)')
        #         elif plot_type == "Histogram":
        #             ax.hist(df[x_column], bins=20, color=color_option)
        #             ax.set_title(f'{x_column} Distribution (Histogram)')
        #             ax.set_xlabel(x_column)
        #             ax.set_ylabel("Frequency")
        #         elif plot_type == "Box Plot":
        #             sns.boxplot(x=df[x_column], y=df[y_column], ax=ax, color=color_option)
        #             ax.set_title(f'{y_column} Distribution by {x_column} (Box Plot)')
        #         elif plot_type == "Pie Chart":
        #             pie_data = df[y_column].value_counts()
        #             ax.pie(pie_data, labels=pie_data.index, colors=sns.color_palette("pastel"), autopct='%1.1f%%')
        #             ax.set_title(f'{y_column} Distribution (Pie Chart)')
        #         elif plot_type == "Heatmap":
        #             sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)
        #             ax.set_title(f'{x_column} Correlation Heatmap')
        #         elif plot_type == "Area Plot":
        #             ax.fill_between(df[x_column], df[y_column], color=color_option, alpha=0)
        #             st.pyplot()
        #             st.success("Pair plot generated.")
        #         else:
        #             if grid_option:
        #                 ax.grid(True)

        #             if legend_option and plot_type != "Pair Plot":
        #                 ax.legend()

        #             st.pyplot(fig)
        #             st.success("Plot generated successfully!")
    
                
        #         if grid_option:
        #             ax.grid(True)
                
        #         if legend_option and plot_type != "Pair Plot":
        #             ax.legend()

        #         st.pyplot(fig)
        #         st.success("Plot generated successfully!")
        #     except Exception as e:  
        #         st.error(f"Error generating plot: {e}")
# else:
#     st.warning("Please upload a CSV file to proceed.")
