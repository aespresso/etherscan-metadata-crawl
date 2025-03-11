# Etherscan 地址元数据爬虫

这是一个简单的Python爬虫工具，用于从Etherscan获取以太坊地址的元数据信息，包括公共名称标签、ENS名称和标签。

## 功能

- 支持直接输入以太坊地址或完整URL
- 自动获取地址的公共名称标签（如 "Binance US 2"）
- 自动获取ENS名称（如 "c0ffeebabe.eth"）
- 自动获取地址标签（如 "White hat"、"Token Contract"等）
- 支持批量处理多个地址

## 环境要求

- Python 3.6+
- 依赖包：
  - requests
  - beautifulsoup4

## 安装

```bash
# 使用pip安装依赖
pip install requests beautifulsoup4

# 或使用Poetry安装依赖
poetry add requests beautifulsoup4
```

## 使用方法

```python
from etherscan_crawl import get_address_metadata

# 方法1：直接使用以太坊地址
metadata = get_address_metadata("0xc0ffeebabe5d496b2dde509f9fa189c25cf29671")

# 方法2：使用完整URL
metadata = get_address_metadata("https://etherscan.io/address/0xc0ffeebabe5d496b2dde509f9fa189c25cf29671")

print(metadata)
```

## 示例输出

```
地址: 0xc0ffeebabe5d496b2dde509f9fa189c25cf29671
元数据: {'ens_name': 'c0ffeebabe.eth', 'labels': ['White hat']}
```

## 批量处理示例

```python
addresses = [
    "0x3ddfa8ec3052539b6c9549f12cea2c295cff5296",
    "0x34ea4138580435B5A521E460035edb19Df1938c1",
    "0xc0ffeebabe5d496b2dde509f9fa189c25cf29671"
]

for address in addresses:
    metadata = get_address_metadata(address)
    print(f"地址: {address}")
    print(f"元数据: {metadata}")
    print("-" * 50)
    time.sleep(3)  # 添加延时避免请求过于频繁
```

## 注意事项

- 请合理控制爬取频率，避免对Etherscan服务器造成过大负担
- 爬取结果可能会随着Etherscan网站结构的变化而失效，需要定期更新爬虫代码
- 本工具仅供学习和研究使用，请遵守Etherscan的使用条款