from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 导入提示模板相关类
import os

class GenerateInputAgent:

    def __init__(self):
        # 读取系统提示语，从文件中加载
        with open("prompts/formatter.txt", "r", encoding="utf-8") as file:
            self.system_prompt = file.read().strip()

        # 创建聊天提示模板，包括系统提示和消息占位符
        self.prompt = ChatPromptTemplate.from_messages([
             ("system", self.system_prompt),  # 系统提示部分
             ("human","{input_str}"),  # 消息占位符
        ])

        self.convert_agent = self.prompt | ChatOpenAI(model="gpt-4o-mini")

    def generate_input(self, origin_input):
        format_str = self.convert_agent.invoke({"input_str":origin_input}).content
        print(format_str)
        # file_path = os.path.join("inputs", 'parse.md')  # 构建文件路径
        # with open(file_path, 'w') as file:
        #     file.write(format_str)
        return format_str

if __name__ == "__main__":
    generate_agent = GenerateInputAgent()
    generate_agent.generate_input("""GitHub Sentinel 是专为大模型（LLMs）时代打造的智能信息检索和高价值内容挖掘 AI Agent。它面向那些需要高频次、大量信息获取的用户，特别是开源爱好者、个人开发者和投资人等。

主要功能
订阅管理：轻松管理和跟踪您关注的 GitHub 仓库。
更新检索：自动检索并汇总订阅仓库的最新动态，包括提交记录、问题和拉取请求。
通知系统：通过电子邮件等方式，实时通知订阅者项目的最新进展。
报告生成：基于检索到的更新生成详细的项目进展报告，支持多种格式和模板，满足不同需求。
多模型支持：结合 OpenAI 和 Ollama 模型，生成自然语言项目报告，提供更智能、精准的信息服务。
定时任务：支持以守护进程方式执行定时任务，确保信息更新及时获取。
图形化界面：基于 Gradio 实现了简单易用的 GUI 操作模式，降低使用门槛。
容器化：项目支持 Docker 构建和容器化部署，便于在不同环境中快速部署和运行。
持续集成：实现了完备的单元测试，便于进一步配置生产级 CI/CD 流程，确保项目的稳定性和高质量交付。
GitHub Sentinel 不仅能帮助用户自动跟踪和分析 GitHub 开源项目 的最新动态，还能快速扩展到其他信息渠道，如 Hacker News 的热门话题，提供更全面的信息挖掘与分析能力。""")
