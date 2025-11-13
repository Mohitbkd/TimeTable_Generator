# 📅 Calendar View Feature

## Overview

The Streamlit app now includes an **Interactive Calendar View** that displays the generated timetable in a beautiful, clickable calendar format - similar to the `timetable_calendar_view_light_v6.html` file.

## Features

### ✨ Interactive Calendar
- **Weekly Grid Layout**: Shows Mon-Sun with time slots
- **Color-coded Events**: Each class is displayed as a colored card
- **Click to View Details**: Click any event to see full information in a modal
- **Responsive Design**: Adapts to different screen sizes
- **Clean UI**: Modern, professional appearance

### 📊 Event Details Modal
When you click on any event, you'll see:
- Course name
- Section
- Teacher
- Room
- Day
- Time (from - to)
- Curriculum
- Semester

### 🎯 View Options
After generating a timetable, you can choose between:
1. **Table View** - Traditional spreadsheet format
2. **Calendar View** - Interactive visual calendar

## How to Use

1. **Generate Timetable**: Upload files and click "Generate Timetable"
2. **Choose View**: After generation, select "Calendar View" from the radio buttons
3. **Explore**: 
   - Scroll through the weekly calendar
   - Click on any event to see details
   - Close modal by clicking "Close" or clicking outside

## Technical Details

### Data Processing
- Reads the generated Excel file from session state
- Parses DAY1-DAY5 columns with time and room information
- Converts to event objects with all necessary details
- Groups events by day and time slot

### Rendering
- Uses `streamlit.components.html` to embed custom HTML/CSS/JavaScript
- Fully self-contained (no external dependencies)
- Responsive grid layout with CSS Grid
- Modal overlay for event details

### Time Format Support
The calendar parser supports multiple time formats:
- `HH:MM:SS` (24-hour with seconds)
- `HH:MM` (24-hour)
- `HH:MM AM/PM` (12-hour)

## Comparison with HTML Version

### Similarities
- ✅ Interactive calendar grid
- ✅ Click to view event details
- ✅ Modal popup for details
- ✅ Clean, modern design
- ✅ Color-coded events

### Differences
- ❌ No file upload (uses generated data directly)
- ❌ No clash detection toggles (shows all events)
- ❌ No AI integration (focused on display)
- ✅ Integrated with Streamlit workflow
- ✅ Automatic data loading from generation

## Future Enhancements

Potential additions:
1. **Clash Detection**: Highlight conflicting events
2. **Filter Options**: Filter by teacher, section, or room
3. **Export Calendar**: Download as iCal or PDF
4. **Print View**: Optimized for printing
5. **Dark Mode**: Toggle between light/dark themes
6. **Week Navigation**: View different weeks if applicable

## Code Structure

```python
# Main function
generate_calendar_html(df_timetable)
  ├── Parse timetable DataFrame
  ├── Extract events from DAY1-DAY5 columns
  ├── Convert to JSON
  └── Generate HTML with embedded CSS/JS

# HTML Components
├── Calendar Grid (CSS Grid layout)
├── Event Cards (clickable divs)
├── Modal Overlay (event details)
└── JavaScript (event handling, rendering)
```

## Browser Compatibility

Tested and works on:
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers

## Performance

- **Fast Rendering**: Handles 100+ events smoothly
- **Lightweight**: No external libraries required
- **Responsive**: Updates instantly on interaction

## Screenshots

### Calendar View
```
┌─────────────────────────────────────────────┐
│  📅 Weekly Timetable - Interactive Calendar │
│  Click on any event to view details         │
├──────┬──────┬──────┬──────┬──────┬──────────┤
│ Time │ Mon  │ Tue  │ Wed  │ Thu  │ Fri      │
├──────┼──────┼──────┼──────┼──────┼──────────┤
│ 9:00 │[CS101]│      │[CS101]│      │[CS101]  │
│ to   │ A    │      │ A    │      │ A        │
│10:00 │ Prof │      │ Prof │      │ Prof     │
├──────┼──────┼──────┼──────┼──────┼──────────┤
│10:00 │      │[MATH]│      │[MATH]│          │
│ to   │      │ B    │      │ B    │          │
│11:00 │      │ Dr.X │      │ Dr.X │          │
└──────┴──────┴──────┴──────┴──────┴──────────┘
```

### Event Details Modal
```
┌────────────────────────────┐
│ Event Details              │
├────────────────────────────┤
│ Course:     CS101          │
│ Section:    A              │
│ Teacher:    Prof. Smith    │
│ Room:       Lab 101        │
│ Day:        Monday         │
│ Time:       9:00 - 10:00   │
│ Curriculum: Computer Sci   │
│ Semester:   3              │
├────────────────────────────┤
│         [Close]            │
└────────────────────────────┘
```

## Troubleshooting

### Calendar not showing
- Check that timetable was generated successfully
- Verify Excel file has TimeTable sheet
- Check browser console for JavaScript errors

### Events not clickable
- Ensure JavaScript is enabled in browser
- Try refreshing the page
- Check that modal HTML is rendering

### Wrong time format
- Verify time columns in Excel are formatted correctly
- Check DAY1_TIME_FROM and DAY1_TIME_TO columns

## Support

For issues or questions about the calendar view:
1. Check the generation log for errors
2. Verify the Excel output has correct format
3. Try switching to Table View to see raw data
4. Check browser developer console for errors

---

**Version**: 1.0  
**Last Updated**: Nov 2025  
**Compatible with**: Streamlit 1.28+
