
Database Name: data.db 


Table Name: ocr_data

Column Names:

brand_name,date_time,recog_enable, entered_line1,
detected_line1,entered_line2,detected_line2,
entered_line3,detected_line3,entered_line4,
detected_line4,good,not_good, detection_time

To view data:

-open command prompt
 sqlite3 data.db

#to view all columns
 select * from ocr_data;

#to view particular column/columns
select column_name1,column_name2,.... from ocr_data;

eg: select brand_name from ocr_data;
or select recog_enable, detection_time from ocr_data;

For Button:

sqlite3 button.db

# to view all columns
  select * from b_data;


