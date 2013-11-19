import csv
import os
import datetime

def exportToCSV( simulationData , title ):

        # generate a unique fipame with a time stamp
        timeStamp = datetime.datetime.now().strftime( "%H-%M-%S%f-%m-%d-%Y" )
        script_dir = os.path.dirname( os.path.abspath(__file__) )
        dest_dir = os.path.join( script_dir, 'csv', 'simulations' )    
        
        try:
                os.makedirs(dest_dir)
        except OSError:
                pass # already exists

        csvPath = os.path.join( dest_dir, title + timeStamp + '.csv' )
        writeCSV = csv.writer( open( csvPath , "wb" ) )

        # write the columns
        writeCSV.writerow( [ "Desired Return", "Risk Tolerance", "Actual Return", "Actual Risk" ] )
        
        # write each row
        for index, simulationRound in enumerate( simulationData ):
                writeCSV.writerow( simulationData[ index ] )
