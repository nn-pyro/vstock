from pydantic import PrivateAttr
from langchain.agents import AgentExecutor
from langchain_core.messages import AIMessage
from datetime import datetime 


class CustomAgentExecutor(AgentExecutor):
    _get_time_called: bool = PrivateAttr(default=False)

    def invoke(self, inputs):
        
        if not self._get_time_called:
            time_result = self.tools[0].run({})  

            
            if isinstance(time_result, datetime):
                time_result = time_result.strftime("%Y-%m-%d %H:%M:%S")

            self._get_time_called = True

            
            inputs["chat_history"].append(AIMessage(content=time_result))
        
        
        return super().invoke(inputs)