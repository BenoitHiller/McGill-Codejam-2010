SET MIG_PATH=.\
SET LOCAL_PATH=.\
REM C:\MSDE\lobaugj\tools\sunjdk\1.6.0_22\bin\java.exe -cp %MIG_PATH%\miglayout-3.7.3.1.jar;%MIG_PATH%\miglayout-3.7.3.1-swing.jar;%LOCAL_PATH%\ms-ipo-client.jar ms.mcgill.dutchipo.clientui.ClientMainFrame
java.exe -Xmx1024m -cp %MIG_PATH%\miglayout-3.7.3.1.jar;%MIG_PATH%\miglayout-3.7.3.1-swing.jar;%LOCAL_PATH%\ms-ipo-client.jar ms.mcgill.dutchipo.clientui.ClientMainFrame

