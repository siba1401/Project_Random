import streamlit as st
import pandas as pd
import random
from io import BytesIO


def split_into_parts(total, max_limits):
    while True:
        parts = []
        remaining = total
        for max_val in max_limits[:-1]:
            part = random.randint(0, min(max_val, remaining))
            parts.append(part)
            remaining -= part
        last_part = remaining
        if 0 <= last_part <= max_limits[-1]:
            parts.append(last_part)
            return parts


def generate_parts_dataframe(file, num_rows, max_limits):
    df1 = pd.read_csv(file)
    totals = df1['Grades'].head(num_rows)

    data = [split_into_parts(t, max_limits) for t in totals]

    part_columns = [f"Part{i + 1}" for i in range(len(max_limits))]
    df = pd.DataFrame(data, columns=part_columns)
    df["Total"] = totals.reset_index(drop=True)
    df["Check"] = df[part_columns].sum(axis=1)

    return df


def main():
    st.title("Grades Splitter App 🎯")

    uploaded_file = st.file_uploader("Upload your grades1.csv file", type="csv")

    if uploaded_file:
        num_rows = st.number_input("Enter number of rows to process", min_value=1, step=1)
        max_limits_input = st.text_input("Enter max limits separated by commas (e.g., 3,3,4)")

        if max_limits_input:
            max_limits = [int(x.strip()) for x in max_limits_input.split(",")]

            if st.button("Generate Splits"):
                df_result = generate_parts_dataframe(uploaded_file, num_rows, max_limits)

                st.dataframe(df_result)

                # Prepare for download
                csv = df_result.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name='grd1.csv',
                    mime='text/csv'
                )


if __name__ == "__main__":
    main()
