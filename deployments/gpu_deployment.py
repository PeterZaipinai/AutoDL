# gpu_deployment.py

from api.api_client import APIClient

REGION_SIGNS = {
    'westDC2': '西北企业区(推荐)',
    'southDC1': '华南企业区(推荐)',
    'suqianDC1': '宿迁企业区(推荐)',
    'beijingDC1': '北京A区',
    'wuhuDC1': '芜湖区',
    'neimengDC1': '内蒙A区',
    'beijingDC3': '北京C区',
    'foshanDC1': '佛山区',
    'westDC1': '西北A区'
}


# CUDA版本的值
# CUDA版本	cuda_v字段传参值（整型）	说明
# 11.1	    111	                    主机上GPU驱动支持的最高CUDA版本>=11.1的主机可调度
# 11.3	    113	                    主机上GPU驱动支持的最高CUDA版本>=11.3的主机可调度
# 11.8	    118	                    主机上GPU驱动支持的最高CUDA版本>=11.8的主机可调度
# 12.0	    120	                    主机上GPU驱动支持的最高CUDA版本>=12.0的主机可调度

class GPUDeploy:

    def __init__(self, api_key):
        self.api_client = APIClient(api_key)

    def get_image_list(self, page_index=1, page_size=10):
        params = {
            'page_index': page_index,
            'page_size': page_size
        }
        resp = self.api_client.post('/images/private/list', params=params)

        if resp['code'] == 'Success':
            return resp['data']['list']
        else:
            print(resp['msg'])
            return None

    def create_deployment(self, name, deployment_type, replica_num, region_sign,
                          gpu_name_set, cuda_v, num_gpus, memory_size_from,
                          memory_size_to, cpu_num_from, cpu_num_to,
                          image_uuid, cmd):

        data = {
            "name": name,
            "deployment_type": deployment_type,
            "replica_num": replica_num,
            "container_template": {
                "region_sign": region_sign,
                "gpu_name_set": gpu_name_set,
                "gpu_num": num_gpus,
                "cuda_v": cuda_v,
                "cpu_num_from": cpu_num_from,
                "cpu_num_to": cpu_num_to,
                "memory_size_from": memory_size_from,
                "memory_size_to": memory_size_to,
                "cmd": cmd,
                "price_from": 1,
                "price_to": 9999,
                "image_uuid": image_uuid,
            },
        }

        resp = self.api_client.post('/deployments', json=data)
        return resp['deployment_uuid']

    def get_deployment_list(self, page_index, page_size):

        params = {
            'page_index': page_index,
            'page_size': page_size
        }

        resp = self.api_client.post('/deployments/list', params=params)
        return resp['list']

    def get_container_list(self, deployment_uuid, page_index=1, page_size=10):

        params = {
            "deployment_uuid": deployment_uuid,
            "page_index": page_index,
            "page_size": page_size
        }

        resp = self.api_client.post('/deployments/containers', params=params)
        return resp['list']

    def scale_replicas(self, deployment_uuid, replica_num):

        data = {
            "deployment_uuid": deployment_uuid,
            "replica_num": replica_num
        }

        resp = self.api_client.put('/deployments/replicas', json=data)
        return resp['code'] == 'Success'

    def stop_container(self, container_uuid, decrease_replica=False):
        data = {
            "deployment_container_uuid": container_uuid,
            "decrease_one_replica_num": decrease_replica
        }
        resp = self.api_client.put("/deployments/containers/stop", json=data)
        return resp["code"] == "Success"

    def get_container_events(self, deployment_uuid, container_uuid=""):
        params = {
            "deployment_uuid": deployment_uuid,
            "deployment_container_uuid": container_uuid,
            "page_index": 1,
            "page_size": 10
        }
        resp = self.api_client.post("/container_events", params=params)
        return resp["list"]

    def stop_deployment(self, deployment_uuid):
        data = {
            "deployment_uuid": deployment_uuid,
            "operate": "stop"
        }
        resp = self.api_client.put("/deployments/operate", json=data)
        return resp["code"] == "Success"

    def delete_deployment(self, deployment_uuid):
        data = {
            "deployment_uuid": deployment_uuid
        }
        resp = self.api_client.delete("/deployments", json=data)
        return resp["code"] == "Success"
