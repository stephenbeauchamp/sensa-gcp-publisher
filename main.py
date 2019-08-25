import daemon
import time
import json
import os
import signal
from pathlib2 import Path
from google.cloud import pubsub_v1

with open('config/config.json') as config_file:
    config = json.load( config_file )

gcp_project_id = config['GCP_PROJECT_ID']
gcp_pubsub_topic_name = config['GCP_PUBSUB_TOPIC_NAME']
fld_src = config['MESSAGE_SOURCE_FOLDER']
fld_pro = config['MESSAGE_PROCESSING_FOLDER']
fld_err = config['MESSAGE_ERROR_FOLDER']
fld_arc = config['MESSAGE_ARCHIVE_FOLDER']
fle_prefix = config['MESSAGE_FILE_PREFIX']

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path( gcp_project_id, gcp_pubsub_topic_name )

futures = dict()

def log(msg):
    print(msg)

def main():
    log("INFO: starting application...")
    #//
    def get_callback( fut, file ):
        def callback( fut ):
            try:
                log( "INFO: response received for " + file + " " + fut.result() )
                os.rename( os.path.join( fld_pro, file ), os.path.join( fld_arc, file ) )
                futures.pop( file )
            except:
                log( 'ERROR: error processing file {} for {}.'.format( fut.exception(), file ) )
                os.rename( os.path.join( fld_pro, file ), os.path.join( fld_err, file ) )
                futures.pop( file )
        return callback
    #//
    while True:
        #// ARE THERE ANY NEW FILES? MOVE THEM TO PROCESSING.
        for file in os.listdir( fld_src ):
            if file.startswith( fle_prefix ):
                log('INFO: found new file ' + file )
                os.rename( os.path.join( fld_src, file ), os.path.join( fld_pro, file ) )
        time.sleep( .100 )
        #// PROCESS FILES
        for file in os.listdir( fld_pro ):
            if file.startswith( fle_prefix ):
                if file not in futures:
                    futures.update( { file: None } ) #// ADD THE FILE NAME TO THE EXPECTED RESPONSE QUEUE
                    msg = Path( os.path.join( fld_pro, file ) ).read_text()
                    future = publisher.publish( topic_path, data = msg.encode( 'utf-8' ) )
                    future.add_done_callback( get_callback( future, file ) )
                    log("INFO: sent publish request for " + file)
        #// RETRY ERROR FILES
        #// CLEAN UP ARCHIVES
        time.sleep( 5 )

def shutdown( signum, frame ):
    log('INFO: received shutdown signal...')
    sys.exit(0)

def daemon_main():
    log("INFO: starting daemon...")
    with daemon.DaemonContext(
      signal_map={
        signal.SIGTERM: shutdown,
        signal.SIGTSTP: shutdown
      }
    ):
        main()

if __name__ == "__main__":
    daemon_main()
