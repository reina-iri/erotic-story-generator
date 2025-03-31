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
        # Здесь можно добавить код для автоматического скачивания модели
        pass
    return "model_object"

model = load_model()

# Function to generate story using system prompt and inputs
def generate_story(theme, genre, mood, length, tags, prompt1, prompt2, prompt3, count):
    # Формируем системное сообщение
    SYSTEM_PROMPT = f"""
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
        # Здесь должна быть логика генерации с использованием модели,
        # сейчас мы используем заглушку
        story = f"Title: Erotic Story\n\nSYSTEM PROMPT:\n{SYSTEM_PROMPT}\n\nAdditional Prompts:\n{prompt1}\n{prompt2}\n{prompt3}\n\nTags: {tags}\n\n(Generated story text...)"
        stories.append(format_story(story))
    return "\n\n---\n\n".join(stories)

# Функции для кнопок "Copy All" и "Save as TXT"
# Пока они просто возвращают тот же текст (в будущем можно расширить функционал)
def copy_all(story_text):
    return story_text

def save_as_txt(story_text):
    # Пока заглушка – возвращаем текст, который можно сохранить вручную
    return story_text

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
        btn_copy = gr.Button("Copy All")
        btn_save = gr.Button("Save as TXT")
    
    output = gr.Textbox(label="Generated Story", lines=15)
    
    # Связываем кнопки с функциями
    btn_generate.click(fn=lambda *args: generate_story(*args, 1), inputs=[theme, genre, mood, length, tags, prompt1, prompt2, prompt3], outputs=output)
    btn_generate3.click(fn=lambda *args: generate_story(*args, 3), inputs=[theme, genre, mood, length, tags, prompt1, prompt2, prompt3], outputs=output)
    btn_copy.click(fn=copy_all, inputs=output, outputs=output)
    btn_save.click(fn=save_as_txt, inputs=output, outputs=output)

demo.launch(server_name="0.0.0.0", server_port=7860)
