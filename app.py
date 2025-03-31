import gradio as gr
import json
import os
from utils.formatters import format_story

# Load model configuration
with open("configs/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Function to load the model (pseudo-code)
def load_model():
    model_path = os.path.join("models", config["model_name"])
    if not os.path.exists(model_path):
        # Add code here to automatically download the model if it doesn't exist
        pass
    return "model_object"

model = load_model()

# Function to generate story
def generate_story(theme, genre, mood, length, tags, prompt1, prompt2, prompt3, count):
    system_prompt = f"""
    You are an erotic storyteller. Write a story from the first-person perspective of a passionate woman.
    The genre is: {genre}.
    The mood is: {mood}.
    The scene is: {theme}.
    Always include emotional depth, sensory detail, and dirty talk.
    Use present tense and make the character feel real and alive.
    Story length: {length}.
    """
    stories = []
    for _ in range(count):
        # Replace this pseudo-code with actual generation logic using the model
        story = f"Title: Erotic Story\n\nThis is a generated story with tags: {tags}.\n{prompt1}\n{prompt2}\n{prompt3}\n..."
        stories.append(format_story(story))
    return "\n\n---\n\n".join(stories)

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Erotic Story Generator")
    with gr.Row():
        theme = gr.Textbox(label="Theme/Scene")
        genre = gr.Dropdown(label="Genre", choices=[
            "Fantasy", "Sci-Fi", "BDSM", "Lesbian", "Taboo", "Voyeur", "Incubus/Succubus",
            "Harem", "Interracial", "Public/Exhibitionism", "Cheating/Married Woman",
            "OnlyFans/Filming", "Sabor Latino", "Celebrity", "Anal", "Gang/Group", "Threesome"
        ])
    with gr.Row():
        mood = gr.Dropdown(label="Mood", choices=[
            "Romantic", "Filthy", "Dominant", "Submissive", "Emotional", "Forbidden",
            "Teasing", "Rough", "Tender", "Playful", "Cruel", "Drunk", "Enchanted", "Sacred", "Humiliated"
        ], multiselect=True)
        length = gr.Radio(label="Length", choices=["short", "medium", "long"])
    tags = gr.Textbox(label="Tags")
    with gr.Row():
        prompt1 = gr.Textbox(label="Art Prompt 1")
        prompt2 = gr.Textbox(label="Art Prompt 2")
        prompt3 = gr.Textbox(label="Art Prompt 3")
    
    with gr.Row():
        btn_generate = gr.Button("Generate Story")
        btn_generate3 = gr.Button("Generate 3 Stories")
    
    output = gr.Textbox(label="Generated Story", lines=15)
    
    btn_generate.click(fn=lambda *args: generate_story(*args, 1), inputs=[theme, genre, mood, length, tags, prompt1, prompt2, prompt3], outputs=output)
    btn_generate3.click(fn=lambda *args: generate_story(*args, 3), inputs=[theme, genre, mood, length, tags, prompt1, prompt2, prompt3], outputs=output)

demo.launch(server_name="0.0.0.0", server_port=7860)
