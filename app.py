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
