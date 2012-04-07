Notes
-----

Client application has been built with java 1.6.0.22
Client application is ms-ipo-client.jar

Batch file (for windows) and shell script (for unix) are included.

Client
------


Windows
run_ms-ipo-client.BAT 

Unix
run_ms-ipo-client.sh

You may need to make the sh script executable. Do this by running the following 
command 

chmod a+x run_ms-ipo-client.sh


Data files
----------

Testing data files are included. These files were generated with the following 
auction target settings. Please configure your server appropriately when running 
the client files listed below. 


File Name   Max      Min      Share Pool      Number of Client  Analysis      
            Share    Share    Size            Transmissions     File          
            Price    Price                                                    
dca.txt     0        100      1000            50                dca-summary.txt
dcb.txt     0        100      10000           500               dcb-summary.txt
dcc.txt     0        100      100000          5000              dcc-summary.txt

The data file have been analyzed using a separate data analysis program with the 
settings given above. The summary data is given in the corresponding file.