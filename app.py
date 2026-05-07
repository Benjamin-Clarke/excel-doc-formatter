import streamlit as st
import pandas as pd

st.title("Access Event Dashboard")

uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=["xlsx", "csv"], key="uploaded_file")
search_query = st.sidebar.text_input("Search")
st.write(f"Current search text: {search_query}")

if uploaded_file is None:
    st.write("Please upload an Excel or CSV file to continue")
else:
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension == 'xlsx':
        try:
            df = pd.read_excel(uploaded_file)
            df.columns = df.columns.str.lower().str.strip()
            st.session_state['dataframe'] = df

            search_cols = [col for col in ['device', 'panel', 'details'] if col in df.columns]
            if search_query and search_cols:
                search_mask = pd.Series(False, index=df.index)
                for col in search_cols:
                    search_mask = search_mask | df[col].astype(str).str.contains(search_query, case=False, na=False)
                display_df = df[search_mask].copy()
            else:
                display_df = df.copy()
                if search_query and not search_cols:
                    st.warning("No searchable columns found (device, panel, details). Search is not applied.")

            st.write("Cleaned column names:", list(df.columns))
            st.write(f"File uploaded successfully. Number of rows loaded: {len(df)}")
            st.divider()
            st.subheader("📊 Dashboard")
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

            st.divider()
            st.subheader("📊 Line Fault Events Analysis")
            keywords = ["line error", "open line", "grounded loop", "tamper"]
            pattern = "|".join(keywords)
            mask = pd.Series(False, index=df.index)
            if 'event' in df.columns:
                mask = mask | df['event'].astype(str).str.contains(pattern, case=False, na=False)
            if 'details' in df.columns:
                mask = mask | df['details'].astype(str).str.contains(pattern, case=False, na=False)
            line_faults = df[mask].copy()
            st.write(f"**Total line fault events: {len(line_faults)}**")
            if 'device' in line_faults.columns:
                device_summary = (
                    line_faults.groupby('device')
                    .size()
                    .reset_index(name='line_fault_count')
                    .sort_values('line_fault_count', ascending=False)
                    .head(20)
                )
                st.markdown("##### Top 20 Devices with Line Fault Events")
                st.dataframe(device_summary, use_container_width=True)
            else:
                st.warning("Device column not found for line fault summary")
            st.markdown("##### All Line Fault Events")
            st.dataframe(line_faults, use_container_width=True)

            st.divider()
            st.subheader("🔍 Search & Event Filtering")
            if search_query:
                st.info(f"**Search Query:** `{search_query}` | **Results:** {len(display_df)} rows")
            else:
                st.write(f"Showing all {len(display_df)} rows")
            if 'event' in df.columns:
                event_options = display_df['event'].dropna().unique().tolist()
                selected_events = st.sidebar.multiselect(
                    "Filter by event type",
                    options=event_options,
                    default=event_options,
                )
                if selected_events:
                    filtered_df = display_df[display_df['event'].isin(selected_events)]
                else:
                    filtered_df = display_df.copy()
                st.markdown(f"##### Filtered Results: {len(filtered_df)} rows")
                st.dataframe(filtered_df, use_container_width=True)
            else:
                st.markdown(f"##### Data Preview: {len(display_df)} rows")
                st.dataframe(display_df.head(5), use_container_width=True)

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

            search_cols = [col for col in ['device', 'panel', 'details'] if col in df.columns]
            if search_query and search_cols:
                search_mask = pd.Series(False, index=df.index)
                for col in search_cols:
                    search_mask = search_mask | df[col].astype(str).str.contains(search_query, case=False, na=False)
                display_df = df[search_mask].copy()
            else:
                display_df = df.copy()
                if search_query and not search_cols:
                    st.warning("No searchable columns found (device, panel, details). Search is not applied.")

            st.write("Cleaned column names:", list(df.columns))
            st.write(f"File uploaded successfully. Number of rows loaded: {len(df)}")
            st.divider()
            st.subheader("📊 Dashboard")
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

            st.divider()
            st.subheader("📊 Line Fault Events Analysis")
            keywords = ["line error", "open line", "grounded loop", "tamper"]
            pattern = "|".join(keywords)
            mask = pd.Series(False, index=df.index)
            if 'event' in df.columns:
                mask = mask | df['event'].astype(str).str.contains(pattern, case=False, na=False)
            if 'details' in df.columns:
                mask = mask | df['details'].astype(str).str.contains(pattern, case=False, na=False)
            line_faults = df[mask].copy()
            st.write(f"**Total line fault events: {len(line_faults)}**")
            if 'device' in line_faults.columns:
                device_summary = (
                    line_faults.groupby('device')
                    .size()
                    .reset_index(name='line_fault_count')
                    .sort_values('line_fault_count', ascending=False)
                    .head(20)
                )
                st.markdown("##### Top 20 Devices with Line Fault Events")
                st.dataframe(device_summary, use_container_width=True)
            else:
                st.warning("Device column not found for line fault summary")
            st.markdown("##### All Line Fault Events")
            st.dataframe(line_faults, use_container_width=True)

            st.divider()
            st.subheader("🔍 Search & Event Filtering")
            if search_query:
                st.info(f"**Search Query:** `{search_query}` | **Results:** {len(display_df)} rows")
            else:
                st.write(f"Showing all {len(display_df)} rows")
            if 'event' in df.columns:
                event_options = display_df['event'].dropna().unique().tolist()
                selected_events = st.sidebar.multiselect(
                    "Filter by event type",
                    options=event_options,
                    default=event_options,
                )
                if selected_events:
                    filtered_df = display_df[display_df['event'].isin(selected_events)]
                else:
                    filtered_df = display_df.copy()
                st.markdown(f"##### Filtered Results: {len(filtered_df)} rows")
                st.dataframe(filtered_df, use_container_width=True)
            else:
                st.markdown(f"##### Data Preview: {len(display_df)} rows")
                st.dataframe(display_df.head(5), use_container_width=True)

            if st.button("Reset / Upload New File"):
                st.session_state.pop('dataframe', None)
                st.session_state.pop('uploaded_file', None)
                st.rerun()
        except Exception as e:
            st.error(f"Error reading the CSV file: {str(e)}")
    else:
        st.error("Unsupported file type. Please upload a .xlsx or .csv file.")