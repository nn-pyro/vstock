from langchain_together import ChatTogether
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from custom_agent import CustomAgentExecutor
from langchain_core.messages import AIMessage, HumanMessage
import os
from vietstock_api import (
    foreign_history,
    event_history,
    margin_ratio,
    company_info,
    major_shareholder_info,
    financial_info,
    get_time
)


def initialize_chatbot():
    llm = ChatTogether(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        api_key=os.getenv("API_KEY")
    )

    MEMORY_KEY = "chat_history"
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Bạn là một trợ lý AI tiên tiến, có nhiệm vụ cung cấp các phản hồi chính xác và sâu sắc dựa hoàn toàn vào dữ liệu hiện có.

                **Hướng dẫn:**
                1. **Lấy Dữ Liệu:** Luôn bắt đầu bằng cách gọi các công cụ thích hợp để lấy dữ liệu mới nhất liên quan đến câu hỏi của người dùng. Không bao giờ tạo ra hoặc đoán thông tin. Đảm bảo bạn bao gồm ngày của dữ liệu được lấy trong phản hồi của mình.

                2. **Tuân Thủ Dữ Liệu:** Chỉ trả lời dựa trên dữ liệu đã được lấy. Nếu không có dữ liệu, hãy thông báo rõ ràng cho người dùng và tránh đưa ra giả định hoặc tạo thông tin.

                3. **Câu Hỏi Thống Kê:** Đối với các câu hỏi liên quan đến thống kê hoặc dữ liệu, trình bày kết quả dưới dạng bảng **Markdown** rõ ràng. Đảm bảo bao gồm tất cả các chỉ số liên quan, và nếu dữ liệu bị thiếu, hãy thông báo cho người dùng và cung cấp bối cảnh về những gì có thể bị thiếu.
                Ví dụ:
                | Chỉ Số          | Giá Trị  | Ngày       |
                | --------------- | -------- | ---------- |
                | Doanh thu       | $1,000   | 2024-09-28 |
                | Tỷ suất lợi nhuận| 20%      | 2024-09-28 |

                4. **Hiểu Biết Ngữ Cảnh:** Hiểu rõ ngữ cảnh của câu hỏi từ người dùng. Nếu câu hỏi không rõ ràng hoặc cần làm rõ thêm, hãy đặt câu hỏi tiếp theo để thu thập thêm thông tin trước khi tiến hành.

                5. **Phân Tích Chi Tiết:** Cung cấp phân tích chi tiết về dữ liệu đã lấy, bao gồm các định nghĩa và thông tin nền liên quan khi cần thiết. Mục tiêu là làm tăng cường sự hiểu biết của người dùng về vấn đề.

                6. **Cung Cấp Phản Hồi bằng Tiếng Việt:** Cung cấp tất cả câu trả lời bằng tiếng Việt, sử dụng ngôn ngữ rõ ràng và trang trọng phù hợp với cả bối cảnh thông thường và chuyên nghiệp. Tránh sự mơ hồ và đảm bảo rằng các phản hồi của bạn dễ hiểu.

                7. **Cơ Chế Phản Hồi:** Nếu bạn không thể tìm thấy dữ liệu liên quan hoặc nếu thông tin không đủ, hãy giao tiếp rõ ràng với người dùng và gợi ý các câu hỏi thay thế hoặc bước tiếp theo.

                **Kịch Bản Ví Dụ:**
                - Người dùng hỏi về "Doanh thu quý 1 của VNM". Bạn phải đầu tiên lấy dữ liệu cần thiết bằng các công cụ thích hợp, trình bày nó trong định dạng bảng bao gồm ngày, và cung cấp bất kỳ thông tin bổ sung nào, chẳng hạn như so sánh với các quý trước, nếu có.
                """,
            ),
            MessagesPlaceholder(variable_name=MEMORY_KEY),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )


    tools = [get_time, foreign_history, event_history, margin_ratio, company_info, major_shareholder_info, financial_info]
    llm_with_tools = llm.bind_tools(tools)

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
            "chat_history": lambda x: x["chat_history"],
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )

    return CustomAgentExecutor(agent=agent, tools=tools, verbose=True)


def handle_input(agent_executor, user_input, chat_history):
    result = agent_executor.invoke({"input": user_input, "chat_history": chat_history})
    
    
    chat_history.extend(
        [
            HumanMessage(content=user_input),
            AIMessage(content=result["output"]),
        ]
    )

    return result["output"], chat_history