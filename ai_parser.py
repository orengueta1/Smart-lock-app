import re
import datetime
from datetime import timedelta

def parse_natural_language(text, api_key=None):
    """
    Parses natural language text to extract date, start time, and end time using Regex.
    No API Key required.
    """
    text = text.lower()
    today = datetime.date.today()
    target_date = today

    # 1. Parse Date - explicit format DD/MM/YY or DD/MM/YYYY
    date_match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})', text)
    if date_match:
        d, m, y = date_match.groups()
        if len(y) == 2:
            y = "20" + y # assume 20xx
        try:
            target_date = datetime.date(int(y), int(m), int(d))
        except ValueError:
            pass # Invalid date, fallback to today
    
    # Relative dates
    elif "yesterday" in text:
        target_date = today - timedelta(days=1)
    elif "tomorrow" in text: # Just in case
        target_date = today + timedelta(days=1)
    elif "today" in text:
         target_date = today
         
    # "N days ago"
    else:
        days_ago_match = re.search(r'(\d+)\s+days?\s+ago', text)
        if days_ago_match:
            days = int(days_ago_match.group(1))
            target_date = today - timedelta(days=days)
        
        # "a week ago", "last week" (approx 7 days)
        elif "week ago" in text or "last week" in text:
            target_date = today - timedelta(days=7)
    
    # 2. Parse Times
    # Pattern to match "9:00", "09:00", "9am", "9 am", "9", "17:00"
    # We look for "from X to Y" or just "X to Y" patterns
    
    # Helper to convert to 24h format
    def to_24h(val, meridiem):
        try:
            val = val.replace(":", ".") # basic normalization
            if "." in val:
                h, m = map(int, val.split("."))
            else:
                h = int(val)
                m = 0
            
            if meridiem and "pm" in meridiem and h < 12:
                h += 12
            if meridiem and "am" in meridiem and h == 12:
                h = 0
            return f"{h:02}:{m:02}"
        except:
            return None

    # Regex for "9am to 5pm", "9:00 to 17:00", "9 to 5", "15:00-20:00"
    # Group 1: Start, Group 2: StartMeridiem, Group 3: End, Group 4: EndMeridiem
    time_pattern = r'(\d{1,2}(?::\d{2})?)\s*(am|pm)?\s*(?:to|-)\s*(\d{1,2}(?::\d{2})?)\s*(am|pm)?'
    match = re.search(time_pattern, text)
    
    start_time = "09:00"
    end_time = "17:00"
    
    if match:
        t1, m1, t2, m2 = match.groups()
        
        # Inference for AM/PM if missing
        if not m1 and not m2:
            s_h = int(t1.split(':')[0])
            e_h = int(t2.split(':')[0])
            
            # Logic: If using 24h format (e.g. 15 to 20), rely on that.
            if s_h > 12 or e_h > 12:
                start_time = to_24h(t1, None)
                end_time = to_24h(t2, None)
            else:
                # "9 to 5" -> 09:00 to 17:00
                if s_h <= 12 and e_h <= 12:
                    if s_h < e_h: 
                         # 9 to 11 -> 09-11
                         pass
                    elif e_h < s_h: 
                         e_h += 12 # 9 to 5 case
                    elif e_h < 7: 
                         e_h += 12
                
                # Re-evaluate based on updated heuristics
                if s_h < 12:
                     start_str_meridiem = "am"
                else:
                     start_str_meridiem = "pm"
                     
                start_time = to_24h(t1, start_str_meridiem)
                
                # For end time
                if int(t2.split(':')[0]) < 12 and int(t2.split(':')[0]) < s_h:
                     end_time = to_24h(t2, "pm")
                else:
                     # default assumption
                     end_time = to_24h(t2, "pm" if int(t2.split(':')[0]) < 12 else "am") # rough guess

                # Let's simplify: if explicit am/pm is absent, AND numbers are small, assume typical workday 9-5
                # If numbers are large (>12), assume 24h.
                # If "15:00-20:00" -> s_h=15.
                
                if s_h > 12 or (":" in t1 and int(t1.split(':')[0]) > 12):
                     start_time = to_24h(t1, None)
                else:
                     start_time = to_24h(t1, "am") # Default start to AM if small number
                     
                if e_h > 12 or (":" in t2 and int(t2.split(':')[0]) > 12):
                     end_time = to_24h(t2, None)
                else:
                     # If end is smaller than start, it's likely PM (9 to 5)
                     if int(t2.split(':')[0]) < int(start_time.split(':')[0]):
                         end_time = to_24h(t2, "pm")
                     else:
                         end_time = to_24h(t2, "pm") # bias towards 5pm vs 5am end

        else:
            # If explicit am/pm
            start_time = to_24h(t1, m1)
            end_time = to_24h(t2, m2)

    return {
        "Date": target_date.strftime("%Y-%m-%d"),
        "Start_Time": start_time if start_time else "09:00",
        "End_Time": end_time if end_time else "17:00"
    }
