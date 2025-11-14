import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime
import warnings
import streamlit.components.v1 as components

# Suppress warnings
warnings.filterwarnings('ignore')

# Import the timetable generation logic
try:
    from ttv5 import TimetableCSPv2, read_input_v2, export_to_template
except ImportError as e:
    st.error(f"Error importing ttv5 module: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Timetable Generator",
    page_icon="📅",
    layout="wide"
)

# Initialize session state
if 'generated_file' not in st.session_state:
    st.session_state.generated_file = None
if 'unscheduled_df' not in st.session_state:
    st.session_state.unscheduled_df = None
if 'generation_log' not in st.session_state:
    st.session_state.generation_log = []

# Title
st.title("📅 Timetable Generator")
st.markdown("---")

# Instructions
st.markdown("""
### 📋 Instructions:
1. **Upload** your input Excel file (`InputData_v2.xlsx`)
2. **Click** Generate Timetable button
3. **Download** the result or **View** in interactive calendar
""")

st.markdown("---")

# File upload section
st.subheader("📁 Upload Input File")
input_file = st.file_uploader(
    "Upload Input Data Excel File",
    type=['xlsx'],
    help="Upload the Excel file containing WINDOW, TIMESLOTS, REQUIREMENTS, DAYS sheets"
)

st.markdown("---")

# Generate button
if st.button("🚀 Generate Timetable", type="primary", use_container_width=True):
    if input_file is None:
        st.error("⚠️ Please upload the input file first!")
    else:
        # Check if template file exists
        template_path = os.path.join(os.getcwd(), "TimeTableImport_SIS.xlsx")
        if not os.path.exists(template_path):
            st.error(f"⚠️ Template file not found: {template_path}")
            st.info("Please ensure TimeTableImport_SIS.xlsx is in the same folder as app.py")
            st.stop()
        
        # Save uploaded file temporarily with unique name
        import tempfile
        temp_fd, input_path = tempfile.mkstemp(suffix='.xlsx', prefix='temp_input_')
        try:
            with os.fdopen(temp_fd, 'wb') as f:
                f.write(input_file.getvalue())
        except Exception:
            os.close(temp_fd)
            raise
        
        # Progress container
        progress_container = st.container()
        with progress_container:
            st.info("🔄 Starting timetable generation...")
            log_placeholder = st.empty()
            
            # Capture generation logs
            import sys
            from io import StringIO
            
            # Redirect stdout to capture logs
            old_stdout = sys.stdout
            sys.stdout = log_buffer = StringIO()
            
            try:
                # Read input data
                log_placeholder.text("📖 Reading input data...")
                input_data = read_input_v2(input_path)
                
                # Initialize CSP solver
                log_placeholder.text("⚙️ Initializing solver...")
                csp = TimetableCSPv2(
                    timeslots=input_data["timeslots"],
                    requirements=input_data["requirements"],
                    days=input_data["days"],
                    teacher_availability=input_data["teacher_availability"],
                    allow_partial=True,
                    debug=True
                )
                
                # Solve
                log_placeholder.text("🔍 Solving constraints... This may take a few minutes...")
                success = csp.solve(seed=123)
                
                # Get logs
                sys.stdout = old_stdout
                generation_logs = log_buffer.getvalue()
                st.session_state.generation_log = generation_logs.split('\n')
                
                if success or csp.allow_partial:
                    log_placeholder.text("✅ Generation complete! Exporting results...")
                    
                    # Export to Excel (save to temp file first)
                    import tempfile
                    temp_output_fd, temp_output_path = tempfile.mkstemp(suffix='.xlsx', prefix='output_')
                    os.close(temp_output_fd)  # Close file descriptor, we'll write with openpyxl
                    
                    try:
                        export_to_template(
                            assignments=csp.assignment,
                            engine=csp,
                            start_date=input_data["start_date"],
                            end_date=input_data["end_date"],
                            output_xlsx=temp_output_path,
                            template_xlsx=template_path,
                            skipped_requirements=csp.skipped_requirements
                        )
                        
                        # Read the generated file into memory
                        with open(temp_output_path, 'rb') as f:
                            st.session_state.generated_file = f.read()
                        
                        # Clean up temp output file
                        try:
                            os.remove(temp_output_path)
                        except:
                            pass
                    except Exception as export_error:
                        try:
                            os.remove(temp_output_path)
                        except:
                            pass
                        raise export_error
                    
                    # Store unscheduled requirements
                    if csp.skipped_requirements:
                        unscheduled_data = []
                        for req, reason in csp.skipped_requirements:
                            unscheduled_data.append({
                                'Course': req.course_code,
                                'Section': req.section_id,
                                'Teacher': req.teacher,
                                'Hours Required': req.min_total_hours,
                                'Reason': reason
                            })
                        st.session_state.unscheduled_df = pd.DataFrame(unscheduled_data)
                    else:
                        st.session_state.unscheduled_df = None
                    
                    log_placeholder.empty()
                    st.success("✅ Timetable generated successfully!")
                    st.rerun()
                else:
                    sys.stdout = old_stdout
                    st.error("❌ Failed to generate timetable. Check the logs below.")
                    
            except Exception as e:
                sys.stdout = old_stdout
                st.error(f"❌ Error during generation: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
            finally:
                # Cleanup - try to remove temp file, but don't fail if locked
                try:
                    if os.path.exists(input_path):
                        os.remove(input_path)
                except PermissionError:
                    # File is locked, will be cleaned up later
                    pass
                except Exception:
                    # Ignore other cleanup errors
                    pass

# Display results if generated
if st.session_state.generated_file is not None:
    st.markdown("---")
    st.subheader("📥 Download Results")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.download_button(
            label="📥 Download Generated Timetable",
            data=st.session_state.generated_file,
            file_name=f"GeneratedTimetable_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        if st.session_state.unscheduled_df is not None and not st.session_state.unscheduled_df.empty:
            st.warning(f"⚠️ {len(st.session_state.unscheduled_df)} requirements could not be scheduled")
    
    # Calendar View
    st.markdown("---")
    st.subheader("📅 Interactive Calendar View")

    st.markdown("Upload a timetable Excel file (e.g. a downloaded result) to preview it below. If you don't upload a file, the most recently generated timetable is shown automatically.")
    calendar_file = st.file_uploader(
        "Upload timetable Excel (.xlsx) to view",
        type=["xlsx"],
        key="calendar_view_uploader"
    )

    try:
        # Determine data source for calendar view
        if calendar_file is not None:
            calendar_bytes = calendar_file.getvalue()
            source_label = "uploaded file"
        else:
            calendar_bytes = st.session_state.generated_file
            source_label = "latest generated timetable"

        if not calendar_bytes:
            st.info("No timetable data available yet. Please upload an Excel file or generate a timetable first.")
            calendar_bytes = None

        if calendar_bytes is None:
            raise ValueError("No timetable bytes available")

        # Read the chosen timetable file
        excel_data = io.BytesIO(calendar_bytes)
        df_timetable = pd.read_excel(excel_data, sheet_name='TimeTable')

        st.caption(f"Showing calendar for {source_label}.")
        
        # Convert timetable to events format for calendar
        events = []
        for _, row in df_timetable.iterrows():
            curriculum = str(row.get('CURRICULUM', ''))
            course = str(row.get('COURSE', ''))
            semester = str(row.get('SEMESTER', ''))
            section = str(row.get('SECTION', ''))
            teacher = str(row.get('TEACHER', ''))
            
            # Process each day (DAY1 to DAY5)
            for day_num in range(1, 6):
                day_col = f'DAY{day_num}'
                time_from_col = f'DAY{day_num}_TIME_FROM'
                time_to_col = f'DAY{day_num}_TIME_TO'
                room_col = f'DAY{day_num}_ROOM'
                
                if day_col in df_timetable.columns and pd.notna(row.get(day_col)):
                    day = str(row.get(day_col, ''))
                    time_from = str(row.get(time_from_col, ''))
                    time_to = str(row.get(time_to_col, ''))
                    room = str(row.get(room_col, ''))
                    
                    if day and time_from and time_to:
                        events.append({
                            'curriculum': curriculum,
                            'semester': semester,
                            'section': section,
                            'course': course,
                            'teacher': teacher,
                            'room': room,
                            'day': day,
                            'timeFrom': time_from,
                            'timeTo': time_to
                        })
        
        # Read the HTML template
        html_template_path = os.path.join(os.getcwd(), "timetable_calendar_view_light_v6.html")
        
        if os.path.exists(html_template_path):
            with open(html_template_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Inject the events data into the HTML
            import json
            events_json = json.dumps(events)
            
            # Find where to inject the data (after the file input logic)
            # We'll add a script that auto-loads the data
            injection_script = f"""
            <script>
            // Auto-load generated timetable data
            window.generatedEvents = {events_json};
            
            // Wait for page to load, then inject data
            window.addEventListener('DOMContentLoaded', function() {{
                if (window.generatedEvents && window.generatedEvents.length > 0) {{
                    // Simulate the data being loaded
                    if (typeof window.handleGeneratedData === 'function') {{
                        window.handleGeneratedData(window.generatedEvents);
                    }} else {{
                        // If the function doesn't exist yet, try to parse and render
                        setTimeout(function() {{
                            if (typeof parseAndRender === 'function') {{
                                const mockData = window.generatedEvents.map(e => ({{
                                    CURRICULUM: e.curriculum,
                                    SEMESTER: e.semester,
                                    SECTION: e.section,
                                    COURSE: e.course,
                                    TEACHER: e.teacher,
                                    ROOM: e.room,
                                    DAY1: e.day === 'Mon' ? e.day : '',
                                    DAY1_TIME_FROM: e.day === 'Mon' ? e.timeFrom : '',
                                    DAY1_TIME_TO: e.day === 'Mon' ? e.timeTo : '',
                                    DAY1_ROOM: e.day === 'Mon' ? e.room : '',
                                    DAY2: e.day === 'Tue' ? e.day : '',
                                    DAY2_TIME_FROM: e.day === 'Tue' ? e.timeFrom : '',
                                    DAY2_TIME_TO: e.day === 'Tue' ? e.timeTo : '',
                                    DAY2_ROOM: e.day === 'Tue' ? e.room : '',
                                    DAY3: e.day === 'Wed' ? e.day : '',
                                    DAY3_TIME_FROM: e.day === 'Wed' ? e.timeFrom : '',
                                    DAY3_TIME_TO: e.day === 'Wed' ? e.timeTo : '',
                                    DAY3_ROOM: e.day === 'Wed' ? e.room : '',
                                    DAY4: e.day === 'Thu' ? e.day : '',
                                    DAY4_TIME_FROM: e.day === 'Thu' ? e.timeFrom : '',
                                    DAY4_TIME_TO: e.day === 'Thu' ? e.timeTo : '',
                                    DAY4_ROOM: e.day === 'Thu' ? e.room : '',
                                    DAY5: e.day === 'Fri' ? e.day : '',
                                    DAY5_TIME_FROM: e.day === 'Fri' ? e.timeFrom : '',
                                    DAY5_TIME_TO: e.day === 'Fri' ? e.timeTo : '',
                                    DAY5_ROOM: e.day === 'Fri' ? e.room : ''
                                }}));
                                parseAndRender(mockData);
                            }}
                        }}, 500);
                    }}
                }}
            }});
            </script>
            """
            
            # Insert the script before </body>
            html_content = html_content.replace('</body>', injection_script + '</body>')
            
            # Display in iframe
            components.html(html_content, height=900, scrolling=True)
            
        else:
            st.error("⚠️ Calendar viewer template not found. Please ensure timetable_calendar_view_light_v6.html is in the same folder.")
            
    except Exception as e:
        st.error(f"❌ Error loading calendar view: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

# Display unscheduled requirements
if st.session_state.unscheduled_df is not None and not st.session_state.unscheduled_df.empty:
    st.markdown("---")
    st.subheader("⚠️ Unscheduled Requirements")
    st.dataframe(
        st.session_state.unscheduled_df,
        use_container_width=True,
        height=300
    )

# Display generation logs in expander
if st.session_state.generation_log:
    with st.expander("📋 View Generation Logs"):
        for log_line in st.session_state.generation_log[-100:]:  # Show last 100 lines
            if log_line.strip():
                st.text(log_line)
