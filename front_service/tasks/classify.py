import tensorflow as tf
import sys
import os
import time
import requests
import configuration

def local_classify(img):
    preds = {}
    # print(os.getcwd())

    # Just disables the warning, doesn't enable AVX/FMA
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    # Read in the image_data
    # image_data = tf.gfile.FastGFile("../images/" + img, 'rb').read()
    
    image_data = tf.gfile.FastGFile(img, 'rb').read()

    # image_data = img.read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("retrained_labels")]

    # Unpersists graph from file
    with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    # Feed the image_data as input to the graph and get first prediction
    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            # preds.append([human_string, score])
            preds[human_string] = score
        # print('%s (score = %.5f)' % (human_string, score))

    return preds

def remote_classify(size,start_time,image,img_name): 
    # img_name = image.name #'n1.jpg'
    # post_url = "http://0.0.0.0:8002/ca_tf/imageUpload/" + img_name
    # post_url = "http://10.0.0.4:8002/ca_tf/imageUpload/" + img_name
    post_url = configuration.classification_server + img_name
    json = {"size": size, "start_time": start_time}
    # files = {"file": image.open()} 
    files = {"file": open(image, "rb")}   
    print("Posting image to central server...") 
    try:
        preds = requests.post(post_url, files=files, data=json,timeout=10)  
        print("Central server OK, \nresults:" + preds.text)
    except requests.exceptions.ConnectionError:
        print("Central server NOT OK! No predictions returned")
        #preds = {"no":"response"}  
        return None  
    return preds.json()  

if __name__ == "__main__":
    img = sys.argv[1]
    preds = local_classify(img)
    print(preds)
