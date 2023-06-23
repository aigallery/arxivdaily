import requests
import json
from utils.AuthV3Util import addAuthParams
import os

# 您的应用ID
APP_KEY = os.getenv("YOUDAO_TRANSLATE_APP_KEY") 
# 您的应用密钥
APP_SECRET = os.getenv("YOUDAO_TRANSLATE_APP_SECRET")


def createRequest(content: str) -> str:
    '''
    note: 将下列变量替换为需要请求的参数
    '''
    q = content #"<p>Decision support systems for classification tasks are predominantly designed to predict the value of the ground truth labels. However, since their predictions are not perfect, these systems also need to make human experts understand when and how to use these predictions to update their own predictions. Unfortunately, this has been proven challenging. In this context, it has been recently argued that an alternative type of decision support systems may circumvent this challenge. Rather than providing a single label prediction, these systems provide a set of label prediction values constructed using a conformal predictor, namely a prediction set, and forcefully ask experts to predict a label value from the prediction set. However, the design and evaluation of these systems have so far relied on stylized expert models, questioning their promise. In this paper, we revisit the design of this type of systems from the perspective of online learning and develop a methodology that does not require, nor assumes, an expert model. Our methodology leverages the nested structure of the prediction sets provided by any conformal predictor and a natural counterfactual monotonicity assumption on the experts' predictions over the prediction sets to achieve an exponential improvement in regret in comparison with vanilla bandit algorithms. We conduct a large-scale human subject study ($n = 2{,}751$) to verify our counterfactual monotonicity assumption and compare our methodology to several competitive baselines. The results suggest that decision support systems that limit experts' level of agency may be practical and may offer greater performance than those allowing experts to always exercise their own agency. </p>"
    lang_from = 'en'
    lang_to = 'zh-CHS'
    vocab_id = 'A52B90D9C31B49FBB309183FEC879956'

    data = {'q': q, 'from': lang_from, 'to': lang_to, 'vocabId': vocab_id}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/api', header, data, 'post')
    dict_data = json.loads(res.content.decode('utf-8'))
    res = dict_data.get("translation")
    return res


def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)

# 网易有道智云翻译服务api调用demo
# api接口: https://openapi.youdao.com/api
if __name__ == '__main__':
    createRequest()
