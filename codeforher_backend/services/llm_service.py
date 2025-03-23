from starlette import status
import os
from langchain.output_parsers import PydanticOutputParser

from codeforher_backend.models.config import ServiceConfig
from codeforher_backend.models.llm import RouteSafetyRequest, RouteSafetyResponse
from codeforher_backend.utils.helpers import raise_service_exception
from langchain.chat_models import AzureChatOpenAI
from codeforher_backend.prompt_templates.templates import get_route_safety_prompt


class LLMService:
    def __init__(self, service_config: ServiceConfig):
        """Initialize LLM Config"""
        self.llm_config = service_config.llm_config
        self.llm_client = self.get_llm()
    
    def get_llm(self) -> AzureChatOpenAI:
        return AzureChatOpenAI(
            api_key="3e33b1a703db4eaf800657cfff73e2db",
            openai_api_version="2024-02-01",
            azure_endpoint="https://dg-llm-service-dev.openai.azure.com/",
            azure_deployment="dg-llm-service-gpt-4o",
        )
        
    def get_route_safety(self, route_safety_request: RouteSafetyRequest) -> RouteSafetyResponse:
        """Get safety analysis for a route using LLM"""
        try:
            # Format route steps for the prompt
            route_text = "\n".join([
                f"{i+1}. {step.instructions} ({step.distance} • {step.duration})"
                for i, step in enumerate(route_safety_request.route_steps)
            ])
            
            
            
            # Get the chat prompt template
            prompt = get_route_safety_prompt()
            prompt_input = {"route_steps": route_text}
            
            parser = PydanticOutputParser(pydantic_object=RouteSafetyResponse)
            
            # Get the chain
            chain = prompt | self.llm_client | parser
            
            # Get the response
            response = chain.invoke(prompt_input)
            print(response.model_dump())
            return response.model_dump()
            
        except Exception as e:
            raise_service_exception(500, f"Failed to analyze route safety: {str(e)}")