import requests
import base64
from config import BAIDU_API_KEY, BAIDU_SECRET_KEY, BAIDU_API_URL

class BaiduAI:
    def __init__(self):
        self.api_key = BAIDU_API_KEY
        self.secret_key = BAIDU_SECRET_KEY
        self.access_token = None

    def get_access_token(self):
        """获取百度AI的access_token"""
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key
        }
        try:
            response = requests.post(url, params=params)
            result = response.json()
            if 'access_token' in result:
                self.access_token = result['access_token']
                return self.access_token
            raise Exception(f"获取access_token失败: {result.get('error_description', '未知错误')}")
        except Exception as e:
            raise Exception(f"获取access_token时出错: {str(e)}")

    def recognize_image(self, image_path):
        """使用百度通用图像识别API识别图片"""
        try:
            # 如果没有access_token，先获取
            if not self.access_token:
                self.get_access_token()

            # 读取图片文件
            with open(image_path, 'rb') as f:
                image = base64.b64encode(f.read())

            # 请求参数
            params = {
                "access_token": self.access_token,
                "baike_num": 1  # 返回百科信息
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                "image": image
            }

            # 发送请求
            response = requests.post(BAIDU_API_URL, params=params, headers=headers, data=data)
            result = response.json()

            if 'error_code' in result:
                raise Exception(f"识别失败: {result.get('error_msg', '未知错误')}")

            # 处理识别结果
            if 'result' in result and result['result']:
                # 获取前5个结果
                top_results = result['result'][:5]
                
                # 处理每个结果，添加百科信息
                processed_results = []
                for item in top_results:
                    result_item = {
                        'name': item['keyword'],
                        'score': item['score'] / 100.0,  # 转换为0-1的置信度
                        'description': ''
                    }
                    
                    # 如果有百科信息，添加描述
                    if 'baike_info' in item:
                        result_item['description'] = item['baike_info'].get('description', '')
                    
                    processed_results.append(result_item)

                # 返回结果
                return {
                    'name': processed_results[0]['name'],  # 最可能的结果
                    'confidence': processed_results[0]['score'],
                    'description': processed_results[0]['description'],
                    'all_results': processed_results
                }
            else:
                raise Exception("未找到识别结果")

        except Exception as e:
            raise Exception(f"识别过程出错: {str(e)}")

    def get_all_results(self, image_path):
        """获取所有识别结果"""
        result = self.recognize_image(image_path)
        return result.get('all_results', []) 