import gradio as gr
from input_parser import parse_input_text
from ppt_generator import generate_presentation
from template_manager import load_template, get_layout_mapping, print_layouts
from layout_manager import LayoutManager
from config import Config
from logger import LOG  # 引入 LOG 模块
from generate_input_agent import GenerateInputAgent
import os


def generate_ppt(content):
    """
    根据用户输入的 content 生成 PPT，并返回 PPT 文件路径供下载。
    你可以在这里实现更复杂的 PPT 生成逻辑。
    """
    # 定义要保存的PPT文件名（此处每次提交都会覆盖同名文件）
    config = Config()  # 加载配置文件

    # 加载 PowerPoint 模板，并打印模板中的可用布局
    prs = load_template(config.ppt_template)  # 加载模板文件
    LOG.info("可用的幻灯片布局:")  # 记录信息日志，打印可用布局
    print_layouts(prs)  # 打印模板中的布局

    # 初始化 LayoutManager，使用配置文件中的 layout_mapping
    layout_manager = LayoutManager(config.layout_mapping)

    generate_input_agent = GenerateInputAgent()
    input_text = generate_input_agent.generate_input(content)

    # 调用 parse_input_text 函数，解析输入文本，生成 PowerPoint 数据结构
    powerpoint_data, presentation_title = parse_input_text(input_text, layout_manager)

    LOG.info(f"解析转换后的 ChatPPT PowerPoint 数据结构:\n{powerpoint_data}")  # 记录调试日志，打印解析后的 PowerPoint 数据

    parent_path = "outputs"
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)  # makedirs 会自动创建多级目录
        print(f"目录 {parent_path} 不存在，已自动创建。")
    else:
        print(f"目录 {parent_path} 已存在，无需创建。")
    # 定义输出 PowerPoint 文件的路径
    output_pptx = f"outputs/{presentation_title}.pptx"

    # 调用 generate_presentation 函数生成 PowerPoint 演示文稿
    generate_presentation(powerpoint_data, config.ppt_template, output_pptx)

    # 返回PPT文件路径，Gradio会自动生成下载链接
    return output_pptx


def build_interface():
    with gr.Blocks(title="ChatPPT") as demo:
        # 1. 网站介绍
        gr.Markdown("## 本网站使用AI大模型自动生成PPT")

        # 2. 文本输入框
        ppt_input = gr.Textbox(
            label="输入PPT内容描述",
            lines=5,
            placeholder="在此输入你想生成PPT的内容要点..."
        )

        # 3. 提交按钮
        submit_button = gr.Button("提交")

        # 下载文件输出组件（Gradio会根据返回的文件路径提供下载链接）
        ppt_output = gr.File(label="下载自动生成的PPT")

        # 点击提交后，将输入传给 generate_ppt，输出生成的文件
        submit_button.click(
            fn=generate_ppt,
            inputs=[ppt_input],
            outputs=[ppt_output]
        )
    return demo


if __name__ == "__main__":
    demo = build_interface()
    demo.launch()
