# 📅 Calendar Viewer Integration Guide

## Overview

The Streamlit app now integrates with your existing `timetable_calendar_view_light_v6.html` file, allowing users to view generated timetables in a beautiful, feature-rich calendar interface.

## How It Works

### Workflow:

1. **Generate Timetable** in Streamlit app
2. **Download** the generated Excel file
3. **Click** "Open Calendar Viewer" button
4. **Upload** the downloaded Excel file to the HTML viewer
5. **Explore** with all the advanced features!

## Features Available in Calendar Viewer

### 🎨 Visual Features:
- ✅ **Weekly Grid Layout**: Beautiful calendar with time slots
- ✅ **Color-coded Events**: Normal events vs. clashing events
- ✅ **Sticky Headers**: Days header stays visible while scrolling
- ✅ **Responsive Design**: Works on desktop and mobile
- ✅ **Modern UI**: Clean, professional appearance

### 🔍 Filtering Options:
- **Curriculum**: Filter by curriculum type
- **Semester**: View specific semester schedules
- **Section**: Focus on particular sections
- **Teacher**: See individual teacher schedules
- **Course**: View specific course schedules
- **Room**: Check room utilization

### ⚠️ Clash Detection:
- **Teacher Clashes**: Same teacher, different sections, same time
- **Section Clashes**: Same section, different courses, same time
- **Room Clashes**: Same room, different courses, same time
- **Visual Highlighting**: Clashing events shown in yellow/orange
- **Toggle Options**: Show/hide clash detection

### 🤖 AI Integration:
- **OpenAI Integration**: Ask AI questions about your timetable
- **Smart Analysis**: Get insights on conflicts, optimization, etc.
- **Secure**: API key stored locally in browser

## User Instructions

### Step-by-Step Guide:

#### 1. Generate Timetable
- Upload input files in Streamlit app
- Configure settings
- Click "Generate Timetable"
- Wait for completion

#### 2. Download Excel File
- Click "📥 Download Generated Timetable" button
- Save the file (e.g., `GeneratedTimetable_20251114_110000.xlsx`)

#### 3. Open Calendar Viewer
- Click "🚀 Open Calendar Viewer" button in the app
- OR manually open `timetable_calendar_view_light_v6.html` in your browser

#### 4. Upload to Viewer
- In the HTML page, click "Upload Excel (.xlsx)"
- Select the downloaded timetable file
- Calendar will automatically populate

#### 5. Explore Features
- Use filter dropdowns to narrow down view
- Click on events to see details
- Enable clash detection checkboxes
- Use AI features (optional, requires OpenAI API key)

## Technical Details

### File Structure:
```
d:\Time Table Generation\
├── app.py                              # Streamlit app
├── ttv5.py                             # Timetable generator
├── timetable_calendar_view_light_v6.html  # Calendar viewer (unchanged)
├── GeneratedTimetable.xlsx             # Output file
└── requirements.txt                    # Dependencies
```

### Integration Method:
- **No modifications** to the HTML file
- Streamlit app provides:
  - Download button for Excel file
  - Link to open HTML viewer
  - Instructions for users
  - Preview table view

### Why This Approach?

**Advantages:**
1. ✅ **Preserves original HTML**: No need to modify your existing viewer
2. ✅ **Full features**: All HTML features work as designed
3. ✅ **Separation of concerns**: Generation and viewing are separate
4. ✅ **Flexibility**: Users can use either Streamlit or standalone HTML
5. ✅ **No conflicts**: No embedding issues or compatibility problems

**User Experience:**
- Simple 2-click process (download + open)
- Clear instructions in the app
- Beautiful visual presentation
- All advanced features available

## Comparison: Streamlit vs HTML Viewer

| Feature | Streamlit App | HTML Viewer |
|---------|---------------|-------------|
| **File Upload** | ✅ Yes | ✅ Yes |
| **Generate Timetable** | ✅ Yes | ❌ No |
| **Table View** | ✅ Yes | ❌ No |
| **Calendar View** | ⚠️ Link to HTML | ✅ Full Featured |
| **Clash Detection** | ❌ No | ✅ Yes |
| **Filters** | ❌ No | ✅ 6 filters |
| **AI Integration** | ❌ No | ✅ Yes |
| **Download Results** | ✅ Yes | ❌ No |
| **Unscheduled Report** | ✅ Yes | ❌ No |

**Best Practice**: Use Streamlit for generation, HTML for visualization!

## Customization Options

### For the HTML Viewer:
The HTML file (`timetable_calendar_view_light_v6.html`) can be customized:
- Modify CSS variables in `:root` section
- Change colors, fonts, spacing
- Add/remove filter options
- Customize clash detection rules

### For the Streamlit App:
The integration section in `app.py` can be customized:
- Change button styling
- Modify instructions
- Add more preview options
- Customize layout

## Troubleshooting

### Issue: "Calendar viewer not found"
**Solution**: Ensure `timetable_calendar_view_light_v6.html` is in the same directory as `app.py`

### Issue: "Button doesn't open HTML file"
**Solution**: 
- Copy the file path shown in the button
- Manually paste it in your browser
- Or double-click the HTML file directly

### Issue: "Excel file not loading in viewer"
**Solution**:
- Make sure you downloaded the file first
- Check file format is `.xlsx`
- Try re-downloading the file

### Issue: "No events showing in calendar"
**Solution**:
- Verify the Excel file has a "TimeTable" sheet
- Check that events have proper day and time columns
- Look for JavaScript errors in browser console

## Browser Compatibility

**Tested and Working:**
- ✅ Chrome/Edge (Chromium) - Recommended
- ✅ Firefox
- ✅ Safari
- ⚠️ Internet Explorer - Not supported

## Security Notes

### API Keys:
- OpenAI API keys are stored in browser's localStorage
- Keys never leave your browser
- Clear browser data to remove stored keys

### File Handling:
- Excel files processed locally in browser
- No data sent to external servers (except OpenAI if used)
- All processing is client-side

## Future Enhancements

Potential improvements:
1. **Direct Integration**: Embed HTML viewer in Streamlit iframe
2. **Auto-load**: Automatically load generated file in viewer
3. **Sync Filters**: Share filter state between Streamlit and HTML
4. **Export Options**: PDF, iCal, PNG export from viewer
5. **Mobile App**: Native mobile version

## Support

### For Streamlit App Issues:
- Check generation logs
- Verify file uploads
- Review error messages

### For HTML Viewer Issues:
- Check browser console (F12)
- Verify Excel file format
- Test with sample data

## Quick Reference

### Streamlit App:
```bash
streamlit run app.py
# Access at: http://localhost:8501
```

### HTML Viewer:
```bash
# Just open in browser:
timetable_calendar_view_light_v6.html
```

### File Locations:
- **Input**: `InputData_v2.xlsx`, `TimeTableImport_SIS.xlsx`
- **Output**: `GeneratedTimetable_YYYYMMDD_HHMMSS.xlsx`
- **Viewer**: `timetable_calendar_view_light_v6.html`

---

**Version**: 1.0  
**Last Updated**: Nov 2025  
**Integration Type**: Link-based (preserves original HTML)
