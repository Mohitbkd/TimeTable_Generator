"""
Standalone script to generate timetable - called by Streamlit app
Usage: python generate_timetable.py <input_file> <template_file> <output_file> [--debug] [--max-attempts N]
"""

import sys
import argparse

# Import from ttv5 - this will work when run as a script
import ttv5

def main():
    parser = argparse.ArgumentParser(description='Generate timetable from Excel input')
    parser.add_argument('input_file', help='Path to input Excel file (InputData_v2.xlsx)')
    parser.add_argument('template_file', help='Path to template Excel file (TimeTableImport_SIS.xlsx)')
    parser.add_argument('output_file', help='Path to output Excel file')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--max-attempts', type=int, default=200, help='Max attempts per variable')
    parser.add_argument('--seed', type=int, default=123, help='Random seed')
    
    args = parser.parse_args()
    
    try:
        # Read input data
        print(f"[INFO] Reading input from: {args.input_file}")
        data = ttv5.read_input_v2(args.input_file)
        
        # Initialize solver
        print(f"[INFO] Initializing solver...")
        engine = ttv5.TimetableCSPv2(
            data["timeslots"],
            data["requirements"],
            data["days"],
            data['teacher_availability'],
            allow_partial=True,
            debug=args.debug
        )
        
        print(f"[INFO] Loaded {len(engine.days)} days, {len(engine.timeslots)} timeslots, {len(engine.requirements)} requirements")
        
        # Solve
        print(f"[INFO] Generating timetable...")
        assignments = engine.solve(seed=args.seed)
        
        # Export
        print(f"[INFO] Exporting to: {args.output_file}")
        ttv5.export_to_template(
            assignments,
            engine,
            data["start_date"],
            data["end_date"],
            args.output_file,
            args.template_file,
            skipped_requirements=engine.skipped_requirements
        )
        
        print(f"[SUCCESS] Timetable generated successfully!")
        print(f"[STATS] Scheduled: {len(assignments)} assignments")
        print(f"[STATS] Unscheduled: {len(engine.skipped_requirements)} requirements")
        
        return 0
        
    except Exception as e:
        print(f"[ERROR] {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
