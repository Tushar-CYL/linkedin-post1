# import streamlit as st
# import requests
# import json
# import os
# import time

# # Set page configuration
# st.set_page_config(
#     page_title="LinkedIn Post Generator with MCP",
#     page_icon="📝",
#     layout="wide"
# )

# # Styling
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 2.5rem;
#         font-weight: bold;
#         color: #0A66C2;
#         margin-bottom: 1rem;
#     }
#     .sub-header {
#         font-size: 1.5rem;
#         font-weight: bold;
#         color: #0A66C2;
#         margin-top: 1rem;
#     }
#     .process-step {
#         background-color: #f0f2f5;
#         border-radius: 10px;
#         padding: 15px;
#         margin: 10px 0;
#     }
#     .step-title {
#         font-weight: bold;
#         color: #0A66C2;
#     }
#     .final-post {
#         background-color: #e6f3ff;
#         border-left: 5px solid #0A66C2;
#         padding: 15px;
#         border-radius: 5px;
#     }
# </style>
# """, unsafe_allow_html=True)

# # App title and description
# st.markdown("<div class='main-header'>LinkedIn Post Generator with MCP</div>", unsafe_allow_html=True)
# st.markdown("""
# This app uses a Multi-agent Collaborative Protocol (MCP) to generate high-quality LinkedIn posts:

# 1. **Brief Writing Agent** (OpenAI) - Creates a structured content brief
# 2. **Research Agent** (Perplexity) - Gathers relevant information and data
# 3. **Strategy Agent** (OpenAI) - Develops content strategy and approaches
# 4. **First Draft Writer** (OpenAI) - Creates initial post drafts
# 5. **LinkedIn Content Expert** (OpenAI) - Polishes drafts into final posts
# """)

# # Sidebar for API settings
# with st.sidebar:
#     st.markdown("### API Configuration")
    
#     # OpenAI API settings
#     st.markdown("#### OpenAI API")
#     openai_api_key = st.text_input("OpenAI API Key", type="password")
#     openai_model = st.selectbox(
#         "OpenAI Model",
#         ["gpt-4-turbo", "gpt-4o", "gpt-4", "gpt-3.5-turbo"],
#         index=0
#     )
    
#     # Perplexity API settings
#     st.markdown("#### Perplexity API")
#     perplexity_api_key = st.text_input("Perplexity API Key", type="password")
#     perplexity_model = st.selectbox(
#         "Perplexity Model",
#         ["pplx-7b-online", "pplx-70b-online", "mixtral-8x7b-online", "sonar"],
#         index=0
#     )
    
#     # User persona settings
#     st.markdown("#### Your LinkedIn Persona")
#     industry = st.selectbox(
#         "Industry",
#         ["Technology", "Marketing", "Finance", "Healthcare", "Education", 
#          "Human Resources", "Sales", "Manufacturing", "Consulting", "Other"]
#     )
#     job_role = st.text_input("Job Role", placeholder="e.g., Marketing Manager, CEO, Software Engineer")
#     writing_style = st.selectbox(
#         "Preferred Writing Style",
#         ["Professional", "Conversational", "Thought Leadership", "Story-based", 
#          "Data-driven", "Inspirational", "Educational"]
#     )
#     user_onboarding_info = f"Industry: {industry}\nJob Role: {job_role}\nWriting Style: {writing_style}"

# # Helper functions for API calls
# def call_openai_api(prompt, system_prompt, model=openai_model):
#     if not openai_api_key:
#         st.error("Please enter your OpenAI API key")
#         return None
        
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {openai_api_key}"
#     }
    
#     payload = {
#         "model": model,
#         "messages": [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": prompt}
#         ],
#         "temperature": 0.7
#     }
    
#     try:
#         response = requests.post(
#             "https://api.openai.com/v1/chat/completions",
#             headers=headers,
#             json=payload
#         )
#         response.raise_for_status()
#         return response.json()["choices"][0]["message"]["content"]
#     except Exception as e:
#         st.error(f"Error calling OpenAI API: {str(e)}")
#         return None

# def call_perplexity_api(prompt, model=perplexity_model):
#     if not perplexity_api_key:
#         st.error("Please enter your Perplexity API key")
#         return None
        
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {perplexity_api_key}"
#     }
    
#     payload = {
#         "model": model,
#         "messages": [
#             {"role": "user", "content": prompt}
#         ]
#     }
    
#     try:
#         response = requests.post(
#             "https://api.perplexity.ai/chat/completions",
#             headers=headers,
#             json=payload
#         )
#         response.raise_for_status()
#         return response.json()["choices"][0]["message"]["content"]
#     except Exception as e:
#         st.error(f"Error calling Perplexity API: {str(e)}")
#         return None

# # MCP Process Steps
# def run_brief_writing_agent(user_idea):
#     system_prompt = """# Role and Objective

# You are a Brief Writing Agent in a LinkedIn content creation workflow. Your task is to take a raw idea or topic from the user and convert it into a detailed content brief that can be used in future steps — including research and post writing.

# # Instructions

# - Structure the user's idea into a complete, actionable brief.
# - Clearly identify the core topic and any supporting subtopics or themes.
# - Infer missing but useful research angles like industry focus, geography, or target persona if not explicitly mentioned.
# - Include what kind of data might support the idea: stats, case studies, trends, opinions, etc.
# - Ensure that the brief is useful enough for a Research Agent to find real-time, relevant information.

# # Output Format

# **Content Brief**

# - **Core Idea / Topic**:  
# - **Primary Keyword / Theme**:  
# - **Supporting Subtopics (if any)**:  
# - **Target Audience or Persona**:  
# - **Relevant Industries / Sectors (if any)**:  
# - **Geographic Focus (if any)**:  
# - **Intent / Purpose of the Post**:  
# - **Preferred Tone**:  
# - **Post Length Preference**:  
# - **Desired Hook / Angle**:  
# - **Call-to-Action**:  
# - **Data Preferences** (e.g. stats, recent trends, case studies, quotes):  
# - **Additional Notes / Style Cues**:  
# """
    
#     user_prompt = f"""Here's an idea I'm thinking about turning into a LinkedIn post. Can you help me structure it into a proper brief that other agents can use to write the content?

# **Raw Idea:**  
# {user_idea}

# Feel free to infer tone, keyword, or structure if it's not clearly mentioned — just don't go overboard. I want something that's detailed enough for a writer to understand what kind of post I'm going for."""

#     return call_openai_api(user_prompt, system_prompt)

# def run_research_agent(content_brief):
#     system_prompt = """# Role and Objective

# You are a Research Agent in a LinkedIn content workflow. Your task is to go on the internet and find the latest, most relevant and credible information related to the topic and keyword provided in the brief.

# # Instructions

# - Extract the primary keyword, topic, and any additional context from the brief.
# - Search for relevant, *recent* content across credible sources like industry journals, news platforms, research databases, company blogs, and thought leader content.
# - Prioritize:
#   - Authenticity: Only use reputable sources (e.g. HBR, McKinsey, Statista, TechCrunch, etc.).
#   - Freshness: Prefer content published within the last 12 months unless otherwise relevant.
#   - Relevance: Information must align closely with the brief's core idea, tone, and audience.

# # Types of Content to Look For

# - Statistics, metrics, or market data  
# - Real case studies or brand examples  
# - Quotes or insights from credible people  
# - Emerging trends or hot takes on the topic  
# - Contrasting opinions if relevant

# # Output Format

# **Research Summary for LinkedIn Post**

# - **Topic Searched**:  
# - **Summary of Findings**: (2–3 paragraphs max)  
# - **Key Statistics / Data Points**:  
# - **Relevant Case Studies / Examples**:  
# - **Insights / Trends Observed**:  
# - **Sources Used with Links**:  

# Do not generate your opinion. Only summarize research. Avoid filler language. Keep it concise and insightful."""

#     user_prompt = f"""Here is the content brief that needs to be researched on. Please find the most recent and credible information available on the internet that supports or adds depth to the topic mentioned.

# **Content Brief:**  
# {content_brief}

# Focus on collecting:
# - Real data and stats
# - Valid case studies or examples
# - Recent news or trend analysis
# - Links to credible sources

# Avoid generic advice — only include what can be verified online."""

#     return call_perplexity_api(user_prompt)

# def run_strategy_agent(content_brief, research_summary, user_onboarding_info):
#     system_prompt = """# Role and Objective

# You are a Strategy Agent in a LinkedIn content creation workflow. Your responsibility is to create a detailed Content Strategy based on the Content Brief, Research Summary, and User Onboarding Preferences. This strategy will guide the writing agent on how to craft multiple styles of LinkedIn posts that feel personalized and aligned with the user's taste and persona.

# # Instructions

# - Analyze the Content Brief and Research Summary carefully.
# - Retrieve and incorporate User Onboarding Information such as:
#   - User's preferred post styles or examples
#   - Desired tone (professional, casual, witty, bold)
#   - User's industry, job role, and persona
# - Identify the **most suitable content pillar** (e.g., personal branding, thought leadership, case study, testimonial, hiring post, announcement, etc.).
# - Define the **content style and tone** based on both the user's persona and the post's purpose.
# - Design **3 different strategic directions** for posts:
#   - Vary the intent (e.g., inspire, educate, engage, invite action).
#   - Vary the use of CTA (some posts should have CTA, some should not).
#   - Ensure the posts feel distinctly different from each other — not just reworded.
# - Recommend **hook styles** that are short, dramatic, or curiosity-inducing.
# - Recommend **CTA styles** (or suggest if no CTA is needed).
# - Set universal **content writing guidelines**:
#   - Use short, easy-to-skim sentences.
#   - Maintain clean formatting with proper line breaks.
#   - Focus on one core message per post.
#   - Maintain voice consistency aligned with user's selected style.

# # Output Format

# **Content Strategy for LinkedIn Post**

# - **Content Pillar**:  
# - **Primary Tone Recommendation**:  
# - **Persona Alignment**: (briefly describe how it reflects user's industry/persona)
# - **Post Length Recommendation**:  
# - **Three Strategic Directions for Post Writing**:
#   - **Post 1**: (Tone, Hook Idea, CTA Idea, Intent)
#   - **Post 2**: (Tone, Hook Idea, CTA Idea, Intent)
#   - **Post 3**: (Tone, Hook Idea, CTA Idea, Intent)
# - **Suggested Hook Styles**:  
# - **Suggested CTA Styles**:  
# - **General Content Writing Guidelines**:
#   - Short sentences
#   - Clear formatting
#   - Voice consistency
#   - Focused core message"""

#     user_prompt = f"""Here's the Content Brief, Research Summary, and the User's Onboarding Preferences for a LinkedIn post idea. Based on these, please create a complete LinkedIn Content Strategy to guide the post writing.

# **Content Brief:**  
# {content_brief}

# **Research Summary:**  
# {research_summary}

# **User Onboarding Information:**  
# {user_onboarding_info}

# Consider the user's preferences in tone, style, and industry persona while preparing the strategy.  
# Each proposed post direction should be distinctly different in its approach and intent."""

#     return call_openai_api(user_prompt, system_prompt)

# def run_first_draft_writer(content_brief, research_summary, content_strategy, user_onboarding_info):
#     system_prompt = """# Role and Objective

# You are a First Draft Writing Agent in a LinkedIn content creation workflow. Your responsibility is to write polished first drafts of LinkedIn posts based on the Content Brief, Research Summary, Content Strategy, and User Onboarding Inputs provided to you.

# # Instructions

# - Study the Content Brief, Research Summary, and Content Strategy carefully.
# - Write **three first drafts** based on the three different directions outlined in the Content Strategy.
# - Each draft must:
#   - Follow the suggested tone and hook style.
#   - Incorporate any recommended CTA (if applicable).
#   - Align with the post's core intent (educate, inspire, engage, invite action).
#   - Reflect the user's persona and industry expertise subtly.
# - Maintain high-quality writing standards:
#   - Strong, attention-catching hook in the first line.
#   - Clear setup or context in the opening paragraph.
#   - Core message must be conveyed clearly.
#   - Sentences should be short, crisp, and easy to skim.
#   - Use clean formatting (line breaks, bullet points if needed).
# - Keep the style aligned with user's preferred post examples.

# # Output Format

# **First Drafts of LinkedIn Posts**

# - **Post Draft 1**: (based on Strategy Direction 1)
# - **Post Draft 2**: (based on Strategy Direction 2)
# - **Post Draft 3**: (based on Strategy Direction 3)

# Each post should be fully standalone, not needing further context.
# Avoid generating explanatory notes — just output the actual LinkedIn post drafts."""

#     user_prompt = f"""Here's the full input information for drafting LinkedIn posts. Please write three LinkedIn post drafts based on the different directions outlined in the Strategy.

# **Content Brief:**  
# {content_brief}

# **Research Summary:**  
# {research_summary}

# **Content Strategy:**  
# {content_strategy}

# **User Onboarding Information:**  
# {user_onboarding_info}

# Each draft should:
# - Follow the recommended tone, hook, CTA, and core message from its assigned Strategy Direction.
# - Be crisp, engaging, and easy to read.
# - Reflect the user's persona and style.

# Do not add explanatory text — just provide the LinkedIn post drafts."""

#     return call_openai_api(user_prompt, system_prompt)

# def run_linkedin_content_expert(draft_post_1, draft_post_2, draft_post_3):
#     system_prompt = """# Role and Objective

# You are a LinkedIn Content Writing Expert in a LinkedIn content creation workflow. Your task is to act as a professional reviewer and editor. You will review the three draft posts provided by the First Draft Writing Actor, provide structured feedback for each, and rewrite improved, final versions of the posts ready for LinkedIn publishing.

# # Instructions

# 1. Review each post critically for:
#    - Natural human tone (not AI-sounding)
#    - Absence of cliche AI language or filler phrases
#    - Simplicity and clarity of language
#    - Short, punchy sentences for skimmability
#    - Strong, dramatic, or curiosity-driven hooks
#    - Clear core message per post
#    - Appropriate tone matching the user's persona
#    - Engaging, non-salesy CTAs (only if recommended)
#    - Alignment with LinkedIn's conversational, story-driven culture

# 2. Avoid:
#    - Complex words or formal jargon unless necessary
#    - AI phrases like "In today's fast-paced world", "Leveraging synergies", "Transformative innovation", etc.
#    - Overuse of symbols like colon ":" and dash "—"
#    - Robotic listing ("Firstly, Secondly, Lastly" unless fitting naturally)

# 3. Improve:
#    - Hook lines to be more emotional, curiosity-driven, or dramatic
#    - Flow between sentences — should feel natural and human, not mechanical
#    - Endings with a strong wrap-up or CTA (if needed)

# 4. Provide feedback first, then rewrite:
#    - Give clear feedback bullet points after each draft.
#    - Then provide the fully edited, final draft for each post separately.

# # Output Format

# **Post 1 Review**

# - **Feedback**:
#   - [Bullet feedback points]
# - **Edited Final Post 1**:  
#   [Final rewritten LinkedIn post]

# ---

# **Post 2 Review**

# - **Feedback**:
#   - [Bullet feedback points]
# - **Edited Final Post 2**:  
#   [Final rewritten LinkedIn post]

# ---

# **Post 3 Review**

# - **Feedback**:
#   - [Bullet feedback points]
# - **Edited Final Post 3**:  
#   [Final rewritten LinkedIn post]

# Do not explain why you made changes unless specifically asked. Only give direct feedback and final edited posts."""

#     user_prompt = f"""Here are three draft LinkedIn posts that need expert review and editing. 

# Please:
# - Analyze each post carefully
# - Give structured feedback on what can be improved
# - Rewrite each post into a final polished LinkedIn post based on the feedback

# Focus on:
# - Removing AI-sounding language
# - Simplifying complex words
# - Improving hooks and CTAs
# - Keeping the sentences short and punchy
# - Aligning tone with the user's persona and intent

# **Draft Post 1:**  
# {draft_post_1}

# **Draft Post 2:**  
# {draft_post_2}

# **Draft Post 3:**  
# {draft_post_3}

# Provide the feedback first, followed by the final edited posts."""

#     return call_openai_api(user_prompt, system_prompt)

# # Extract draft posts from the first draft writer output
# def extract_draft_posts(first_draft_output):
#     drafts = []
#     sections = first_draft_output.split("**Post Draft")
    
#     # Skip the first part (before the drafts)
#     for i in range(1, min(4, len(sections))):
#         section = sections[i].strip()
#         if ":" in section:
#             post_content = section.split(":", 1)[1].strip()
#             drafts.append(post_content)
    
#     # If we didn't get 3 drafts, handle the error
#     while len(drafts) < 3:
#         drafts.append("No draft available")
    
#     return drafts[0], drafts[1], drafts[2]

# # Main application layout
# col1, col2 = st.columns([1, 1])

# with col1:
#     st.markdown("<div class='sub-header'>Generate Your LinkedIn Post</div>", unsafe_allow_html=True)
    
#     user_idea = st.text_area(
#         "Your LinkedIn Post Idea", 
#         height=150,
#         placeholder="Enter your LinkedIn post idea or topic here. For example: 'I want to share insights about remote work productivity trends and how they're affecting middle management roles.'"
#     )
    
#     generate_button = st.button("Generate LinkedIn Posts", type="primary", use_container_width=True)
    
#     if generate_button and user_idea:
#         # Create a placeholder for progress
#         progress_placeholder = st.empty()
        
#         # Set up progress bar
#         progress_bar = progress_placeholder.progress(0)
#         status_text = st.empty()
        
#         # Process step 1: Brief Writing Agent
#         status_text.markdown("**Step 1/5:** Brief Writing Agent (OpenAI) is creating your content brief...")
#         content_brief = run_brief_writing_agent(user_idea)
#         progress_bar.progress(20)
        
#         if content_brief:
#             st.session_state["content_brief"] = content_brief
            
#             # Process step 2: Research Agent
#             status_text.markdown("**Step 2/5:** Research Agent (Perplexity) is gathering information...")
#             research_summary = run_research_agent(content_brief)
#             progress_bar.progress(40)
            
#             if research_summary:
#                 st.session_state["research_summary"] = research_summary
                
#                 # Process step 3: Strategy Agent
#                 status_text.markdown("**Step 3/5:** Strategy Agent (OpenAI) is developing content strategy...")
#                 content_strategy = run_strategy_agent(content_brief, research_summary, user_onboarding_info)
#                 progress_bar.progress(60)
                
#                 if content_strategy:
#                     st.session_state["content_strategy"] = content_strategy
                    
#                     # Process step 4: First Draft Writer
#                     status_text.markdown("**Step 4/5:** First Draft Writer (OpenAI) is creating drafts...")
#                     first_draft_output = run_first_draft_writer(content_brief, research_summary, content_strategy, user_onboarding_info)
#                     progress_bar.progress(80)
                    
#                     if first_draft_output:
#                         st.session_state["first_draft_output"] = first_draft_output
                        
#                         # Extract individual drafts
#                         draft_post_1, draft_post_2, draft_post_3 = extract_draft_posts(first_draft_output)
                        
#                         # Process step 5: LinkedIn Content Expert
#                         status_text.markdown("**Step 5/5:** LinkedIn Content Expert (OpenAI) is polishing drafts...")
#                         final_output = run_linkedin_content_expert(draft_post_1, draft_post_2, draft_post_3)
#                         progress_bar.progress(100)
                        
#                         if final_output:
#                             st.session_state["final_output"] = final_output
#                             status_text.markdown("✅ **Complete!** Your LinkedIn posts have been generated.")
                            
#                             # Force a rerun to display the results
#                             time.sleep(1)
#                             st.experimental_rerun()

# with col2:
#     st.markdown("<div class='sub-header'>Results</div>", unsafe_allow_html=True)
    
#     # Display results if available
#     if "content_brief" in st.session_state:
#         with st.expander("Content Brief", expanded=False):
#             st.markdown(f"<div class='process-step'>{st.session_state['content_brief']}</div>", unsafe_allow_html=True)
    
#     if "research_summary" in st.session_state:
#         with st.expander("Research Summary", expanded=False):
#             st.markdown(f"<div class='process-step'>{st.session_state['research_summary']}</div>", unsafe_allow_html=True)
    
#     if "content_strategy" in st.session_state:
#         with st.expander("Content Strategy", expanded=False):
#             st.markdown(f"<div class='process-step'>{st.session_state['content_strategy']}</div>", unsafe_allow_html=True)
    
#     if "first_draft_output" in st.session_state:
#         with st.expander("First Drafts", expanded=False):
#             st.markdown(f"<div class='process-step'>{st.session_state['first_draft_output']}</div>", unsafe_allow_html=True)
    
#     if "final_output" in st.session_state:
#         st.markdown("### Final LinkedIn Posts")
        
#         # Split the final output into sections
#         final_output = st.session_state["final_output"]
#         post_sections = final_output.split("---")
        
#         # Display each final post with copy button
#         for i, section in enumerate(post_sections):
#             if "Edited Final Post" in section:
#                 post_number = i + 1
                
#                 # Extract the final post
#                 final_post = section.split("Edited Final Post")[1].split(":", 1)[1].strip()
                
#                 # Create tabs for each post
#                 tab_title = f"Post {post_number}"
#                 with st.expander(tab_title, expanded=(post_number == 1)):
#                     # Add feedback section
#                     if "Feedback" in section:
#                         feedback = section.split("Feedback")[1].split("Edited Final Post")[0].strip()
#                         st.markdown(f"**Feedback:**\n{feedback}")
                    
#                     # Add the final post with copy button
#                     st.markdown("<div class='final-post'>", unsafe_allow_html=True)
#                     st.markdown(final_post)
#                     st.markdown("</div>", unsafe_allow_html=True)
                    
#                     # Copy button
#                     if st.button(f"Copy Post {post_number}", key=f"copy_{post_number}"):
#                         # Use JavaScript to copy to clipboard
#                         st.markdown(f"""
#                         <script>
#                             navigator.clipboard.writeText(`{final_post}`);
#                             alert('Copied to clipboard!');
#                         </script>
#                         """, unsafe_allow_html=True)
#                         st.success("Post copied to clipboard!")

import streamlit as st
import requests
import json
import os
import time

# Set page configuration
st.set_page_config(
    page_title="LinkedIn Post Generator with MCP",
    page_icon="📝",
    layout="wide"
)

# Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0A66C2;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #0A66C2;
        margin-top: 1rem;
    }
    .process-step {
        background-color: #f0f2f5;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .step-title {
        font-weight: bold;
        color: #0A66C2;
    }
    .final-post {
        background-color: #e6f3ff;
        border-left: 5px solid #0A66C2;
        padding: 15px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown("<div class='main-header'>LinkedIn Post Generator with MCP</div>", unsafe_allow_html=True)
st.markdown("""
This app uses a Multi-agent Collaborative Protocol (MCP) to generate high-quality LinkedIn posts:

1. **Brief Writing Agent** (OpenAI) - Creates a structured content brief
2. **Research Agent** (Perplexity) - Gathers relevant information and data
3. **Strategy Agent** (OpenAI) - Develops content strategy and approaches
4. **First Draft Writer** (OpenAI) - Creates initial post drafts
5. **LinkedIn Content Expert** (OpenAI) - Polishes drafts into final posts
""")

# Sidebar for API settings
with st.sidebar:
    st.markdown("### API Configuration")
    
    # OpenAI API settings
    st.markdown("#### OpenAI API")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    openai_model = st.selectbox(
        "OpenAI Model",
        ["gpt-4-turbo", "gpt-4o", "gpt-4", "gpt-3.5-turbo"],
        index=0
    )
    
    # Perplexity API settings
    st.markdown("#### Perplexity API")
    perplexity_api_key = st.text_input("Perplexity API Key", type="password")
    perplexity_model = st.selectbox(
        "Perplexity Model",
        ["pplx-7b-online", "pplx-70b-online", "mixtral-8x7b-online", "sonar"],
        index=0
    )
    
    # User persona settings
    st.markdown("#### Your LinkedIn Persona")
    industry = st.selectbox(
        "Industry",
        ["Technology", "Marketing", "Finance", "Healthcare", "Education", 
         "Human Resources", "Sales", "Manufacturing", "Consulting", "Other"]
    )
    job_role = st.text_input("Job Role", placeholder="e.g., Marketing Manager, CEO, Software Engineer")
    writing_style = st.selectbox(
        "Preferred Writing Style",
        ["Professional", "Conversational", "Thought Leadership", "Story-based", 
         "Data-driven", "Inspirational", "Educational"]
    )
    user_onboarding_info = f"Industry: {industry}\nJob Role: {job_role}\nWriting Style: {writing_style}"

# Helper functions for API calls
def call_openai_api(prompt, system_prompt, model=openai_model):
    if not openai_api_key:
        st.error("Please enter your OpenAI API key")
        return None
        
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Error calling OpenAI API: {str(e)}")
        return None

def call_perplexity_api(prompt, model=perplexity_model):
    if not perplexity_api_key:
        st.error("Please enter your Perplexity API key")
        return None
        
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {perplexity_api_key}"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Error calling Perplexity API: {str(e)}")
        return None

# MCP Process Steps
def run_brief_writing_agent(user_idea):
    system_prompt = """# Role and Objective

You are a Brief Writing Agent in a LinkedIn content creation workflow. Your task is to take a raw idea or topic from the user and convert it into a detailed content brief that can be used in future steps — including research and post writing.

# Instructions

- Structure the user's idea into a complete, actionable brief.
- Clearly identify the core topic and any supporting subtopics or themes.
- Infer missing but useful research angles like industry focus, geography, or target persona if not explicitly mentioned.
- Include what kind of data might support the idea: stats, case studies, trends, opinions, etc.
- Ensure that the brief is useful enough for a Research Agent to find real-time, relevant information.

# Output Format

**Content Brief**

- **Core Idea / Topic**:  
- **Primary Keyword / Theme**:  
- **Supporting Subtopics (if any)**:  
- **Target Audience or Persona**:  
- **Relevant Industries / Sectors (if any)**:  
- **Geographic Focus (if any)**:  
- **Intent / Purpose of the Post**:  
- **Preferred Tone**:  
- **Post Length Preference**:  
- **Desired Hook / Angle**:  
- **Call-to-Action**:  
- **Data Preferences** (e.g. stats, recent trends, case studies, quotes):  
- **Additional Notes / Style Cues**:  
"""
    
    user_prompt = f"""Here's an idea I'm thinking about turning into a LinkedIn post. Can you help me structure it into a proper brief that other agents can use to write the content?

**Raw Idea:**  
{user_idea}

Feel free to infer tone, keyword, or structure if it's not clearly mentioned — just don't go overboard. I want something that's detailed enough for a writer to understand what kind of post I'm going for."""

    return call_openai_api(user_prompt, system_prompt)

def run_research_agent(content_brief):
    system_prompt = """# Role and Objective

You are a Research Agent in a LinkedIn content workflow. Your task is to go on the internet and find the latest, most relevant and credible information related to the topic and keyword provided in the brief.

# Instructions

- Extract the primary keyword, topic, and any additional context from the brief.
- Search for relevant, *recent* content across credible sources like industry journals, news platforms, research databases, company blogs, and thought leader content.
- Prioritize:
  - Authenticity: Only use reputable sources (e.g. HBR, McKinsey, Statista, TechCrunch, etc.).
  - Freshness: Prefer content published within the last 12 months unless otherwise relevant.
  - Relevance: Information must align closely with the brief's core idea, tone, and audience.

# Types of Content to Look For

- Statistics, metrics, or market data  
- Real case studies or brand examples  
- Quotes or insights from credible people  
- Emerging trends or hot takes on the topic  
- Contrasting opinions if relevant

# Output Format

**Research Summary for LinkedIn Post**

- **Topic Searched**:  
- **Summary of Findings**: (2–3 paragraphs max)  
- **Key Statistics / Data Points**:  
- **Relevant Case Studies / Examples**:  
- **Insights / Trends Observed**:  
- **Sources Used with Links**:  

Do not generate your opinion. Only summarize research. Avoid filler language. Keep it concise and insightful."""

    user_prompt = f"""Here is the content brief that needs to be researched on. Please find the most recent and credible information available on the internet that supports or adds depth to the topic mentioned.

**Content Brief:**  
{content_brief}

Focus on collecting:
- Real data and stats
- Valid case studies or examples
- Recent news or trend analysis
- Links to credible sources

Avoid generic advice — only include what can be verified online."""

    return call_perplexity_api(user_prompt)

def run_strategy_agent(content_brief, research_summary, user_onboarding_info):
    system_prompt = """# Role and Objective

You are a Strategy Agent in a LinkedIn content creation workflow. Your responsibility is to create a detailed Content Strategy based on the Content Brief, Research Summary, and User Onboarding Preferences. This strategy will guide the writing agent on how to craft multiple styles of LinkedIn posts that feel personalized and aligned with the user's taste and persona.

# Instructions

- Analyze the Content Brief and Research Summary carefully.
- Retrieve and incorporate User Onboarding Information such as:
  - User's preferred post styles or examples
  - Desired tone (professional, casual, witty, bold)
  - User's industry, job role, and persona
- Identify the **most suitable content pillar** (e.g., personal branding, thought leadership, case study, testimonial, hiring post, announcement, etc.).
- Define the **content style and tone** based on both the user's persona and the post's purpose.
- Design **3 different strategic directions** for posts:
  - Vary the intent (e.g., inspire, educate, engage, invite action).
  - Vary the use of CTA (some posts should have CTA, some should not).
  - Ensure the posts feel distinctly different from each other — not just reworded.
- Recommend **hook styles** that are short, dramatic, or curiosity-inducing.
- Recommend **CTA styles** (or suggest if no CTA is needed).
- Set universal **content writing guidelines**:
  - Use short, easy-to-skim sentences.
  - Maintain clean formatting with proper line breaks.
  - Focus on one core message per post.
  - Maintain voice consistency aligned with user's selected style.

# Output Format

**Content Strategy for LinkedIn Post**

- **Content Pillar**:  
- **Primary Tone Recommendation**:  
- **Persona Alignment**: (briefly describe how it reflects user's industry/persona)
- **Post Length Recommendation**:  
- **Three Strategic Directions for Post Writing**:
  - **Post 1**: (Tone, Hook Idea, CTA Idea, Intent)
  - **Post 2**: (Tone, Hook Idea, CTA Idea, Intent)
  - **Post 3**: (Tone, Hook Idea, CTA Idea, Intent)
- **Suggested Hook Styles**:  
- **Suggested CTA Styles**:  
- **General Content Writing Guidelines**:
  - Short sentences
  - Clear formatting
  - Voice consistency
  - Focused core message"""

    user_prompt = f"""Here's the Content Brief, Research Summary, and the User's Onboarding Preferences for a LinkedIn post idea. Based on these, please create a complete LinkedIn Content Strategy to guide the post writing.

**Content Brief:**  
{content_brief}

**Research Summary:**  
{research_summary}

**User Onboarding Information:**  
{user_onboarding_info}

Consider the user's preferences in tone, style, and industry persona while preparing the strategy.  
Each proposed post direction should be distinctly different in its approach and intent."""

    return call_openai_api(user_prompt, system_prompt)

def run_first_draft_writer(content_brief, research_summary, content_strategy, user_onboarding_info):
    system_prompt = """# Role and Objective

You are a First Draft Writing Agent in a LinkedIn content creation workflow. Your responsibility is to write polished first drafts of LinkedIn posts based on the Content Brief, Research Summary, Content Strategy, and User Onboarding Inputs provided to you.

# Instructions

- Study the Content Brief, Research Summary, and Content Strategy carefully.
- Write **three first drafts** based on the three different directions outlined in the Content Strategy.
- Each draft must:
  - Follow the suggested tone and hook style.
  - Incorporate any recommended CTA (if applicable).
  - Align with the post's core intent (educate, inspire, engage, invite action).
  - Reflect the user's persona and industry expertise subtly.
- Maintain high-quality writing standards:
  - Strong, attention-catching hook in the first line.
  - Clear setup or context in the opening paragraph.
  - Core message must be conveyed clearly.
  - Sentences should be short, crisp, and easy to skim.
  - Use clean formatting (line breaks, bullet points if needed).
- Keep the style aligned with user's preferred post examples.

# Output Format

**First Drafts of LinkedIn Posts**

- **Post Draft 1**: (based on Strategy Direction 1)
- **Post Draft 2**: (based on Strategy Direction 2)
- **Post Draft 3**: (based on Strategy Direction 3)

Each post should be fully standalone, not needing further context.
Avoid generating explanatory notes — just output the actual LinkedIn post drafts."""

    user_prompt = f"""Here's the full input information for drafting LinkedIn posts. Please write three LinkedIn post drafts based on the different directions outlined in the Strategy.

**Content Brief:**  
{content_brief}

**Research Summary:**  
{research_summary}

**Content Strategy:**  
{content_strategy}

**User Onboarding Information:**  
{user_onboarding_info}

Each draft should:
- Follow the recommended tone, hook, CTA, and core message from its assigned Strategy Direction.
- Be crisp, engaging, and easy to read.
- Reflect the user's persona and style.

Do not add explanatory text — just provide the LinkedIn post drafts."""

    return call_openai_api(user_prompt, system_prompt)

def run_linkedin_content_expert(draft_post_1, draft_post_2, draft_post_3):
    system_prompt = """# Role and Objective

You are a LinkedIn Content Writing Expert in a LinkedIn content creation workflow. Your task is to act as a professional reviewer and editor. You will review the three draft posts provided by the First Draft Writing Actor, provide structured feedback for each, and rewrite improved, final versions of the posts ready for LinkedIn publishing.

# Instructions

1. Review each post critically for:
   - Natural human tone (not AI-sounding)
   - Absence of cliche AI language or filler phrases
   - Simplicity and clarity of language
   - Short, punchy sentences for skimmability
   - Strong, dramatic, or curiosity-driven hooks
   - Clear core message per post
   - Appropriate tone matching the user's persona
   - Engaging, non-salesy CTAs (only if recommended)
   - Alignment with LinkedIn's conversational, story-driven culture

2. Avoid:
   - Complex words or formal jargon unless necessary
   - AI phrases like "In today's fast-paced world", "Leveraging synergies", "Transformative innovation", etc.
   - Overuse of symbols like colon ":" and dash "—"
   - Robotic listing ("Firstly, Secondly, Lastly" unless fitting naturally)

3. Improve:
   - Hook lines to be more emotional, curiosity-driven, or dramatic
   - Flow between sentences — should feel natural and human, not mechanical
   - Endings with a strong wrap-up or CTA (if needed)

4. Provide feedback first, then rewrite:
   - Give clear feedback bullet points after each draft.
   - Then provide the fully edited, final draft for each post separately.

# Output Format

**Post 1 Review**

- **Feedback**:
  - [Bullet feedback points]
- **Edited Final Post 1**:  
  [Final rewritten LinkedIn post]

---

**Post 2 Review**

- **Feedback**:
  - [Bullet feedback points]
- **Edited Final Post 2**:  
  [Final rewritten LinkedIn post]

---

**Post 3 Review**

- **Feedback**:
  - [Bullet feedback points]
- **Edited Final Post 3**:  
  [Final rewritten LinkedIn post]

Do not explain why you made changes unless specifically asked. Only give direct feedback and final edited posts."""

    user_prompt = f"""Here are three draft LinkedIn posts that need expert review and editing. 

Please:
- Analyze each post carefully
- Give structured feedback on what can be improved
- Rewrite each post into a final polished LinkedIn post based on the feedback

Focus on:
- Removing AI-sounding language
- Simplifying complex words
- Improving hooks and CTAs
- Keeping the sentences short and punchy
- Aligning tone with the user's persona and intent

**Draft Post 1:**  
{draft_post_1}

**Draft Post 2:**  
{draft_post_2}

**Draft Post 3:**  
{draft_post_3}

Provide the feedback first, followed by the final edited posts."""

    return call_openai_api(user_prompt, system_prompt)

# Extract draft posts from the first draft writer output
def extract_draft_posts(first_draft_output):
    drafts = []
    sections = first_draft_output.split("**Post Draft")
    
    # Skip the first part (before the drafts)
    for i in range(1, min(4, len(sections))):
        section = sections[i].strip()
        if ":" in section:
            post_content = section.split(":", 1)[1].strip()
            drafts.append(post_content)
    
    # If we didn't get 3 drafts, handle the error
    while len(drafts) < 3:
        drafts.append("No draft available")
    
    return drafts[0], drafts[1], drafts[2]

# Main application layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<div class='sub-header'>Generate Your LinkedIn Post</div>", unsafe_allow_html=True)
    
    user_idea = st.text_area(
        "Your LinkedIn Post Idea", 
        height=150,
        placeholder="Enter your LinkedIn post idea or topic here. For example: 'I want to share insights about remote work productivity trends and how they're affecting middle management roles.'"
    )
    
    generate_button = st.button("Generate LinkedIn Posts", type="primary", use_container_width=True)
    
    if generate_button and user_idea:
        # Create a placeholder for progress
        progress_placeholder = st.empty()
        
        # Set up progress bar
        progress_bar = progress_placeholder.progress(0)
        status_text = st.empty()
        
        # Process step 1: Brief Writing Agent
        status_text.markdown("**Step 1/5:** Brief Writing Agent (OpenAI) is creating your content brief...")
        content_brief = run_brief_writing_agent(user_idea)
        progress_bar.progress(20)
        
        if content_brief:
            st.session_state["content_brief"] = content_brief
            
            # Process step 2: Research Agent
            status_text.markdown("**Step 2/5:** Research Agent (Perplexity) is gathering information...")
            research_summary = run_research_agent(content_brief)
            progress_bar.progress(40)
            
            if research_summary:
                st.session_state["research_summary"] = research_summary
                
                # Process step 3: Strategy Agent
                status_text.markdown("**Step 3/5:** Strategy Agent (OpenAI) is developing content strategy...")
                content_strategy = run_strategy_agent(content_brief, research_summary, user_onboarding_info)
                progress_bar.progress(60)
                
                if content_strategy:
                    st.session_state["content_strategy"] = content_strategy
                    
                    # Process step 4: First Draft Writer
                    status_text.markdown("**Step 4/5:** First Draft Writer (OpenAI) is creating drafts...")
                    first_draft_output = run_first_draft_writer(content_brief, research_summary, content_strategy, user_onboarding_info)
                    progress_bar.progress(80)
                    
                    if first_draft_output:
                        st.session_state["first_draft_output"] = first_draft_output
                        
                        # Extract individual drafts
                        draft_post_1, draft_post_2, draft_post_3 = extract_draft_posts(first_draft_output)
                        
                        # Process step 5: LinkedIn Content Expert
                        status_text.markdown("**Step 5/5:** LinkedIn Content Expert (OpenAI) is polishing drafts...")
                        final_output = run_linkedin_content_expert(draft_post_1, draft_post_2, draft_post_3)
                        progress_bar.progress(100)
                        
                        if final_output:
                            st.session_state["final_output"] = final_output
                            status_text.markdown("✅ **Complete!** Your LinkedIn posts have been generated.")
                            
                            # Force a rerun to display the results
                            time.sleep(1)
                            st.rerun()

with col2:
    st.markdown("<div class='sub-header'>Results</div>", unsafe_allow_html=True)
    
    # Display results if available
    if "content_brief" in st.session_state:
        with st.expander("Content Brief", expanded=False):
            st.markdown(f"<div class='process-step'>{st.session_state['content_brief']}</div>", unsafe_allow_html=True)
    
    if "research_summary" in st.session_state:
        with st.expander("Research Summary", expanded=False):
            st.markdown(f"<div class='process-step'>{st.session_state['research_summary']}</div>", unsafe_allow_html=True)
    
    if "content_strategy" in st.session_state:
        with st.expander("Content Strategy", expanded=False):
            st.markdown(f"<div class='process-step'>{st.session_state['content_strategy']}</div>", unsafe_allow_html=True)
    
    if "first_draft_output" in st.session_state:
        with st.expander("First Drafts", expanded=False):
            st.markdown(f"<div class='process-step'>{st.session_state['first_draft_output']}</div>", unsafe_allow_html=True)
    
    if "final_output" in st.session_state:
        st.markdown("### Final LinkedIn Posts")
        
        # Split the final output into sections
        final_output = st.session_state["final_output"]
        post_sections = final_output.split("---")
        
        # Display each final post with copy button
        for i, section in enumerate(post_sections):
            if "Edited Final Post" in section:
                post_number = i + 1
                
                # Extract the final post
                final_post = section.split("Edited Final Post")[1].split(":", 1)[1].strip()
                
                # Create tabs for each post
                tab_title = f"Post {post_number}"
                with st.expander(tab_title, expanded=(post_number == 1)):
                    # Add feedback section
                    if "Feedback" in section:
                        feedback = section.split("Feedback")[1].split("Edited Final Post")[0].strip()
                        st.markdown(f"**Feedback:**\n{feedback}")
                    
                    # Add the final post with copy button
                    st.markdown("<div class='final-post'>", unsafe_allow_html=True)
                    st.markdown(final_post)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Copy button
                    if st.button(f"Copy Post {post_number}", key=f"copy_{post_number}"):
                        # Use JavaScript to copy to clipboard
                        st.markdown(f"""
                        <script>
                            navigator.clipboard.writeText(`{final_post}`);
                            alert('Copied to clipboard!');
                        </script>
                        """, unsafe_allow_html=True)
                        st.success("Post copied to clipboard!")