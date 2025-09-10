# Getting the API Key from env file
import os
from dotenv import load_dotenv
load_dotenv()

# Importing Groq
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

from langgraph.checkpoint.memory import MemorySaver  # Conversation History 
from langgraph.graph import START, MessagesState, StateGraph
# Stategraph - Class for graphs/nodes

# For chatbot templates on how it responds etc (system_instr)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

model = ChatGroq(model="llama-3.1-8b-instant" , api_key=os.getenv("GROQ_API_KEY"))

# response = model.invoke(
#     [
#         HumanMessage(content="Hello, I am Bob!")
#     ]
# )

predefined_bot_personas = {
    "default" : "",
    "precise" : "Generate precise, apt responses. Keep the word limit short",
    "pirate" : "You talk like a pirate. Answer all questions to the best of your ability." , 
    "roast" : "Always responds with witty or sarcastic roasts, no matter what the user says." , 
    "shakespeare" : "Responds to all queries in old-English, Shakespeare-style prose. Keep it slightly reader-friendly" , 
    "emoji" : "Emoji Translator Bot: Converts everything into emoji-speak." , 
    "introvert" : "You are an introvert. Talk as less as possible, be socially awkward and autistic" , 
    "yoda" : "Talk like Yoda from Star Wars. Rearrange sentences and sound wise and mysterious." , 
    "socratic": "Never answer directly. Only respond with thoughtful questions that guide the user to figure out the answer themselves.",
    

}


# Making each app with the specific bot persona style
bot_personas = {}

def init_chatbot_style(persona: str):


    # Defining a new graph
    workflow = StateGraph(state_schema=MessagesState)

    # Defining a prompt for our model
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                predefined_bot_personas[persona],  # FIXED: use actual persona text
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    # Defining a function to call the model
    def call_model(state: MessagesState):
        prompt = prompt_template.invoke(state)
        response = model.invoke(prompt)
        return {"messages": [response]}  # FIXED: wrap in list


    workflow.add_edge(START , "model")
    workflow.add_node("model" , call_model)

    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    bot_personas[persona] = app
    return app

#************************************************************************************************************************************************

# Deleting the chat history whenever called
def clear_persona_history(persona: str):
    del bot_personas[persona]

#************************************************************************************************************************************************

def response(user_input: str , past_messages , persona: str):

    if persona not in bot_personas:   # FIXED: don’t reinit every time
        app = init_chatbot_style(persona)
    else:
        app = bot_personas[persona]

    config = {"configurable" : {"thread_id" : f"{persona}"}}

    input_messages = [HumanMessage(content=user_input)]
    output = app.invoke({"messages" : input_messages} , config)  # FIXED: no need for past_messages

    return output["messages"]


#************************************************************************************************************************************************

# if __name__ == "__main__":
    
#     while True:
#         query = input("You: ")

#         if query == "exit":
#             break

#         input_messages = [HumanMessage(content = query)]
        
#         # output = app.invoke({"messages": input_messages}, config)
#         # output["messages"][-1].pretty_print()

#         for chunk, metadata in app.stream(
#             {"messages": input_messages},
#             stream_mode="messages",
#         ):
#             if isinstance(chunk, AIMessage):  # Filter to just model responses
#                 print(chunk.content, end="")

#         print()
