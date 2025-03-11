import requests
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def get_address_metadata(address):
    """
    获取以太坊地址的元数据信息
    
    参数:
    address -- 以太坊地址，可以是完整URL或仅地址字符串
    
    返回:
    包含地址元数据的字典
    """
    # 检查输入是否为完整URL，如果不是则组装
    if address.startswith('http'):
        url = address
    else:
        # 直接使用输入的地址，保留0x前缀
        url = f"https://etherscan.io/address/{address}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("获取页面失败: ", response.status_code)
        return None, None, None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 获取元数据
    metadata = {}
    
    # 获取公共名称标签（如 "Binance US 2"）
    public_name_tag = None
    summary_section = soup.find('section', id='ContentPlaceHolder1_divSummary')
    if summary_section:
        # 查找第一个带有hash-tag类的span标签，通常是公共名称标签
        first_badge = summary_section.find('a', class_='badge')
        if first_badge:
            span_tag = first_badge.find('span', class_='hash-tag')
            if span_tag:
                public_name_tag = span_tag.text.strip()
                metadata['public_name_tag'] = public_name_tag
    
    # 获取ENS名称
    ens_name = None
    if summary_section:
        ens_div = summary_section.find('div', id='ensName')
        if ens_div:
            # 尝试直接获取文本
            ens_text = ens_div.get_text(strip=True)
            if ens_text:
                # 清理文本，只保留ENS名称
                if '.eth' in ens_text:
                    ens_name = ens_text.split('.eth')[0] + '.eth'
                    metadata['ens_name'] = ens_name
    
    # 获取标签（如 "Binance"）
    labels = []
    labels_div = None
    if summary_section:
        labels_div = summary_section.find('div', id='ContentPlaceHolder1_divLabels')
    
    if labels_div:
        # 查找所有标签，包括a标签和span标签
        label_elements = labels_div.find_all(['a', 'span'], class_='badge')
        for element in label_elements:
            span_tag = element.find('span', class_='hash-tag')
            if span_tag:
                label_text = span_tag.text.strip()
                labels.append(label_text)
    
    metadata['labels'] = labels
    
    return metadata

# 使用示例
if __name__ == "__main__":
    # 可以直接输入地址
    addresses = [
        "0x3ddfa8ec3052539b6c9549f12cea2c295cff5296",
        "0x34ea4138580435B5A521E460035edb19Df1938c1",
        "0xc0ffeebabe5d496b2dde509f9fa189c25cf29671",
        "0x4838b106fce9647bdf1e7877bf73ce8b0bad5f97",
        "0x8aebf766fc6b1199d85c8257c847a1d98682121a",
        "0x388c818ca8b9251b393131c08a736a67ccb19297",
        "0xf17e65822b568b3903685a7c9f496cf7656cc6c2"
    ]

    for address in addresses:
        metadata = get_address_metadata(address)
        print(f"地址: {address}")
        print(f"元数据: {metadata}")
        print("-" * 50)
        time.sleep(3)