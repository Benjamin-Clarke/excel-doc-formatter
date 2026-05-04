import streamlit as st
import pandas as pd

st.title("Access Event Dashboard")

uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=["xlsx", "csv"], key="uploaded_file")

if uploaded_file is None:
    st.write("Please upload an Excel or CSV file to continue")
else:
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension == 'xlsx':
        try:
            df = pd.read_excel(uploaded_file)
            df.columns = df.columns.str.lower().str.strip()
            st.session_state['dataframe'] = df
            st.write("Cleaned column names:", list(df.columns))
            st.write(f"File uploaded successfully. Number of rows loaded: {len(df)}")
            st.subheader("Dashboard")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Events", len(df))
            with col2:
                if 'device' in df.columns:
                    st.metric("Unique Devices", df['device'].nunique())
                else:
                    st.warning("Device column not found")
            with col3:
                if 'panel' in df.columns:
                    st.metric("Unique Panels", df['panel'].nunique())
                else:
                    st.warning("Panel column not found")

            st.subheader("Line Fault Events")
            keywords = ["line error", "open line", "grounded loop", "tamper"]
            pattern = "|".join(keywords)
            mask = pd.Series(False, index=df.index)
            if 'event' in df.columns:
                mask = mask | df['event'].astype(str).str.contains(pattern, case=False, na=False)
            if 'details' in df.columns:
                mask = mask | df['details'].astype(str).str.contains(pattern, case=False, na=False)
            line_faults = df[mask].copy()
            st.write(f"Total line fault events: {len(line_faults)}")
            if 'device' in line_faults.columns:
                device_summary = (
                    line_faults.groupby('device')
                    .size()
                    .reset_index(name='line_fault_count')
                    .sort_values('line_fault_count', ascending=False)
                    .head(20)
                )
                st.subheader("Top 20 Devices with Line Fault Events")
                st.dataframe(device_summary)
            else:
                st.warning("Device column not found for line fault summary")
            st.dataframe(line_faults)

            if 'event' in df.columns:
                event_options = df['event'].dropna().unique().tolist()
                selected_events = st.sidebar.multiselect(
                    "Filter by event type",
                    options=event_options,
                    default=event_options,
                )
                if selected_events:
                    filtered_df = df[df['event'].isin(selected_events)]
                else:
                    filtered_df = df.copy()
                st.write(f"Filtered rows: {len(filtered_df)}")
                st.dataframe(filtered_df)
            else:
                st.dataframe(df.head(5))

            if st.button("Reset / Upload New File"):
                st.session_state.pop('dataframe', None)
                st.session_state.pop('uploaded_file', None)
                st.rerun()
        except Exception as e:
            st.error(f"Error reading the Excel file: {str(e)}")
    elif file_extension == 'csv':
        try:
            df = pd.read_csv(uploaded_file)
            df.columns = df.columns.str.lower().str.strip()
            st.session_state['dataframe'] = df
            st.write("Cleaned column names:", list(df.columns))
            st.write(f"File uploaded successfully. Number of rows loaded: {len(df)}")
            st.subheader("Dashboard")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Events", len(df))
            with col2:
                if 'device' in df.columns:
                    st.metric("Unique Devices", df['device'].nunique())
                else:
                    st.warning("Device column not found")
            with col3:
                if 'panel' in df.columns:
                    st.metric("Unique Panels", df['panel'].nunique())
                else:
                    st.warning("Panel column not found")

            st.subheader("Line Fault Events")
            keywords = ["line error", "open line", "grounded loop", "tamper"]
            pattern = "|".join(keywords)
            mask = pd.Series(False, index=df.index)
            if 'event' in df.columns:
                mask = mask | df['event'].astype(str).str.contains(pattern, case=False, na=False)
            if 'details' in df.columns:
                mask = mask | df['details'].astype(str).str.contains(pattern, case=False, na=False)
            line_faults = df[mask].copy()
            st.write(f"Total line fault events: {len(line_faults)}")
            if 'device' in line_faults.columns:
                device_summary = (
                    line_faults.groupby('device')
                    .size()
                    .reset_index(name='line_fault_count')
                    .sort_values('line_fault_count', ascending=False)
                    .head(20)
                )
                st.subheader("Top 20 Devices with Line Fault Events")
                st.dataframe(device_summary)
            else:
                st.warning("Device column not found for line fault summary")
            st.dataframe(line_faults)

            if 'event' in df.columns:
                event_options = df['event'].dropna().unique().tolist()
                selected_events = st.sidebar.multiselect(
                    "Filter by event type",
                    options=event_options,
                    default=event_options,
                )
                if selected_events:
                    filtered_df = df[df['event'].isin(selected_events)]
                else:
                    filtered_df = df.copy()
                st.write(f"Filtered rows: {len(filtered_df)}")
                st.dataframe(filtered_df)
            else:
                st.dataframe(df.head(5))

            if st.button("Reset / Upload New File"):
                st.session_state.pop('dataframe', None)
                st.session_state.pop('uploaded_file', None)
                st.rerun()
        except Exception as e:
            st.error(f"Error reading the CSV file: {str(e)}")
    else:
        st.error("Unsupported file type. Please upload a .xlsx or .csv file.")