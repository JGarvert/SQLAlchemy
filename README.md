# SQLAlchemy Homework - Surfs Up!

### What's this all about?

There are two parts to this project.  This first part is to load and analyize some climate data and the second is to create an app based on the queries developed in the first part.  Basic fundamenals of python, sqlalchemy, sqlite, and flask are required.

## Part 1:
Included in the this are a couple of csv files and some images. Packages used include matplotlip, numpy, pandas, datetime, and sqlalchemy

Load the packages, create an engine using squlite, map a database, and save table refrences to base classes.

Perform some numerical and statistical analysis:
A. Find latest data in dataset. Using that, load latest 12 months of data into a Pandas dataframe and plot a bar chart of daily precipitation
B. Review which station was the most active (e.g. had the most 'hits' of data). Using that station, plot a histogram of that station of the frequency of temperatures.

Don't forget to close out the session!


## Part 2:
Create an app to show off the results!  This includes fundamental understanding of Flask and JSON to create an API.

A. Create a homepage with all available routes
B. Using JSON:
    * Create dictionary using `date` as the key and `prcp` as the values
    * Create a list of stations
    * Create a ist of temperature observations (TOBS) for the most recent year.
    * Create a list of min, max, and avg temp for a given start or stop date range.  Note to graders and users, dates will need to be manually enetered into the URL.  The date range will not be prompted. When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date. When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.