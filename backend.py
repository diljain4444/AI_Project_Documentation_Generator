from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langgraph.graph import StateGraph,START,END
from langchain_core.prompts import PromptTemplate
from pydantic import Field,BaseModel
import os
from typing import TypedDict,Annotated,List,Optional
from langchain_core.output_parsers import PydanticOutputParser

hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
llm=HuggingFaceEndpoint(repo_id="Qwen/Qwen2.5-7B-Instruct",huggingfacehub_api_token=hf_token)
model=ChatHuggingFace(llm=llm)

class Section(BaseModel):
    heading:str
    content:List[str]

class doc_schema(BaseModel):
    title:str=Field(description="the title of the documentation")
    section:List[Section]="this will contain the list of all the sections"
class state(TypedDict):
    topic:Optional[str]
    context:Optional[str]
    all_headings:List[str]
    tone:str
    result:doc_schema
    file_path:str
    status:str

    

class decode_heading(BaseModel):
    headings:List[str]=Field(description="list of all the heading for the given content")
parser_decode=PydanticOutputParser(pydantic_object=decode_heading)
def decoder_node(state):
    if state.get("topic"):
        content=state["topic"]
    else:
        content=state["context"]
    tone=state["tone"]
    prompt=PromptTemplate(
        template="""
        You are a senior technical architect and professional documentation specialist.

Your task is to analyze the provided project input and design the most appropriate
documentation structure for it.

The project input may be:
- a short project topic, OR
- a detailed project description or context

You must dynamically determine which documentation sections are necessary
based on:
- the project domain and purpose
- system complexity
- technical depth
- intended audience

The tone of the documentation must strictly follow this user-defined tone:
{tone}
(Examples: Formal, Semi-Formal, Technical, Academic, Business-Oriented)

Guidelines:
- DO NOT use predefined or hardcoded documentation templates
- DO NOT reuse generic headings unless they are genuinely relevant
- Headings must be professional, meaningful, and specific to the project
- Prefer clarity over verbosity in section titles
- Avoid redundant or overlapping sections
- Decide the number of sections dynamically ( atleast typically 8-15 depending on complexity)
- Generate ONLY top-level section headings
- Do NOT generate content, explanations, summaries, or subheadings
- Return the output as a clean numbered list only, with no extra text
Project Input:
{project_input}
\n IMPORTANT NOTE->you must have to follow the given schema \n {format_instruction}

""",input_variables=["tone","project_input"],partial_variables={"format_instruction":parser_decode.get_format_instructions()}
    )    
    chain=prompt|model|parser_decode
    response=chain.invoke({"project_input":content,"tone":tone})

    return {"all_headings":response.headings}




parser=PydanticOutputParser(pydantic_object=doc_schema)

def topic_based(state):
    heading=state["all_headings"]
    final_heading=[f"-{head} \n "for head in heading]
    topic=state["topic"]
    tone=state["tone"]
    prompt=PromptTemplate(
        template="""
You are an expert technical documentation writer.

Your task is to generate a COMPLETE, PROFESSIONAL project documentation in given TONE->{tone}
based ONLY on the given project topic.always keep in mind to provide BIG and RELEVANT output

⚠️ VERY IMPORTANT OUTPUT RULES:
- You MUST return the output in STRICT JSON format
- The JSON MUST match the schema exactly
- Do NOT add explanations, comments, markdown, or extra text
- Do NOT wrap the output in ``` or any formatting
- Every section must be meaningful and detailed

- Generate detailed, in-depth explanations for every section.
- For each section, include multiple bullet points (at least 7–9) with examples, reasoning, or technical details.
- Add relevant subpoints if needed to clarify complex concepts.
- Assume the reader is a developer or stakeholder; provide professional and practical information.
- If the context or topic is small, expand it with general relevant knowledge and common practices in the field.


========================
CONTENT GUIDELINES
========================
- Title should be clear and professional
- Create MULTIPLE sections (minimum atleast 8–10 or according to user)
- Each section must have:
  - A clear heading
  - Multiple bullet-style content points (as list of strings)
- Use simple, professional, and technical language
- Assume the documentation is for developers and stakeholders

Recommended sections (you may add more if relevant):
{final_heading} \n

========================
PROJECT TOPIC
========================
{topic}

Now generate the documentation strictly according to the schema.
\n {format_instruction}
        
""",input_variables=["topic","tone","final_heading"],partial_variables={
    "format_instruction":parser.get_format_instructions()
} )
    
    chain=prompt|model|parser
    response=chain.invoke({"topic":topic,"tone":tone,"final_heading":final_heading})
    return {"result":response}


def context_based(state):
    context=state["context"]
    tone=state["tone"]
    heading=state["all_headings"]
    final_heading=[f"-{head} \n "for head in heading]
    prompt=PromptTemplate(

        template="""
    You are an expert technical documentation architect.

Your task is to CONVERT the given project context into a clean,
well-structured, and professional project documentation in given TONE->{tone}.always keep in mind to provide BIG and RELEVANT output

The input context may be unstructured, informal, incomplete, or very brief.

If the provided context is:
- Detailed → strictly organize and rewrite it
- Brief or insufficient → intelligently EXPAND it with reasonable,
  industry-standard assumptions that align with the topic

When adding information:
- Keep it realistic and commonly accepted
- Do NOT introduce advanced or speculative features
- Ensure all added information fits naturally into the documentation

⚠️ VERY IMPORTANT OUTPUT RULES:
- You MUST return the output in STRICT JSON format
- The JSON MUST match the schema exactly
- Do NOT add explanations, comments, markdown, or extra text
- Do NOT wrap the output in ``` or any formatting

- Generate detailed, in-depth explanations for every section.
- For each section, include multiple bullet points (at least 7–9) with examples, reasoning, or technical details.
- Add relevant subpoints if needed to clarify complex concepts.
- Assume the reader is a developer or stakeholder; provide professional and practical information.
- If the context or topic is small, expand it with general relevant knowledge and common practices in the field.



========================
STRUCTURING GUIDELINES
========================
- Derive the title from the context
- Group related ideas into logical sections
- Each section must include multiple concise bullet-style points
- Rewrite content in a professional, technical tone
- Avoid redundancy across sections

If context is minimal, you may introduce standard sections such as:
{final_heading}\n

========================
PROJECT CONTEXT
========================
{context}

Now generate the documentation strictly according to the schema.

\n {format_instruction} """,input_variables=["context","tone","final_heading"],partial_variables={"format_instruction":parser.get_format_instructions()}
)
    chain=prompt|model|parser
    response=chain.invoke({"context":context,"tone":tone,"final_heading":final_heading})
    return {"result":response}




from docx import Document
from datetime import datetime
import os
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def docx_generator(state):
    output=state["result"]
    doc=Document()

    p=doc.add_paragraph()
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    run=p.add_run(output.title)
    run.bold=True
    run.underline=True
    run.font.size=Pt(24)
    run.font.color.rgb=RGBColor(0, 51, 102)
    doc.add_paragraph()

    for section in output.section:
        doc.add_paragraph()
        s=doc.add_paragraph(style="List Number")
        run=s.add_run(section.heading)
        run.bold=True
        run.underline=True
        run.font.size=Pt(20)
        run.font.color.rgb=RGBColor(0, 0, 128)
        s.paragraph_format.space_after = Pt(6)

        
        for content in section.content:
            a=doc.add_paragraph(style="List Bullet")
            run=a.add_run(content)
            run.font.size=Pt(16)
            run.font.color.rgb=RGBColor(30,30,30)
            a.paragraph_format.space_before = Pt(4)
            a.paragraph_format.space_after = Pt(4)

                    
            

    filename = f"{output.title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    path=os.path.join("generated_docx",filename)
    os.makedirs("generated_docx", exist_ok=True)
    doc.save(path)
    return{"status":"done","file_path":path}
    


graph=StateGraph(state)
def condition(state):
    if(state.get("topic")):
        return "topic"
    else: return "context"


graph.add_node("topic",topic_based)
graph.add_node("doc",docx_generator)
graph.add_node("context",context_based)
graph.add_node("decode",decoder_node)
graph.add_edge(START,"decode")
graph.add_conditional_edges("decode", condition,({
    "topic":"topic","context":"context"
}))
graph.add_edge("topic","doc")
graph.add_edge("context","doc")
graph.add_edge("doc",END)

workflow=graph.compile()

