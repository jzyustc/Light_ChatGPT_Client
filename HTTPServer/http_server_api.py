import os
import json
from flask import Flask, request, send_file

def create_http_server(ip="0.0.0.0", port=8000, share_data_path="data/file_transfer_server_data.json"):
    app = Flask("HTTP Server")

    ######################
    ## 1. File Transfer ##
    ######################
    share_data = open(share_data_path, 'r')

    @app.route("/file_transfer/view")
    def file_transfer_view_path():
        # path : shared_folder/sub_path
        shared_folders = json.loads(share_data.read())
        shared_folder = shared_folders[request.args.get('shareId')]["path"]
        sub_path = request.args.get('sub')
        sub_path = "" if sub_path is None else sub_path

        shared_path = os.path.join(shared_folder, sub_path)
        if os.path.isfile(shared_path):
            return {"-1": os.path.split(sub_path)[1]}
        elif os.path.isdir(shared_path):
            sub_files = os.listdir(shared_path)
            sub_files = dict(zip(list(range(len(sub_files))), sub_files))
            return sub_files
        else :
            return {"error": "path not exist"}

    @app.route("/file_transfer/download")
    def file_transfer_download_path():
        # path : shared_folder/sub_path
        shared_folders = json.loads(share_data.read())
        shared_folder = shared_folders[request.args.get('shareId')]["path"]
        sub_path = request.args.get('sub')
        sub_path = "" if sub_path is None else sub_path

        shared_path = os.path.join(shared_folder, sub_path)
        if os.path.isfile(shared_path):
            return send_file(shared_path, as_attachment=True)
        elif os.path.isdir(shared_path):
            return {"error": "path is a folder"}
        else :
            return {"error": "path not exist"}


    app.run(host=ip, port=port)


if __name__ == '__main__':
    from multiprocessing import Process
    
    def test(c):
        import time
        print('test1', c)
        time.sleep(10)
        print('test2', c)

    p1 = Process(target=create_http_server, args=("0.0.0.0", 8000, "data/file_transfer_server_data.json"))
    p1.start()

    p2 = Process(target=test, args=('Python'))
    p2.start()
    
    process_list = [p1, p2]
    for p in process_list:
        p.join()

    print('end')