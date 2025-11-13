"""
Wrapper module for ttv5.py to safely import only the necessary classes and functions
without executing the main script code.
"""

import pandas as pd
import sys
sys.setrecursionlimit(20000)
from dataclasses import dataclass
from datetime import datetime, time
from typing import List, Dict, Tuple, Optional
import itertools, random, math
from openpyxl import load_workbook

# Import only the functions and classes we need from ttv5
# We'll copy the essential parts here to avoid import issues

def parse_time(val) -> time:
    """
    Parse time values in both 12-hour (e.g., '01:30 PM') and 24-hour (e.g., '13:30')
    formats into a datetime.time object.
    Returns None if input is empty or NaN.
    """
    if pd.isna(val) or str(val).strip() == "":
        return None

    # if already a time or datetime
    if isinstance(val, time):
        return val
    if isinstance(val, datetime):
        return val.time()

    s = str(val).strip().upper().replace('.', ':')  # normalize '1.30 PM' -> '1:30 PM'

    # ✅ Try common 12-hour and 24-hour formats
    time_formats = [
        "%I:%M %p",    # 12-hour format with minutes (e.g., "01:30 PM")
        "%I %p",       # 12-hour format without minutes (e.g., "1 PM")
        "%H:%M:%S",    # 24-hour format with seconds (e.g., "13:30:00")
        "%H:%M",       # 24-hour format (e.g., "13:30")
    ]

    for fmt in time_formats:
        try:
            dt = datetime.strptime(s, fmt)
            return dt.time()
        except ValueError:
            continue

    return None

@dataclass
class Timeslot:
    id: str
    start: time
    end: time

    @property
    def duration_min(self) -> int:
        s_min = self.start.hour * 60 + self.start.minute
        e_min = self.end.hour * 60 + self.end.minute
        return e_min - s_min

@dataclass
class Requirement:
    course_code: str
    curriculum: str
    semester: str
    section_id: str
    teacher: str    
    slots_required: int
    min_total_hours: float
    available_rooms: List[str]  # comma-split in input; empty means no room assignment

# Import the main classes from ttv5
try:
    # Try to import from ttv5 if it's been fixed
    from ttv5 import TimetableCSPv2, read_input_v2, export_to_template
except Exception:
    # If import fails, we need to define them here or handle the error
    # For now, let's just re-raise with a better message
    raise ImportError("Could not import from ttv5.py. Please ensure the file is properly formatted.")
