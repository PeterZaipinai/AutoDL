# main.py
from containers.container import Container
from deployments.gpu_deployment import GPUDeploy

API_TOKEN = "xxxx"  # API Token
IMAGE_UUID = "xxxx"  # 镜像UUID
REGION_SIGN = "neimengDC1"
GPU_NAME_SET = [
    "RTX A5000"
]
NUM_GPUS = 1
CUDA_VERSION = 118
CPU_NUM = 15
MEMORY_SIZE_FORM = 1
MEMORY_SIZE_TO = 256
CPU_NUM_FORM = 1
CPU_NUM_TO = 128

init_cmd = """
bash /root/tzwm-autodl-sd-webui/common/scripts/init-download.sh &&
source /root/tzwm-autodl-sd-webui/common/scripts/init-proxy.sh global &&  
bash /root/tzwm-autodl-sd-webui/a1111-pack/scripts/restart-webui.sh
"""

# 在init_cmd后面添加sleep infinity
CMD = f"{init_cmd} && sleep infinity"  # 保证容器不会退出

deploy = GPUDeploy(API_TOKEN)

images = deploy.get_image_list()
if images:
    print(images)
else:
    print("获取镜像失败")

# 创建部署,获取部署UUID
uuid = deploy.create_deployment(
    name="弹性部署",
    deployment_type="ReplicaSet",
    region_sign=REGION_SIGN,
    gpu_name_set=GPU_NAME_SET,
    cuda_v=CUDA_VERSION,
    num_gpus=NUM_GPUS,
    memory_size_from=MEMORY_SIZE_FORM,
    memory_size_to=MEMORY_SIZE_TO,
    cpu_num_from=CPU_NUM_FORM,
    cpu_num_to=CPU_NUM_TO,
    image_uuid=IMAGE_UUID,
    cmd=CMD
)

deploy_list = deploy.get_deployment_list(1, 50)
print(deploy_list)

# # 停止部署
# deploy.stop_deployment(uuid)
#
# # 删除部署
# deploy.delete_deployment(uuid)


# # 初始化部署对象
# deploy = GPUDeploy(API_TOKEN)
# images = deploy.get_image_list()
# if images:
#     print(images)
# else:
#     print("获取镜像失败")
#
# # 创建部署,获取部署UUID
# uuid = deploy.create_deployment(...)
#
# deploy_list = deploy.get_deployment_list(1, 10)
#
# # 获取容器列表
# containers = deploy.get_container_list(uuid)
#
# # 操作容器
# for c in containers:
#     container = Container(deploy, c.uuid)
#     container.stop()
#
# deploy.stop_deployment(uuid)
#
# # 删除部署
# deploy.delete_deployment(uuid)
