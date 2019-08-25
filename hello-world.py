import time
import json
from google.cloud import pubsub_v1

with open('config/config.json') as config_file:
    config = json.load( config_file )

gcp_project_id = config['GCP_PROJECT_ID']
gcp_pubsub_topic_name = config['GCP_PUBSUB_TOPIC_NAME']

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path( gcp_project_id, gcp_pubsub_topic_name )

futures = dict()

def main():

    def get_callback( fut, data ):
        def callback( fut ):
            try:
                print( "publish callback " + fut.result() )
                futures.pop( data )
            except:
                print( 'Please handle {} for {}.'.format( fut.exception(), data ) )
        return callback



    for i in range( 3 ):
        data = str( i )
        futures.update( { data: None } )
        future = publisher.publish( topic_path, data = data.encode( 'utf-8' ) )
        future.add_done_callback( get_callback( future, data ) )

    while futures:
        time.sleep( 5 )
