# 📅 Timetable Generator - Streamlit Application

A web-based timetable generation system using Constraint Satisfaction Problem (CSP) solver with Streamlit interface.

## 🚀 Features

- ✅ **Web Interface**: Easy-to-use Streamlit application
- ✅ **File Upload**: Upload Excel input files directly
- ✅ **Automatic Conflict Resolution**: Handles teacher, section, and room conflicts
- ✅ **Teacher Availability**: Respects teacher availability constraints
- ✅ **Virtual Room Support**: Unlimited capacity for online classes
- ✅ **Partial Solution Mode**: Skips impossible requirements and continues
- ✅ **Unscheduled Report**: Shows which requirements couldn't be scheduled with reasons
- ✅ **Download Results**: Download generated timetable as Excel file
- ✅ **📅 Interactive Calendar View**: Visual weekly calendar with clickable events (NEW!)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🛠️ Installation

1. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

### Option 1: Run Streamlit Web Application (Recommended)

1. **Start the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** (should open automatically at `http://localhost:8501`)

3. **Upload files:**
   - Upload your `InputData_v2.xlsx` file
   - Upload your `TimeTableImport_SIS.xlsx` template file

4. **Configure settings** (optional):
   - Enable/disable partial solution mode
   - Enable/disable debug mode
   - Adjust max attempts per variable
   - Set random seed for reproducibility

5. **Generate timetable:**
   - Click "Generate Timetable" button
   - Wait for processing (may take a few minutes for large datasets)

6. **Download results:**
   - Click "Download Generated Timetable" button
   - Review unscheduled requirements if any

7. **View timetable:**
   - Choose between **Table View** or **Calendar View**
   - **Calendar View**: Interactive weekly calendar with clickable events
   - Click on any event to see full details (course, teacher, room, time, etc.)

### Option 2: Run Command Line Script

```bash
python ttv5.py
```

**Note**: Make sure `InputData_v2.xlsx` and `TimeTableImport_SIS.xlsx` are in the same directory.

## 📁 Input File Requirements

### Required Sheets in InputData_v2.xlsx:

1. **WINDOW**: Start and end dates
   - Columns: `start_date`, `end_date`

2. **TIMESLOTS**: Available time slots
   - Columns: `slot_id`, `start_time`, `end_time`

3. **REQUIREMENTS**: Course requirements
   - Columns: `course_code`, `curriculum`, `semester`, `section_id`, `teacher`, `slots_required`, `min_total_hours`, `available_rooms`

4. **DAYS**: Available days
   - Columns: `day`

### Optional Sheets:

5. **BREAKS**: Break times for sections
   - Columns: `curriculum`, `semester`, `section_id`, `day`, `break_from`, `break_to`

6. **TEACHER_AVAILABILITY**: Teacher availability windows
   - Columns: `teacher`, `day`, `available_from`, `available_to`

## 🎨 Streamlit Interface Features

### Main Interface:
- **File Upload Section**: Drag and drop or browse for Excel files
- **Configuration Panel**: Adjust solver parameters
- **Progress Tracking**: Real-time progress bar and status updates
- **Generation Log**: View detailed processing logs
- **Results Display**: Summary of scheduled and unscheduled requirements

### Sidebar:
- **Instructions**: Step-by-step guide
- **Required Sheets**: List of mandatory Excel sheets
- **Features**: Overview of capabilities
- **Version Info**: Application version and update date

### Results Section:
- **Download Button**: Get generated timetable Excel file
- **Unscheduled Table**: View requirements that couldn't be scheduled
- **Recommendations**: Tips to fix unscheduled requirements

## ⚙️ Configuration Options

### Solver Parameters:

- **Partial Solution Mode** (default: enabled)
  - Skips impossible requirements and continues solving
  - Generates report of unscheduled requirements

- **Debug Mode** (default: disabled)
  - Shows detailed processing information
  - Useful for troubleshooting
  - **Note**: Slower execution when enabled

- **Max Attempts Per Variable** (default: 200)
  - Number of attempts before skipping a stuck requirement
  - Lower values = faster but may skip more requirements
  - Higher values = slower but tries harder to schedule

- **Random Seed** (default: 123)
  - Set for reproducible results
  - Different seeds may produce different valid solutions

## 🔧 Performance Tips

### For Large Datasets (500+ records):

1. **Disable Debug Mode**: Significantly faster execution
2. **Reduce Max Attempts**: Set to 100-150 for faster skipping
3. **Pre-filter Data**: Split by semester or year
4. **Expand Teacher Availability**: More flexible schedules = easier solving
5. **Use Online Rooms**: Virtual rooms have unlimited capacity

### Expected Performance:
- **50-100 records**: 1-2 minutes
- **100-250 records**: 3-5 minutes
- **250-500 records**: 5-10 minutes
- **500+ records**: 10-30 minutes (consider batch processing)

## 📊 Output Files

### GeneratedTimetable.xlsx contains:

1. **TimeTable Sheet**: Successfully scheduled courses
   - Columns: STARTDATE, ENDDATE, CURRICULUM, COURSE, SEMESTER, SECTION, TEACHER
   - DAY1-5 with TIME_FROM, TIME_TO, ROOM, LINK for each day

2. **Unscheduled Sheet** (if any): Requirements that couldn't be scheduled
   - Columns: Course, Section, Teacher, Curriculum, Semester, Slots Required, Min Hours, Available Rooms, Reason

## 🐛 Troubleshooting

### Common Issues:

1. **"No feasible timetable found"**
   - Enable partial solution mode
   - Reduce slots_required in input file
   - Expand teacher availability
   - Add more timeslots

2. **"Room occupied" errors**
   - Use "Online" for virtual classes (unlimited capacity)
   - Add more physical rooms
   - Reduce concurrent sections

3. **Slow execution**
   - Disable debug mode
   - Reduce max attempts per variable
   - Split large datasets into batches

4. **Import errors in Streamlit**
   - Make sure `ttv5.py` is in the same directory as `app.py`
   - Install all requirements: `pip install -r requirements.txt`

## 📝 Virtual Room Support

Rooms containing these keywords are treated as virtual (unlimited capacity):
- `online`
- `virtual`
- `zoom`
- `teams`
- `meet`
- `webex`
- `remote`

**Example**: A room named "Online" or "Zoom Room" can host multiple classes simultaneously.

## 🔄 Algorithm Details

The timetable generator uses:
- **Constraint Satisfaction Problem (CSP)** approach
- **Backtracking search** with intelligent heuristics
- **Minimum Remaining Values (MRV)** for variable ordering
- **Least Constraining Value (LCV)** for value ordering
- **Forward checking** for early conflict detection
- **Partial solution mode** for handling over-constrained problems

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the generation log for specific errors
3. Check the unscheduled requirements report for recommendations

## 📄 License

This project is provided as-is for educational and institutional use.

## 🔖 Version History

- **v1.0** (Nov 2025): Initial Streamlit application release
  - Web interface with file upload
  - Real-time progress tracking
  - Downloadable results
  - Unscheduled requirements report
