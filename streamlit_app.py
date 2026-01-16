#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 Streamlit 实现的美元汇率转换网页应用
支持美元转换为人民币或日元
"""

import urllib.request
import json
import ssl
import streamlit as st


def get_exchange_rate(target_currency):
    """
    获取美元对目标货币的实时汇率
    使用免费的汇率 API 接口
    
    参数:
        target_currency: 目标货币代码，如 'CNY' 或 'JPY'
    
    返回:
        (rate, error_message): 汇率和错误信息（如果有）
    """
    # 默认汇率字典（如果API调用失败时使用）
    default_rates = {
        'CNY': 7.2,
        'JPY': 150.0
    }
    
    # 创建一个不验证 SSL 证书的上下文（为了解决某些系统的证书问题）
    # 实际生产环境中建议正确安装证书，而不是关闭验证
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        # 使用免费的汇率 API（exchangerate.host）
        url = f"https://api.exchangerate.host/latest?base=USD&symbols={target_currency}"

        # 使用 urllib 发送 HTTP 请求
        with urllib.request.urlopen(url, timeout=5, context=ctx) as response:
            data = json.loads(response.read().decode())
            rate = data["rates"][target_currency]
            return rate, None  # rate, error_message
    except Exception as e:
        # 返回错误信息，并使用默认汇率
        default_rate = default_rates.get(target_currency, 1.0)
        return default_rate, f"获取实时汇率失败：{e}（已使用默认汇率 {default_rate}，仅供参考）"


def main():
    # 设置页面标题
    st.set_page_config(page_title="美元汇率转换工具", page_icon="💱")

    # 页面标题和说明
    st.title("💱 美元汇率转换工具")
    st.write("请输入美元金额，选择目标货币，程序会获取实时汇率并转换。")

    # 币种选择器
    target_currency = st.selectbox(
        "选择目标货币：",
        options=["CNY", "JPY"],
        format_func=lambda x: "人民币 (CNY)" if x == "CNY" else "日元 (JPY)"
    )

    # 输入组件：美元金额（允许负数输入，以便后续检查）
    usd_amount = st.number_input(
        "请输入美元金额：",
        value=100.0,
        step=1.0,
        format="%.2f",
    )

    # 检查是否为负数
    if usd_amount < 0:
        st.error("❌ 错误：不能输入负数！请输入大于等于 0 的金额。")
        return  # 如果是负数，直接返回，不执行转换

    # 点击按钮进行转换
    if st.button("开始转换"):
        with st.spinner("正在获取实时汇率，请稍候..."):
            rate, error_msg = get_exchange_rate(target_currency)

        # 如果有错误信息，给出提示
        if error_msg:
            st.warning(error_msg)

        # 计算目标货币金额
        converted_amount = usd_amount * rate

        # 根据币种选择显示符号和名称
        currency_info = {
            "CNY": {"symbol": "¥", "name": "人民币"},
            "JPY": {"symbol": "¥", "name": "日元"}
        }
        
        currency_symbol = currency_info[target_currency]["symbol"]
        currency_name = currency_info[target_currency]["name"]

        # 显示结果
        st.success("转换完成！")
        st.write(f"**美元金额：** ${usd_amount:.2f}")
        st.write(f"**当前汇率：** 1 USD = {rate:.4f} {target_currency}")
        st.write(f"**{currency_name}金额：** {currency_symbol}{converted_amount:,.2f}")


if __name__ == "__main__":
    main()