import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime
import sys
import warnings

# Suppress numpy warnings
warnings.filterwarnings('ignore')

# Import the timetable generation logic
try:
    from ttv5 import TimetableCSPv2, read_input_v2, export_to_template
    print("[INFO] Successfully imported ttv5 module")
except ImportError as e:
    st.error(f"Error importing ttv5 module: {e}")
    st.error("Please ensure ttv5.py is in the same directory as app.py")
    st.stop()

# Function to generate calendar HTML view
def generate_calendar_html(df_timetable):
    """Generate interactive calendar HTML from timetable dataframe"""
    
    # Convert timetable to events format
    events = []
    
    for _, row in df_timetable.iterrows():
        curriculum = row.get('CURRICULUM', '')
        course = row.get('COURSE', '')
        semester = row.get('SEMESTER', '')
        section = row.get('SECTION', '')
        teacher = row.get('TEACHER', '')
        
        # Process each day (DAY1 to DAY5)
        for day_num in range(1, 6):
            day_col = f'DAY{day_num}'
            time_from_col = f'DAY{day_num}_TIME_FROM'
            time_to_col = f'DAY{day_num}_TIME_TO'
            room_col = f'DAY{day_num}_ROOM'
            
            if day_col in df_timetable.columns and pd.notna(row.get(day_col)):
                day = row.get(day_col, '')
                time_from = row.get(time_from_col, '')
                time_to = row.get(time_to_col, '')
                room = row.get(room_col, '')
                
                if day and time_from and time_to:
                    events.append({
                        'day': day,
                        'time_from': str(time_from),
                        'time_to': str(time_to),
                        'course': course,
                        'section': section,
                        'teacher': teacher,
                        'room': room,
                        'curriculum': curriculum,
                        'semester': semester
                    })
    
    # Convert events to JSON
    import json
    events_json = json.dumps(events)
    
    # Generate HTML with embedded calendar viewer
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: #f7f9fc;
                padding: 20px;
            }}
            .calendar-container {{
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .calendar-header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                text-align: center;
            }}
            .calendar-grid {{
                display: grid;
                grid-template-columns: 80px repeat(7, 1fr);
                gap: 1px;
                background: #e5e7eb;
            }}
            .day-header {{
                background: #f3f4f6;
                padding: 12px;
                font-weight: 600;
                text-align: center;
                border-bottom: 2px solid #d1d5db;
            }}
            .time-slot {{
                background: white;
                padding: 8px;
                font-size: 11px;
                color: #6b7280;
                text-align: right;
            }}
            .event-cell {{
                background: white;
                padding: 4px;
                min-height: 60px;
                position: relative;
            }}
            .event {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 8px;
                border-radius: 6px;
                margin: 2px 0;
                font-size: 11px;
                cursor: pointer;
                transition: transform 0.2s;
            }}
            .event:hover {{
                transform: scale(1.02);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }}
            .event-title {{
                font-weight: 600;
                margin-bottom: 4px;
            }}
            .event-details {{
                font-size: 10px;
                opacity: 0.9;
            }}
            .legend {{
                padding: 15px 20px;
                background: #f9fafb;
                border-top: 1px solid #e5e7eb;
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
                font-size: 12px;
                color: #6b7280;
            }}
            .modal {{
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.5);
                z-index: 1000;
                align-items: center;
                justify-content: center;
            }}
            .modal.active {{
                display: flex;
            }}
            .modal-content {{
                background: white;
                padding: 30px;
                border-radius: 12px;
                max-width: 500px;
                width: 90%;
                box-shadow: 0 20px 25px rgba(0,0,0,0.3);
            }}
            .modal-header {{
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 20px;
                color: #1f2937;
            }}
            .modal-body {{
                color: #4b5563;
                line-height: 1.6;
            }}
            .modal-row {{
                display: flex;
                margin: 10px 0;
                padding: 8px 0;
                border-bottom: 1px solid #f3f4f6;
            }}
            .modal-label {{
                font-weight: 600;
                width: 120px;
                color: #6b7280;
            }}
            .modal-value {{
                flex: 1;
                color: #1f2937;
            }}
            .close-btn {{
                background: #667eea;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                cursor: pointer;
                margin-top: 20px;
                font-weight: 600;
            }}
            .close-btn:hover {{
                background: #5568d3;
            }}
        </style>
    </head>
    <body>
        <div class="calendar-container">
            <div class="calendar-header">
                <h2>📅 Weekly Timetable - Interactive Calendar View</h2>
                <p style="margin-top: 8px; opacity: 0.9;">Click on any event to view details</p>
            </div>
            
            <div class="calendar-grid" id="calendar">
                <!-- Calendar will be generated here -->
            </div>
            
            <div class="legend">
                <span><strong>Total Events:</strong> <span id="eventCount">0</span></span>
                <span><strong>Days:</strong> Mon-Fri</span>
                <span><strong>💡 Tip:</strong> Click on events to see full details</span>
            </div>
        </div>
        
        <div class="modal" id="eventModal">
            <div class="modal-content">
                <div class="modal-header" id="modalTitle">Event Details</div>
                <div class="modal-body" id="modalBody"></div>
                <button class="close-btn" onclick="closeModal()">Close</button>
            </div>
        </div>
        
        <script>
            const events = {events_json};
            const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
            
            // Parse time string to minutes
            function parseTime(timeStr) {{
                const str = String(timeStr).trim();
                
                // Try HH:MM:SS format
                let match = str.match(/^(\\d{{1,2}}):(\\d{{2}}):(\\d{{2}})$/);
                if (match) {{
                    return parseInt(match[1]) * 60 + parseInt(match[2]);
                }}
                
                // Try HH:MM format
                match = str.match(/^(\\d{{1,2}}):(\\d{{2}})$/);
                if (match) {{
                    return parseInt(match[1]) * 60 + parseInt(match[2]);
                }}
                
                // Try 12-hour format
                match = str.match(/^(\\d{{1,2}}):(\\d{{2}})\\s*(AM|PM)$/i);
                if (match) {{
                    let hours = parseInt(match[1]);
                    const mins = parseInt(match[2]);
                    const ampm = match[3].toUpperCase();
                    if (ampm === 'PM' && hours !== 12) hours += 12;
                    if (ampm === 'AM' && hours === 12) hours = 0;
                    return hours * 60 + mins;
                }}
                
                return 0;
            }}
            
            // Format minutes to time string
            function formatTime(mins) {{
                const hours = Math.floor(mins / 60);
                const minutes = mins % 60;
                const ampm = hours >= 12 ? 'PM' : 'AM';
                const h12 = hours % 12 || 12;
                return `${{h12}}:${{String(minutes).padStart(2, '0')}} ${{ampm}}`;
            }}
            
            // Group events by day and time
            function groupEvents() {{
                const grouped = {{}};
                days.forEach(day => {{
                    grouped[day] = {{}};
                }});
                
                events.forEach(event => {{
                    const day = event.day;
                    const timeKey = `${{event.time_from}}-${{event.time_to}}`;
                    if (!grouped[day]) grouped[day] = {{}};
                    if (!grouped[day][timeKey]) grouped[day][timeKey] = [];
                    grouped[day][timeKey].push(event);
                }});
                
                return grouped;
            }}
            
            // Get all unique time slots
            function getTimeSlots() {{
                const slots = new Set();
                events.forEach(event => {{
                    slots.add(`${{event.time_from}}-${{event.time_to}}`);
                }});
                return Array.from(slots).sort((a, b) => {{
                    const aStart = parseTime(a.split('-')[0]);
                    const bStart = parseTime(b.split('-')[0]);
                    return aStart - bStart;
                }});
            }}
            
            // Show event details in modal
            function showEventDetails(event) {{
                const modal = document.getElementById('eventModal');
                const modalBody = document.getElementById('modalBody');
                
                modalBody.innerHTML = `
                    <div class="modal-row">
                        <div class="modal-label">Course:</div>
                        <div class="modal-value">${{event.course}}</div>
                    </div>
                    <div class="modal-row">
                        <div class="modal-label">Section:</div>
                        <div class="modal-value">${{event.section}}</div>
                    </div>
                    <div class="modal-row">
                        <div class="modal-label">Teacher:</div>
                        <div class="modal-value">${{event.teacher}}</div>
                    </div>
                    <div class="modal-row">
                        <div class="modal-label">Room:</div>
                        <div class="modal-value">${{event.room}}</div>
                    </div>
                    <div class="modal-row">
                        <div class="modal-label">Day:</div>
                        <div class="modal-value">${{event.day}}</div>
                    </div>
                    <div class="modal-row">
                        <div class="modal-label">Time:</div>
                        <div class="modal-value">${{event.time_from}} - ${{event.time_to}}</div>
                    </div>
                    <div class="modal-row">
                        <div class="modal-label">Curriculum:</div>
                        <div class="modal-value">${{event.curriculum}}</div>
                    </div>
                    <div class="modal-row">
                        <div class="modal-label">Semester:</div>
                        <div class="modal-value">${{event.semester}}</div>
                    </div>
                `;
                
                modal.classList.add('active');
            }}
            
            function closeModal() {{
                document.getElementById('eventModal').classList.remove('active');
            }}
            
            // Close modal on background click
            document.getElementById('eventModal').addEventListener('click', (e) => {{
                if (e.target.id === 'eventModal') closeModal();
            }});
            
            // Render calendar
            function renderCalendar() {{
                const calendar = document.getElementById('calendar');
                const grouped = groupEvents();
                const timeSlots = getTimeSlots();
                
                // Header row
                let html = '<div class="day-header">Time</div>';
                days.forEach(day => {{
                    html += `<div class="day-header">${{day}}</div>`;
                }});
                
                // Time slot rows
                timeSlots.forEach(slot => {{
                    const [start, end] = slot.split('-');
                    html += `<div class="time-slot">${{start}}<br>to<br>${{end}}</div>`;
                    
                    days.forEach(day => {{
                        const dayEvents = grouped[day][slot] || [];
                        html += '<div class="event-cell">';
                        dayEvents.forEach(event => {{
                            html += `
                                <div class="event" onclick='showEventDetails(${{JSON.stringify(event)}})'>
                                    <div class="event-title">${{event.course}}</div>
                                    <div class="event-details">
                                        ${{event.section}} • ${{event.teacher}}<br>
                                        ${{event.room}}
                                    </div>
                                </div>
                            `;
                        }});
                        html += '</div>';
                    }});
                }});
                
                calendar.innerHTML = html;
                document.getElementById('eventCount').textContent = events.length;
            }}
            
            // Initialize
            renderCalendar();
        </script>
    </body>
    </html>
    """
    
    return html

# Page configuration
st.set_page_config(
    page_title="Timetable Generator",
    page_icon="📅",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">📅 Timetable Generator</div>', unsafe_allow_html=True)

# Sidebar for instructions
with st.sidebar:
    st.header("📖 Instructions")
    st.markdown("""
    ### How to Use:
    1. **Upload Input File**: Upload your `InputData_v2.xlsx` file
    2. **Upload Template**: Upload your `TimeTableImport_SIS.xlsx` template
    3. **Configure Settings**: Adjust solver parameters if needed
    4. **Generate**: Click "Generate Timetable" button
    5. **Download**: Download the generated timetable
    
    ### Required Sheets in Input File:
    - WINDOW
    - TIMESLOTS
    - REQUIREMENTS
    - DAYS
    - BREAKS (optional)
    - TEACHER_AVAILABILITY (optional)
    
    ### Features:
    - ✅ Automatic conflict resolution
    - ✅ Teacher availability checking
    - ✅ Virtual room support (Online classes)
    - ✅ Partial solution mode (skips impossible requirements)
    - ✅ Unscheduled requirements report
    """)
    
    st.markdown("---")
    st.markdown("**Version**: 1.0")
    st.markdown("**Last Updated**: Nov 2025")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 Upload Input Files")
    
    # File uploader for input data
    input_file = st.file_uploader(
        "Upload Input Data Excel File (InputData_v2.xlsx)",
        type=['xlsx'],
        help="Upload the Excel file containing WINDOW, TIMESLOTS, REQUIREMENTS, DAYS sheets"
    )
    
    # File uploader for template
    template_file = st.file_uploader(
        "Upload Template Excel File (TimeTableImport_SIS.xlsx)",
        type=['xlsx'],
        help="Upload the template Excel file for output formatting"
    )

with col2:
    st.subheader("⚙️ Solver Configuration")
    
    # Configuration options
    allow_partial = st.checkbox(
        "Enable Partial Solution Mode",
        value=True,
        help="Skip impossible requirements and continue solving"
    )
    
    debug_mode = st.checkbox(
        "Enable Debug Mode",
        value=False,
        help="Show detailed debug output (slower but helpful for troubleshooting)"
    )
    
    max_attempts = st.slider(
        "Max Attempts Per Variable",
        min_value=50,
        max_value=500,
        value=200,
        step=50,
        help="Number of attempts before skipping a stuck requirement"
    )
    
    random_seed = st.number_input(
        "Random Seed",
        min_value=1,
        max_value=9999,
        value=123,
        help="Set random seed for reproducible results"
    )

# Initialize session state
if 'generated_file' not in st.session_state:
    st.session_state.generated_file = None
if 'generation_log' not in st.session_state:
    st.session_state.generation_log = []
if 'unscheduled_df' not in st.session_state:
    st.session_state.unscheduled_df = None

# Generate button
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    generate_button = st.button(
        "🚀 Generate Timetable",
        type="primary",
        use_container_width=True,
        disabled=(input_file is None or template_file is None)
    )

# Process generation
if generate_button:
    if input_file and template_file:
        try:
            # Save uploaded files temporarily
            input_path = "temp_input.xlsx"
            template_path = "temp_template.xlsx"
            output_path = "GeneratedTimetable.xlsx"
            
            with open(input_path, "wb") as f:
                f.write(input_file.getbuffer())
            
            with open(template_path, "wb") as f:
                f.write(template_file.getbuffer())
            
            # Progress indicator
            progress_bar = st.progress(0)
            status_text = st.empty()
            log_container = st.expander("📋 Generation Log", expanded=True)
            
            with log_container:
                log_area = st.empty()
            
            # Capture output
            class StreamlitLogger:
                def __init__(self):
                    self.logs = []
                
                def write(self, text):
                    if text.strip():
                        self.logs.append(text.strip())
                        log_area.text_area("Logs", "\n".join(self.logs[-50:]), height=300)
                
                def flush(self):
                    pass
            
            logger = StreamlitLogger()
            old_stdout = sys.stdout
            sys.stdout = logger
            
            try:
                # Step 1: Read input data
                status_text.text("📖 Reading input data...")
                progress_bar.progress(10)
                data = read_input_v2(input_path)
                
                # Step 2: Initialize solver
                status_text.text("🔧 Initializing solver...")
                progress_bar.progress(20)
                engine = TimetableCSPv2(
                    data["timeslots"],
                    data["requirements"],
                    data["days"],
                    data['teacher_availability'],
                    allow_partial=allow_partial,
                    debug=debug_mode
                )
                
                # Step 3: Run diagnostics
                status_text.text("🔍 Running diagnostics...")
                progress_bar.progress(30)
                print(f"[INFO] Loaded {len(engine.days)} days, {len(engine.timeslots)} timeslots, {len(engine.requirements)} requirements")
                
                # Step 4: Solve
                status_text.text("⚙️ Generating timetable... This may take a few minutes...")
                progress_bar.progress(40)
                assignments = engine.solve(seed=random_seed)
                
                progress_bar.progress(70)
                
                # Step 5: Export
                status_text.text("📝 Exporting timetable...")
                progress_bar.progress(80)
                export_to_template(
                    assignments,
                    engine,
                    data["start_date"],
                    data["end_date"],
                    output_path,
                    template_path,
                    skipped_requirements=engine.skipped_requirements
                )
                
                progress_bar.progress(100)
                status_text.text("✅ Timetable generated successfully!")
                
                # Read generated file
                with open(output_path, "rb") as f:
                    st.session_state.generated_file = f.read()
                
                # Store unscheduled requirements
                if engine.skipped_requirements:
                    unscheduled_data = []
                    for req, reason in engine.skipped_requirements:
                        unscheduled_data.append({
                            "Course": req.course_code,
                            "Section": req.section_id,
                            "Teacher": req.teacher,
                            "Curriculum": req.curriculum,
                            "Semester": req.semester,
                            "Slots Required": req.slots_required,
                            "Min Hours": req.min_total_hours,
                            "Reason": reason
                        })
                    st.session_state.unscheduled_df = pd.DataFrame(unscheduled_data)
                
                st.session_state.generation_log = logger.logs
                
            finally:
                sys.stdout = old_stdout
            
            # Success message
            st.markdown(f"""
                <div class="success-box">
                    <h3>✅ Success!</h3>
                    <p><strong>Scheduled:</strong> {len(assignments)} assignments</p>
                    <p><strong>Unscheduled:</strong> {len(engine.skipped_requirements)} requirements</p>
                    <p>Click the download button below to get your timetable.</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Clean up temp files
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(template_path):
                os.remove(template_path)
            
        except Exception as e:
            sys.stdout = old_stdout
            st.markdown(f"""
                <div class="error-box">
                    <h3>❌ Error</h3>
                    <p>{str(e)}</p>
                </div>
            """, unsafe_allow_html=True)
            st.exception(e)

# Download section
if st.session_state.generated_file:
    st.markdown("---")
    st.subheader("📥 Download Results")
    
    col_dl1, col_dl2 = st.columns([1, 1])
    
    with col_dl1:
        st.download_button(
            label="📥 Download Generated Timetable",
            data=st.session_state.generated_file,
            file_name=f"GeneratedTimetable_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True
        )
    
    with col_dl2:
        if st.session_state.unscheduled_df is not None and not st.session_state.unscheduled_df.empty:
            st.info(f"⚠️ {len(st.session_state.unscheduled_df)} requirements could not be scheduled")
    
    # Calendar View Option
    st.markdown("---")
    st.subheader("📅 Interactive Calendar View")
    
    view_option = st.radio(
        "Choose view:",
        ["Table View", "Calendar View"],
        horizontal=True,
        key="view_option"
    )
    
    if view_option == "Calendar View":
        st.info("📌 Interactive calendar with clash detection - Click on events to see details")
        
        # Read the generated timetable to create calendar view
        import streamlit.components.v1 as components
        
        try:
            # Read the generated Excel file from session state
            excel_data = io.BytesIO(st.session_state.generated_file)
            df_timetable = pd.read_excel(excel_data, sheet_name='TimeTable')
            
            # Generate HTML calendar view
            calendar_html = generate_calendar_html(df_timetable)
            
            # Display the calendar
            components.html(calendar_html, height=800, scrolling=True)
            
        except Exception as e:
            st.error(f"Error generating calendar view: {str(e)}")
            st.info("Showing table view instead")
            st.dataframe(df_timetable, use_container_width=True)
    else:
        # Show table view
        try:
            excel_data = io.BytesIO(st.session_state.generated_file)
            df_timetable = pd.read_excel(excel_data, sheet_name='TimeTable')
            st.dataframe(df_timetable, use_container_width=True, height=600)
        except Exception as e:
            st.error(f"Error loading timetable: {str(e)}")

# Display unscheduled requirements
if st.session_state.unscheduled_df is not None and not st.session_state.unscheduled_df.empty:
    st.markdown("---")
    st.subheader("⚠️ Unscheduled Requirements")
    st.dataframe(
        st.session_state.unscheduled_df,
        use_container_width=True,
        height=400
    )
    
    # Recommendations
    with st.expander("💡 Recommendations to Fix Unscheduled Requirements"):
        st.markdown("""
        ### How to Fix Unscheduled Requirements:
        
        1. **Reduce slots_required**: Lower the number of required slots for these courses in the Excel file
        2. **Expand teacher availability**: Add more available time slots in the TEACHER_AVAILABILITY sheet
        3. **Assign different teachers**: Choose teachers with more availability
        4. **Check for conflicts**: Look for duplicate or conflicting requirements
        5. **Add more timeslots**: Increase available time slots in the TIMESLOTS sheet
        6. **Use online rooms**: Change physical rooms to "Online" for more flexibility
        """)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>Timetable Generator v1.0 | Powered by Constraint Satisfaction Problem (CSP) Solver</p>
    </div>
""", unsafe_allow_html=True)
