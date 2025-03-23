from langchain.prompts import ChatPromptTemplate

def get_route_safety_prompt() -> ChatPromptTemplate:
    template = """
    ### Input Data
    - Route Steps: {route_steps}
    
    Analyze the following route and provide safety insights and tips. Consider road conditions, traffic patterns, and general safety aspects.


    Please provide:
    1. General Insights about the route
    2. Safety Tips for different times of day
    3. Road conditions and traffic patterns
    4. Any specific areas of concern
    

    ### **Output Format**
    Return a valid JSON object following this structure:
    ```json
    {{
        "general_insights" : <general insights about the route>,
        "safety_tips" : <safety tips for different times of day>,
        "road_conditions" : <road conditions and traffic patterns>,
        "areas_of_concern" : <specific areas of concern>
    }}
    ```
    
    """
    
    return ChatPromptTemplate.from_template(template) 